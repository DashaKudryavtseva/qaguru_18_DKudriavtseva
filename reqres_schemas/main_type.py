from voluptuous import Schema, PREVENT_EXTRA


class ReqresSchema:
    single_schema: Schema({})
    list_schema: Schema({})
    support: Schema({})

    def __init__(self, data: Schema({})):
        self.support = Schema(
            {"url": str, "text": str}, extra=PREVENT_EXTRA, required=True
        )

        self.list_schema = Schema(
            {
                "page": int,
                "per_page": int,
                "total": int,
                "total_pages": int,
                "data": [data],
                "support": self.support,
            },
            extra=PREVENT_EXTRA,
            required=True,
        )

        self.single_schema = Schema(
            {"data": data, "support": self.support},
            extra=PREVENT_EXTRA,
            required=True,
        )


class ReqresSchemaUser:
    user: Schema({})

    def __init__(self):
        self.user = Schema(
            {
                "id": int,
                "email": str,
                "first_name": str,
                "last_name": str,
                "avatar": str,
            },
            extra=PREVENT_EXTRA,
            required=True,
        )


class ReqresSchemaColor:
    color: Schema({})

    def __init__(self):
        self.color = Schema(
            {"id": int, "name": str, "year": int, "color": str, "pantone_value": str},
            extra=PREVENT_EXTRA,
            required=True,
        )
