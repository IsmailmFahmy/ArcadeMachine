"""
Snake Game Implementation

This script implements the classic Snake game using Pygame. It includes various challenges for functionality,
such as generating fruit, detecting collisions, and managing game state.
"""
import sys
import os
import time
from operator import truediv

import pygame
import random
from config import get_game_config, initialize_snake

################################################################################################################
# Functions
def Store_Score(score):
    full_score=[]
    with open("score.txt", "a") as f:
        f.write(str(score) + "\n")
        f.close()
    with open("score.txt", "r") as f:
        for line in f.readlines():
            full_score.append(int(line))
        f.close()
    print(full_score)
    return full_score

def pause_screen(game_window,windowx,windowy,colors):
    PAUSED=True
    while PAUSED:
        rank_font = pygame.font.SysFont('Arial bold', 50)

        rank_surface = rank_font.render('PRESS SPACE TO CONTINUE', True, colors["green"])
        center=rank_surface.get_rect(center=(windowx/2, windowy/2))
        game_window.blit(rank_surface,center)


        score_txt=rank_font.render(f'Score: {score}',True,(34,56,45))

        text_width, _ = score_txt.get_size()
        text_x = windowx - text_width - 20  # Align to the right edge
        text_y = 0
        game_window.blit(score_txt,(text_x, text_y))


        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # CHALLENGE 1: Improve input handling for smoother gameplay
                if event.key == pygame.K_SPACE:
                    PAUSED=False

