from settings import *
from sprites import Ball, Paddle


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("pong")
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
        self.running = True
        self.clock = pygame.time.Clock()

        # grop
        self.all_sprites = pygame.sprite.Group()
        self.paddle_sprites = pygame.sprite.Group()

        # sprites
        self.player = Paddle(POS['player'], SPEED['player'], (self.all_sprites, self.paddle_sprites))
        self.ball = Ball(self.all_sprites, self.paddle_sprites)
        
    def run(self):
        while self.running:
            #dt 
            dt = self.clock.tick() / 1000

            # events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # update
            self.all_sprites.update(dt)

            # draw
            self.display_surface.fill(COLORS['bg'])
            self.all_sprites.draw(self.display_surface)
            pygame.display.update()

        pygame.quit()

if __name__ == '__main__':
    Game().run()
            
