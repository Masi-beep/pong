from settings import *


class Paddle(pygame.sprite.Sprite):
    def __init__(self, pos, speed, groups):
        super().__init__(groups)
        self.image = pygame.Surface(SIZE['paddle'])
        self.image.fill(COLORS['paddle'])
        self.rect = self.image.get_frect(center = pos)
        self.speed = speed
        self.direction = pygame.Vector2()
    
    # this update method would probably move to a inherited player class but works for now
    def update(self, dt):
        if self.rect.bottom > WINDOW_HEIGHT:
            self.rect.bottom = WINDOW_HEIGHT 
        elif self.rect.top < 0:
            self.rect.top = 0
        keys = pygame.key.get_pressed()
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.rect.center += self.speed * self.direction * dt


class Ball(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.Surface(SIZE['ball'])
        self.image.fill(COLORS['ball'])
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
        self.speed = SPEED['ball']
        self.direction = pygame.Vector2(1,1)

    def update(self, dt):
        if self.rect.bottom > WINDOW_HEIGHT or self.rect.top < 0:
            self.direction.y *= -1
        if self.rect.right > WINDOW_WIDTH or self.rect.left < 0:
            self.direction.x *= -1
        self.rect.center += self.direction * self.speed * dt


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("pong")
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
        self.running = True
        self.clock = pygame.time.Clock()

        # grop
        self.all_sprites = pygame.sprite.Group()

        # surfaces
        self.player = Paddle(POS['player'], SPEED['player'], self.all_sprites)
        self.ball = Ball(self.all_sprites)
        
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
            
