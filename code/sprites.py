from settings import * 
from random import choice, uniform


class Paddle(pygame.sprite.Sprite):
    def __init__(self, pos, speed, groups):
        super().__init__(groups)
        # image
        self.image = pygame.Surface(SIZE['paddle'], pygame.SRCALPHA) 
        pygame.draw.rect(self.image, COLORS['paddle'], pygame.FRect((0,0), SIZE['paddle']), 0, 5)
        # shadow
        self.shadow_surf = self.image.copy()
        pygame.draw.rect(self.shadow_surf, COLORS['paddle shadow'], pygame.FRect((0,0), SIZE['paddle']), 0, 5)  

        # rect & movement
        self.rect = self.image.get_frect(center = pos)
        self.old_rect = self.rect.copy()
        self.speed = speed
        self.direction = 0

    def move(self, dt):
        self.rect.centery += self.speed * self.direction * dt
        self.rect.bottom = WINDOW_HEIGHT if self.rect.bottom > WINDOW_HEIGHT else self.rect.bottom
        self.rect.top = 0 if self.rect.top < 0 else self.rect.top

    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.get_direction()
        self.move(dt)


class Player(Paddle):
    def __init__(self, pos, speed, groups):
        super().__init__(pos, speed, groups)

    def get_direction(self):
        keys = pygame.key.get_pressed()
        self.direction = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])


class Opponent(Paddle):
    def __init__(self, pos, speed, groups, ball):
        super().__init__(pos, speed, groups)
        self.ball = ball

    def get_direction(self):
        self.direction = 1 if self.rect.centery < self.ball.rect.centery else -1
        if self.ball.direction.x >= 0:
            self.direction = 0
        #if self.ball.rect.centerx > WINDOW_WIDTH/2 and self.ball.direction.x >= 0:
        #    self.direction = 0

class Ball(pygame.sprite.Sprite):
    def __init__(self, groups, paddle_sprites, update_score):
        super().__init__(groups)
        self.paddle_sprites = paddle_sprites
        self.update_score = update_score

        # image
        self.image = pygame.Surface(SIZE['ball'], pygame.SRCALPHA)
        pygame.draw.circle(self.image, COLORS['ball'], (SIZE['ball'][0]/2,SIZE['ball'][1]/2), SIZE['ball'][0]/2)
        # shadow
        self.shadow_surf = self.image.copy()
        pygame.draw.circle(self.shadow_surf, COLORS['ball shadow'], (SIZE['ball'][0]/2,SIZE['ball'][1]/2), SIZE['ball'][0]/2)
        
        # rect & movement
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
        self.old_rect = self.rect.copy()
        self.speed = SPEED['ball']
        self.direction = pygame.Vector2(choice((1,-1)),uniform(0.7,0.8) * choice((-1,1)))
        self.speed_modifier = 0
        
        # spawn timer
        self.start_time = pygame.time.get_ticks()
        self.duration = 1200

    def move(self, dt):
        self.rect.x += self.direction.x * self.speed * dt * self.speed_modifier
        self.collisions("horizontal")
        self.rect.y += self.direction.y * self.speed * dt * self.speed_modifier
        self.collisions("vertical")

    def collisions(self, direction): # remember add self.old_rect = self.rect.copy() to both sprites & update it 
        for sprite in self.paddle_sprites:
            if sprite.rect.colliderect(self.rect):
                if direction == "horizontal":
                    if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                        self.rect.right = sprite.rect.left
                        self.direction.x *= -1
                    elif self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
                        self.rect.left = sprite.rect.right
                        self.direction.x *= -1
                else:
                    if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                        self.rect.bottom = sprite.rect.top
                        self.direction.y *= -1
                    elif self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                        self.rect.top = sprite.rect.bottom
                        self.direction.y *= -1

    def wall_collision(self):
        if self.rect.top <= 0:
            self.rect.top = 0
            self.direction.y *= -1
        
        if self.rect.bottom >= WINDOW_HEIGHT:
            self.rect.bottom = WINDOW_HEIGHT
            self.direction.y *= -1
        
        if self.rect.right >= WINDOW_WIDTH or self.rect.left <= 0:
            self.update_score('player' if self.rect.x < WINDOW_WIDTH/2 else 'opponent')
            self.direction = pygame.Vector2()
            self.reset()

    def reset_timer(self):
        if pygame.time.get_ticks() - self.start_time >= self.duration:
            self.speed_modifier = 1
        else:
            self.speed_modifier = 0

    def reset(self):
        self.rect.center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2) 
        self.direction = pygame.Vector2(choice((1,-1)),uniform(0.7,0.8) * choice((-1,1)))
        self.start_time = pygame.time.get_ticks()

    def update(self, dt):
        self.old_rect = self.rect.copy() # previous frame
        self.reset_timer()
        self.move(dt) # current frame
        self.wall_collision()


