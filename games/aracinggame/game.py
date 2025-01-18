import struct

import pygame
import platform, os
import json
from car import newCar, handleCarEvents, updateCar, pos, rpm, gear, speed, rotatedTexture, friction, redlining, \
    automatic
from math import pi
import json



pygame.mixer.pre_init()
pygame.mixer.init()
pygame.init()
if platform.system() == "Linux":
    screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
else:
    screen = pygame.display.set_mode((0,0))
clock = pygame.time.Clock()
window_size = pygame.display.get_window_size()
pygame.mouse.set_visible(False)
FPS = 60



gearSetting = False
highscores = []
def read_highscores():
    global highscores
    highscores.clear()

    if not os.path.exists("highscores/"):
        os.mkdir("highscores")
    #create new file if not already there
    if not os.path.exists("highscores/highscores.txt"):
        
        with open("highscores/highscores.txt", "w") as f:
            for i in range(10):
                f.write("x 999999999\n") #default line. Bad Time to allow for better scores

    with open("highscores/highscores.txt", "r") as f:
        arr = f.read().splitlines()
    for score in arr:
        highscores.append(score.split(" "))
read_highscores()

def write_highscores(highscores):
    with open("highscores/highscores.txt", "w") as f:
        for score in highscores:
            f.write(score[0] + " " +score[1] + "\n")



#HACKATHON CHALLENGE 1
#The watch of the timekeeper gets the time in miliseconds and shows it to the timekeeper as a string format 'MM:SS:MMM'.
#START HERE: Implement the logic to calculate minutes, seconds, and milliseconds.
def convert_Time(miliseconds):
    seconds = miliseconds//1000
    minutes = seconds//60
    seconds = seconds - minutes*60
    miliseconds = miliseconds %1000
    return f"{minutes:02}:{seconds:02}:{miliseconds:03}"


#the drawn game map
game_map = None
#the 2-bit collision map
collision_map = None

#zoom
zoom_game_map = 4

#contains all checkpoints of form [[x,y,width,height],...]
#size is radius of checkpoint  
map_checkpoints = []

#contains the surface of the checkpoint
surface_Checkpoint = None
surface_under_checkpoint = None

#index of the next checkpoint in the map_checkpoints 
next_checkpoint = 0

car = None
car_tex = None
#the ghost of the best player
use_ghost = False #HACKATHON CHALLENGE 3.2: Enable when you want to test your simulated car. Go to other 3.2 to find implementation position
ghost_car = None
ghost_tex = None



#action = pygame.event
ghost_movements = [] #contains this information: [(tick,[actions]),(tick,[actions])]
ghost_next_movement_index = 0 
#has the ghost rode its path?
ghost_finished = False

#contains all currently pressed buttons by the ghost
ghost_currently_pressed = None

#speedometer and other UI textures
speedometer_Background_Scaled = None
speedometer_Scale = 3 # 1/scale
speedometer_Needle_Scaled = None
rpmmeter_Background_Scaled = None
rpmmeter_Scale = 4 #1/scale
rpmmeter_Needle_Scaled = None

#HACKATHON CHALLENGE 3.1.1 - Write and save Temporal Car Aura
# The "temporal car aura" is a way to record your actions during a game run. 
# It captures the sequence of game events (e.g., key presses) along with the corresponding game ticks (timestamps).
# This data allows you to replay your past run as a "ghost car."

# You get the "temporal car aura" as a list of tuples in the form [(tick, [pygame.event])]
# so for example:
#[(1, event(type = keydown, key = w)), (3,event(type = keyup, key = w), ...)]
#
#look here to learn more about pygame events and how you get type and key: https://www.pygame.org/docs/ref/event.html
#Your task is to save this data to a file so it can be used later to recreate the ghost car's behavior. 
#Think about in which format you want to save the "aura" in a file
#Docstrings are also added for suggestions in collapsibles
def write_ghost_car(event_array_with_ticks):
    """
    Save the 'temporal car aura' to a file.
    
    Args:
        event_array_with_ticks (list): A list of tuples where each tuple contains:
            - tick (int): The timestamp of the event.
            - events (list): A list of pygame.event.Event objects for that tick.
            
    Suggestions:
        - Choose a file format that can store both the tick and the event data (e.g., JSON or pickle).
        - Ensure pygame events are serialized properly.
    """
    # file = open("events.txt", "w")
    # json.dump(event_array_with_ticks, file)
    # file.close()
    print("Writing ghost car")
    print(event_array_with_ticks)
    with open("ghost_car.json", "w") as file:
        for e in event_array_with_ticks:
            print(e)
            for element in e:
                    json.dump(element, file)
            file.write("\n")
        file.close()




