from django.contrib.auth.decorators import login_required
from django.template.context_processors import request
from . import models


def notifications(request):
    if request.user.id is not None:
        Notifications = dict()
        Notifications["notifications"] = models.notifications.objects.filter(
            user=request.user
        ).order_by("-created_at")[0:10]
        Notifications["count_notification"] = models.notifications.objects.filter(
            user=request.user, read=False
        ).count
        return Notifications
    else:
        Notifications = dict()
        Notifications["notification"] = ["Nothin to see here"]
        return Notifications
