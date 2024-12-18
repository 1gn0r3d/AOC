# --- Day 4: Ceres Search ---
# "Looks like the Chief's not here. Next!" One of The Historians pulls
# out a device and pushes the only button on it. After a brief flash, you
# recognize the interior of the Ceres monitoring station!
#
# As the search for the Chief continues, a small Elf who lives on the
# station tugs on your shirt; she'd like to know if you could help her
# with her word search (your puzzle input). She only has to find one word: XMAS.
#
# This word search allows words to be horizontal, vertical, diagonal,
# written backwards, or even overlapping other words. It's a little
# unusual, though, as you don't merely need to find one instance of XMAS
# - you need to find all of them. Here are a few ways XMAS might appear,
# where irrelevant characters have been replaced with .:
#
# ..X...
# .SAMX.
# .A..A.
# XMAS.S
# .X....
#
# The actual word search will be full of letters instead. For example:
#
# MMMSXXMASM
# MSAMXMSMSA
# AMXSXMAAMM
# MSAMASMSMX
# XMASAMXAMM
# XXAMMXXAMA
# SMSMSASXSS
# SAXAMASAAA
# MAMMMXMMMM
# MXMXAXMASX
#
# In this word search, XMAS occurs a total of 18 times; here's the same
# word search again, but where letters not involved in any XMAS have been replaced with .:
#
# ....XXMAS.
# .SAMXMS...
# ...S..A...
# ..A.A.MS.X
# XMASAMX.MM
# X.....XA.A
# S.S.S.S.SS
# .A.A.A.A.A
# ..M.M.M.MM
# .X.X.XMASX
#
# Take a look at the little Elf's word search. How many times does XMAS appear?
#
# --- Part Two ---
# The Elf looks quizzically at you. Did you misunderstand the assignment?
#
# Looking for the instructions, you flip over the word search to find
# that this isn't actually an XMAS puzzle; it's an X-MAS puzzle in which
# you're supposed to find two MAS in the shape of an X. One way to
# achieve that is like this:
#
# M.S
# .A.
# M.S
# Irrelevant characters have again been replaced with . in the above
# diagram. Within the X, each MAS can be written forwards or backwards.
#
# Here's the same example from before, but this time all of the X-MASes
# have been kept instead:
#
# .M.S......
# ..A..MSMS.
# .M.S.MAA..
# ..A.ASMSM.
# .M.S.M....
# ..........
# S.S.S.S.S.
# .A.A.A.A..
# M.M.M.M.M.
# ..........
# In this example, an X-MAS appears 9 times.
#
# Flip the word search from the instructions back over to the word search
# side and try again. How many times does an X-MAS appear?
from src.fileparser import load_file


def find_characters_in_row(row: list, character: str = 'X') -> list[int]:
    return [i for i, _ in enumerate(row) if row[i] == character]


def find_character_in_direction(
    matrix: list[list[str]],
    start_location: tuple[int],
    direction: tuple[int]
) -> bool:
    """
    Searches for a character in a certain direction from the starting location.
    Returns the character in the given direction,
    Raises an IndexError if the character is out of bounds of the matrix.

    The direction is indicated with an x,y tuple and accepts only
    values of -1 an 1 for the direction.
    """
    # print(f"{direction=}")
    x = start_location[0] + direction[0]
    y = start_location[1] + direction[1]
    # print(f"{x=}, {y=}")
    if x < 0 or y < 0:
        raise IndexError

    return matrix[y][x]


def search_for_X_MAS(
    matrix: list[list[str]],
    start_location: tuple[int]
) -> bool:
    """
    Searches for two times the word 'MAS', shaped like an X in the matrix.
    Returns true if the X shaped MAS words are found for the giving starting location.
    The function assumes the starting location contains the letter 'A',
    the center of the crossed 'MAS'
    """
    directions = [
        (-1, -1),
        (-1, 1)
    ]
    for direction in directions:
        # print(f"{direction=}")
        try:
            character1 = find_character_in_direction(
                matrix=matrix,
                direction=direction,
                start_location=start_location
            )
        except IndexError:
            # print('Index out of range.')
            return False
        # print(f"{character1=}")
        if character1 not in ['M', 'S']:
            return False
        oposite_direction = tuple(-1 * i for i in direction)
        # print(f"{oposite_direction=}")
        try:
            character2 = find_character_in_direction(
                matrix=matrix,
                direction=oposite_direction,
                start_location=start_location
            )
        except IndexError:
            # print('Index out of range.')
            return False
        # print(f"{character2=}")
        if character2 not in ['M', 'S']:
            return False
        if character1 == character2:
            return False
    return True


if __name__ == '__main__':
    # filename = 'd4_example.txt'
    filename = 'd4.txt'
    data = load_file(filename)

    x_mas_found = 0
    for y, row in enumerate(data):
        # print(row)
        x_locations = find_characters_in_row(row=row, character='A')
        for i, x in enumerate(x_locations):
            # print(f"{x=}, {y=}")
            x_mas_found += search_for_X_MAS(
                matrix=data,
                start_location=(x, y)
            )
    print(x_mas_found)
