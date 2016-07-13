
import pytz
import tzlocal

from django.utils import timezone

class TimezoneMiddleware(object):
    def process_request(self, request):
        tz=str(tzlocal.get_localzone().zone)
        timezone.activate(pytz.timezone(tz))
