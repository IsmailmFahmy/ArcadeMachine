import pygame


def get_game_config():
    """
    Provides the general configuration settings for the Snake game.

    Returns:
        dict: A dictionary containing the following keys:
            - "snake_speed" (int): The speed of the snake in frames per second.
            - "window_size" (tuple): The dimensions of the game window (width, height).
            - "colors" (dict): Colors used in the game:
                - "black": Background color.
                - "white": Fruit and text color.
                - "green": Snake color.
            - "fruits_path" (dict): Paths to fruit sprite images.
            - "fruits_scale" (tuple): Scale for the fruit sprites (width, height).
    """
    # Speed of snake (frames per second)
    snake_speed = 15

    # Window size
    window_x = 720
    window_y = 480

    # Colors
    black = pygame.Color(0, 0, 0)  # Background color of the game
    white = pygame.Color(255, 255, 255)  # Fruit and text color
    green = pygame.Color(0, 255, 0)  # Snake color
    red = pygame.Color(255, 0, 0)  # game over

    # fruits path
    APPLE_PATH = "assets/sprites/apple1.png"
    BANANA_PATH = "assets/sprites/banana1.png"
    CHERRY_PATH = "assets/sprites/cherry.png"
    COCONUT_PATH = "assets/sprites/coconut.png"
    STRAWBERRY_PATH = "assets/sprites/strawberry1.png"
    # fruits scale

    return {
        "snake_speed": snake_speed,
        "window_size": (window_x, window_y),
        "colors": {
            "black": black,
            "white": white,
            "green": green,
            "red": red,
        },
        "fruits_path": {
            "apple": APPLE_PATH,
            "banana": BANANA_PATH,
            "cherry": CHERRY_PATH,
            "coconut": COCONUT_PATH,
            "strawbarry": STRAWBERRY_PATH,
        },
    }


def initialize_snake():
    """
    Initializes the snake's starting position and body.

    Returns:
        tuple:
            - list: The initial position of the snake's head [x, y].
            - list: The initial segments of the snake's body, each represented as [x, y].
    """
    # Define the snake's initial position
    # HINT: Adjust these values for a different starting point.
    initial_snake_position = [100, 50]

    # Define the snake's initial body
    # HINT: You can increase or decrease the number of blocks for a longer or shorter starting snake.
    initial_snake_body = [[100, 50], [90, 50], [80, 50], [70, 50]]

    return initial_snake_position, initial_snake_body
