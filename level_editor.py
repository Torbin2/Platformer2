import pygame
import json

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
                    self.temp()
                    return
            

            self.screen.fill("darkgreen")

            self.clock.tick(60)
            pygame.display.update()

    def temp(self):
        self.tiles = {}
        for i in range(100):

        
            self.tiles[str(i)] = {"pos": [i, 0], "type" : "block", "variant" : "3"}
            self.tiles[str(i+100)] = {"pos": [i, 30], "type" : "block", "variant" : "1"}
            self.tiles[str(i+200)] = {"pos": [0, i], "type" : "block", "variant" : "2"}
            self.tiles[str(i+300)] = {"pos": [60, i], "type" : "block", "variant" : "4"}

        for i in range(10):
            self.tiles[str(i+400)] = {"pos": [12, i + 5], "type" : "spike", "variant" : "snake"}


        with open("levels.json" , "w") as f:
            json.dump(self.tiles, f)
#FORMAT IN JSON:{"xy" : [IsBlock?(bool) ,x ,y , color, type],
#                "xy" : [IsBlock?(bool) ,x ,y , color, type], }