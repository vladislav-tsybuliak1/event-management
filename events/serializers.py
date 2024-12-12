from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from events.models import Event


class EventSerializer(serializers.ModelSerializer):
    organizer = serializers.CharField(
        source="organizer.username",
        read_only=True,
    )
    participants = serializers.IntegerField(
        source="participants.count",
        read_only=True,
    )
    class Meta:
        model = Event
        fields = (
            "id",
            "title",
            "description",
            "start_time",
            "end_time",
            "location",
            "organizer",
            "participants",
        )
        read_only_fields = (
            "id",
            "organizer",
            "participants",
        )


class EventListSerializer(EventSerializer):
    start_time = serializers.SerializerMethodField()
    end_time = serializers.SerializerMethodField()

    def get_start_time(self, obj: Event) -> str:
        return obj.start_time.strftime("%d %b %Y %H:%M")

    def get_end_time(self, obj: Event) -> str:
        return obj.end_time.strftime("%d %b %Y %H:%M")


class EventCreateUpdateSerializer(EventSerializer):
    def validate(self, attrs: dict) -> dict:
        data = super().validate(attrs=attrs)
        Event.validate_time_and_location(
            start_time=attrs.get(
                "start_time",
                self.instance.start_time if self.instance else None,
            ),
            end_time=attrs.get(
                "end_time",
                self.instance.end_time if self.instance else None,
            ),
            location=attrs.get(
                "location",
                self.instance.location if self.instance else None,
            ),
            error_to_raise=ValidationError,
            current_event_id=self.instance.pk if self.instance else None,
        )
        return data
