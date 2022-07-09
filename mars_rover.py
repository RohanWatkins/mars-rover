import argparse
import os

def validate_plateau_coords(coordinates : str) -> list:
    """
        Validate plateau coordinates
    """
    if not isinstance(coordinates, str):
        raise ValueError('Plateau coords must be a str in the format int int, e.g. 5 5')
    if len(coordinates) == 0:
        raise ValueError('Plateau coords must be in the format int int, e.g. 5 5')

    coordinates = coordinates.split(' ')
    if len(coordinates) != 2:
        raise ValueError('Plateau coords must be in the format int int, e.g. 5 5')
    coordinates[0] = int(coordinates[0])
    coordinates[1] = int(coordinates[1])
    return coordinates

def validate_rover_position(position : str) -> list:
    """
        Validate a string is in the correct format to be a rover position.
        The expected format is x y direction where x and y are integers and direction is one of N, E, S or W.
    """
    if not isinstance(position, str):
        raise ValueError('Rover position must be a non empty string in the format int int [N, E, S, W]')
    if len(position) == 0:
        raise ValueError('Rover position must be a non empty string in the format int int [N, E, S, W]')
    position_list = position.split()
    if len(position_list) != 3:
        raise ValueError('Rover position must be a non empty string in the format int int [N, E, S, W]')
    position_list[0] = int(position_list[0])
    position_list[1] = int(position_list[1])
    position_list[2] = position_list[2].upper()
    if position_list[2] not in ['N', 'E', 'S', 'W']:
        raise ValueError('Rover position must be a non empty string in the format int int [N, E, S, W]')

    return position_list

def validate_rover_orders(order : str) -> str:
    """
        Validate that an order only contains characters L R and M
    """
    if not isinstance(order, str):
        raise ValueError('Orders must be a string')
    order = order.upper()
    for char in order:
        if char not in ['L', 'R', 'M']:
            raise ValueError('Orders must only contain the characters L R and M')
    return order

def validate_rover_commands(commands : list) -> list:
    """
        Validate rover commands
    """
    valid_commands = []
    for rover_number in range(0, len(commands)-1,2):
        valid_commands.append(validate_rover_position(commands[rover_number]))
        valid_commands.append(validate_rover_orders(commands[rover_number+1]))

    return valid_commands

def validate_input(filepath : str) -> tuple:
    """
        Validate the provided input file
    """
    if not os.path.isfile(filepath):
        raise ValueError(f'{filepath} does not exist')
    else:
        with open(filepath, 'r', encoding='utf-8') as file:
            commands = file.read().splitlines()
        if len(commands) == 0:
            raise ValueError('expected an odd number of lines in the commands file')
        if len(commands) % 2 == 0:
            raise ValueError('expected an odd number of lines in the commands file')

        plateau_coords = validate_plateau_coords(commands[0])
        rover_commands = validate_rover_commands(commands[1:])

    return (plateau_coords, rover_commands)

def is_on_plateau(coords : list, plateau_coords : list) -> bool:
    """
        Check if a coordinate is on the plateau.
    """
    x_valid = coords[0] >= 0 and coords[0] <= plateau_coords[0]
    y_valid = coords[1] >= 0 and coords[1] <= plateau_coords[1]
    return x_valid and y_valid

def navigate(plateau_coords : list, rover_commands : list) -> list:
    """
        Move the rovers and return the final rover positions
    """
    rover_positions = rover_commands[::2]
    for position in rover_positions:
        if not is_on_plateau(position, plateau_coords):
            raise ValueError('Invalid rover starting position ' + ' '.join(str(x) for x in position))
    final_positions = []
    for rover_number in range(0, len(rover_commands)-1,2):
        rover_position = rover_commands[rover_number]
        for command in rover_commands[rover_number+1]:
            if command == 'M':
                if rover_position[-1] == 'N':
                    rover_position[1] += 1
                elif rover_position[-1] == 'E':
                    rover_position[0] += 1
                elif rover_position[-1] == 'S':
                    rover_position[1] -= 1
                elif rover_position[-1] == 'W':
                    rover_position[0] -= 1
            elif command == 'L':
                if rover_position[-1] == 'N':
                    rover_position[-1] = 'W'
                elif rover_position[-1] == 'E':
                    rover_position[-1] = 'N'
                elif rover_position[-1] == 'S':
                    rover_position[-1] = 'E'
                elif rover_position[-1] == 'W':
                    rover_position[-1] = 'S'
            elif command == 'R':
                if rover_position[-1] == 'N':
                    rover_position[-1] = 'E'
                elif rover_position[-1] == 'E':
                    rover_position[-1] = 'S'
                elif rover_position[-1] == 'S':
                    rover_position[-1] = 'W'
                elif rover_position[-1] == 'W':
                    rover_position[-1] = 'N'
            if not is_on_plateau(rover_position, plateau_coords):
                raise ValueError('Tried to move a rover off the plateau to ' + ' '.join(str(x) for x in rover_position))

        final_positions.append(rover_position)
    return final_positions

def main():
    """ Script entry point """
    parser = argparse.ArgumentParser(description='Mars Rover Navigation Program')
    parser.add_argument('--commands', type=str, help='file of plateau coordinates rover positions and commands', required=True)
    args = parser.parse_args()

    plateau_coords, rover_commands = validate_input(args.commands)
    final_positions = navigate(plateau_coords, rover_commands)
    for position in final_positions:
         print(' '.join(str(x) for x in position))

if __name__ == '__main__':
    main()
