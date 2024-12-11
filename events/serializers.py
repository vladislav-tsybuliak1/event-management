from rest_framework import serializers

from events.models import Event


class EventSerializer(serializers.ModelSerializer):
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


class EventListSerializer(EventSerializer):
    start_time = serializers.SerializerMethodField()
    end_time = serializers.SerializerMethodField()

    def get_start_time(self, obj: Event) -> str:
        return obj.start_time.strftime("%d %b %Y %H:%M")

    def get_end_time(self, obj: Event) -> str:
        return obj.end_time.strftime("%d %b %Y %H:%M")