def generate_boom_position(snake_body,window_x, window_y,fruit_list,boom_list,score):
    """
    generates a random position for the boom.

    Args:
        snake_body
        window_y
        window_x
        fruit
        boom_list
        len boomlist =score//50

    returns:
        new boom list
    """
    print("boom number:"+str(score//50))
    if len(boom_list)<score//50+1:
        boomx = snake_body[0][0]
        boomy = snake_body[0][1]
        checklist= fruit_list+snake_body+boom_list
        while [boomx,boomy] in checklist:
            boomx = random.randint(0,window_x//10)*10
            boomy = random.randint(0,window_y//10)*10
        boom_list.append([boomx,boomy])
    return boom_list


def generate_fruit_position(snake_body, window_x, window_y):
    """
    Generates a random position for the fruit, ensuring it does not overlap with the snake's body.

    Args:
        snake_body (list): List of [x, y] positions representing the snake's body.
        window_x (int): Width of the game window.
        window_y (int): Height of the game window.

    Returns:
        tuple: A tuple (x, y) representing the fruit's position.
    """
    # CHALLENGE 4: make sure the fruit doesn't spawn on the snakes body
    # CHALLENGE 2: Implement the function generate_fruit_position to spawn a fruit RANDOMLY
    fruitx=snake_body[0][0]
    fruity=snake_body[0][1]

    for [fruitx, fruity] in snake_body:
        fruitx=random.randint(0,int(window_x/10))*10
        fruity=random.randint(0,int(window_y/10))*10

    return fruitx, fruity



def check_boundary_collision(snake_position, window_x, window_y):
    """
    Checks if the snake's head has collided with the game window's boundary.

    Args:
        snake_position (list): [x, y] position of the snake's head.
        window_x (int): Width of the game window.
        window_y (int): Height of the game window.

    Returns:
        bool: True if a collision occurred, False otherwise.
    """
    # CHALLENGE 5: stay Inside the Arena!!
    if snake_position[0] < 0 or snake_position[0] >= window_x or snake_position[1] < 0 or snake_position[1] >= window_y:
        return True
    else:
        return False
    pass



def check_self_collision(snake_position, snake_body):
    """
    Checks if the snake's head has collided with its own body.

    Args:
        snake_position (list): [x, y] position of the snake's head.
        snake_body (list): List of [x, y] positions representing the snake's body.

    Returns:
        bool: True if a self-collision occurred, False otherwise.
    """
    # CHALLENGE 6: Stay in One Piece!!
    if snake_position in snake_body[1:]:
        return True
    else :
        return False
    pass

def check_boom_collision(snake_position, boom_list):
    if(snake_position in boom_list):
        return True
    else:
        return False

def game_over(game_window,window_x,window_y,colors,score):
    """
    Handles the Game Over sequence, displaying a message and pausing the game before quitting.

    Args:
        game_window (pygame.Surface): The Pygame surface for the game window.
        window_x (int): Width of the game window.
        window_y (int): Height of the game window.
        colors (dict): Dictionary of color mappings.

    Returns:
        None
    """
    # CHALLENGE 7: Game Over in Style!
    game_over_font = pygame.font.SysFont('Arial bold', 80)
    game_window.fill(colors['red'])
    game_over_text = game_over_font.render('Game Over', True, colors["green"])
    game_over_pos =game_over_text.get_rect(center=(window_x/2, (window_y/2) - (window_x // 5) ))
    game_window.blit(game_over_text, game_over_pos)

    store_score = Store_Score(score)
    store_score.sort(reverse=True)
    print("Game Over,score:"+str(score))
    print("Full score list"+str(store_score))



    # CURRENT SCORE TEXT RENDER
    score_font = pygame.font.SysFont('Arial bold', 40)
    score_txt=score_font.render(f'Score: {score}',True,(34,56,45))
    text_width, _ = score_txt.get_size()
    text_x = window_x - text_width - 50  # Align to the right edge
    text_y = 0
    game_window.blit(score_txt,(text_x, text_y))


    # rank_surface = rank_font.render('Ranking', True, colors["green"])
    # center=rank_surface.get_rect(center=(window_x/2, window_y/2))
    # score_text = score_font.render('Your Score:'+str(score), True, colors["green"])

    # center=rank_surface.get_rect(center=(window_x/2, window_y/2))
    # score_pos = score_text.get_rect(center=(window_x/2, window_y/2))
    # game_window.blit(score_text,score_pos)


    # HIGH SCORE TEXT RENDER
    high_score_text = score_font.render(f'Highest Score: {str(store_score[0])}', True, colors["green"])
    high_score_pos = high_score_text.get_rect(center=(window_x/2, window_y/2))
    game_window.blit(high_score_text, high_score_pos)



    pygame.display.flip()

    time.sleep(3)  # render game over for 3 sec then quit
    pygame.quit()
    sys.exit()
    # pygame.draw.rect(game_window, colors['red'], (window_x//2, window_y//2, 10, 10))



# CHALLENGE 8: High-score (file operation)
# CHALLENGE 9: pause the screen

# CHALLENGE 10: Bombs


###########################################################################
# Setup

# # Initialize pygame
pygame.init()

# Load game configuration
config = get_game_config()
window_x, window_y = config["window_size"]
snake_speed = config["snake_speed"]
colors = config["colors"]
boom_list = []
# Create game window
boom_damage=3
pygame.display.set_caption("Snake")
game_window = pygame.display.set_mode((window_x, window_y))

imagename=["apple1.png","banana1.png","cherry.png","coconut.png","strawberry1.png"]
images=[]
sourceFileDir = os.path.dirname(os.path.abspath(__file__))
#image = pygame.image.load(os.path.join(sourceFileDir, "Images", "Frame1.png"))
#image load to array
defaultimagesize=[20,20]
for i in imagename:
    image=pygame.image.load(os.path.join(sourceFileDir, "assets", "sprites",i)).convert()
    image=pygame.transform.scale(image,defaultimagesize)
    images.append(image)


# Set up initial game state
snake_position, snake_body = initialize_snake()  # Initialize snake

# Initial fruit position (fixed position)
fruit_position = [360, 240]
fruit_spawn = True

#  CHALLENGE 2: call the function you implemented and spawn the fruit
fruit_position=generate_fruit_position(snake_body, window_x, window_y)

# Define the initial direction and score
direction = "RIGHT"  # Snake starts moving to the right
score = 0

# CHALLENGE 10 : initialisation of list of bombs

# Highscore file name
filename = "high_score.txt"

# Set up the clock for controlling the game speed
fps = pygame.time.Clock()

#################################################################
# Game loop
while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            # CHALLENGE 1: Improve input handling for smoother gameplay
            if event.key == pygame.K_LEFT and direction != "RIGHT":
                direction = "LEFT"
            elif event.key == pygame.K_RIGHT and direction != "LEFT":
                direction = "RIGHT"
            elif event.key == pygame.K_UP and direction != "DOWN":
                direction = "UP"
            elif event.key == pygame.K_DOWN and direction != "UP":
                direction = "DOWN"
            elif event.key == pygame.K_p:
                pause_screen(game_window,window_x,window_y,colors)
            elif event.key == pygame.K_SPACE:
                pause_screen(game_window, window_x, window_y, colors)


    # CHALLENGE 1: Movement logic
    if direction == "LEFT":
        snake_position[0] -= 10
    elif direction == "RIGHT":
        snake_position[0] += 10
    elif direction == "UP":
        snake_position[1] -= 10
    elif direction == "DOWN":
        snake_position[1] += 10
    # Snake body growing mechanism if fruit and snake collide score
    snake_body.insert(0, list(snake_position))
    if (
        snake_position[0] in [fruit_position[0],fruit_position[0]+10]
        and snake_position[1] in [fruit_position[1],fruit_position[1]+10]
    ):
        fruit_position=generate_fruit_position(snake_body, window_x, window_y)
        score += 1
        print(score)
        boom_list=generate_boom_position(snake_body,window_x,window_y,[fruit_position],boom_list,score)
        pass
    else:
        snake_body.pop()

    # CHALLENGE 3: Generate a new fruit position when the previous one is eaten (Hints 3 and 4)

    if(check_boundary_collision(snake_position, window_x, window_y)):
        game_over(game_window,window_x,window_y,colors,score)
    # CHALLENGE 5: make sure the 'check_boundary_collision' is used

    if(check_self_collision(snake_position, snake_body)):
        game_over(game_window,window_x,window_y,colors,score)
    # CHALLENGE 6: call the function you implemented

    # CHALLENGE 8: High-score Logic
    if(check_boom_collision(snake_position,boom_list)):
        boom_list.remove(snake_position)
        boom_list=generate_boom_position(snake_body,window_x,window_y,[fruit_position],boom_list,score)
        if len(snake_body)<=boom_damage:
            game_over(game_window,window_x,window_y,colors,score)
        else:
            score -= boom_damage//2
            #score = max(score,0)
            for i in range(boom_damage):
                snake_body.pop()

    # CHALLENGE 10: use the function you implemented

    # Draw the game window
    game_window.fill(colors["black"])  # Fill background
    for pos in snake_body:
        pygame.draw.rect(
            game_window, colors["green"], pygame.Rect(pos[0], pos[1], 10, 10)
        )  # Draw snake

    # CHALLENGE 11
    for boom in boom_list:
        pygame.draw.rect(
            game_window,
            colors["red"],
            pygame.Rect(boom[0], boom[1], 10, 10),
        )

    pygame.draw.rect(
        game_window,
        colors["white"],
        pygame.Rect(fruit_position[0], fruit_position[1], 10, 10),
    )  # Draw fruit

    game_window.blit(images[4], fruit_position)
   # pygame.display.flip()
    pygame.display.update()
    fps.tick(snake_speed)
