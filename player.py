from math import ceil

import pygame

import levelmap
from enums import PlayerState, Events

OFFSETS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0),(1, 1),
           (0, 2), (0,-2)]


PhYSICS_MOD = 1
SPEED_MOD = 1


class Player:

    def __init__(self, screen):
        
        self.rect = pygame.Rect(231, 109, 9, 19)
        self.speed = [0,0]
        self.screen = screen

        self.mouse_pressed = [False, False, False]
        self.keys_pressed = {"space" : False,
                             "shift": False,
                             "a/d": False,
                             "r": False}

        self.gravity = -1 #1 is down, -1 is up

        self.state = PlayerState.GROUNDED
        self.jumps = 2
        self.flips = 1

        self.last_checkpoint_pos: tuple[int, int] = self.rect.center
        self._last_checkpoint: levelmap.Tile | None = None

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.speed[0] -= 0.4 * PhYSICS_MOD * SPEED_MOD
            self.keys_pressed["a/d"] = True
        elif keys[pygame.K_d]:
            self.speed[0] += 0.4 * PhYSICS_MOD * SPEED_MOD
            self.keys_pressed["a/d"] = True
        else:
            self.keys_pressed["a/d"] = False

        if keys[pygame.K_SPACE] and self.jumps > 0:
                
                if not self.keys_pressed["space"]:
                    self.jumps -= 1

                    if self.gravity == 1:
                        self.speed[1] = -12 * PhYSICS_MOD
                    else: self.speed[1] = +12 * PhYSICS_MOD
                
                self.keys_pressed["space"] = True 
        else: self.keys_pressed["space"] = False

        if keys[pygame.K_LSHIFT]:
            if self.flips > 0:
                if not self.keys_pressed["shift"]:

                    self.flips -= 1
                    self.gravity = -self.gravity
            
            self.keys_pressed["shift"] = True
        else: self.keys_pressed["shift"] = False

        if keys[pygame.K_r]:

            if not self.keys_pressed["r"]:

                self.die()

            self.keys_pressed["r"] = True

        else: self.keys_pressed["r"] = False

    def die(self) -> None:
        print(f"Player died at {self.rect.x // 10}, {self.rect.y // 10}")
        print(self.last_checkpoint_pos)
        self.rect.center = self.last_checkpoint_pos

        self.speed = [0.0, 0.0]
        self.gravity = 1
        self.jumps = 2
        self.flips = 1

    def handle_events(self, collider: levelmap.Collider, events: Events, tilemap: levelmap.TileMap) -> None:
        match events:
            case Events.DEATH: self.die()
            case Events.GET_CHECKPOINT:
                if not isinstance(collider, levelmap.BlockCollider):
                    raise NotImplementedError()
                rect = collider._rect
                self.last_checkpoint_pos = rect.center

                if self._last_checkpoint is not None:
                    if not isinstance(self._last_checkpoint.renderer, levelmap.SolidBlockRenderer):
                        raise ValueError()
                    self._last_checkpoint.renderer.texture_num = 0

                self._last_checkpoint = tilemap.level.get(rect.x // 10, rect.y // 10)
                if not isinstance(self._last_checkpoint.renderer, levelmap.SolidBlockRenderer):
                    raise ValueError()
                self._last_checkpoint.renderer.texture_num = 1
                
            case _:raise NotImplementedError(events)
            
        

    def apply_mov(self, tilemap: levelmap.TileMap): #and collison with blocks
        # left & right (back and forth (Sisphus reference>!!!!!!???))

        repeats = ceil(abs(self.speed[0]) / 10) + 1
        stepx = self.speed[0] / repeats

        for _ in range(repeats):
            
            self.rect.centerx += stepx


            for collider, events in tilemap.collide(self.rect):
                if events is None:
                    if not isinstance(collider, levelmap.BlockCollider):
                        raise NotImplementedError()
                    rect = collider._rect

                    if self.speed[0] > 0:
                        self.rect.right = rect.left
                        self.speed[0] -= 4 * PhYSICS_MOD
                        if self.speed[0] < 0: self.speed[0] = 0 #in case of direction shift by collision
                        break

                    elif self.speed[0] < 0:
                        self.rect.left = rect.right
                        self.speed[0] += 4 * PhYSICS_MOD
                        if self.speed[0] > 0: self.speed[0] = 0#in case of direction shift by collision
                        break
                    else: pass
                else:
                    self.handle_events(collider, events, tilemap)
            else:
                continue
            break

        # gravity,
        if self.speed[1] * self.gravity < 10: #grav is 1/-1
            self.speed[1] += 0.7 * self.gravity * PhYSICS_MOD
              
        repeats = ceil(abs(self.speed[1]) / 10) + 1
        stepy = self.speed[1]/ repeats

        ground_touch = False

        for _ in range(repeats):

            self.rect.centery += stepy
            ground_check_rect = pygame.Rect(self.rect.x,
                                            self.rect.top - 9 + (22 * (self.gravity + 1) / 2),
                                            9, 12) # Makes player grounded earlier

            for _, events in tilemap.collide(ground_check_rect):
                if events is None:
                    if (self.speed[1] > 0 and self.gravity == 1) or (self.speed[1] < 0 and self.gravity == -1):
                        ground_touch = True

            for collider, events in tilemap.collide(self.rect):
                if events is None:
                    if not isinstance(collider, levelmap.BlockCollider):
                        raise NotImplementedError()
                    rect = collider._rect

                    if self.speed[1] > 0:
                        self.rect.bottom = rect.top
                        self.speed[1] = 0
                        break
                    elif self.speed[1] < 0:
                        self.rect.top = rect.bottom
                        self.speed[1] = 0
                        break
                else:
                    self.handle_events(collider, events, tilemap)
            else:
                continue
            break

        if ground_touch:
            self.state = PlayerState.GROUNDED
            self.flips = 1
            self.jumps = 2
        else: self.state = PlayerState.AIR

    def friction(self):
        #higher if not pressing a/d, (could remove)
        if self.keys_pressed["a/d"] == True:
            mult = 1
        else: mult = 10

        #higher if grounded
        if self.state == PlayerState.GROUNDED: num = abs(self.speed[0]) /  20 * mult #makes friction 1/50 * mul from speed
        else: num = abs(self.speed[0]) / 25 * mult

        #check if speed is positive
        try:polarity = (self.speed[0] / abs(self.speed[0]))
        except ZeroDivisionError: polarity = False

        #apply speed based on all of the above
        if abs(self.speed[0]) - num < 0 or num < 0.01: self.speed[0] = 0
        else: self.speed[0] -= num * polarity

    def update_camera(self, camera):

        delta = [camera[0] - (self.rect.centerx -480), camera[1] - (self.rect.centery - 270)]
        camera[0] -= delta[0] / 10
        camera[1] -= delta[1] / 10

        return camera

    def draw(self, camera, scale):
        drawn_rect = pygame.Rect((self.rect.left - camera[0]) * scale, (self.rect.top - camera[1])* scale, self.rect.width* scale, self.rect.height* scale)
        
        colors = [(255, 0), (255, 128), (255, 255)]
        # FF8000 128

        color = colors[self.jumps]
        # if self.jumps < 2
        #     color = "blue"
        color += ((0, 255)[self.flips],)
        pygame.draw.rect(self.screen, color, drawn_rect)


    def update(self, tilemap: levelmap.TileMap):
        self.input()
        self.apply_mov(tilemap)
        self.friction()
