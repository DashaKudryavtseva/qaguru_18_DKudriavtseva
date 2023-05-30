from voluptuous import Schema, PREVENT_EXTRA


class EmployeeSchema:
    '''Описание Schema для создания/изменения user на https://reqres.in/'''

    created: Schema({})
    updated: Schema({})

    def __init__(self):
        self.created = Schema(
            {"name": str, "job": str, "id": str, "createdAt": str},
            extra=PREVENT_EXTRA,
            required=True,
        )
        self.updated = Schema(
            {"name": str, "job": str, "updatedAt": str},
            extra=PREVENT_EXTRA,
            required=True,
        )
