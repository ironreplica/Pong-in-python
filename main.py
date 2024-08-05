import pygame
# Followed along with Tech with Tims youtube tutorial. https://www.youtube.com/watch?v=vVGTZlnnX3U
import pygame.docs

# Initialization
pygame.init()

# Setting up the window
WIDTH, HEIGHT = 900, 700
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pong')

WHITE = (255,255,255)
BLACK = (0,0,0)

PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_RADIUS = 6

WINNING_SCORE = 10

SCORE_FONT = pygame.font.SysFont('comicsans', 50)

class Paddle:
    COLOR = WHITE
    VELOCITY = 4
    def __init__(self, x, y, width, height):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height
        
    def draw(self, window):
        pygame.draw.rect(window, self.COLOR, (self.x, self.y, self.width, self.height))
    def move(self, up=True):
        if up:
            self.y -= self.VELOCITY
        else:
            self.y += self.VELOCITY
    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
# Ball
class Ball:
    MAX_VEL = 5
    COLOR = WHITE
    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_vel = self.MAX_VEL
        self.y_vel = 0
    def draw(self, window):
        pygame.draw.circle(window, self.COLOR, (self.x,self.y),self.radius)
    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel
    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_vel = 0
        self.x_vel *= -1


# Drawing on the screen
def draw(window, paddles, ball, l_score, r_score):
    window.fill(BLACK)
    
    left_score_text = SCORE_FONT.render(f'{l_score}', 1, WHITE)
    right_score_text = SCORE_FONT.render(f'{r_score}', 1, WHITE)
    window.blit(left_score_text, (WIDTH//4 - left_score_text.get_width()/2, 20))
    window.blit(right_score_text, (WIDTH * (3/4) - right_score_text.get_width()/2, 20))
    
    for paddle in paddles:
        paddle.draw(WINDOW)
    for i in range(10, HEIGHT, HEIGHT//20):
        if i % 2 == 1:
            continue
        pygame.draw.rect(window, WHITE, (WIDTH//2 - 5, i, 10, HEIGHT//20))
        
    ball.draw(window)
    pygame.display.update()

# Handling the collision
def handle_collision(ball, left_paddle, right_paddle):
    # Ceiling collision
    if ball.y + ball.radius >= HEIGHT:
        ball.y_vel *= -1
    # Floor collision
    elif ball.y - ball.radius <= 0:
        ball.y_vel *= -1
    
    if ball.x_vel < 0:
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_vel *= -1
                
                middle_y = left_paddle.y + left_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (left_paddle.height / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel
    else:
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_vel *= -1
                
                middle_y = right_paddle.y + right_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (right_paddle.height / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel

# Paddle movement
def handle_paddle_movement(keys, left_paddle, right_paddle):
    if keys[pygame.K_w] and left_paddle.y - left_paddle.VELOCITY >= 0:
        left_paddle.move(up=True)
    if keys[pygame.K_s] and left_paddle.y + left_paddle.VELOCITY + left_paddle.height <= HEIGHT:
        left_paddle.move(up=False)
    if keys[pygame.K_UP] and right_paddle.y - right_paddle.VELOCITY >= 0:
        right_paddle.move(up=True)
    if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.VELOCITY + right_paddle.height <= HEIGHT:
        right_paddle.move(up=False)

# Main loop
def main():
    running = True
    clock = pygame.time.Clock()
    
    left_paddle = Paddle(10, HEIGHT//2 - PADDLE_HEIGHT //2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT //2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = Ball(WIDTH//2, HEIGHT//2, BALL_RADIUS)
    
    left_score = 0
    right_score = 0
    
    
    
    while running:
        clock.tick(60) # FPS
        draw(WINDOW, [left_paddle,right_paddle], ball, left_score, right_score)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys, left_paddle, right_paddle)
        ball.move()
        handle_collision(ball,left_paddle,right_paddle)
        
        if ball.x < 0:
            right_score += 1
            ball.reset()
        elif ball.x > WIDTH:
            left_score += 1
            ball.reset()
        if left_score >= WINNING_SCORE:
            win_text = 'Left Player Won!'
            text = SCORE_FONT.render(win_text, 1, WHITE)
            WINDOW.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
            pygame.display.update()
            pygame.time.delay(5000)
            left_paddle.reset()
            right_paddle.reset()
            ball.reset()
            left_score = 0
            right_score = 0
        elif right_score >= WINNING_SCORE:
            win_text = 'Right Player Won!'
            text = SCORE_FONT.render(win_text, 1, WHITE)
            WINDOW.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
            pygame.display.update()
            pygame.time.delay(5000)
            left_paddle.reset()
            right_paddle.reset()
            ball.reset()
            left_score = 0
            right_score = 0
    pygame.quit()
    
if __name__ == '__main__':
    main()