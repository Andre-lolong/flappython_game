import pygame, sys, random

# Initialize Game
pygame.init()
game_state = 1
score = 0
has_moved = False

# Window Setup
window_w = 400
window_h = 600
screen = pygame.display.set_mode((window_w, window_h))
pygame.display.set_caption("Flappython")
clock = pygame.time.Clock()
fps = 60

# Load Fonts
font = pygame.font.Font("fonts/BaiJamjuree-Bold.ttf", 60) 
# Load Sounds
slap_sfx = pygame.mixer.Sound("sounds/slap.wav") 
woosh_sfx = pygame.mixer.Sound("sounds/woosh.wav")
score_sfx = pygame.mixer.Sound("sounds/score.wav")

# Load Images
player_img = pygame.image.load("images/player.png") 
pipe_up_img = pygame.image.load("images/pipe_up.png")
pipe_down_img = pygame.image.load("images/pipe_down.png")
ground_img = pygame.image.load("images/ground.png")
bg_img = pygame.image.load("images/background.png")
bg_width = bg_img.get_width()

# Variable Setup
bg_scroll_spd = 1
ground_scroll_spd = 2

# Base class for game objects 
class GameObject:
    def __init__(self, x_value):
        self.x_value = x_value

    def update(self):
        pass

    def draw(self):
        pass

class Player(GameObject):
    def __init__(self, x_value, y_value):
        super().__init__(x_value) 
        self.y_value = y_value
        self.velocity = 0
        self.rect = pygame.Rect(self.x_value, self.y_value, player_img.get_width(), player_img.get_height())

    def jump(self):
        self.velocity = -10

    def update(self):
        self.velocity += 0.75
        self.y_value += self.velocity
        self.rect.y = self.y_value

    def draw(self):
        screen.blit(player_img, (self.x_value, self.y_value))

class Pipe(GameObject):
    def __init__(self, x_value, height, gap, velocity):
        super().__init__(x_value)
        self.height = height
        self.gap = gap
        self.velocity = velocity
        self.scored = False
        self.top_pipe_rect = pygame.Rect(self.x_value, 0, pipe_down_img.get_width(), self.height)
        self.bottom_pipe_rect = pygame.Rect(self.x_value, self.height + self.gap, pipe_up_img.get_width(), window_h - (self.height + self.gap))

    def update(self):
        self.x_value -= self.velocity
        self.top_pipe_rect.x = self.x_value
        self.bottom_pipe_rect.x = self.x_value

    def draw(self):
        # Draw top pipe
        screen.blit(pipe_down_img, (self.x_value, 0 - pipe_down_img.get_height() + self.height))
        # Draw bottom pipe
        screen.blit(pipe_up_img, (self.x_value, self.height + self.gap))

def scoreboard():
    show_score = font.render(str(score), True, (10, 40, 9))
    score_rect = show_score.get_rect(center=(window_w // 2, 64))
    screen.blit(show_score, score_rect)

def game():
    global game_state
    global score
    global has_moved
    bg_x_pos = 0
    ground_x_pos = 0

    player = Player(168, 300)
    pipes = [Pipe(600, random.randint(30, 250), 220, 2.4)]

    game_objects_to_draw_and_update = [player] + pipes

    while game_state != 0:
        while game_state == 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    has_moved = True
                    if event.key == pygame.K_SPACE:
                        pygame.mixer.Sound.play(woosh_sfx)
                        player.jump()

            if has_moved:
                for obj in game_objects_to_draw_and_update:
                    obj.update()

                for pipe in pipes:
                    if player.rect.colliderect(pipe.top_pipe_rect) or player.rect.colliderect(pipe.bottom_pipe_rect):
                        player = Player(168, 300)
                        pipes = [Pipe(600, random.randint(30, 250), 220, 2.4)]
                        game_objects_to_draw_and_update = [player] + pipes 
                        score = 0
                        has_moved = False
                        pygame.mixer.Sound.play(slap_sfx)

                if player.y_value < -64 or player.y_value > 536:
                    player = Player(168, 300)
                    pipes = [Pipe(600, random.randint(30, 250), 220, 2.4)]
                    game_objects_to_draw_and_update = [player] + pipes 
                    score = 0
                    has_moved = False
                    pygame.mixer.Sound.play(slap_sfx)

                if pipes[0].x_value < -pipe_up_img.get_width():
                    pipes.pop(0)
                    new_pipe = Pipe(400, random.randint(30, 280), 220, 2.4)
                    pipes.append(new_pipe)
                    game_objects_to_draw_and_update.append(new_pipe) 

                for pipe in pipes:
                    if not pipe.scored and pipe.x_value + pipe_up_img.get_width() < player.x_value:
                        score += 1
                        pygame.mixer.Sound.play(score_sfx)
                        pipe.scored = True

            bg_x_pos -= bg_scroll_spd
            ground_x_pos -= ground_scroll_spd

            if bg_x_pos <= -bg_width:
                bg_x_pos = 0
            if ground_x_pos <= -bg_width:
                ground_x_pos = 0

            screen.fill("blue")
            screen.blit(bg_img, (bg_x_pos, 0))
            screen.blit(bg_img, (bg_x_pos + bg_width, 0))
            screen.blit(ground_img, (ground_x_pos, 536))
            screen.blit(ground_img, (ground_x_pos + bg_width, 536))

            for obj in game_objects_to_draw_and_update:
                obj.draw()

            scoreboard()
            pygame.display.flip()
            clock.tick(fps)
game() 
