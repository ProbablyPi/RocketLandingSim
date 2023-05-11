import pythonGraph, random
import rocket_ai as rocket_ai
import rocket_ga

# CONSTANTS
WINDOW_WIDTH  = 1800
WINDOW_HEIGHT = 800
BOAT_WIDTH = 120
BOAT_HEIGHT = 30
ROCKET_WIDTH = 50
ROCKET_HEIGHT = ROCKET_WIDTH
GRAVITY = 0.08

# Performance Variables
time_elapsed = 0
fuel_consumed = 0
num_crashes = 0
num_landings = 0
max_score = 0

# Simulation Variables
NUM_RUNS_PER_SCENARIO = 10
num_runs = 0

# Terrain
terrain_list = []
GROUND_HEIGHT = 0
WATER_HEIGHT  = 0
GROUND_LENGTH = 0

# Rocket
rocket_x = 0
rocket_y = 0
rocket_vx = 0
rocket_vy = 0
rocket_boosting = True
rocket_thrust_up = 0
rocket_thrust_right = 0
rocket_thrust_left = 0

# Boat (i.e., Landing Pad)
boat_start_x = 0
boat_start_y = 0
boat_start_vx = 0
boat_x = 0
boat_y = 0
boat_vx = 0

# Initializes the Simulation
def initialize_simulation(generate_new_scenario):
    global time_elapsed, fuel_consumed
    initialize_terrain(generate_new_scenario)
    initialize_boat(generate_new_scenario)
    initialize_rocket(generate_new_scenario)
    time_elapsed = 0
    fuel_consumed = 0
     


# Initializes the Terrain

def initialize_terrain(generate_new_scenario):
    global terrain_list, GROUND_LENGTH, GROUND_HEIGHT, WATER_HEIGHT
    
    if generate_new_scenario == True:
        terrain_list = []
        
        GROUND_LENGTH = random.randint(0.1 * WINDOW_WIDTH, 0.2 * WINDOW_WIDTH)
        GROUND_HEIGHT = random.randint(100, int(0.4 * WINDOW_HEIGHT))
        WATER_HEIGHT  = random.randint(50, GROUND_HEIGHT)
        
        for x in range(0, WINDOW_WIDTH):
            if x > GROUND_LENGTH:
                terrain_list.append(WATER_HEIGHT)
            else:
                terrain_list.append(GROUND_HEIGHT)


# Initializes the Boat
def initialize_boat(generate_new_scenario):
    global boat_start_x, boat_start_y, boat_start_vx, boat_x, boat_y, boat_vx
    
    if generate_new_scenario == True:
        boat_start_x = random.randint(WINDOW_WIDTH * 0.5, WINDOW_WIDTH - BOAT_WIDTH)
        boat_start_y = WINDOW_HEIGHT - WATER_HEIGHT
        boat_start_vx = random.random() * 2.0 - 1.0
    
    boat_x = boat_start_x
    boat_y = boat_start_y
    boat_vx = boat_start_vx


# Initializes the Rocket

def initialize_rocket(generate_new_scenario):
    global rocket_x, rocket_y, rocket_vx, rocket_vy, rocket_boosting
    rocket_x = GROUND_LENGTH * 0.5
    rocket_y = WINDOW_HEIGHT - GROUND_HEIGHT
    rocket_vx = 0
    rocket_vy = 0
    rocket_boosting = True


# Draws all of the in game objects

def erase_objects():
    pythonGraph.clear_window(pythonGraph.colors.BLACK)


# Draws all of the in game objects
def draw_objects():
    draw_terrain()
    draw_boat()
    draw_rocket()
    draw_hud()
  

# Draws the Terrain
def draw_terrain():
    for x in range(0, WINDOW_WIDTH):
        if x > GROUND_LENGTH:
            pythonGraph.draw_line(x, WINDOW_HEIGHT, x, WINDOW_HEIGHT - terrain_list[x], "light_blue")
        else:
            pythonGraph.draw_line(x, WINDOW_HEIGHT, x, WINDOW_HEIGHT - terrain_list[x], "green")


# Draws the Boat
def draw_boat():
    pythonGraph.draw_image("boat.png", boat_x, boat_y - 25, BOAT_WIDTH, BOAT_HEIGHT)


# Draws the Rocket (and Thrusters)
def draw_rocket():
    pythonGraph.draw_image("rocket.png", rocket_x-ROCKET_WIDTH/2, rocket_y-ROCKET_HEIGHT, ROCKET_WIDTH, ROCKET_HEIGHT)
    if rocket_thrust_up > 0:
        pythonGraph.draw_circle(rocket_x, rocket_y, 4, "YELLOW", True)
    if rocket_thrust_right > 0:
        pythonGraph.draw_circle(rocket_x-ROCKET_WIDTH/3, rocket_y-ROCKET_HEIGHT/5, 4, "YELLOW", True)
    if rocket_thrust_left > 0:
        pythonGraph.draw_circle(rocket_x+ROCKET_WIDTH/3, rocket_y-ROCKET_HEIGHT/5, 4, "YELLOW", True)
    if rocket_y < 0:
        pythonGraph.draw_line(rocket_x, 5, rocket_x + ROCKET_WIDTH, 5, "YELLOW", 5)

