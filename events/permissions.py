from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOrganizerOrReadOnly(BasePermission):
    """
    Custom permission to allow event organizers to update/delete their own events.
    All users can retrieve event data.
    """

    def has_object_permission(self, request, view, obj) -> bool:
        if request.method in SAFE_METHODS:
            return True
        return obj.organizer == request.user
