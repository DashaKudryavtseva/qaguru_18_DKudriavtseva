from voluptuous import Schema, PREVENT_EXTRA


class ReqresSchema:
    base_url: str
    single_schema: Schema({})
    list_schema: Schema({})
    support: Schema({})

    def __init__(self, data: Schema({})):
        self.base_url = 'https://reqres.in/api/'

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
    user_schema: Schema({})

    def __init__(self):
        self.user_schema = Schema(
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
    color_schema: Schema({})

    def __init__(self):
        self.color_schema = Schema(
            {
                'name': str,
                'job': str,
                'id': str,
                'createdAt': str,
            },
            extra=PREVENT_EXTRA,
            required=True,
        )
