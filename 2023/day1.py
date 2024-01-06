from pathlib import Path
import re

filepath = Path(__file__).parent / "d1.txt"

# filepath = Path(__file__).parent / "d1_example.txt"
# filepath = Path(__file__).parent / "d1_example2.txt"


DIGITS = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}

regex = re.compile(r"(?=(one|two|three|four|five|six|seven|eight|nine|\d))")


def find_first_digit(text_string: str):
    return regex.findall(text_string)


def convert_str_to_digit(string: str):
    try:
        digit = int(string)
    except ValueError:
        digit = DIGITS[string]
    return digit


def main():
    with filepath.open() as file:
        # I want to use a generator to do this, just because
        rows = (row for row in file)
        sum = 0
        for row in rows:
            digits = find_first_digit(row)
            if not digits:
                continue

            first_digit = convert_str_to_digit(digits[0])
            last_digit = convert_str_to_digit(digits[-1])

            calibration_value = f"{first_digit}{last_digit}"

            sum += int(calibration_value)

    print(f"{sum=}")


if __name__ == "__main__":
    main()
