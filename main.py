from addressbook import AddressBook, Record
from error import (
    ContactNotFoundError,
    DuplicatePhoneNumberError,
    InvalidArgumentsError,
    PhoneNumberNotFoundError,
)


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Command or data entered incorrectly"
        except KeyError:
            return "User with this name not found"
        except IndexError:
            return "Give me name please."
        except (
            ContactNotFoundError,
            InvalidArgumentsError,
            DuplicatePhoneNumberError,
            PhoneNumberNotFoundError,
        ) as e:
            return f"Error: {e}"
        except Exception as e:
            return f"Непредвиденная ошибка: {e}"

    return inner


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        try:
            record.add_phone(phone)
        except Exception as e:
            print(f"Error: {e}")
    return message


@input_error
def change_contact(args, book):
    name, old_phone, new_phone = args
    if not name or not old_phone or not new_phone or old_phone == new_phone:
        raise InvalidArgumentsError(
            "To update a contact's phone number, the command must be entered in the format: [name], [old_phone], [new_phone]"
        )
    record = book.find(name)
    if not record:
        raise ContactNotFoundError("Contact not found.")
    record.edit_phone(old_phone, new_phone)
    return "Contact updated."


@input_error
def show_phone(args, book):
    name = args[0]
    record = book.find(name)
    if not record:
        raise ContactNotFoundError("Contact not found.")
    return record.find_all_phones()


@input_error
def show_all(book):
    if len(book.data) <= 0:
        return "Your contact list is empty."
    res = ""
    for record in book.data.values():
        res += f"{record}\n"
    return res


@input_error
def add_birthday(args, book):
    name, birthday = args
    record = book.find(name)
    if record is None:
        raise ContactNotFoundError("Contact not found.")
    if not birthday:
        raise ValueError("Date of birth not specified or specified incorrectly")
    record.birthday = birthday
    return f"Contact {name} added birthday {birthday}"


@input_error
def show_birthday(args, book):
    name = args[0]
    record = book.find(name)
    if record is None:
        raise ContactNotFoundError("Contact not found.")
    return record.birthday


@input_error
def birthdays(book):
    birthday_list = book.get_upcoming_birthdays()
    if birthday_list:
        res = "Birthdays in the next 7 days:\n"
        for contact in birthday_list:
            res += f"Name: {contact["name"]} Congratulation date: {contact["congratulation_date"]}\n"
        return res
    return "There are no birthdays in the next 7 days."


def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        if not user_input:
            print("Enter the correct command.")
            continue
        command, *args = parse_input(user_input)
        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(show_all(book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(book))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