# Draws the On Screen Text
def draw_hud():
    pythonGraph.draw_text("Max Score: " + str(round(max_score, 1)), 0, 0, "WHITE")
    pythonGraph.draw_text("Time Elapsed: " + str(time_elapsed), 0, 25, "WHITE")
    pythonGraph.draw_text("Fuel Consumed: " + str(round(fuel_consumed, 2)), 0, 50, "WHITE")
    pythonGraph.draw_text("X Velocity: " + str(round(rocket_vx, 2)), 0, 75, "WHITE")
    pythonGraph.draw_text("Y Velocity: " + str(round(rocket_vy, 2)), 0, 100, "WHITE")
    pythonGraph.draw_text("Crashes: " + str(num_crashes) + "  Landings: " + str(num_landings), 0, 125, "WHITE")

# Updates all animated objects
def update_objects():
    update_boat()
    update_rocket()


# Initializes the Terrain
def update_rocket():
    global rocket_x, rocket_y, rocket_vy, rocket_vx, rocket_boosting, rocket_thrust_up, rocket_thrust_right, rocket_thrust_left, fuel_consumed
            
    # Launch 
    if rocket_boosting == True:
        # Initializes Thrusters
        rocket_thrust_up = 0
        rocket_thrust_right = 0
        rocket_thrust_left = 0
        
        if rocket_y < WINDOW_HEIGHT / 2:
            rocket_thrust_right = 0.25
        else:
            rocket_thrust_up = 0.35
            
        if rocket_x > GROUND_LENGTH:
            rocket_boosting = False

    # Updating Velocity
    rocket_vy -= rocket_thrust_up
    rocket_vx -= abs(rocket_thrust_left)
    rocket_vx += abs(rocket_thrust_right)
    
    # Updating Fuel Consumed
    fuel_consumed = fuel_consumed + abs(rocket_thrust_up) + abs(rocket_thrust_right) + abs(rocket_thrust_left)
    
    # Updating Position
    rocket_x += rocket_vx
    rocket_y += rocket_vy
    rocket_vy += GRAVITY


# Updates the Landing Pad / Boat
def update_boat():
    global boat_x, boat_vx
    boat_x += boat_vx
    
    if boat_x < WINDOW_WIDTH/2 or boat_x + BOAT_WIDTH > WINDOW_WIDTH:
        boat_vx *= -1


# Checks for Manual (or eventually) AI Input
def get_input():
    global rocket_thrust_up, rocket_thrust_right, rocket_thrust_left
    
    rocket_thrust_up = 0
    rocket_thrust_right = 0
    rocket_thrust_left = 0
             
    if rocket_boosting == False:
        ai_decision = rocket_ai.run_autopilot(num_runs, rocket_x - ROCKET_WIDTH/2, rocket_y, rocket_vx, rocket_vy, ROCKET_WIDTH, boat_x, boat_y, BOAT_WIDTH)
        rocket_thrust_left = ai_decision[0]
        rocket_thrust_right = ai_decision[1]
        rocket_thrust_up = ai_decision[2]
        
        if pythonGraph.key_down("left"):
            rocket_thrust_left = 0.1
            
        if pythonGraph.key_down("right"):
            rocket_thrust_right = 0.1
                
        if pythonGraph.key_down("up"):
            rocket_thrust_up = 0.5


# Detects if the Rocket has hit the ground or a boundary
def is_simulation_over():
    if rocket_boosting == False:
        rocket_left = int(rocket_x - ROCKET_WIDTH/2)
        rocket_right = int(rocket_x + ROCKET_WIDTH/2)
        
        # Checks for Collisions with the Sides
        if rocket_left < 0 or rocket_right >= WINDOW_WIDTH:
            return True
        
        # Checks for Collisions with the Ground
        for x in range(rocket_left, rocket_right):
            if (rocket_y >= WINDOW_HEIGHT - terrain_list[x]):
                return True


    return False


# Analyzes the Results of the Simulation
def analyze_results():
    global max_score, num_landings, num_crashes
    
    rocket_left = int(rocket_x - ROCKET_WIDTH/2)
    rocket_right = int(rocket_x + ROCKET_WIDTH/2)
        
    w1 = 0.4
    w2 = 0.4
    w3 = 0.1
    w4 = 0.1
        
    if rocket_left >= boat_x and rocket_right <= boat_x + BOAT_WIDTH:
        score = w1 * (100 / rocket_vy) + w2 * (abs(100 / rocket_vx)) + (-w3 * fuel_consumed) + (-w4 * time_elapsed)
        num_landings += 1
    else:
        score = -2000
        num_crashes += 1

    rocket_ga.score_ai(num_runs, score)
    
    max_score = max(score, max_score)
        
# "Main Program"
pythonGraph.open_window(WINDOW_WIDTH, WINDOW_HEIGHT)
pythonGraph.set_window_title("Rocket Landing Simulator")  

# Initializes the Simulation At Least Once
initialize_simulation(True)
    
# Main "Game Loop"
while pythonGraph.window_not_closed():
    if is_simulation_over() == False:
        erase_objects()
        draw_objects()
        get_input()
        update_objects()
        time_elapsed = time_elapsed + 1
    else:
        analyze_results()
        num_runs = num_runs + 1
        if num_runs == NUM_RUNS_PER_SCENARIO:
            num_runs = 0
            initialize_simulation(True)
        else:
            initialize_simulation(False)
        
    pythonGraph.update_window()




