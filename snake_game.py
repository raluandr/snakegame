import pygame
import time
import random

# initialize Pygame
pygame.init()

# colors
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# screen dim
dis_width = 800
dis_height = 600

dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game')

# block size for snake and food
snake_block = 20  
snake_speed = 10  
# images
try:
    snake_head_img = pygame.image.load('snake_head.png')
    food_img = pygame.image.load('food.png')
    obstacle_img = pygame.image.load('obstacle.png')  
    snake_head_img = pygame.transform.scale(snake_head_img, (snake_block, snake_block))
    food_img = pygame.transform.scale(food_img, (snake_block, snake_block))
    obstacle_img = pygame.transform.scale(obstacle_img, (snake_block, snake_block))  
    print("Images loaded successfully.")
except pygame.error as e:
    print(f"Error loading image: {e}")
    pygame.quit()
    quit()

# sound effects
pygame.mixer.init()
try:
    eat_sound = pygame.mixer.Sound('eat.wav')
    game_over_sound = pygame.mixer.Sound('game_over.wav')
except pygame.error as e:
    print(f"Error loading sound: {e}")
    pygame.quit()
    quit()

# set up the clock for controlling the game's frame rate
clock = pygame.time.Clock()

# fonts
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

# current score
def your_score(score):
    value = score_font.render("Your Score: " + str(score), True, black)
    dis.blit(value, [0, 0])

# high score
def high_score(high_score):
    value = score_font.render("High Score: " + str(high_score), True, black)
    dis.blit(value, [dis_width - 200, 0])

# draw the snake
def our_snake(snake_block, snake_list):
    for x in snake_list:
        dis.blit(snake_head_img, (x[0], x[1]))

# display a message
def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])

# draw obstacles
def draw_obstacles(obstacles):
    for obstacle in obstacles:
        dis.blit(obstacle_img, (obstacle[0], obstacle[1]))

# game
def gameLoop():
    game_over = False
    game_close = False

    # init pos of snake
    x1 = dis_width / 2
    y1 = dis_height / 2

    # init movement of snake
    x1_change = 0
    y1_change = 0

    # snake list and init length
    snake_List = []
    Length_of_snake = 1

    # pos of the food
    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    # obs
    obstacles = [[round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0,
                  round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0]
                 for _ in range(10)]

    # high score
    high_score_value = 0

    
    while not game_over:

        # game over
        while game_close:
            dis.fill(blue)
            message("You Lost! Press Q-Quit or C-Play Again", red)
            your_score(Length_of_snake - 1)
            high_score(high_score_value)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        # collisions with boundaries
        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True
            pygame.mixer.Sound.play(game_over_sound)
        x1 += x1_change
        y1 += y1_change
        dis.fill(blue)
        dis.blit(food_img, (foodx, foody))
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        # collisions with itself
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True
                pygame.mixer.Sound.play(game_over_sound)

        # collisions with obstacles
        for obstacle in obstacles:
            if x1 == obstacle[0] and y1 == obstacle[1]:
                game_close = True
                pygame.mixer.Sound.play(game_over_sound)

        our_snake(snake_block, snake_List)
        draw_obstacles(obstacles)
        your_score(Length_of_snake - 1)
        high_score(high_score_value)

        pygame.display.update()

        # if the snake has eaten the food
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1
            pygame.mixer.Sound.play(eat_sound)

            # update high score
            if Length_of_snake - 1 > high_score_value:
                high_score_value = Length_of_snake - 1

        # control the speed of the snake
        clock.tick(snake_speed)

    # quit the game
    pygame.quit()
    quit()

gameLoop()