#HACKATHON CHALLENGE 3.1.2 - Read Temporal Car Aura
# The saved "temporal car aura" file from 3.1 is now used to recreate the ghost car's data.
# read the "temporal car aura" from the file you saved it in in 3.1 and return it in the form [(tick, [pygame.event])]
# Ensure the events are properly deserialized into pygame.event.Event objects.
#Docstrings are also added for suggestions in collapsibles
def read_ghost_car():
    """
    Load the 'temporal car aura' from a file and return it.
    
    Returns:
        list: A list of tuples where each tuple contains:
            - tick (int): The timestamp of the event.
            - events (list): A list of pygame.event.Event objects for that tick.
            
    Suggestions:
        - Read the file in the same format you used for saving.
        - Handle errors like missing or corrupted files gracefully.
    """


    return



tick_count = 0

start_Position = (10000/zoom_game_map,10000/zoom_game_map)
car_position = start_Position[:] # copy start position into car position

timer = 0
game_round = 1 
#on a succesful run which name should be used to safe the highscore
entered_Name = ""
final_time = 0

#the gamestate the game starts in
init_Gamestate = None
gamestate = None
def game(screen, lastButtons):
    global gamestate, init_Gamestate, _speed, _rpm, _gear, game_map, car, car_tex, zoom_game_map, tick_count, event_array_with_ticks
    #music_fadeout()
    #region utility functions
    def start_Timer(set = 0):
        global timer
        timer = set
        return timer


    def render_Car(screen, car, car_texture):
        rotated_texture, target_rect = rotatedTexture(car, car_texture)
        #draw the car on the middle of the screen
        screen.blit(rotated_texture, (screen.get_width() / 2 - rotated_texture.get_width()/2,screen.get_height()/2 - rotated_texture.get_height()/2))
        return screen

    def render_ghost(screen,ghost,ghost_texture):
        global car, zoom_game_map, ghost_movements
        if len(ghost_movements) != 0:
            rotated_texture, target_rect = rotatedTexture(ghost, ghost_texture)
            #draw the ghost on the middle of the screen
            screen.blit(rotated_texture, (-(pos(car)[0]-pos(ghost)[0]) + screen.get_width()/2 - rotated_texture.get_width()/2, -(pos(car)[1]-pos(ghost)[1]) + screen.get_height()/2 - rotated_texture.get_height()/2))
        return screen

    def render_UI(screen,timer_Value,speed,rpm,gear):
        global game_round
    
        def draw_Roundscale(screen,background,needle,scale,shown_value,max_value,offset_bottom_right):
            global speedometer_Needle
            #draw the speedometer
            
            #load speedometer when not loaded
            background_pos_x = screen.get_width()-background.get_width()- offset_bottom_right[0]
            background_pos_y = screen.get_height()-background.get_height()- offset_bottom_right[1] 
            screen.blit(background, (background_pos_x, background_pos_y))

            #write value as number
            font_roundscales = pygame.font.SysFont("Comic",background.get_height()//8)
            screen = draw_Text(screen,font_roundscales,"white",str(shown_value),(background_pos_x + background.get_width() // 2 - font_roundscales.size(str(shown_value))[0] // 2, background_pos_y + background.get_height()*4/5 ))

            #rotate needle to speed. 130.645 represents zero, -130.645 max speed
            needle_rotated = pygame.transform.rotate(needle, 130.645-shown_value/max_value*261.29)
            target_rect = needle_rotated.get_rect(center = needle.get_rect(center = (background_pos_x + background.get_width()//2, background_pos_y + background.get_height()//2)).center)
            
            screen.blit(needle_rotated, target_rect)

            

            return screen, background

        #draw the timer
        font_Timer = pygame.font.SysFont("comic", screen.get_height()//10)
        screen = draw_Text(screen, font_Timer ,"white",convert_Time(timer_Value),(10,10))

        #draw the roundscales
        global speedometer_Background_Scaled, rpmmeter_Background_Scaled, speedometer_Scale, rpmmeter_Scale, speedometer_Needle_Scaled, speedometer_Needle_Scaled
        speedometer_offset = 10
        screen, speedometer = draw_Roundscale(screen, speedometer_Background_Scaled, speedometer_Needle_Scaled , speedometer_Scale, int(speed), 300, (speedometer_offset, speedometer_offset))
        screen, rpm_o_meter = draw_Roundscale(screen, rpmmeter_Background_Scaled,rpmmeter_Needle_Scaled , rpmmeter_Scale, int(rpm), 7500, (speedometer.get_width() + 10, 10)) #7500 is the max value on the rpm scale

        #draw the current gear
        font_Speedometer = pygame.font.SysFont("comic", screen.get_height()//40)
        screen = draw_Text(screen,font_Speedometer,"white",str(gear),(screen.get_width() - speedometer_offset - speedometer.get_width() - rpm_o_meter.get_width()//2 - font_Speedometer.size(str(gear))[0] // 2, screen.get_height() - speedometer_offset - rpm_o_meter.get_height()*11/32))

        #draw the round
        screen = draw_Text(screen,font_Timer,"yellow",str(game_round) + "/3",(screen.get_width()-font_Timer.size(str(game_round) + "/3")[0]-speedometer_offset, speedometer_offset))


        return screen
    
    
    def render_Map(screen, game_map, car_position):
        global map_checkpoints,next_checkpoint, surface_Checkpoint, zoom_game_map
        
        #draw the map. the coordinates are left shifted by 20000
        screen.blit(game_map,(-car_position[0] + screen.get_width()/2,-car_position[1] + screen.get_height()/2)) 
        
        #draw the checkpoint surface on the map position given in the file
        if len(map_checkpoints)-1 != next_checkpoint:
            game_map.blit(surface_Checkpoint,(map_checkpoints[next_checkpoint][0], map_checkpoints[next_checkpoint][1]))

        
        return screen
    
    #returns true if car is in checkpoint
    def check_Checkpoint(car_position, checkpoint):
        #first check if x is in bounds and then if y is in bounds
        return (checkpoint[0] <= car_position[0] <= checkpoint[0]+checkpoint[2]) and (checkpoint[1] <= car_position[1] <= checkpoint[1]+checkpoint[3])

    # Bonus Hackathon Challenge 2: Checkpoint Reminder
    # START HERE: Complete the function check_near_Checkpoint().
    # Then use 'Ctrl+f' to search for:checkpoint handling or Bonus Hackathon Challenge 2

    def check_near_Checkpoint():

        return

    #create a checkpoint and stores it in surface_checkpoint
    #also stores the picture under the current checkpoint in surface_under_checkpoint
    def create_Checkpoint(next_checkpoint):
        global surface_Checkpoint,surface_under_checkpoint,map_checkpoints, game_map

        checkpoint = map_checkpoints[next_checkpoint]
        #create a surface for the checkpoint
        surface_Checkpoint = pygame.Surface((checkpoint[2], checkpoint[3]))
        #set black as transparent so only the outline is shown
        surface_Checkpoint.set_colorkey("black")
        #draw the red outline on the surface
        pygame.draw.rect(surface_Checkpoint, "red", (0,0,checkpoint[2],checkpoint[3]), width=4)

        #remember the old surface under the checkpoint
        surface_under_checkpoint = pygame.Surface((checkpoint[2], checkpoint[3]))
        surface_under_checkpoint.blit(game_map,(0,0),(checkpoint[0],checkpoint[1],checkpoint[2],checkpoint[3]))

    # check the type of ground the car is on
    def check_Ground(car_position):
        global collision_map
        collision_color = collision_map.get_at((int(car_position[0]), int(car_position[1])))
        # table of different speed types
        if collision_color == pygame.Color("black"):
            return 1
        elif collision_color == pygame.Color(247, 247, 247):  # white:
            return 0.5
        elif collision_color == pygame.Color(128, 128, 128):  # grey:
            return 0.001
        return 0  # only reached if no valid color, thus never reached
    
    #simulate the ghost. in_start_phase is bool to specifiy if car is allowed to move. needed for revving phase
    def drive_Ghost(screen,in_start_phase):
        global ghost_car,ghost_tex, ghost_movements, tick_count, ghost_next_movement_index, use_ghost, ghost_currently_pressed, ghost_finished
        if use_ghost:
            current_tick_events = [] 
            # HACKATHON CHALLENGE 3.2
            # The crazy Doc wants you to implement a hologram. 
            # He already did part of the work and simulates the car using the "temporal aura" stored in `ghost_movements`.
            # However, the simulation requires translating the temporal aura (recorded events) into inputs the simulator understands.
            # Your tasks:
            # 1. Populate `current_tick_events`: Extract all events from `ghost_movements` that should occur at the current `tick_count`.
            #    - Each event in `ghost_movements` is stored as (tick, [pygame.event]).
            #    - Use the `tick_count` to determine which events should be active now.
            # 2. Update `ghost_currently_pressed`: This should mimic the structure of `pygame.key.get_pressed()`.
            #    - Create a list where each index represents a key and its value is `True` if the key is pressed in the current simulation.
            #    - Use the `ghost_movements` to determine which keys should be "pressed."
            #
            # Be careful:
            # - Handle cases where the simulation has not started yet (in_start_phase is True).
            # - Test your implementation by setting `use_ghost = True` at the other HACKATHON CHALLENGE 3.2.
            #   Docstrings are also added for suggestions in collapsibles
            # 
        # Step 1: Populate `current_tick_events` based on the current tick count
        # Start - while ghost_next_movement_index < len(ghost_movements):
            """
            Step 1: Populate `current_tick_events` based on the current tick count.

            `ghost_movements` is a list of tuples where each tuple contains:
            - `tick`: The game tick at which the event(s) occurred.
            - `events`: A list of pygame events (e.g., KEYDOWN, KEYUP).

            Your task:
                - Iterate through `ghost_movements` and extract events that match the current `tick_count`.
                - Add these events to `current_tick_events`.
                - Ensure you update `ghost_next_movement_index` as you process events to avoid rechecking already processed entries.

            Hints:
                - Use a `while` loop to iterate through `ghost_movements` starting at `ghost_next_movement_index`.
                - Stop processing when you encounter a tick greater than `tick_count`.
            """



            # Step 2: Update `ghost_currently_pressed` based on current events
            ghost_currently_pressed = [False] * 512  # Create a list for all possible keys 
            """
            Step 2: Update `ghost_currently_pressed` to reflect the state of keys based on the current events.

            `ghost_currently_pressed` should be a list that mimics the output of `pygame.key.get_pressed()`.
            - Each index in the list corresponds to a key, and its value is `True` if the key is pressed, or `False` if it is not.

            Your task:
                - Iterate through `current_tick_events` (populated in Step 1).
                - For each `KEYDOWN` event, set the corresponding index in `ghost_currently_pressed` to `True`.
                - For each `KEYUP` event, set the corresponding index in `ghost_currently_pressed` to `False`.

            Hints:
                - Use the `event.type` attribute to differentiate between `KEYDOWN` and `KEYUP` events.
                - Use `event.key` to get the key code, which corresponds to the index in `ghost_currently_pressed`.
            """

            #Crazy Docs mini simulated car
            signals_ghost = handleCarEvents(ghost_car,current_tick_events,ghost_currently_pressed)
            friction(ghost_car, check_Ground(pos(ghost_car)))
            updateCar(ghost_car, signals_ghost, FPS)
            screen = render_ghost(screen,ghost_car,ghost_tex)
        
        return screen

    #endregion

    #the handlers for the different stages of the game
    #region gamehandler

    #first called function. initializes the game
    def not_started(screen,pressed_keys):
        global game_map, collision_map, gamestate, map_checkpoints, next_checkpoint ,car_position, start_Position, car, car_tex,game_round,gearSetting
        global zoom_game_map
        #reset variables
        next_checkpoint = 0
        game_round = 1




        car = newCar()
        automatic(car,gearSetting)


        #the initial car variables
        car["posmul"] = 50.0/zoom_game_map
        car["angle"] = pi/2
        car_position = start_Position[:]
        pos(car, car_position) # set the car position

        #create ghost car
        global ghost_movements, ghost_car,ghost_tex, ghost_finished, ghost_next_movement_index, ghost_currently_pressed
        ghost_car = dict(newCar())
        ghost_car["posmul"] = 50.0/zoom_game_map
        ghost_car["angle"] = pi/2
        pos(ghost_car, start_Position[:]) # set the car position
        ghost_finished = False
        ghost_next_movement_index = 0
        #set all pressed buttons to zero
        ghost_currently_pressed = [False for x in pygame.key.get_pressed()][:]
        

        #load map
        game_map = pygame.image.load("maps/map1/map.png").convert()
        game_map = pygame.transform.scale(game_map, (game_map.get_width()/zoom_game_map, game_map.get_height()/zoom_game_map)).convert()
        collision_map = pygame.image.load("maps/map1/map_collision_2bit.png")
        collision_map = pygame.transform.scale(collision_map, (collision_map.get_width()/zoom_game_map, collision_map.get_height()/zoom_game_map))
        #load car
        car_tex = pygame.image.load("pics/car.png")
        car_tex = pygame.transform.scale(car_tex, (120/zoom_game_map,60/zoom_game_map))
        car_tex = car_tex.convert_alpha(car_tex)
        #load ghost tex
        ghost_tex = pygame.image.load("pics/ghost.png")
        ghost_tex = pygame.transform.scale(ghost_tex, (120/zoom_game_map,60/zoom_game_map))
        #make slightly transparent
        ghost_tex = ghost_tex.convert_alpha(ghost_tex)
        ghost_tex.set_alpha(128)

        #load speedometer texture
        global speedometer_Background_Scaled, speedometer_Needle, speedometer_Scale

        backgroundImage = pygame.image.load("pics/speedometer.png")
        #scale speedometer to desired size
        speedometer_Background_Scaled = pygame.transform.scale(backgroundImage, (backgroundImage.get_width() //speedometer_Scale, backgroundImage.get_height() //speedometer_Scale) )
        speedometer_Background_Scaled = speedometer_Background_Scaled.convert_alpha()
        #load rpm-meter
        global rpmmeter_Background_Scaled, rpmmeter_Scale

        rpmBackgroundImage = pygame.image.load("pics/rpmmeter.png")
        rpmmeter_Background_Scaled = pygame.transform.scale(rpmBackgroundImage, (rpmBackgroundImage.get_width() //rpmmeter_Scale, rpmBackgroundImage.get_height() //rpmmeter_Scale) )
        rpmmeter_Background_Scaled = rpmmeter_Background_Scaled.convert_alpha()
        #load needle for roundscales
        global speedometer_Needle_Scaled, rpmmeter_Needle_Scaled
        
        needle = pygame.image.load("pics/speedneedle.png")
        speedometer_Needle_Scaled = pygame.transform.scale(needle,  (needle.get_width() //speedometer_Scale, needle.get_height() //speedometer_Scale))     
        speedometer_Needle_Scaled = speedometer_Needle_Scaled.convert_alpha()
        rpmmeter_Needle_Scaled = pygame.transform.scale(needle,  (needle.get_width() //rpmmeter_Scale, needle.get_height() //rpmmeter_Scale))     
        speedometer_Needle_Scaled = speedometer_Needle_Scaled.convert_alpha()

        #load in the checkpoints
        map_checkpoints.clear() #clear old checkpoints from previous runs
        with open("maps/map1/checkpoints.txt","r") as f:
            lines = f.read().splitlines() 
        for line in lines:
            map_checkpoints.append([int(value)/zoom_game_map for value in line.split(" ")]) #split at space for coordinates and space

        #create the first checkpoint surface
        create_Checkpoint(0)

        #load the ghost movements of the best player
        ghost_movements = read_ghost_car()
        

        gamestate = input_expected #switch to expect input
        return screen

    #waits for the Player to press spacebar
    def input_expected(screen,pressed_keys):
        global car_position, gamestate, car,car_tex, event_array_with_ticks, tick_count
        car_position = pos(car)
        screen = render_Map(screen, game_map, car_position)
        screen = render_Car(screen,car,car_tex)
        screen = render_UI(screen, 0, round(speed(car)*3.6), int(rpm(car)), gear(car)) #gets 0 instead of the timer because the timer is not supposed to progress while waiting

        #draw the input required text on screen
        font = pygame.font.SysFont("Comic", screen.get_width()//7, bold=True, italic=True)
        screen = draw_Text(screen, font,"yellow","Press space to start!",(screen.get_width()/2-font.size("Press space to start!")[0]/2, screen.get_height()/2 - font.size("Press space to start!")[1] / 2))
        
       

        if pressed_keys[pygame.K_SPACE]:
            start_Timer()
            gamestate = start_timer
            play_speedchime.last_tick = tick_count = 0
            event_array_with_ticks = []
        
        
        return screen

    # the initial 3 sec timer
    def start_timer(screen,pressed_keys):
        global car_position, gamestate, car, car_tex
        car_position = pos(car)
        screen = render_Map(screen, game_map, car_position)
        screen = render_Car(screen, car, car_tex)
        screen = render_UI(screen, 0, round(speed(car)*3.6), int(rpm(car)), gear(car)) #gets 0 instead of the timer because the timer is not supposed to progress while waiting
        font = pygame.font.SysFont("Comic", screen.get_width()//7, bold=True, italic=True)

        #catch s and disallow it 
        if pressed_keys[pygame.K_s] or automatic(car) and pressed_keys[pygame.K_w]:
            array = [isPressed for isPressed in pressed_keys]
            array[pygame.K_s] = False
            if automatic(car): array[pygame.K_w] = False
            pressed_keys = array

        #allow car to increase rpm in timer here
        #lastbuttons is not global to disallow shifting
        signals = handleCarEvents(car, lastButtons, pressed_keys)
        friction(car, check_Ground(car_position))
        car = updateCar(car, signals, FPS)
        
        screen = drive_Ghost(screen,True)
        #countdown
        timer_value = 3-int(timer)//1000
        if timer_value <= 0:
            gamestate = show_go
        else:
            timer_value = str(timer_value)
            screen = draw_Text(screen, font,"yellow",timer_value,(screen.get_width()/2-font.size(timer_value)[0]/2, screen.get_height()/2 - font.size(timer_value)[1] / 2))
        return screen

    #shows the the go symbol
    def show_go(screen, pressed_keys):
        global gamestate, lastButtons, car, car_tex
        screen = render_Map(screen, game_map, pos(car))
        screen = render_Car(screen, car , car_tex)
        screen = render_UI(screen, 0, round(speed(car)*3.6), int(rpm(car)), gear(car)) #gets 0 instead of the timer because the timer is not supposed to progress while waiting

        timer_value = 3-int(timer)//1000

        if timer_value < 0:
            start_Timer()
            gamestate = game_running
            return screen

        font = pygame.font.SysFont("Comic", screen.get_width()//7, bold=True, italic=True)
        screen = draw_Text(screen, font,"yellow","GO!!!",(screen.get_width()/2-font.size("GO!!!")[0]/2, screen.get_height()/2 - font.size("GO!!!")[1] / 2))


        #allow car to drive on go 
        signals = handleCarEvents(car, lastButtons, pressed_keys)
        friction(car, check_Ground(pos(car)))
        car = updateCar(car, signals, FPS)

        screen = drive_Ghost(screen,False)
        return screen

    #the car is driving
    def game_running(screen, pressed_keys):
        global car_position,map_checkpoints, next_checkpoint, gamestate, surface_under_checkpoint, game_round, car, car_tex, lastButtons, final_time
        car_position = pos(car)
        screen = render_Map(screen, game_map, car_position)
        #render ghost car
        screen = drive_Ghost(screen,False)
        screen = render_UI(screen, int(timer), round(speed(car)*3.6), int(rpm(car)), gear(car))

    # Bonus Hackathon Challenge 1:
    # Implement a feature to display a warning message whenever the car is reversing.
    #
    # Scenario:
    # - When the player presses the reverse key (`S`), a warning message should appear on the screen.
    # - The warning message should disappear as soon as the reverse key is released.
    #
    # Tasks:
    # 1. Detect when the reverse key (`S`) is pressed using `pressed_keys`.
    # 2. Create a warning message (e.g., "Warning: You are moving in reverse direction!") and render it on the screen.
    #
    # Provided Hints:
    # - Use the `pressed_keys` parameter to check the state of the `S` key (`pygame.K_s`).
    # - Use Pygame's `pygame.font.Font` or `pygame.font.SysFont` to render text dynamically.
    # - The message should only appear while the reverse key is actively pressed.
    
    # Bonus Hackathon Challenge 1: Reverse Warning
    # Your task starts here!
    #Start using this - if pressed_keys[pygame.K_s]:



        #update the car and play sounds
        signals = handleCarEvents(car, lastButtons, pressed_keys)
        friction(car, check_Ground(car_position))
        oldGear = gear(car)
        car = updateCar(car, signals, FPS)
        screen = render_Car(screen, car, car_tex)

        if redlining(car) and gear(car) not in ("6", "N", "R"):
            play_speedchime()
        if oldGear < gear(car):
            play_upshift()
        elif oldGear > gear(car):
            play_downshift()
        

        #check if collision with something
        if check_Ground(pos(car)) == 0.001:
            gamestate = game_over


        # Bonus Hackathon Challenge 2: Checkpoint Reminder
        # Observe checkpoint handling and continue working here.

        #checkpoint handling
        if check_Checkpoint(car_position,map_checkpoints[next_checkpoint]):
            #overdraw the old checkpoint
            game_map.blit(surface_under_checkpoint,(map_checkpoints[next_checkpoint][0], map_checkpoints[next_checkpoint][1]))
            
            next_checkpoint += 1
            #if last checkpoint
            if len(map_checkpoints) == next_checkpoint:
                if game_round >= 3:
                    gamestate = game_finished
                    final_time = int(timer)
                else:
                    game_round += 1
                next_checkpoint = 0
                
            #create new checkpoint surface for drawing
            create_Checkpoint(next_checkpoint)

        return screen

    #when you crashed and did not complete the track
    def game_over(screen,pressed_keys):
        global current_scene, gamestate
        #write game over
        font_Big = pygame.font.SysFont("Comic", screen.get_width()//7, bold=True)
        text_Size_Big = font_Big.size("GAME OVER")
        screen = draw_Text(screen, font_Big,"yellow","GAME OVER",(screen.get_width()/2 - text_Size_Big[0]/2, screen.get_height()/2 - text_Size_Big[1] / 2))
        #writes return to main menu
        font_Small = pygame.font.SysFont("Comic", screen.get_width()//12, bold=True)
        text_Size_Small = font_Small.size("press space to try again")
        screen = draw_Text(screen, font_Small,"yellow","press space to try again",(screen.get_width()/2 - text_Size_Small[0]/2, screen.get_height()/2 - text_Size_Small[1] / 2 + text_Size_Big[1] + 10))
        
        if pressed_keys[pygame.K_SPACE]:
            gamestate = not_started
        write_ghost_car(event_array_with_ticks)

        return screen

    #when you completed the track
    def game_finished(screen,pressed_keys):
        global entered_Name, lastButtons, highscores, current_scene, gamestate, ghost_movements
        #write Game finished
        font = pygame.font.SysFont("Comic", screen.get_width()//7, bold=True)
        text_Size_Big = font.size("GAME FINISHED")
        screen = draw_Text(screen, font,"yellow","GAME FINISHED",(screen.get_width()/2-text_Size_Big[0]/2, screen.get_height()/2 - text_Size_Big[1] / 2))
        #write the time
        font = pygame.font.SysFont("Comic", screen.get_width()//12, bold=True)
        text = "Your time is: {time}".format(time = convert_Time(final_time))  
        text_Size_Time = font.size(text)
        screen = draw_Text(screen, font,"yellow",text,(screen.get_width()/2-text_Size_Time[0]/2, screen.get_height()/2 - text_Size_Time[1] / 2 + text_Size_Big[1] + 10))
        #write name input prompt
        text = "Please enter your name: {name}".format(name=entered_Name)  
        text_Size_Prompt = font.size(text)
        screen = draw_Text(screen, font,"yellow",text,(screen.get_width()/2-text_Size_Prompt[0]/2, screen.get_height()/2 - text_Size_Prompt[1] / 2 + text_Size_Big[1] + text_Size_Time[1] + 10))
       
        #listen for text inputs
        for pressedButton in lastButtons:
            if pressedButton.type == pygame.KEYDOWN:
                if pressedButton.key == pygame.K_BACKSPACE:
                    #delete last character
                    entered_Name = entered_Name[:-1] 
                elif pressedButton.key == pygame.K_RETURN:
                    #save highscore if under top ten
                    for i in range(len(highscores)):
                        
                        if int(highscores[0][1]) > final_time:
                            write_ghost_car(event_array_with_ticks)
                        if int(highscores[i][1]) > final_time:
                            place = i
                            highscores = highscores[:place] + ["x"] +  highscores[place:-1] #leave last user out and put in placeholder for current user
                            highscores[place] = [entered_Name, str(final_time)]
                            write_highscores(highscores)
                            
                            #go to highscores if you have a highscore
                            current_scene = highscore
                            play_music_in_loop()
                            read_highscores()
                            gamestate = not_started
                            return screen
                    ghost_movements = read_ghost_car()
                    current_scene = main_menu
                    play_music_in_loop()
                    gamestate = not_started
                    return screen
                elif pressedButton.key == pygame.K_HOME or pressedButton.key == pygame.K_TAB:
                    print("Debug ghost created")
                    write_ghost_car(event_array_with_ticks)
                elif pressedButton.key != pygame.K_SPACE:
                    entered_Name += pressedButton.unicode
        
        #write the written name

        
        return screen

    #endregion

    #initialize the gamestate possibilities. Only called the first time
    if init_Gamestate == None:
        #different game stages
        #gamestates = [not_started, input_expected,start_timer,show_go,game_running,game_over,game_finished]
        gamestate = not_started
        init_Gamestate = not_started 

    #get the pressed keys for further handling. lastbuttons not ideal because it contains 
    #all events which would need to be filtered
    pressed_keys = pygame.key.get_pressed()
    screen = gamestate(screen, pressed_keys)
    
    return screen


    
    


def leave(screen, lastButton):
    write_ghost_car(event_array_with_ticks)
    exit()

pygame.font.init()
font_header = pygame.font.Font("font/FFFFORWA.TTF", window_size[1]//6) 
font_selectable = pygame.font.Font("font/FFFFORWA.TTF", window_size[1]//20)
font_scores = pygame.font.Font("font/FFFFORWA.TTF", window_size[1]//30)

#draws a text on the screen
def draw_Text(screen,font,color,text,position):
    img = font.render(text, False, color)
    screen.blit(img,position)
    return screen


#region music and sounds
pygame.mixer.set_num_channels(3)
music_channel = pygame.mixer.Channel(0)
sound1_channel = pygame.mixer.Channel(1)
sound2_channel = pygame.mixer.Channel(2)

music_volume_100 = 100 #no floats, if used divide by 100
sound_volume_100 = 100 #no floats, if used divide by 100
general_volume = 3 # not an option for user, make everything more quiet

music_channel.set_volume(music_volume_100 / 100 / general_volume)
sound1_channel.set_volume(sound_volume_100 / 100 / general_volume)
sound2_channel.set_volume(sound_volume_100 / 100 / general_volume)

sound_select = pygame.mixer.Sound("sounds/menu_select.mp3")
sound_chime = pygame.mixer.Sound("sounds/speedchime.mp3")
sound_upshift = pygame.mixer.Sound("sounds/upshift.mp3")
sound_downshift = pygame.mixer.Sound("sounds/downshift.mp3")
music_gasgasgas = pygame.mixer.Sound("sounds/gasgasgas.mp3")

def play_selection():
    global sound1_channel
    sound1_channel.play(sound_select)

def play_speedchime():
    global sound1_channel, sound_chime, tick_count, FPS

    if play_speedchime.last_tick + FPS * 1.1 <= tick_count:
        sound1_channel.play(sound_chime)
        play_speedchime.last_tick = tick_count

def play_upshift():
    global sound2_channel
    sound2_channel.play(sound_upshift)

def play_downshift():
    global sound2_channel
    sound2_channel.play(sound_downshift)

def play_music_in_loop():
    global music_channel
    music_channel.play(music_gasgasgas, -1)
play_music_in_loop()

def music_fadeout():
    global music_channel
    music_channel.fadeout(8000)#1 sec fadeout
#endregion

#HACKATHON CHALLENGE 2
#Implement another option to change from manual to automatic and display the text in the options' menu. 
#To implement the automatic car itself go to car.py and ctrl+f HACKATHON CHALLENGE 2
#START HERE: Add 'Automatic Mode' to the options menu
#HINT: Use the gearSetting variable to toggle manual/automatic. Use the car property "automatic" to prepare for the real implementation
option_selected = 0
option_choosable = ["Music volume up", "Music volume down", "Sound volume up", "Sound volume down","Automatic Mode","exit"]
def options(screen, lastButton):
    global option_selected, option_choosable, music_volume_100, sound_volume_100, current_scene, selected, general_volume, gearSetting
    draw_Text(screen, font_header,"white" ,"Options", (50,window_size[1]/12))

    for i in lastButton:
        if i.type == pygame.KEYDOWN:
            if i.key in (pygame.K_w, pygame.K_UP): #choose option further up
                option_selected -= 1
                play_selection()
            elif i.key in (pygame.K_s, pygame.K_DOWN): #option option further down
                option_selected += 1
                play_selection()
            elif i.key == pygame.K_RETURN: #on option pressed
                if option_selected == 0:
                    if music_volume_100 <= 90:
                        music_volume_100 += 10
                elif option_selected == 1:
                    if music_volume_100 >= 10:
                        music_volume_100 -= 10
                elif option_selected == 2:
                    if sound_volume_100 <= 90:
                        sound_volume_100 += 10
                elif option_selected == 3:
                    if sound_volume_100 >= 10:
                        sound_volume_100 -= 10
                elif option_selected == 4:
                    gearSetting = not gearSetting
                elif option_selected == 5:
                    option_selected = 0
                    current_scene = main_menu
                    selected = 0
                play_selection()

    music_channel.set_volume(music_volume_100 / 100 / general_volume)
    sound1_channel.set_volume(sound_volume_100 / 100 / general_volume)
    sound2_channel.set_volume(sound_volume_100 / 100 / general_volume)

    option_selected %= len(option_choosable) #make options flip around when going down so first option is selected

    for i in range(len(option_choosable)): #draw all options on the screen
        if i == option_selected:
            font_selectable.set_underline(True)
        if option_choosable[i] != "exit":
            draw_Text(screen, font_selectable, "white", option_choosable[i], (50,window_size[1]/5*2 + window_size[1]/10*i) )
        else:
            draw_Text(screen, font_selectable,"white", "exit", (window_size[0]-50-font_selectable.size("exit")[0],window_size[1]-50-font_selectable.size("exit")[1]))

        font_selectable.set_underline(False)
    gearStr="Off"
    if gearSetting :
        gearStr="On"
    else: gearStr="Off"

    draw_Text(screen, font_selectable, "white", str(music_volume_100) + "%", (window_size[0] - font_selectable.size(str(music_volume_100) + "%")[0] - 50,window_size[1]/5*2))
    draw_Text(screen, font_selectable, "white", str(sound_volume_100) + "%", (window_size[0] - font_selectable.size(str(sound_volume_100) + "%")[0] - 50,window_size[1]/5*2 +  + window_size[1]/10*2))
    draw_Text(screen, font_selectable,"white",gearStr,(window_size[0] - font_selectable.size(str(sound_volume_100) + "%")[0] - 50,window_size[1]/5*2 +  + window_size[1]/10*4))


    return screen


def highscore(screen, lastButton):
    global highscores, font_header, font_scores, font_selectable, current_scene, selected
    draw_Text(screen, font_header,"white", "Highscores", (50,window_size[1]/12) )
    for i in range(len(highscores)):
        draw_Text(screen,font_scores,"white", str(i+1) + ". : " + highscores[i][0], (50,window_size[1]*9/24 + window_size[1]/20*i*1.2))
        draw_Text(screen, font_scores,"white", convert_Time(int(highscores[i][1])), (window_size[0]-100-font_selectable.size("exit")[0]-font_scores.size(convert_Time(int(highscores[i][1])))[0],window_size[1]*9/24 + window_size[1]/20*i*1.2))
        
    font_selectable.set_underline(True)
    draw_Text(screen, font_selectable,"white", "exit", (window_size[0]-50-font_selectable.size("exit")[0],window_size[1]-50-font_selectable.size("exit")[1]))
    for i in lastButton:
        if i.type == pygame.KEYDOWN:
            if i.key == pygame.K_RETURN:
                current_scene = main_menu
                play_selection()
                selected = 0
    font_selectable.set_underline(False)

    return screen



selected = 0
choosable = [("play", game), ("options", options), ("highscores", highscore), ("exit", leave)]
def main_menu(screen, lastButton):
    global font_header, font_selectable, selected, current_scene
    for i in lastButton:
        if i.type == pygame.KEYDOWN:
            if i.key in (pygame.K_w, pygame.K_UP):
                selected -= 1
                play_selection()
            elif i.key in (pygame.K_s, pygame.K_DOWN):
                selected += 1
                play_selection()
            elif i.key == pygame.K_RETURN:
                current_scene = choosable[selected][1]
                play_selection()
    selected %= len(choosable)

    #überschrift
    draw_Text(screen, font_header, "white", "Mumble Club", (50,window_size[1]/6) )

    #auswählbares
    for i in range(len(choosable)):
        if i == selected:
            font_selectable.set_underline(True)
        draw_Text(screen, font_selectable,"white", choosable[i][0], (50,window_size[1]/2 + window_size[1]/10*i) )
        font_selectable.set_underline(False)
    return screen

current_scene = main_menu
#scenes = [game, options, highscore, exit, main_menu]
event_array_with_ticks = []

while True:
    lastButtons = []
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                    
            lastButtons.append(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if current_scene != main_menu:
                        current_scene = main_menu
                        play_music_in_loop()
                        gamestate = init_Gamestate #resets game to start
                    else:
                        pygame.quit()
                        exit()
                
        
    # event_array_with_ticks.append((tick_count, lastButtons[:]))
    event_array_with_ticks.append((tick_count, ()))

    screen.fill("black")
    screen = current_scene(screen, lastButtons)
    lastButtons.clear()

    pygame.display.flip()

    clock.tick(FPS)
    tick_count += 1
    timer += 1000/FPS

