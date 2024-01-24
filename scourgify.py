"""
a program that:
Expects the user to provide two command-line arguments:
    the name of an existing CSV file to read as input, whose columns are assumed to be, in order, name and house, and
    the name of a new CSV to write as output, whose columns should be, in order, first, last, and house.
Converts that input to that output, splitting each name into a first name and last name.
"""
from sys import exit, argv
from csv import DictReader, DictWriter

# too few arguments:
if len(argv) < 3:
    exit("Too few command-line arguments")
# too many arguments:
if len(argv) > 3:
    exit("Too many command-line arguments")

# list to store newly formatted data, where each elemnt is a dictionary of each student containing, first name, last name, and house:
students = []

# read the initial file and rearrange then into new file format, storing them into students list:
try:
    with open(argv[1]) as oldfile:  # open the first CSV file to read
        for row in DictReader(oldfile):  # read each lines in the file as a dictionary
            # identify the first and last name append them alonside the house:
            students.append(
                { 
                    "first": row["name"].split(", ")[1],  # last name comes after comma and a blank in "name"
                    "last": row["name"].split(", ")[0],  # first name is everything before comma in "name"
                    "house": row["house"],  # house is just house, same
                }
            )
except FileNotFoundError:  # if the file's not found, exit
    exit("Could not read invalid_file.csv")

# write new file with cleaned-up format:
with open(argv[2], "w") as newfile:
    # using DictWriter, create a new file with apt field headers for 3 columns:
    writer = DictWriter(newfile, fieldnames=["first", "last", "house"])
    writer.writeheader()  # can't forget the header at the top
    # because students already have iterables of dictionaries, we can use writerows:
    writer.writerows(students)
