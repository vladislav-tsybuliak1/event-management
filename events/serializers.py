from rest_framework import serializers

from events.models import Event


class EventSerializer(serializers.ModelSerializer):
    organizer = serializers.CharField(
        source="organizer.username",
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
        )
        read_only_fields = (
            "id",
            "organizer",
        )


class EventListSerializer(EventSerializer):
    start_time = serializers.SerializerMethodField()
    end_time = serializers.SerializerMethodField()

    def get_start_time(self, obj: Event) -> str:
        return obj.start_time.strftime("%d %b %Y %H:%M")

    def get_end_time(self, obj: Event) -> str:
        return obj.end_time.strftime("%d %b %Y %H:%M")
