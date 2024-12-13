from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiExample,
    OpenApiResponse,
)
from rest_framework import status

from events.schemas.examples.events import (
    list_example_json,
    create_update_request_example_json,
    create_update_response_example_json,
    unauthorised_401_no_token,
    unauthorised_401_invalid_token,
    bad_request_400_empty_fields,
    bad_request_400_overlapping_event,
    bad_request_400_event_in_the_past,
    bad_request_400_end_time_before_start_time,
    detail_example_json,
    not_found_404,
    bad_request_400_update_past_event, forbidden_403,
)
from events.serializers import (
    EventListSerializer,
    EventCreateUpdateSerializer,
    EventRetrieveSerializer,
)

UNAUTHORISED_OPEN_API_RESPONSE = OpenApiResponse(
    description="Unauthorized",
    response=OpenApiTypes.OBJECT,
    examples=[
        OpenApiExample(
            name="No token example",
            value=unauthorised_401_no_token,
            response_only=True,
        ),
        OpenApiExample(
            name="Invalid token example",
            value=unauthorised_401_invalid_token,
            response_only=True,
        ),
    ],
)

NOT_FOUND_OPEN_API_RESPONSE = OpenApiResponse(
    description="Not found",
    response=OpenApiTypes.OBJECT,
    examples=[
        OpenApiExample(
            name="Not found",
            value=not_found_404,
            response_only=True,
        )
    ],
)

FORBIDDEN_OPEN_API_RESPONSE = OpenApiResponse(
    description="Forbidden",
    response=OpenApiTypes.OBJECT,
    examples=[
        OpenApiExample(
            name="Forbidden example",
            value=forbidden_403,
            response_only=True,
        ),
    ]
)

CREATE_UPDATE_REQUEST_EXAMPLE = OpenApiExample(
    name="Event request example",
    value=create_update_request_example_json,
    request_only=True,
)

CREATE_UPDATE_RESPONSE_EXAMPLE = OpenApiExample(
    name="Event response example",
    value=create_update_response_example_json,
    response_only=True,
)

EMPTY_FIELDS_OPEN_API_EXAMPLE = OpenApiExample(
    name="Empty required fields example",
    value=bad_request_400_empty_fields,
    response_only=True,
)

OVERLAPPING_EVENTS_OPEN_API_EXAMPLE = OpenApiExample(
    name="Overlapping event example",
    value=bad_request_400_overlapping_event,
    response_only=True,
)

CREATE_UPDATE_PAST_EVENT_OPEN_API_EXAMPLE = OpenApiExample(
    name="Event with start time in the past example",
    value=bad_request_400_event_in_the_past,
    response_only=True,
)

CREATE_UPDATE_END_TIME_BEFORE_START_TIME_OPEN_API_EXAMPLE = OpenApiExample(
    name="Event with the ending time before starting time example",
    value=bad_request_400_end_time_before_start_time,
    response_only=True,
)

UPDATE_PAST_EVENT_OPEN_API_EXAMPLE = OpenApiExample(
    name="Updated event that started or is finished example",
    value=bad_request_400_update_past_event,
    response_only=True,
)


event_schema = extend_schema_view(
    list=extend_schema(
        description="Retrieve list of events, allowing filters & ordering",
        parameters=[
            OpenApiParameter(
                name="title",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description=(
                    "Filter by title name. Case insensitive. "
                    "Example: '?title=networking'"
                ),
                required=False,
            ),
            OpenApiParameter(
                name="organizer",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description=(
                    "Filter by username. Case insensitive. "
                    "Example: '?organizer=john'"
                ),
                required=False,
            ),
            OpenApiParameter(
                name="location",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description=(
                    "Filter by location name. Case insensitive. "
                    "Example: '?location=headquarters'"
                ),
                required=False,
            ),
            OpenApiParameter(
                name="start_date",
                type=OpenApiTypes.DATE,
                location=OpenApiParameter.QUERY,
                description=(
                    "Filter by starting date. Format: YYYY-MM-DD. "
                    "Example: '?start_date=2024-12-15'"
                ),
                required=False,
            ),
            OpenApiParameter(
                name="participating",
                type=OpenApiTypes.BOOL,
                location=OpenApiParameter.QUERY,
                description=(
                    "Filter events in which current authenticated user participates. "
                    "Example: '?participating=true'"
                ),
                required=False,
            ),
            OpenApiParameter(
                name="organizing",
                type=OpenApiTypes.BOOL,
                location=OpenApiParameter.QUERY,
                description=(
                    "Filter events that are organized by current authenticated user. "
                    "Example: '?organizing=true'"
                ),
                required=False,
            ),
        ],
        examples=[
            OpenApiExample(
                name="Event list example",
                value=list_example_json,
            )
        ],
        responses={
            status.HTTP_200_OK: EventListSerializer(many=True),
        },
    ),
    create=extend_schema(
        description="Create a new event",
        request=EventCreateUpdateSerializer(),
        examples=[
            CREATE_UPDATE_REQUEST_EXAMPLE,
            CREATE_UPDATE_RESPONSE_EXAMPLE,
        ],
        responses={
            status.HTTP_201_CREATED: EventCreateUpdateSerializer(),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description="Bad request, invalid data",
                response=OpenApiTypes.OBJECT,
                examples=[
                    EMPTY_FIELDS_OPEN_API_EXAMPLE,
                    OVERLAPPING_EVENTS_OPEN_API_EXAMPLE,
                    CREATE_UPDATE_PAST_EVENT_OPEN_API_EXAMPLE,
                    CREATE_UPDATE_END_TIME_BEFORE_START_TIME_OPEN_API_EXAMPLE,
                ],
            ),
            status.HTTP_401_UNAUTHORIZED: UNAUTHORISED_OPEN_API_RESPONSE,
        },
    ),
    retrieve=extend_schema(
        description="Retrieve detail event information",
        examples=[
            OpenApiExample(
                name="Event detail example",
                value=detail_example_json,
            )
        ],
        responses={
            status.HTTP_200_OK: EventRetrieveSerializer(),
            status.HTTP_404_NOT_FOUND: NOT_FOUND_OPEN_API_RESPONSE,
        },
    ),
    update=extend_schema(
        description="Update event information",
        request=EventCreateUpdateSerializer(),
        examples=[
            CREATE_UPDATE_REQUEST_EXAMPLE,
            CREATE_UPDATE_RESPONSE_EXAMPLE,
        ],
        responses={
            status.HTTP_200_OK: EventCreateUpdateSerializer(),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description="Bad request, invalid data",
                response=OpenApiTypes.OBJECT,
                examples=[
                    EMPTY_FIELDS_OPEN_API_EXAMPLE,
                    UPDATE_PAST_EVENT_OPEN_API_EXAMPLE,
                    OVERLAPPING_EVENTS_OPEN_API_EXAMPLE,
                    CREATE_UPDATE_PAST_EVENT_OPEN_API_EXAMPLE,
                    CREATE_UPDATE_END_TIME_BEFORE_START_TIME_OPEN_API_EXAMPLE,
                ],
            ),
            status.HTTP_401_UNAUTHORIZED: UNAUTHORISED_OPEN_API_RESPONSE,
            status.HTTP_403_FORBIDDEN: FORBIDDEN_OPEN_API_RESPONSE,
            status.HTTP_404_NOT_FOUND: NOT_FOUND_OPEN_API_RESPONSE,
        },
    ),
)
