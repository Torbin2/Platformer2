import pygame

class LevelEditor:
    def __init__(self, scale):
        self.scale = scale

        self.screen = pygame.display.set_mode((640 * self.scale, 360* self.scale))#16 *4: 9 * 4
        
        self.clock = pygame.time.Clock()

    def main(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    return
            print("a")

            self.screen.fill("darkgreen")

            self.clock.tick(60)
            pygame.display.update()

#FORMAT IN JSON:{"xy" : [IsBlock?(bool) ,x ,y , color, type],
#                "xy" : [IsBlock?(bool) ,x ,y , color, type], }