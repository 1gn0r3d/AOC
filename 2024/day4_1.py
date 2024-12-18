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
from src.fileparser import load_file


def find_characters_in_row(row: list, character: str = 'X') -> list[int]:
    return [i for i, _ in enumerate(row) if row[i] == character]


def find_character_in_direction(
    matrix: list[list[str]],
    start_location: tuple[int],
    character: str,
    direction: tuple[int]
) -> bool:
    """
    Searches for a character in a certain direction from the starting location.
    Returns true if the character is found in the given direction,
    returns false if the character is not found, or if the index is ount of
    bounds of the matrix supplied.

    The direction is indicated with an x,y tuple and accepts only
    values of -1 an 1 for the direction.
    """
    # print(f"{direction=}")
    x = start_location[0] + direction[0]
    y = start_location[1] + direction[1]
    # print(f"{x=}, {y=}")
    if x < 0 or y < 0:
        print(f"{x < 0=}")
        print(f"{y < 0=}")
        return False

    try:
        character_in_direction = matrix[y][x]
    except IndexError:
        print("Index out of range.")
        return False

    # print(f"{character_in_direction=}")
    # print(f"{character=}")
    if character == character_in_direction:
        return True
    return False


def search_for_words(
        matrix: list[list],
        start_location: tuple[int],
        word: str = 'XMAS'
) -> int:
    """
    Searches for a word in a matrix given a starting location.
    Returns how many times the word is found starting from that location.
    """
    directions = []
    for x in range(-1, 2):
        for y in range(-1, 2):
            if x == 0 and y == 0:
                continue
            directions.append({'dir': (x, y)})
    # print(f"{start_location=}")
    for direction in directions:
        for i, character in enumerate(word):
            # print(i, character)
            if i == 0:
                continue
            character_found = find_character_in_direction(
                matrix=matrix,
                character=character,
                start_location=start_location,
                direction=(direction['dir'][0] * i, direction['dir'][1] * i)
            )
            # print(character_found)
            if not character_found:
                direction['word_found'] = False
                break
            if i == len(word) - 1:
                direction['word_found'] = True

    # print(directions)
    words_found = 0
    for direction in directions:
        if direction['word_found'] == True:
            words_found += 1
    return words_found


if __name__ == '__main__':
    # filename = 'd4_example.txt'
    filename = 'd4.txt'
    data = load_file(filename)

    words_found = 0
    for y, row in enumerate(data):
        # print(row)
        x_locations = find_characters_in_row(row)
        for i, x in enumerate(x_locations):
            # print(f"{x=}, {y=}")
            words_found += search_for_words(matrix=data, start_location=(x, y))
    print(words_found)
