import pygame
import json
from scripts.load_images import load_images, load_image

class LevelEditor:
    def __init__(self, scale):
        self.scale = scale

        self.screen = pygame.display.set_mode((640 * self.scale, 360* self.scale))#16 *4: 9 * 4
        self.camera = [0, 0]
        
        self.selected = {1 : "block",
                         2 : "spike_cube",
                         3 : "snake"}
        self.bar = 0 #for blocks_num >9
        self.key_press = 1


        with open("json_files/levels.json" , "r") as f:
            self.tilemap : dict = json.load(f)
        self.tilenumber = max(tuple(map(int, [i for i in self.tilemap]))) + 1
        print(self.tilenumber)

        self.images = {
            "spike_cube" : load_image("spike_cube.png"),
            "blocks" : load_images("tiles/"),
            "snake" : load_image("snake.png"),
        }

        self.directions = {
            pygame.K_w : [0, -1, False],
            pygame.K_a : [-1, 0, False],
            pygame.K_s : [0, 1, False],
            pygame.K_d : [1, 0, False],
        }
        self.movement = (0, 0)
        
        self.clock = pygame.time.Clock()

        #self.scale_to_grid = lambda x: [x[0] // (10 * scale), x[1] // (10 * scale)]
    
    def render(self, pos: list[int, int], tile_type : str, variant: str):
        if tile_type == "block":
            draw_rect = pygame.Rect((pos[0] * 10 - self.camera[0]) * self.scale, (pos[1] * 10 - self.camera[1])* self.scale, 10* self.scale, 10* self.scale)
            self.screen.blit(pygame.transform.scale(self.images["blocks"][int(variant)], (draw_rect.width, draw_rect.height )), draw_rect.topleft)
        elif tile_type in ("spike_cube"):
            draw_rect = pygame.Rect((pos[0] * 10- self.camera[0]) * self.scale, (pos[1] * 10- self.camera[1])* self.scale, 10* self.scale, 10* self.scale)
            self.screen.blit(pygame.transform.scale(self.images[variant], (draw_rect.width, draw_rect.height )), draw_rect.topleft)

    def quit(self):
        with open("json_files/levels.json" , "w") as f:
            json.dump(self.tilemap, f)
        self.run = False

    def create_tile(self, _pos: list[int, int], type: str, remove: bool):
        pos = [(_pos[0] + self.camera[0] * self.scale) // (10 * self.scale), (_pos[1] + self.camera[1]* self.scale) // (10 * self.scale)]
        
        tiles_on_pos = [x for x in self.tilemap if self.tilemap[x]["pos"] == pos]
        if remove: 
            for i in tiles_on_pos:
                if self.tilemap[i]["type"] == "block":
                    self.update_variants(self.tilemap[i]["pos"], add = False)
                self.tilemap.pop(i)
            return
        elif tiles_on_pos:#tile exists already
            for i in tiles_on_pos:
                if self.tilemap[i]["type"] == "block":
                    self.update_variants(self.tilemap[i]["pos"], add = False)
                self.tilemap.pop(i)
        
        if type == "block": 
            self.tilemap[self.tilenumber] = {"pos": pos, "type": type, "variant": 1}
            self.update_variants(pos, add = True)
        if type in ("spike_cube", "snake"):
            self.tilemap[self.tilenumber] = {"pos": pos, "type": "spike", "variant": type}
        self.tilenumber += 1

    def update_variants(self, new_block_pos, add: bool = True): #TODO
        pass
    
    def main(self):
        self.run = True
        while self.run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()

                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: self.quit()
                    
                    #movement
                    if event.key in (pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d,):
                        self.movement = (int(self.directions[event.key][0]) * 20, int(self.directions[event.key][1] * 20))
                        self.directions[event.key][2] = True
                    
                    #tile selection
                    if int(event.key) in range(48, 58):
                        self.key_press = int(event.key)-48 + (self.bar * 10)
                
                elif event.type == pygame.KEYUP:
                    #movement
                    if event.key in (pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d): self.directions[event.key][2] = False
                    
                    if not [i for i in self.directions if self.directions[i][2] == True]: 
                        self.movement = (0, 0)
                    else: 
                        for i in self.directions:
                            if self.directions[i][2]:
                                self.movement = (int(self.directions[i][0]) * 20, int(self.directions[i][1] * 20))
                    
     
            self.camera = [self.camera[0] + self.movement[0], self.camera[1] + self.movement[1]]
            self.screen.fill("black")

            for i in self.tilemap:
                tile = self.tilemap[i]
                self.render(tile["pos"], tile["type"], tile["variant"])

            mouse_press = pygame.mouse.get_pressed()
            if mouse_press[0] or mouse_press[2]:
                x = self.selected[self.key_press] if self.key_press in self.selected else "block"
                self.create_tile(pygame.mouse.get_pos(), x, mouse_press[2])

            self.clock.tick(60)
            pygame.display.update()

    def temp(self):
        self.tiles = {}
        for i in range(100):

        
            self.tiles[str(i)] = {"pos": [i, 0], "type" : "block", "variant" : "3"}
            self.tiles[str(i+100)] = {"pos": [i, 40], "type" : "block", "variant" : "1"}
            self.tiles[str(i+200)] = {"pos": [0, i], "type" : "block", "variant" : "2"}
            self.tiles[str(i+300)] = {"pos": [60, i], "type" : "block", "variant" : "4"}

        for i in range(10):
            self.tiles[str(i+400)] = {"pos": [12, i + 5], "type" : "spike", "variant" : "snake"}


        with open("json_files/levels.json" , "w") as f:
            json.dump(self.tiles, f)