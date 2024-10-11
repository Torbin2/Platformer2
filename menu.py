import pygame

class Menu:
    def __init__(self):
        self.screen = pygame.display.set_mode((1000, 1000))
        pygame.display.set_caption('game')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(pygame.font.get_default_font(), 50)
        self.colors = ["#041413", "#25BEB3", "#146963"]
        

        self.options = {"start" : 25,
                        "options" : 50,
                        "quit" : 60 }
        self.selected = 0

        

    def render(self):

        for num, key in enumerate(self.options):
            if num == self.selected: fill = self.colors[1]
            else: fill = self.colors[2]
            text = self.font.render(key, 1, (fill))
            rect = text.get_rect(midtop = (500, self.options[key] * 10))

            self.screen.blit(text, rect)    

    def main(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        if self.selected != 0:
                            self.selected -= 1
                    elif event.key==pygame.K_s:
                        if self.selected != len(self.options):
                            self.selected += 1

                    elif event.key == pygame.K_RETURN:
                        match self.selected:
                            case 0:
                                return
                            case 1: pass
                            case 2:
                                pygame.quit()
                                exit()
                                

                            
            self.screen.fill(self.colors[0])

            self.render()

            self.clock.tick(60)
            pygame.display.update()
            



