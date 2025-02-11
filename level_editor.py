import math
import pygame

import levelmap
from enums import BlockVariants

OFFSETS = [(0, -1),(0, 1),(-1, 0),(1, 0),(0,0) ]
CORNER_OFFSETS = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
OPPOSING_CORNER = { "BOTTOMRIGHT": (1,1), "TOPRIGHT" : (1,-1), "BOTTOMLEFT" : (-1, 1), "TOPLEFT" : (-1, -1)}

SCREEN_SIZE = (960, 540)

class LevelEditor:
    def __init__(self, scale, level_name : str):
        self.scale = scale

        self.screen = pygame.display.set_mode((SCREEN_SIZE[0] * self.scale, SCREEN_SIZE[1]* self.scale))#16 *4: 9 * 4
        self.camera = [0, 0]
        self.mov_multiplier = 1

        self.tilemap = levelmap.TileMap(self.screen, self.scale, True, level_name)
        
        self.selected = {
            1: 'BLOCK',
            2: 'SPIKE',
            3: 'CHECKPOINT',
            
            # 3 : Type.SPIKE_SNAKE
        }
        self.bar = 0
        self.key_press = 1
        self.cursor_size = 1
        self.block_size = 10

        self.directions = {
            pygame.K_w : [0, -1, False],
            pygame.K_a : [-1, 0, False],
            pygame.K_s : [0, 1, False],
            pygame.K_d : [1, 0, False],
        }
        self.movement = (0, 0)

        self.run = True
        self.clock = pygame.time.Clock()

        #self.scale_to_grid = lambda x: [x[0] // (10 * scale), x[1] // (10 * scale)]

    def quit(self):
        self.tilemap.level.save(self.tilemap)

        self.run = False

    def create_tiles(self, mouse_pos, remove: bool):
        offset_len = range(int(-0.5 * self.cursor_size), int(0.5 * self.cursor_size + 1))

        # rx = (tx - camera[0]) * tilemap.scale
        # tx = rx / tilemap.scale + camera[0]
        # where tx = ix * 10
        # ix = (rx / tilemap.scale + camera[0]) / 10
        # where  tilemap.scale = self.block_size / 10 * self.scale  and  rx = mouse_pos[0]
        block_pos = (
            math.floor((mouse_pos[0] / (self.block_size / 10 * self.scale) + self.camera[0]) / 10),
            math.floor((mouse_pos[1] / (self.block_size / 10 * self.scale) + self.camera[1]) / 10)
        )

        for x_offset in offset_len: 
            for y_offset in offset_len:

                new_block_pos = (block_pos[0] + x_offset, block_pos[1] + y_offset)
                t = self.selected[self.key_press] if self.key_press in self.selected else 'BLOCK'
                
                self.create_tile(new_block_pos, t, remove)

    def create_tile(self, pos: tuple[int, int], type_name: str, remove: bool):
        if remove:
            value = None
        else:
            value = self.tilemap.get_tile_factory(type_name).create(*pos)
        self.tilemap.level.set(pos[0], pos[1], value)

        self.update_block_variants(pos)

    def update_block_variants(self, new_block_pos) -> None:
        def should_connect(pos: tuple[int, int], offset: tuple[int, int] = (0, 0), allow_air: bool = False) -> bool:
            pos = (pos[0] + offset[0], pos[1] + offset[1])
            tile = self.tilemap.level.get(*pos)
            if allow_air:
                return tile is None or issubclass(tile.renderer.__class__, levelmap.ConnectedSolidBlockRenderer)
            else:
                return tile is not None and issubclass(tile.renderer.__class__, levelmap.ConnectedSolidBlockRenderer)

        surrounding_blocks = []
        for offset in OFFSETS + CORNER_OFFSETS:
            surrounding_block = self.pos_to_str(new_block_pos, offset)
            if should_connect(surrounding_block):
                surrounding_blocks.append(surrounding_block)

        for block in surrounding_blocks:  # could save tiles_around for every tile to optimize
            tiles_around = {(0, -1): False, (0, 1): False, (-1, 0): False, (1, 0): False}
            # find tiles around
            for offset in OFFSETS:
                if should_connect(block, offset):
                    tiles_around[offset] = True
            tiles_around[(0, 0)] = False

            #update variant accordingly
            
            block_str = ""
            amount_around = [tiles_around[x] for x in tiles_around].count(True)

            if  amount_around in (0, 1):
                block_str = "ALL"

            elif amount_around == 4:
                corners = {(-1, -1) : False, (-1, 1): False, (1, -1): False, (1, 1): False}
                missing= 0
                for corner in CORNER_OFFSETS:
                    if should_connect(block, corner):
                        corners[corner] = True
                    else:
                        missing += 1

                if not corners[(-1, -1)]: block_str += "TOPLEFT"
                if not corners[(1, -1)]: block_str += "TOPRIGHT"

                if not corners[(-1, 1)]: block_str += "BOTTOMLEFT"   
                if not corners[(1, 1)]: block_str += "BOTTOMRIGHT"

                if block_str == "": block_str = "FREE"
                elif missing in (3, 4) : block_str = "ALL"
                elif block_str == "TOPLEFTBOTTOMLEFT": block_str = "RIGHT"
                elif block_str == "TOPRIGHTBOTTOMRIGHT": block_str = "LEFT"
                elif block_str == "TOPLEFTTOPRIGHT": block_str = "BOTTOM"
                elif block_str == "BOTTOMLEFTBOTTOMRIGHT": block_str = "TOP"
                else: block_str += "_NO_OPPOSITE_CORNER"
            
            else: 
                
                if tiles_around[(0, -1)]: block_str += "TOP"
                if tiles_around[(0, 1)]: block_str += "BOTTOM"

                if tiles_around[(-1, 0)]: block_str += "LEFT"
                if tiles_around[(1, 0)]: block_str += "RIGHT"

                block_str = block_str.removeprefix("TOPBOTTOM").removesuffix("LEFTRIGHT") or block_str
                
                if block_str in OPPOSING_CORNER:
                    if should_connect(block, OPPOSING_CORNER[block_str]):
                        block_str += "_CORNER"
                
            if block_str == "": block_str = "ALL"

            tile = self.tilemap.level.get(*block)
            if tile is not None:
                tile.renderer.texture_num = getattr(BlockVariants, block_str)
    
    def pos_to_str(self, pos: tuple[int, int], offset: tuple[int, int] = (0, 0)) -> tuple[int, int]:
        return pos[0] + offset[0], pos[1] + offset[1]
    
    def highlight_cursor(self, mouse_pos) -> None:
        cube_size = self.block_size * self.scale * self.cursor_size

        s = pygame.Surface((cube_size, cube_size), pygame.SRCALPHA)   
        s.fill((255,255,255,128))                         
        self.screen.blit(s, (mouse_pos[0] - 0.5 * cube_size, mouse_pos[1] - 0.5 * cube_size))

    def main(self):
        self.run = True
        while self.run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()

                if event.type == pygame.MOUSEWHEEL:
                    self.cursor_size = max(1, self.cursor_size + 2 * event.y) #1 or -1
                    self.block_size = round(max(1, self.block_size + 0.2 * event.x), 2)
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: self.quit()
                    if event.key == pygame.K_SPACE: self.camera = [0, 0]

                    # if event.key == pygame.K_t:
                    #     print('updating block variants')
                    #     for tile_pos in self.tilemap.level._tiles:
                    #         self.update_block_variants(tile_pos)
                    #     print('done')
                    if event.key == pygame.K_e: self.block_size = 10
                    
                    #movement
                    if event.key in (pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d):
                        self.movement = (int(self.directions[event.key][0]) * 20 * self.mov_multiplier, int(self.directions[event.key][1] * 20 * self.mov_multiplier))
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
            pygame.draw.rect(self.screen, ("white"), pygame.Rect((-self.camera[0]) * self.scale,(-self.camera[1]) * self.scale, self.scale * 9, self.scale *19))

            self.tilemap.scale = self.block_size / 10 * self.scale
            self.tilemap.scale_images()
            self.tilemap.render(self.camera)

            mouse_pos = pygame.mouse.get_pos() 
            mouse_press = pygame.mouse.get_pressed()
            
            self.highlight_cursor(mouse_pos)

            if mouse_press[0] or mouse_press[2]:
                self.create_tiles(mouse_pos, mouse_press[2])


            if self.clock.get_fps() < 25:
                self.mov_multiplier = 10
                print(self.clock.get_fps())
            else: self.mov_multiplier = 1
            
            self.clock.tick(60)
            pygame.display.update()
