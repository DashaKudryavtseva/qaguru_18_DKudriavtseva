from voluptuous import Schema, PREVENT_EXTRA


class RegisterSchema:
    sucsessfull: Schema({})

    def __init__(self):
        self.sucsessfull = Schema(
            {"id": int, "token": str},
            extra=PREVENT_EXTRA,
            required=False,
        )
