from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiExample,
)
from rest_framework import status

from events.schemas.examples.events import list_example_json
from events.serializers import EventListSerializer

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
)
