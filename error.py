class InvalidArgumentsError(Exception):
    """Error: invalid number."""

    pass


class DuplicatePhoneNumberError(Exception):
    """Error: number already exists."""

    pass


class PhoneNumberNotFoundError(Exception):
    """Error: phone number not found."""

    pass


class ContactNotFoundError(Exception):
    """Error: contact not found."""

    pass
