from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.CharField(max_length=255)
    organizer = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="organized_events",
    )
    participants = models.ManyToManyField(
        to=settings.AUTH_USER_MODEL,
        blank=True,
        related_name="participated_events",
    )

    class Meta:
        ordering = ["start_time"]

    def __str__(self) -> str:
        return (
            f"Event '{self.title}' "
            f"({self.start_time.strftime('%d %b %Y %H:%M')}-"
            f"{self.end_time.strftime('%d %b %Y %H:%M')})"
        )

    @staticmethod
    def validate_time_and_location(
        start_time: datetime,
        end_time: datetime,
        location: str,
        error_to_raise: type[Exception],
    ) -> None:
        """
        Validates time and location constraints:
        - Start time must be before end time.
        - Start time must be in the future.
        - No overlapping events at the same location.
        """
        if start_time >= end_time:
            raise error_to_raise(
                "Event starting time must be before its ending time."
            )
        if start_time < now():
            raise error_to_raise("Event starting time must be in the future.")

        overlapping_events = Event.objects.filter(
            location=location, end_time__gt=start_time, start_time__lt=end_time
        )
        if overlapping_events.exists():
            raise error_to_raise(
                f"An event at '{location}' overlaps with this time period."
            )

    def clean(self) -> None:
        Event.validate_time_and_location(
            start_time=self.start_time,
            end_time=self.end_time,
            location=self.location,
            error_to_raise=ValidationError,
        )

    def save(self, *args, **kwargs) -> None:
        self.full_clean()
        super().save(*args, **kwargs)
