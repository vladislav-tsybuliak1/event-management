import django_filters
from django.db.models import QuerySet, Case, When, Value, IntegerField
from django.utils.timezone import now

from events.models import Event


class EventFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(
        lookup_expr="icontains",
        label="Event Title",
    )
    organizer = django_filters.CharFilter(
        field_name="organizer__username",
        lookup_expr="icontains",
        label="Organizer Username",
    )
    location = django_filters.CharFilter(
        lookup_expr="icontains",
        label="Location Name",
    )
    start_date = django_filters.DateFilter(
        field_name="start_time",
        lookup_expr="date",
        label="Start Date",
    )
    participating = django_filters.BooleanFilter(
        method="filter_participating",
        label="Events I participate in",
    )
    organizing = django_filters.BooleanFilter(
        method="filter_organizing",
        label="Events I organize",
    )
    ordering = django_filters.OrderingFilter(
        fields=(
            ("start_time", "start_time"),
            ("title", "title"),
            ("location", "location"),
        ),
        field_labels={
            "start_time": "Start time",
            "title": "Title",
            "location": "Location",
        },
        label="Order by",
    )

    class Meta:
        model = Event
        fields = (
            "title",
            "organizer",
            "location",
            "start_date",
            "participating",
            "organizing",
            "ordering",
        )

    def filter_participating(self, queryset, name, value) -> QuerySet:
        """
        Filters events where the current user is a participant.
        """
        if value and self.request.user.is_authenticated:
            return queryset.filter(participants=self.request.user)
        return queryset.none()

    def filter_organizing(self, queryset, name, value) -> QuerySet:
        """
        Filters events where the current user is the organizer.
        """
        if value and self.request.user.is_authenticated:
            return queryset.filter(organizer=self.request.user)
        return queryset.none()
