import pygame
import json

from scripts.load_images import load_images, load_image
from scripts.enums import Type, BlockVariants

class LevelEditor:
    def __init__(self, scale):
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


        with open("json_files/levels.json" , "r") as f:
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
                self.screen.blit(pygame.transform.scale(self.images[tile["type"]][int(tile["variant"])], (draw_rect.width, draw_rect.height )), draw_rect.topleft)
            
            elif tile["type"] in Type.SPIKES:
                draw_rect = pygame.Rect((tile["pos"][0] * self.block_size- self.camera[0]) * self.scale, (tile["pos"][1] * self.block_size- self.camera[1])* self.scale,
                                        self.block_size* self.scale, self.block_size* self.scale)
                self.screen.blit(pygame.transform.scale(self.images[tile["type"]], (draw_rect.width, draw_rect.height )), draw_rect.topleft)

    def quit(self):
        for i in self.tilemap:
            self.tilemap[i]["type"] = str(self.tilemap[i]["type"])

        with open("json_files/levels.json" , "w") as f:
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
        tile_str:str = str(int(pos[0])) + ";" + str(int(pos[1]))

        if remove: 
            if tile_str in self.tilemap:
                if self.tilemap[tile_str]["type"] == Type.BLOCK:
                    self.update_variants(pos, add = False)
                self.tilemap.pop(tile_str)
            return
        
        if type == Type.BLOCK: 
            self.tilemap[tile_str] = {"pos": pos, "type": type, "variant": 1}
            self.update_variants(pos, add = True)
        if type in Type.SPIKES:
            self.tilemap[tile_str] = {"pos": pos, "type": type}

    def update_variants(self, new_block_pos, add: bool = True): #TODO
        pass
    
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

        
            self.tiles[str(i)] = {"pos": [i, 0], "type" : Type.BLOCK, "variant" : "3"}
            self.tiles[str(i+100)] = {"pos": [i, 40], "type" : "block", "variant" : "1"}
            self.tiles[str(i+200)] = {"pos": [0, i], "type" : "block", "variant" : "2"}
            self.tiles[str(i+300)] = {"pos": [60, i], "type" : "block", "variant" : "4"}

        for i in range(10):
            self.tiles[str(i+400)] = {"pos": [12, i + 5], "type" : "spike", "variant" : "snake"}


        with open("json_files/levels.json" , "w") as f:
            json.dump(self.tiles, f)