from rest_framework.exceptions import ValidationError


class PersonError(ValidationError):
    """
    PersonError raised for errors in the individuals input.
    @param detail: explanation of the error
    """

    def __init__(self, detail):
        super().__init__({'Person Error': detail})


