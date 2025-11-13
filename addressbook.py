from builtins import property
from collections import UserDict
from datetime import datetime
import re
from error import (
    DuplicatePhoneNumberError,
    InvalidArgumentsError,
    PhoneNumberNotFoundError,
)


class Field:
    def __init__(self, value: str):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, name):
        if type(name) != str:
            raise InvalidArgumentsError(f"Name must be a string")
        name = name.strip()
        super().__init__(name)


class Phone(Field):
    def __init__(self, phone):
        phone = phone.strip()
        pattern = r"^\d{10}$"
        if not re.fullmatch(pattern, phone):
            raise InvalidArgumentsError(
                f"The number '{phone}' is invalid! It must be 10 characters (numbers) long."
            )
        super().__init__(phone)


class Birthday(Field):
    def __init__(self, value):
        try:
            if datetime.strptime(value, "%d.%m.%Y"):
                super().__init__(value)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")


class Record:
    def __init__(self, name: str):
        try:
            self.name = Name(name)
        except InvalidArgumentsError:
            raise
        self.phones = []
        self._birthday = None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

    def add_phone(self, phone: str):
        try:
            ph = Phone(phone)
            if ph:
                for p in self.phones:
                    if p.value == ph.value:
                        raise DuplicatePhoneNumberError(
                            f"Contact {self.name} already has the telephone number {phone}."
                        )
                self.phones.append(ph)
        except (InvalidArgumentsError, DuplicatePhoneNumberError):
            raise
        except Exception:
            raise

    def edit_phone(self, old_phone, new_phone):
        if not old_phone or not new_phone or old_phone == new_phone:
            raise InvalidArgumentsError("Phone numbers entered incorrectly.")
        [index] = [i for i, p in enumerate(self.phones) if p.value == old_phone]
        self.phones[index] = Phone(new_phone)

    def find_phone(self, phone):
        if not phone:
            raise InvalidArgumentsError("Phone numbers entered incorrectly.")
        for p in self.phones:
            if p.value == phone:
                return p.value
        raise PhoneNumberNotFoundError("Phone number not found.")

    def find_all_phones(self):
        if len(self.phones) > 0:
            return f"Phones: {'; '.join(p.value for p in self.phones)}"
        return None

    def remove_phone(self, phone):
        if not phone or len(phone) != 10:
            raise InvalidArgumentsError("Phone numbers entered incorrectly.")
        [index] = [i for i, p in enumerate(self.phones) if p.value == phone]
        del self.phones[index]
        return phone

    @property
    def birthday(self):
        return self._birthday

    @birthday.setter
    def birthday(self, birthday):
        self._birthday = Birthday(birthday)


class AddressBook(UserDict):
    def add_record(self, record: Record):
        if not isinstance(record, Record):
            raise ValueError(
                "In AddressBook, you can append only an object of the Record class."
            )
        name_key = record.name.value
        if not name_key:
            raise ValueError("You cannot add a contact without a name to AddressBook.")
        if name_key in self.data:
            raise DuplicatePhoneNumberError("Contact with that name already exists.")
        self.data[name_key] = record
        return self.data[name_key]

    def find(self, name):
        if not name in self.data:
            return None
        return self.data[name]

    def delete(self, name):
        if not name:
            raise InvalidArgumentsError("Name entered incorrectly.")
        if name in self.data:
            contact = self.data[name]
            del self.data[name]
            return contact

    def get_upcoming_birthdays(self, interval=7):
        res = []
        today = datetime.today().date()

        for contact in self.data.values():
            user_birthday_datetime = datetime.strptime(
                contact.birthday, "%d.%m.%Y"
            ).date()
            birthday_this_year = user_birthday_datetime.replace(year=today.year)

            if 0 <= ((birthday_this_year - today).days) < interval:
                res.append(
                    {
                        "name": contact["name"],
                        "congratulation_date": birthday_this_year.strftime(
                            "DD.MM.YYYY"
                        ),
                    }
                )
        return sorted(res, key=lambda contact: contact["congratulation_date"])
