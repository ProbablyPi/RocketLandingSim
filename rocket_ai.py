import rocket_ga

# Initializes the AI Population
rocket_ga.initialize_genetic_algorithm(4, 2, 10.0, 15.0)

#rocket_ga.use_ai_configuration(0.3, 0.3, 2.5, 100)


# Runs the AI
def get_student_name():
    return "Ayush Agarwal"


# Runs the AI
def run_autopilot(run_number, rocket_x, rocket_y, rocket_vx, rocket_vy, ROCKET_WIDTH, landing_pad_x, landing_pad_y, LANDING_PAD_WIDTH):
    ai = rocket_ga.get_ai(run_number)
    THRUST_AMOUNT_X = ai[0]
    THRUST_AMOUNT_Y = ai[1]
    MAX_X_THRUST = ai[2]
    MAX_Y_THRUST = ai[3]
    
    THRUST_UP = 0
    THRUST_RIGHT = 0
    THRUST_LEFT = 0
    
    rocket_left = rocket_x
    rocket_right = rocket_x + ROCKET_WIDTH
    landing_pad_center = (landing_pad_x + landing_pad_x + LANDING_PAD_WIDTH) / 2
    
    above_pad = (rocket_left >= (landing_pad_x + 0.25 * LANDING_PAD_WIDTH)  and rocket_right <= (landing_pad_x + 0.75 * LANDING_PAD_WIDTH))
    
    if rocket_x < landing_pad_center:
         if rocket_vx + THRUST_AMOUNT_X < MAX_X_THRUST:
             THRUST_RIGHT = THRUST_AMOUNT_X
         elif rocket_vx - THRUST_AMOUNT_X > MAX_X_THRUST:
             THRUST_LEFT = THRUST_AMOUNT_X
    
    if rocket_x > landing_pad_center:
        if rocket_vx - THRUST_AMOUNT_X > -MAX_X_THRUST:
            THRUST_LEFT = THRUST_AMOUNT_X
        elif rocket_vx + THRUST_AMOUNT_X < -MAX_X_THRUST:
            THRUST_RIGHT = THRUST_AMOUNT_X
    
    if rocket_vy > MAX_Y_THRUST:
        if rocket_vy > MAX_Y_THRUST:
            THRUST_UP = THRUST_AMOUNT_Y
    
    return (THRUST_LEFT, THRUST_RIGHT, THRUST_UP)