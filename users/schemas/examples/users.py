from drf_spectacular.utils import OpenApiExample


REGISTER_REQUEST_OPEN_API_EXAMPLE = OpenApiExample(
    name="User register request example",
    value={
        "username": "Tech_Dragon",
        "email": "tech.dragon@test.com",
        "password": "test123test",
    },
    request_only=True,
)

REGISTER_RESPONSE_OPEN_API_EXAMPLE = OpenApiExample(
    name="User register response example",
    value={
        "id": 12,
        "username": "Tech_Dragon",
        "email": "tech.dragon@test.com",
        "is_staff": False,
    },
    response_only=True,
)

EMPTY_FIELDS_OPEN_API_EXAMPLE = OpenApiExample(
    name="Empty required fields example",
    value={
        "username": ["This field is required."],
        "email": ["This field is required."],
        "password": ["This field is required."],
    },
    response_only=True,
)

NOT_VALID_USERNAME_OPEN_API_EXAMPLE = OpenApiExample(
    name="Not valid username example",
    value={
        "username": [
            "Enter a valid username. This value may contain only letters, numbers, and @/./+/-/_ characters."
        ]
    },
    response_only=True,
)

USERNAME_EXISTS_OPEN_API_EXAMPLE = OpenApiExample(
    name="Username exists example",
    value={"username": ["A user with that username already exists."]},
    response_only=True,
)

NOT_VALID_EMAIL_OPEN_API_EXAMPLE = OpenApiExample(
    name="Not valid email example",
    value={"email": ["Enter a valid email address."]},
    response_only=True,
)

EMAIL_EXISTS_OPEN_API_EXAMPLE = OpenApiExample(
    name="Email already exists example",
    value={"email": ["user with this email address already exists."]},
    response_only=True,
)

NOT_VALID_PASSWORD_OPEN_API_EXAMPLE = OpenApiExample(
    name="Not valid password example",
    value={"password": ["Ensure this field has at least 5 characters."]},
    response_only=True,
)
