import json
import time
import typing

import pygame

from os import listdir


def render_loading_screen(screen: pygame.Surface, font: pygame.font.Font | None, background_color='#041413', color='#25BEB3'):
    screen.fill(background_color)
    if font is not None:
        s = font.render('Loading', True, color)
        screen.blit(s, [screen.get_size()[i] // 2 - s.get_size()[i] // 2 for i in range(2)])
    pygame.display.update()

_last_render_load_progress_indicator_time = None

def render_load_progress_indicator(screen: pygame.Surface, color='#25BEB3', height_mult: float = 0.1) -> typing.Callable[[float], None]:
    def _render_load_progress_indicator(progress: float) -> None:
        global _last_render_load_progress_indicator_time
        if _last_render_load_progress_indicator_time is None or time.time() - _last_render_load_progress_indicator_time > 0.1:
            height = screen.get_height() * height_mult
            y = screen.get_height() - height
            width = round(screen.get_width() * progress)

            pygame.draw.rect(screen, color, (0, y, width, height))
            pygame.display.update()
            _last_render_load_progress_indicator_time = time.time()

    return _render_load_progress_indicator


FONT_SIZE = 60
SCREEN_SIZE = (640, 360)

class Menu:
    def __init__(self):

        try:
            with open("settings.json", "r") as f:
                self.settings = json.load(f)
        except FileNotFoundError:
            self.settings = {
                "window_size": 1,
                "textures" : True,
                "high_fps": False,
                "sound": False,
                "level" : None,
            }
            with open("settings.json", "w") as f:
                json.dump(self.settings, f)
        
        self.scale = self.settings["window_size"]

        self.screen = pygame.display.set_mode((SCREEN_SIZE[0] * self.scale, SCREEN_SIZE[1]* self.scale))#16 *4: 9 * 4  
        self.clock = pygame.time.Clock()
        
        self.font = pygame.font.Font(pygame.font.get_default_font(), FONT_SIZE* self.scale)
        self.smaller_font = pygame.font.Font(pygame.font.get_default_font(), int(FONT_SIZE / 1.5) * self.scale)
        
        self.colors = ["#041413", "#25BEB3", "#146963"]

        self.viewing = "main"
        self.selected = 0
        
        self.options = {"start" : SCREEN_SIZE[1] // 6,
                        "level_editor" : SCREEN_SIZE[1] // 3,
                        "options" : SCREEN_SIZE[1] // 2 + FONT_SIZE*0.6,
                        "quit" : SCREEN_SIZE[1] // 2 + FONT_SIZE * 1.7}
        
        self.available_levels : list[str] = sorted(list(map(lambda x: x.removesuffix(".p2l"),listdir("levels/"))))
        if self.settings["level"] not in self.available_levels:
            if self.available_levels:
                level = self.available_levels[0]
                print(f'Level does not exist, loading {level}')
                self.settings["level"] = level
            else:
                raise EnvironmentError('No levels to load')

        
    def render(self):
        #print(sorted(self.options, key=lambda key: key[1]), sorted(self.options),sorted(self.options, key=lambda key: self.options[key]))
        if self.viewing == 'main':
            for num, key in enumerate(sorted(self.options, key=lambda key: self.options[key])):
                if num == self.selected: fill = self.colors[1]
                else: fill = self.colors[2]
                text = self.font.render(key, 1, (fill))
                rect = text.get_rect(midtop = (self.screen.get_width() / 2, self.options[key] * self.scale))

                self.screen.blit(text, rect)    
        
        elif self.viewing == 'settings': 
            for num, key in enumerate(sorted(self.settings)):
                if num == self.selected: fill = self.colors[1]
                else: fill = self.colors[2]
                #setting name
                text = self.smaller_font.render(key, 1, (fill))
                rect = text.get_rect(topleft = (10 * self.scale , num * int(FONT_SIZE *0.67) * self.scale))
                self.screen.blit(text, rect)  

                #setting value
                text = self.smaller_font.render(str(self.settings[key]), 1, (fill))
                rect = text.get_rect(topright = (self.screen.get_width() - 10 * self.scale, num * int(FONT_SIZE *0.67) * self.scale))
                self.screen.blit(text, rect)  
            #back button
            self.screen.blit(self.smaller_font.render("back", 1, (self.colors[1] if len(self.settings) == self.selected else self.colors[2])), 
                             text.get_rect(topleft = (10 * self.scale , len(self.settings) * int(FONT_SIZE *0.67) * self.scale))) 

    def apply_setting(self):
        self.scale = self.settings["window_size"]
        self.screen = pygame.display.set_mode((SCREEN_SIZE[0] * self.scale, SCREEN_SIZE[1]* self.scale))
        self.font = pygame.font.Font(pygame.font.get_default_font(), FONT_SIZE* self.scale)
        self.smaller_font = pygame.font.Font(pygame.font.get_default_font(), int(FONT_SIZE / 1.5) * self.scale)

    def handle_input(self):
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
                        elif self.viewing == "settings" and self.selected < len(self.settings) :
                            self.selected += 1

                    elif event.key == pygame.K_RETURN:
                        if self.viewing == 'main':
                            match self.selected:
                                case 0:
                                    self.run = False
                                case 1:
                                    from level_editor import LevelEditor
                                    LevelEditor(self.scale, self.screen, self.settings["level"]).main()
                                case 2: self.viewing = 'settings'
                                case 3:
                                    pygame.quit()
                                    exit()

                        elif self.viewing == 'settings': 
                            match sorted(self.settings)[self.selected] if self.selected < len(self.settings) else "back":
                                case "window_size": 
                                    if self.settings["window_size"] >= 4: self.settings["window_size"] = 1 
                                    else: self.settings["window_size"] += 1
                                
                                case "level": 
                                    next_level:int = (self.available_levels.index(self.settings["level"]) + 1) % len(self.available_levels)
                                    self.settings["level"] = self.available_levels[next_level]

                                case "textures": self.settings["textures"] = not self.settings["textures"]
                                case "high_fps": self.settings["high_fps"] = not self.settings["high_fps"]
                                case "sound": self.settings["sound"] = not self.settings["sound"]

                                case "back":
                                    self.viewing = 'main'
                                    self.selected = 0
                                    self.apply_setting()
                                    
                                    with open('settings.json', "w") as f:
                                        json.dump(self.settings, f)
                                case _:
                                    print("setting's not implented")

    def main(self, restart:bool = False):
        if restart: self.run = True
        while self.run:
            self.handle_input()

            self.screen.fill(self.colors[0])
            self.render()

            self.clock.tick(60)
            pygame.display.update()