import unittest

from mars_rover import *

class TestValidatePlateauCoords(unittest.TestCase):
    """ Test the validate_plateau_coords function """
    def test_valid(self):
        for x in range(0, 10):
            for y in range(0, 10):
                coordinates = f'{x} {y}'
                with self.subTest(coordinates=coordinates):
                    value = validate_plateau_coords(coordinates)
                    self.assertEqual(value[0], x)
                    self.assertEqual(value[1], y)

    def test_invalid(self):
        invalid_coordinates = [
            '',
            None,
            ' ',
            '5.5',
            '6,2',
            123,
            '2.1 3.0',
            '10 2 1'
        ]
        for coordinates in invalid_coordinates:
            with self.subTest(coordinates=coordinates):
                self.assertRaises(ValueError, validate_plateau_coords, coordinates)


class TestValidateRoverPosition(unittest.TestCase):
    """ Test the validate_rover_position function """
    def test_valid(self):
        valid = [
            ['1 2 N', [1, 2, 'N']],
            ['3 3 E', [3, 3, 'E']],
            ['0 0 S', [0, 0, 'S']],
            ['12 7 W', [12, 7, 'W']]
        ]
        for position in valid:
           with self.subTest(position=position):
               value = validate_rover_position(position[0])
               self.assertListEqual(position[1], value)

    def test_invalid(self):
        invalid = [
            '',
            None,
            ' ',
            '5.5',
            '6,2',
            123,
            '2.1 3.0',
            '10 2 1',
            '1 2 P',
            'E N 2',
            '1 2 N N',
            '5 5 M'
        ]
        for position in invalid:
            with self.subTest(position=position):
                self.assertRaises(ValueError, validate_rover_position, position)


class TestValidateRoverOrders(unittest.TestCase):
    """ Test the validate_rover_orders function """
    def test_valid(self):
        valid = [
            ['LLLLLRRMMM', 'LLLLLRRMMM'],
            ['LRMLRM', 'LRMLRM'],
            ['', ''],
            ['LLLLLLLLLLLLLLLLLLLLL', 'LLLLLLLLLLLLLLLLLLLLL'],
            ['l', 'L'],
            ['r', 'R'],
            ['m', 'M']
        ]
        for order in valid:
           with self.subTest(order=order):
               value = validate_rover_orders(order[0])
               self.assertEqual(order[1], value)

    def test_invalid(self):
        invalid = [
            None,
            ' ',
            '5.5',
            '6,2',
            123,
            '2.1 3.0',
            '10 2 1',
            '1 2 P',
            'E N 2',
            '1 2 N N',
            '5 5 M',
            'LRMD',
            'L2',
            'sflndso'
        ]
        for order in invalid:
            with self.subTest(order=order):
                self.assertRaises(ValueError, validate_rover_orders, order)


class TestValidateRoverCommands(unittest.TestCase):
    """ Test the validate_rover_commands function """
    def test_valid(self):
        valid = [
            [['1 2 N', 'LMLMLMLMM', '3 3 E', 'MMRMMRMRRM'], [[1, 2, 'N'], 'LMLMLMLMM', [3, 3, 'E'], 'MMRMMRMRRM']]
        ]
        for command in valid:
           with self.subTest(command=command):
               value = validate_rover_commands(command[0])
               self.assertEqual(command[1], value)

class TestValidateInput(unittest.TestCase):
    """ Test the validate_input function """
    def test_valid(self):
        valid = [
            ['test_valid.txt', [[5, 5], [[1, 2, 'N'], 'LMLMLMLMM', [3, 3, 'E'], 'MMRMMRMRRM']]]
        ]
        for filepath in valid:
           with self.subTest(filepath=filepath):
               plateau_coords, rover_commands = validate_input(filepath[0])
               self.assertEqual(filepath[1][0], plateau_coords)
               self.assertEqual(filepath[1][1], rover_commands)


class TestIsOnPlateau(unittest.TestCase):
    """ Test the is_on_plateau function """
    def test_valid(self):
        plateau_coords = [20,20]
        for x in range(0, 20):
            for y in range(0, 20):
                coordinates = [x, y]
                with self.subTest(coords=coordinates, plateau_coords=plateau_coords):
                    self.assertTrue(is_on_plateau(coordinates, plateau_coords))

    def test_invalid(self):
        plateau_coords = [20,20]
        for x in range(21, 30):
            for y in range(21, 30):
                coordinates = [x, y]
                with self.subTest(coords=coordinates, plateau_coords=plateau_coords):
                    self.assertFalse(is_on_plateau(coordinates, plateau_coords))
        for x in range(-1, -10, -1):
            for y in range(-1, -10, -1):
                coordinates = [x, y]
                with self.subTest(coords=coordinates, plateau_coords=plateau_coords):
                    self.assertFalse(is_on_plateau(coordinates, plateau_coords))

class TestNavigate(unittest.TestCase):
    """ Test the navigate function """
    def test_valid(self):
        plateau_coords, rover_commands = validate_input('test_valid.txt')
        final_positions = navigate(plateau_coords, rover_commands)
        self.assertListEqual(final_positions, [[1, 3, 'N'], [5, 1, 'E']])
