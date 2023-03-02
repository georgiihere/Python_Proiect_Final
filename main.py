import datetime
import re
import sys
from availability import *


# presents all book in the database
def check():
    for i in order_books_by_availability():
        for key, val in i.items():
            if key != "Date":
                print(f"{key} : {val}")
            elif (datetime.datetime.utcnow().date()-val.date()).days == 0:
                print("Last Used : today")
            elif (datetime.datetime.utcnow().date()-val.date()).days > 365:
                print(f"Last Used : {round((datetime.datetime.utcnow().date()-val.date()).days/365,1)} years ago")
            else:
                print(f"Last Used : {(datetime.datetime.utcnow().date() - val.date()).days} days ago")
        print(30 * "=")


# verifies if the user input for the book kind is fiction or nonfiction
# prompts the user to provide one of the 2 options if not
def add_kind():
    while True:
        try:
            kind = input("Enter the type of the book (fiction/nonfiction): ").upper()
            assert kind == "FICTION" or kind == "NONFICTION"
            return kind
        except AssertionError:
            print("Please enter one of the provided 2 types of book...")


# adds book to Pybrary, with the status set as AVAILABLE
# also uses today's date as the set date for the book
def add():
    print("Add a book")
    title = input("Enter the title of the book: ")
    author = input("Enter the author of the book: ")
    kind = add_kind()
    genre = input("Enter the genre of the book: ")

    new_book = {
        "Title": title,
        "Author": author,
        "Type": kind,
        "Genre": genre,
        "Status": "AVAILABLE",
        "Date": datetime.datetime.now()
    }

    books.insert_one(new_book)

    print(f"{title} has been added to the Pybrary! ")


# return book to the Pybrary (changes book status from AVAILABLE to NOT_AVAILABLE)
def take():
    title = input("Enter the title of the book you wish to take: ")
    book = books.find_one({"Title": {"$regex": re.compile(title, re.IGNORECASE)}})
    if book:
        if book["Status"] == "AVAILABLE":
            books.update_one({"_id": book["_id"]},
                             {"$set": {"Status": "NOT_AVAILABLE", "Date": datetime.datetime.utcnow()}})
            print(f"{book['Title']} has been taken. Please return it within 14 days.")
        else:
            print(f"Sorry, {book['Title']} is not available at the moment.")
    else:
        print(f"{title} is not in the Pybrary.")


# deletes book from Pybrary (completely removes book from database)
def remove():
    title = input("Enter the title of the book you wish to remove: ")
    book = books.find_one({"Title": {"$regex": re.compile(title, re.IGNORECASE)}})
    if book:
        result = books.delete_one({"_id": book["_id"]})
        if result.deleted_count == 1:
            print(f"{book['Title']} has been removed from the Pybrary.")
        else:
            print("An error occurred while deleting the book.")
    else:
        print(f"{title} is not in the Pybrary.")


# receives book back into the Pybrary
# (changes book status from NOT_AVAILABLE to AVAILABLE)
def receive():
    title = input("Enter the title of the book you wish to return: ")
    book = books.find_one({"Title": {"$regex": re.compile(title, re.IGNORECASE)}})
    if book:
        if book["Status"] == "NOT_AVAILABLE":
            books.update_one({"_id": book["_id"]},
                             {"$set": {"Status": "AVAILABLE", "Date": datetime.datetime.utcnow()}})
            print(f"{book['Title']} has been returned.")
        else:
            print(f"Sorry, {book['Title']} was already returned.")
    else:
        print(f"{title} is not in the Pybrary database.")


def main():
    option_dictionary = {
        "1": check,
        "2": add,
        "3": take,
        "4": remove,
        "5": receive,
        "6": sys.exit
    }

    while True:
        print(60 * "*")
        print("PYBRARY".center(60))
        print(60 * "*")
        print("Welcome to your Pybrary!What would you like to do today?".center(60))
        print("1.Check the books\n2.Add a book\n3.Take a book\n4.Remove a book\n5.Return a book\n6.Exit")
        print(60 * "*")

        option = input("Choose your option: ")
        if option in option_dictionary:
            option_dictionary[option]()
            input("Press return to continue...")
        else:
            print("Oops!That's not a valid option!Try again.")


if __name__ == "__main__":
    main()
