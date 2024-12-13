from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiResponse,
)
from rest_framework import status

from users.schemas.examples.users import (
    EMPTY_FIELDS_OPEN_API_EXAMPLE,
    NOT_VALID_USERNAME_OPEN_API_EXAMPLE,
    USERNAME_EXISTS_OPEN_API_EXAMPLE,
    EMAIL_EXISTS_OPEN_API_EXAMPLE,
    NOT_VALID_EMAIL_OPEN_API_EXAMPLE,
    NOT_VALID_PASSWORD_OPEN_API_EXAMPLE,
    REGISTER_REQUEST_OPEN_API_EXAMPLE,
    REGISTER_RESPONSE_OPEN_API_EXAMPLE,
)
from users.serializers import UserSerializer

user_register_schema = extend_schema_view(
    post=extend_schema(
        description="Register new user",
        request=UserSerializer(),
        examples=[
            REGISTER_REQUEST_OPEN_API_EXAMPLE,
            REGISTER_RESPONSE_OPEN_API_EXAMPLE,
        ],
        responses={
            status.HTTP_201_CREATED: UserSerializer(),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description="Bad request, invalid data",
                response=OpenApiTypes.OBJECT,
                examples=[
                    EMPTY_FIELDS_OPEN_API_EXAMPLE,
                    NOT_VALID_USERNAME_OPEN_API_EXAMPLE,
                    USERNAME_EXISTS_OPEN_API_EXAMPLE,
                    NOT_VALID_EMAIL_OPEN_API_EXAMPLE,
                    EMAIL_EXISTS_OPEN_API_EXAMPLE,
                    NOT_VALID_PASSWORD_OPEN_API_EXAMPLE,
                ],
            ),
        },
    )
)
