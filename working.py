import re

"""
Implement a function that:
    expects a str in either of the 12-hour formats below and returns the corresponding str in 24-hour format (i.e., 9:00 to 17:00).
        9:00 AM to 5:00 PM
        9 AM to 5 PM
    Expect that AM and PM will be capitalized (with no periods therein) and that there will be a space before each
"""


def main():
    print(convert(input("Hours: ")))


def convert(s):
    # check if the given time's FORMAT is valid:
    if not (time := re.search(r"(\d{1,2}):?(\d{2})? (AM|PM) to (\d{1,2}):?(\d{2})? (AM|PM)", s.strip())):
        raise ValueError # if the input to convert is not in either of acceptable formats, raise ValueError:

    # NOW >> get components of both times:
    start_hour, end_hour = int(time.group(1)), int(time.group(4))
    # If no minutes given, set them to 00:
    if time.group(2) is None:
        start_minute = end_minute = 0
    else:
        start_minute, end_minute = int(time.group(2)), int(time.group(5))

    # MUST check if either time is invalid (e.g., 12:60 AM, 13:00 PM, etc.):
    if not (1 <= start_hour <= 12 and 0 <= start_minute < 60) or not (1 <= end_hour <= 12 and 0 <= end_minute < 60):
        raise ValueError

    # NOW >> convert PM components to 24-hr format
    # CASE 1: when it's AM to PM
    if time.group(3) == "AM":
        # add 12 to convert to 24hr format. But, if it's 12 PM or 12:00 PM, leave it unchanged
        end_hour += (12 if end_hour != 12 else 0)  # 12 PM (or 12:00 PM) is just 12:00 so don't change
        start_hour %= 12 # this makes sure that 12:00 AM (or 12 AM) is converted to 0:00

    # CASE 2: when it's PM to AM
    else:
        # add 12 to convert to 24hr format. But, if it's 12 PM or 12:00 PM, leave it unchanged
        start_hour += (12 if start_hour != 12 else 0)  # 12 PM (or 12:00 PM) is just 12:00 so don't change
        end_hour %= 12  # this makes sure that 12:00 AM (or 12 AM) is converted to 0:00

    return f"{start_hour:02}:{start_minute:02} to {end_hour:02}:{end_minute:02}"


if __name__ == "__main__":
    main()
