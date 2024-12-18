def load_file(filename: str) -> list[list]:
    with open(filename, 'r') as file:
        file_contents = file.read().splitlines()

    return file_contents


def d5_load_printing_instructions(filename: str) -> tuple[list[str]]:
    """
    Loads the file for day5, and splits it in a list of conditionals and a
    list of page instructions
    """
    file_contents = load_file(filename)
    instructions = {}
    pages = []
    for line in file_contents:
        if '|' in line:
            line_contents = line.split('|')
            try:
                instructions[int(line_contents[0])].append(int(line_contents[1]))
            except KeyError:
                instructions[int(line_contents[0])] = [int(line_contents[1])]
        elif ',' in line:
            page_contents = line.split(',')
            pages.append([int(p) for p in page_contents])
    return instructions, pages
