from datetime import date
from re import fullmatch
from sys import exit
import inflect


# this function validates if the user enters correct DoB in YYYY-MM-DD format
# if it's not valid date, it exits the program
# if valid, it returns a tuple of date elements as integers: (year, month, day)
def valid_DOB(dateOfBirth):
    # Exit via sys.exit if the user does not input a date in YYYY-MM-DD format.
    if not (date := fullmatch(r"(\d{4})-(\d{2})-(\d{2})", dateOfBirth)):
        exit("Invalid date")  # again, we ensure that no exceptions are raised.
    else:  # if valid format, we return year, month, and days
        return int(date[1]), int(date[2]), int(date[3])
    # Examples of Valid/Invalid format:
    # January 1, 2019 -> Invalid
    # Dec. 1, 2020 -> Invalid
    # 1990-1-1 -> Invalid
    # 1934-01-01 -> Valid


# this function accepts timedelta object from datetime library and converts total seconds to minutes.
get_minutes = lambda timedelta: int(timedelta.total_seconds() / 60)

# this function accepts a numeric value of minutes and returns English words of that number:
nums_to_words = lambda number: inflect.engine().number_to_words(
    number, andword=""
)  # without any "and" between words


def main():
    # prompts the user for their date of birth, then store it as a date object:
    user_DOB = date(
        *valid_DOB(input("Date of Birth: "))
    )  # unpacking operator '*' automatically assings respective arguments

    # the time difference between today and user_DOB represented as minutes:
    minutes = get_minutes(date.today() - user_DOB)

    print(f"{nums_to_words(minutes).capitalize()} minutes")


if __name__ == "__main__":
    main()
