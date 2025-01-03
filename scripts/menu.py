import pygame
import json
from scripts.level_editor import LevelEditor

FONT_SIZE = 35
class Menu:
    def __init__(self):

        try:
            with open("json_files/settings.json", "r") as f:
                self.settings = json.load(f)
        except FileNotFoundError:
            self.settings = {
                "window_size": 2,
                "textures" : False,
                "high_fps": False,
                "sound": False,
                "back": ""
            }
            with open("json_files/settings.json", "w") as f:
                json.dump(self.settings, f)
        
        self.scale = self.settings["window_size"]

        self.screen = pygame.display.set_mode((640 * self.scale, 360* self.scale))#16 *4: 9 * 4
        
        self.clock = pygame.time.Clock()
        
        self.font = pygame.font.Font(pygame.font.get_default_font(), FONT_SIZE* self.scale)
        self.colors = ["#041413", "#25BEB3", "#146963"]

        self.viewing = "main"
        self.selected = 0
        

        self.options = {"start" : 60,
                        "level_editor" : 110,
                        "options" : 210,
                        "quit" : 260}
        


    def render(self):
        if self.viewing == 'main':
            for num, key in enumerate(self.options):
                if num == self.selected: fill = self.colors[1]
                else: fill = self.colors[2]
                text = self.font.render(key, 1, (fill))
                rect = text.get_rect(midtop = (self.screen.get_width() / 2, self.options[key] * self.scale))

                self.screen.blit(text, rect)    
        
        elif self.viewing == 'settings': 
            for num, key in enumerate(self.settings):
                if num == self.selected: fill = self.colors[1]
                else: fill = self.colors[2]
                #setting name
                text = self.font.render(key, 1, (fill))
                rect = text.get_rect(topleft = (10 * self.scale , num * FONT_SIZE * self.scale))
                self.screen.blit(text, rect)  

                #setting value
                text = self.font.render(str(self.settings[key]), 1, (fill))
                rect = text.get_rect(topright = (self.screen.get_width() - 10 * self.scale, num * FONT_SIZE * self.scale))
                self.screen.blit(text, rect)  

    def apply_setting(self):
        self.scale = self.settings["window_size"]
        self.screen = pygame.display.set_mode((640 * self.scale, 360* self.scale))
        self.font = pygame.font.Font(pygame.font.get_default_font(), FONT_SIZE* self.scale)

    def main(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        if self.selected > 0:
                            self.selected -= 1
                    elif event.key == pygame.K_s:
                        if self.viewing == "main" and self.selected < len(self.options) - 1:
                            self.selected += 1
                        elif self.viewing == "settings" and self.selected < len(self.settings) -1 :
                            self.selected += 1

                    elif event.key == pygame.K_RETURN:
                        if self.viewing == 'main':
                            match self.selected:
                                case 0:
                                    return self.settings
                                case 1:
                                    LevelEditor(self.scale).main()
                                case 2: self.viewing = 'settings'
                                case 3:
                                    pygame.quit()
                                    exit()

                        elif self.viewing == 'settings':
                            if "textures" not in self.settings:
                                self.settings["textures"] = True
                            match self.selected:
                                case 0: 
                                    if self.settings["window_size"] >= 9: self.settings["window_size"] = 1 
                                    else: self.settings["window_size"] += 1
                                case 1: self.settings["textures"] = not self.settings["textures"]
                                case 2: 
                                    self.settings["high_fps"] = not self.settings["high_fps"]
                                
                                case 3: 
                                    self.settings["sound"] = not self.settings["sound"]

                                case 4: 
                                    self.viewing = 'main'
                                    self.selected = 0
                                    self.apply_setting()
                                    
                                    with open('json_files/settings.json', "w") as f:
                                        json.dump(self.settings, f)
                                case _: print("?")

            self.screen.fill(self.colors[0])
            self.render()

            self.clock.tick(60)
            pygame.display.update()