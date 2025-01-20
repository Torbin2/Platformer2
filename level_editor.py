import pygame
import json

from load_images import load_images, load_image
from enums import Type, BlockVariants

OFFSETS = [(0, -1),(0, 1),(-1, 0),(1, 0),(0,0) ]
CORNER_OFFSETS = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
OPPOSING_CORNER = { "BOTTOMRIGHT": (1,1), "TOPRIGHT" : (1,-1), "BOTTOMLEFT" : (-1, 1), "TOPLEFT" : (-1, -1)}

class LevelEditor:
    def __init__(self, scale, level_name : str):
        self.scale = scale

        self.screen = pygame.display.set_mode((640 * self.scale, 360* self.scale))#16 *4: 9 * 4
        self.camera = [0, 0]
        
        self.selected = {1 : Type.BLOCK,
                         2 : Type.SPIKE_CUBE,
                         3 : Type.SPIKE_SNAKE}
        self.bar = 0
        self.key_press = 1
        self.cursor_size = 1
        self.block_size = 10

        self.selected_level:str = "levels/" + level_name
        with open(self.selected_level , "r") as f:
            self.tilemap : dict = json.load(f)

            if self.tilemap != {}:
                for i in self.tilemap:
                    self.tilemap[i]["type"] = eval(self.tilemap[i]["type"])

        self.images = {
            Type.SPIKE_CUBE : load_image("spike_cube.png"),
            Type.BLOCK : load_images("tiles/"),
            Type.SPIKE_SNAKE : load_image("snake.png"),
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
    
    def render(self, tile, pos):
    
        if 0 < pos[0] *self.block_size - self.camera[0] < 640 * self.scale and 0 < pos[1] *self.block_size - self.camera[1] < 360 * self.scale:
            if tile["type"] == Type.BLOCK:
                draw_rect = pygame.Rect((tile["pos"][0] * self.block_size - self.camera[0]) * self.scale, (tile["pos"][1] * self.block_size - self.camera[1])* self.scale, self.block_size* self.scale, self.block_size* self.scale)
                self.screen.blit(pygame.transform.scale(self.images[Type.BLOCK][tile["variant"]], (draw_rect.width, draw_rect.height )), draw_rect.topleft)
            
            elif tile["type"] in Type.SPIKES:
                draw_rect = pygame.Rect((tile["pos"][0] * self.block_size- self.camera[0]) * self.scale, (tile["pos"][1] * self.block_size- self.camera[1])* self.scale,
                                        self.block_size* self.scale, self.block_size* self.scale)
                self.screen.blit(pygame.transform.scale(self.images[tile["type"]], (draw_rect.width, draw_rect.height )), draw_rect.topleft)

    def quit(self):
        for i in self.tilemap:
            self.tilemap[i]["type"] = str(self.tilemap[i]["type"])

        with open(self.selected_level , "w") as f:
            json.dump(self.tilemap, f)
        self.run = False

        self.tilemap = {}

    def create_tiles(self, mouse_pos, remove:bool):
        offset_len = range(int(-0.5 * self.cursor_size), int(0.5 * self.cursor_size + 1))
        block_pos = ((mouse_pos[0] + self.camera[0] * self.scale) // (self.block_size * self.scale), 
                    (mouse_pos[1] + self.camera[1]* self.scale) // (self.block_size * self.scale))

        for x_offset in offset_len: 
            for y_offset in offset_len:

                new_block_pos = (block_pos[0] + x_offset, block_pos[1] + y_offset)
                t = self.selected[self.key_press] if self.key_press in self.selected else Type.BLOCK
                
                self.create_tile(new_block_pos, t, remove)

    def create_tile(self, pos: tuple[int, int], type: Type, remove: bool):
        tile_str:str = self.pos_to_str(pos)

        if remove: 
            if tile_str in self.tilemap:
                sort = self.tilemap[tile_str]["type"]
                self.tilemap.pop(tile_str)

                if sort == Type.BLOCK:
                    self.update_block_variants(pos)
                
            return
        
        if type == Type.BLOCK: 
            self.tilemap[tile_str] = {"pos": pos, "type": type, "variant": 1}
            self.update_block_variants(pos)
        if type in Type.SPIKES:
            self.tilemap[tile_str] = {"pos": pos, "type": type}

    def update_block_variants(self, new_block_pos) -> int:
        surrounding_blocks = []
        for offset in OFFSETS + CORNER_OFFSETS:
            surrounding_block: str = self.pos_to_str(new_block_pos, offset)
            try:
                if self.tilemap[surrounding_block]["type"] == Type.BLOCK: 
                    surrounding_blocks.append((new_block_pos[0] + offset[0], new_block_pos[1] + offset[1]))
            except KeyError: pass

        
        for block in surrounding_blocks: #could save tiles_around for every tile to optimize
            tiles_around = {(0, -1) : False, (0, 1) : False, (-1, 0) : False,(1, 0) : False,}
            
            #find tiles aound
            for offset in OFFSETS:
                try:
                    if self.tilemap[self.pos_to_str(block, offset)]["type"] == Type.BLOCK: 
                        tiles_around[offset] = True
                except KeyError: pass
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
                    try:
                        if self.tilemap[self.pos_to_str(block, corner)]["type"] == Type.BLOCK: 
                            corners[corner] = True
                        else: missing += 1
                    except KeyError: missing += 1

                if not corners[(-1, -1)]: block_str += "TOPLEFT"
                elif not corners[(1, -1)]: block_str += "TOPRIGHT"

                if not corners[(-1, 1)]: block_str += "BOTTOMLEFT"   
                elif not corners[(1, 1)]: block_str += "BOTTOMRIGHT"

                if block_str == "": block_str = "FREE"
                elif missing in (3, 4) : block_str = "ALL"
                elif block_str == "TOPLEFTBOTTOMLEFT": block_str = "RIGHT"
                elif block_str == "TOPRIGHTBOTTOMRIGHT": block_str = "LEFT"
                else: block_str += "_CORNER"
            
            else: 
                
                if tiles_around[(0, -1)]: block_str += "TOP"
                if tiles_around[(0, 1)]: block_str += "BOTTOM"

                if tiles_around[(-1, 0)]: block_str += "LEFT"
                if tiles_around[(1, 0)]: block_str += "RIGHT"

                block_str = block_str.removeprefix("TOPBOTTOM").removesuffix("LEFTRIGHT")
                
                if block_str in OPPOSING_CORNER:
                    try:
                        if self.tilemap[self.pos_to_str(block, OPPOSING_CORNER[block_str])]["type"] != Type.BLOCK:
                            block_str = "ALL"
                    except KeyError: block_str = "ALL"
                
            if block_str == "": block_str = "ALL"
            self.tilemap[self.pos_to_str(block)]["variant"] = eval("BlockVariants." + block_str)
            #print("BlockVariants." + block_str)
    
    def pos_to_str(self, pos, offset = (0, 0)) ->str:
        return str(int(pos[0] + offset[0])) + ";" + str(int(pos[1] + offset[1]))
    
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
                    
                    #movement
                    if event.key in (pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d):
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
                self.render(self.tilemap[i], tuple(map(int, i.split(";"))))

            mouse_pos = pygame.mouse.get_pos() 
            mouse_press = pygame.mouse.get_pressed()
            
            self.highlight_cursor(mouse_pos)

            if mouse_press[0] or mouse_press[2]:
                self.create_tiles(mouse_pos, mouse_press[2])

            self.clock.tick(60)
            pygame.display.update()

    def temp(self):
        self.tiles = {}
        for i in range(100):

        
            self.tiles[str(i)] = {"pos": [i, 0], "type" : "Type.BLOCK", "variant" : "3"}
            self.tiles[str(i+100)] = {"pos": [i, 40], "type" : "Type.BLOCK", "variant" : "1"}
            self.tiles[str(i+200)] = {"pos": [0, i], "type" : "Type.BLOCK", "variant" : "2"}
            self.tiles[str(i+300)] = {"pos": [60, i], "type" : "Type.BLOCK", "variant" : "4"}

        for i in range(10):
            self.tiles[str(i+400)] = {"pos": [12, i + 5], "type" : "Type.SPIKE_CUBE"}


        with open(self.selected_level , "w") as f:
            json.dump(self.tiles, f)