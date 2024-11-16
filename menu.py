import pygame
import json

class Menu:
    def __init__(self):

        try:
            with open("settings.json", "r") as f:
                self.settings = json.load(f)
        except FileNotFoundError:
            self.settings = {
                "window_size": 2,
                "high_fps": False,
                "sound": False,
                "back": ""
            }
            with open("settings.json", "w") as f:
                json.dump(self.settings, f)
        
        self.scale = self.settings["window_size"]

        self.screen = pygame.display.set_mode((480 * self.scale, 270* self.scale))
        pygame.display.set_caption('game')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(pygame.font.get_default_font(), 25* self.scale)
        self.colors = ["#041413", "#25BEB3", "#146963"]

        self.viewing = "main"
        self.selected = 0
        

        self.options = {"start" : 40,
                        "options" : 140,
                        "quit" : 180}
        


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
                rect = text.get_rect(topleft = (4 * self.scale , num * 24 * self.scale))
                self.screen.blit(text, rect)  

                #setting value
                text = self.font.render(str(self.settings[key]), 1, (fill))
                rect = text.get_rect(topright = (self.screen.get_width() - 4 * self.scale, num * 24 * self.scale))
                self.screen.blit(text, rect)  

    def apply_setting(self):#scuffed
        self.scale = self.settings["window_size"]
        self.screen = pygame.display.set_mode((480 * self.scale, 270* self.scale))
        self.font = pygame.font.Font(pygame.font.get_default_font(), 25* self.scale)

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
                                case 1: self.viewing = 'settings'
                                case 2:
                                    pygame.quit()
                                    exit()

                        elif self.viewing == 'settings':
                            match self.selected:
                                case 0: 
                                    if self.settings["window_size"] >= 9: self.settings["window_size"] = 1 
                                    else: self.settings["window_size"] += 1

                                case 1: 
                                    self.settings["high_fps"] = not self.settings["high_fps"]
                                
                                case 2: 
                                    self.settings["sound"] = not self.settings["sound"]

                                case 3: 
                                    self.viewing = 'main'
                                    self.selected = 0
                                    self.apply_setting()
                                    
                                    with open('settings.json', "w") as f:
                                        json.dump(self.settings, f)

            self.screen.fill(self.colors[0])
            self.render()

            self.clock.tick(60)
            pygame.display.update()