from voluptuous import Schema, PREVENT_EXTRA


class EmployeeSchema:
    employee_schema: Schema({})

    def __init__(self):
        self.color_schema = Schema(
            {"id": int, "name": str, "year": int, "color": str, "pantone_value": str},
            extra=PREVENT_EXTRA,
            required=True,
        )
