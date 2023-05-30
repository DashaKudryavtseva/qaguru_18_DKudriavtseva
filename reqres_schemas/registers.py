from voluptuous import Schema, PREVENT_EXTRA


class RegisterSchema:
    '''Описание Schema для регистрации/входа пользователя на https://reqres.in/'''

    sucsessfull: Schema({})

    def __init__(self):
        self.sucsessfull = Schema(
            {"id": int, "token": str},
            extra=PREVENT_EXTRA,
            required=False,
        )
