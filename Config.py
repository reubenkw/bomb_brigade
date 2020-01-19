class Cfg:
    # Display Settings
    fps = 10
    map_x_tiles = 64
    map_y_tiles = 64
    map_display_scale = 10
    display_x = map_x_tiles * map_display_scale
    display_y = map_y_tiles * map_display_scale

    bomb_delay = 20

    # Resources
    # Deposit size should be between 0 and 1

    health_max = 5
    health_start = 1
    health_num_deposit = 2
    health_deposit_size = 0.55
    health_fitness_harvest_reward = 0.3
    health_fitness_take_reward = 2.0

    bombs_max = 5
    bombs_start = 2
    bombs_num_deposit = 2
    bombs_deposit_size = 0.7
    bombs_fitness_harvest_reward = 0.2
    bombs_fitness_place_reward = 1.0

    walls_max = 20
    walls_start = 5
    walls_num_deposit = 2
    walls_deposit_size = 0.7
    walls_fitness_harvest_reward = 0.1
    walls_fitness_place_reward = 0.2
