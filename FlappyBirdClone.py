
import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Set up the game window
screen_width = 400
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flappy Bird')

# Load game assets
bird_img = pygame.image.load('bird.png').convert_alpha()
pipe_img = pygame.image.load('pipe.png').convert_alpha()
bg_img = pygame.image.load('background.png').convert()
font = pygame.font.SysFont(None, 48)

# Define the Bird class
class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = bird_img
        self.rect = self.image.get_rect(center=(50, screen_height//2))
        self.velocity = 0
        self.gravity = 0.5
        self.jump_force = -10

    def update(self):
        self.velocity += self.gravity
        self.rect.y += self.velocity  

        if self.rect.top <= 0 or self.rect.bottom >= screen_height:
            game_over()

    def jump(self):
        self.velocity = self.jump_force

# Define the Pipe class
class Pipe(pygame.sprite.Sprite):
    def __init__(self, height, position, is_bottom):
        super().__init__()
        self.image = pygame.transform.scale(pipe_img, (50, height))
        if is_bottom:
            self.image = pygame.transform.rotate(self.image, 180)
            self.rect = self.image.get_rect(bottomleft=(position, screen_height))
        else:
            self.rect = self.image.get_rect(topleft=(position, 0))
        self.speed = 4
        self.passed = False

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()

    def check_pass(self, bird):
        if not self.passed and self.rect.right < bird.rect.left:
            self.passed = True
            return True
        return False

# Define the game objects
all_sprites = pygame.sprite.Group()
pipes = pygame.sprite.Group()
bird = Bird()
all_sprites.add(bird)

# Define game variables
score = 0

# Define game functions
def generate_pipes():
    pipe_gap = 200
    pipe_pos = screen_width + 60
    top_pipe_height = random.randint(50, screen_height//2 - pipe_gap//2)
    bottom_pipe_height = screen_height - top_pipe_height - pipe_gap
    top_pipe = Pipe(top_pipe_height, pipe_pos, False)
    bottom_pipe = Pipe(bottom_pipe_height, pipe_pos, True)
    pipes.add(top_pipe, bottom_pipe)
    all_sprites.add(top_pipe, bottom_pipe)

def show_score():
    score_text = font.render(str(score), True, (255, 255, 255))
    score_rect = score_text.get_rect(center=(screen_width//2, 50))
    screen.blit(score_text, score_rect)

def game_over():
    game_over_text = font.render('Game Over', True, (255, 255, 255))
    game_over_rect = game_over_text.get_rect(center=(screen_width//2, screen_height//2))
    screen.blit(game_over_text, game_over_rect)

    pygame.display.update()
    pygame.time.delay(2000)

    # Reset game variables and objects
    bird.rect.center = (50, screen_height//2)
    bird.velocity = 0
    pipes.empty()
    all_sprites.empty()
    all_sprites.add(bird)
    global score
    score = 0

def game_loop():
    global score
    
    running = True
    clock = pygame.time.Clock()
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()
        
        # Update game objects
        all_sprites.update()
        
        # Generate new pipes
        if len(pipes) < 3:
            generate_pipes()
        
        # Check for collisions
        if pygame.sprite.spritecollide(bird, pipes, False):
            game_over()
            running = False
        
        # Check for passing pipes
        for pipe in pipes:
            if pipe.check_pass(bird):
                score += 1
        
        # Draw game objects
        screen.blit(bg_img, (0, 0))
        all_sprites.draw(screen)
        show_score()
        
        # Update the display
        pygame.display.update()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

game_loop()
