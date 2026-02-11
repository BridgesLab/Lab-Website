from communication.models import LabAddress
from django.conf import settings

def lab_metadata(request):
    """
    Injects global lab data into every template context.
    """
    return {
        'lab_name': settings.LAB_NAME,
        'twitter_handle': settings.TWITTER_NAME,
        'facebook_handle': settings.FACEBOOK_NAME,
        'google_plus_id': settings.GOOGLE_PLUS_ID,
        'lab_address': LabAddress.objects.filter(type="Primary").first(),
    }