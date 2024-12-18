# --- Day 6: Guard Gallivant ---
# The Historians use their fancy device again, this time to whisk you all
# away to the North Pole prototype suit manufacturing lab... in the year
# 1518! It turns out that having direct access to history is very
# convenient for a group of historians.
#
# You still have to be careful of time paradoxes, and so it will be
# important to avoid anyone from 1518 while The Historians search for the
# Chief. Unfortunately, a single guard is patrolling this part of the lab.
#
# Maybe you can work out where the guard will go ahead of time so that
# The Historians can search safely?
#
# You start by making a map (your puzzle input) of the situation. For example:
#
# ....#.....
# .........#
# ..........
# ..#.......
# .......#..
# ..........
# .#..^.....
# ........#.
# #.........
# ......#...
# The map shows the current position of the guard with ^ (to indicate the
# guard is currently facing up from the perspective of the map). Any
# obstructions - crates, desks, alchemical reactors, etc. - are shown as #.
#
# Lab guards in 1518 follow a very strict patrol protocol which involves
# repeatedly following these steps:
#
# If there is something directly in front of you, turn right 90 degrees.
# Otherwise, take a step forward.
# Following the above protocol, the guard moves up several times until
# she reaches an obstacle (in this case, a pile of failed suit prototypes):
#
# ....#.....
# ....^....#
# ..........
# ..#.......
# .......#..
# ..........
# .#........
# ........#.
# #.........
# ......#...
# Because there is now an obstacle in front of the guard, she turns right
# before continuing straight in her new facing direction:
#
# ....#.....
# ........>#
# ..........
# ..#.......
# .......#..
# ..........
# .#........
# ........#.
# #.........
# ......#...
# Reaching another obstacle (a spool of several very long polymers), she
# turns right again and continues downward:
#
# ....#.....
# .........#
# ..........
# ..#.......
# .......#..
# ..........
# .#......v.
# ........#.
# #.........
# ......#...
# This process continues for a while, but the guard eventually leaves the
# mapped area (after walking past a tank of universal solvent):
#
# ....#.....
# .........#
# ..........
# ..#.......
# .......#..
# ..........
# .#........
# ........#.
# #.........
# ......#v..
# By predicting the guard's route, you can determine which specific
# positions in the lab will be in the patrol path. Including the guard's
# starting position, the positions visited by the guard before leaving
# the area are marked with an X:
#
# ....#.....
# ....XXXXX#
# ....X...X.
# ..#.X...X.
# ..XXXXX#X.
# ..X.X.X.X.
# .#XXXXXXX.
# .XXXXXXX#.
# #XXXXXXX..
# ......#X..
# In this example, the guard will visit 41 distinct positions on your
# map.
#
# Predict the path of the guard. How many distinct positions will the
# guard visit before leaving the mapped area?
import numpy as np
from src.fileparser import load_file


class Guard():
    def __init__(self, guard_identifier: str, initial_position: list[int, int]):
        self.location = np.array(initial_position)
        if guard_identifier == '>':
            self.direction = np.array((1, 0))
        elif guard_identifier == 'v':
            self.direction = np.array((0, 1))
        elif guard_identifier == '<':
            self.direction = np.array((-1, 0))
        elif guard_identifier == '^':
            self.direction = np.array((0, -1))
        print(f"initial position: {initial_position}")

    def rotate(self, angle: int = 90):
        angle = np.radians(angle)
        rotation_matrix = np.array([
            [np.cos(angle), -np.sin(angle)],
            [np.sin(angle), np.cos(angle)]
        ])
        print("rotating.")
        self.direction = np.dot(rotation_matrix, self.direction).astype(int)

    def walk(self):
        self.location += self.direction
        print(f"walking forward. new pos: {self.location}")

    def look_ahead(self):
        return self.location + self.direction


def find_guard_initial_position(map: list[str]) -> dict[str, list[int, int] | str]:
    guard_identifiers = ['>', 'v', '<', '^']
    for y, row in enumerate(map):
        for x, id in enumerate(row):
            if id in guard_identifiers:
                return {
                    'initial_position': [x, y],
                    'guard_identifier': id
                }


def walk_guard_on_map(map: list[str], guard: Guard):
    """
    Walks the guard on the map, crossing spots the guard has entered.
    Stops walking around if the guard leaves the map.
    Rotates the guard when he hits a non free pathway.
    """
    value_on_map = map[guard.location[1]][guard.location[0]]
    row = map[guard.location[1]]
    map[guard.location[1]] = row[:guard.location[0]] + "X" + row[guard.location[0] + 1:]

    location_in_front_of_guard = guard.look_ahead()
    try:
        if map[location_in_front_of_guard[1]][location_in_front_of_guard[0]] in ['.', 'X']:
            guard.walk()

        elif map[location_in_front_of_guard[1]][location_in_front_of_guard[0]] == '#':
            guard.rotate()

        walk_guard_on_map(map, guard)
    except IndexError:
        return map


def count_positions_on_map(map: list[str]) -> int:
    locations_visited = 0
    for row in map:
        locations_visited += row.count('X')
    return locations_visited


if __name__ == '__main__':
    filename = 'd6_example.txt'
    map = load_file(filename)
    for r in map:
        print(r)
    guard_info = find_guard_initial_position(map)
    guard = Guard(**guard_info)
    map = walk_guard_on_map(map, guard)

    for r in map:
        print(r)

    print(f"locations visited by guard: {count_positions_on_map(map)}")
