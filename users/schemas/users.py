from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiResponse,
)
from rest_framework import status

from events.schemas.events import UNAUTHORISED_OPEN_API_RESPONSE
from users.schemas.examples.users import (
    EMPTY_FIELDS_OPEN_API_EXAMPLE,
    NOT_VALID_USERNAME_OPEN_API_EXAMPLE,
    USERNAME_EXISTS_OPEN_API_EXAMPLE,
    EMAIL_EXISTS_OPEN_API_EXAMPLE,
    NOT_VALID_EMAIL_OPEN_API_EXAMPLE,
    NOT_VALID_PASSWORD_OPEN_API_EXAMPLE,
    REGISTER_REQUEST_OPEN_API_EXAMPLE,
    REGISTER_RESPONSE_OPEN_API_EXAMPLE,
    USER_DETAIL_OPEN_API_EXAMPLE,
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

user_manage_schema = extend_schema_view(
    get=extend_schema(
        description="Retrieve information about yourself",
        examples=[
            USER_DETAIL_OPEN_API_EXAMPLE,
        ],
        responses={
            status.HTTP_200_OK: UserSerializer(),
            status.HTTP_401_UNAUTHORIZED: UNAUTHORISED_OPEN_API_RESPONSE,
        },
    ),
    put=extend_schema(
        description="Update information about yourself",
        request=UserSerializer(),
        examples=[
            REGISTER_REQUEST_OPEN_API_EXAMPLE,
            REGISTER_RESPONSE_OPEN_API_EXAMPLE,
        ],
        responses={
            status.HTTP_200_OK: UserSerializer(),
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
            status.HTTP_401_UNAUTHORIZED: UNAUTHORISED_OPEN_API_RESPONSE,
        },
    ),
    patch=extend_schema(
        description="Update partially information about yourself",
        request=UserSerializer(partial=True),
        examples=[
            REGISTER_REQUEST_OPEN_API_EXAMPLE,
            REGISTER_RESPONSE_OPEN_API_EXAMPLE,
        ],
        responses={
            status.HTTP_200_OK: UserSerializer(),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description="Bad request, invalid data",
                response=OpenApiTypes.OBJECT,
                examples=[
                    NOT_VALID_USERNAME_OPEN_API_EXAMPLE,
                    USERNAME_EXISTS_OPEN_API_EXAMPLE,
                    NOT_VALID_EMAIL_OPEN_API_EXAMPLE,
                    EMAIL_EXISTS_OPEN_API_EXAMPLE,
                    NOT_VALID_PASSWORD_OPEN_API_EXAMPLE,
                ],
            ),
            status.HTTP_401_UNAUTHORIZED: UNAUTHORISED_OPEN_API_RESPONSE,
        },
    ),
)
