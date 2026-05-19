from communication.models import LabAddress
from django.conf import settings

def lab_metadata(request):
    """
    Injects global lab data into every template context.
    """

    # Get the LabAddress object first
    lab_addr_obj = LabAddress.objects.filter(type="Primary").select_related('address').first()

    return {
        'lab_name': settings.LAB_NAME,
        'twitter_handle': settings.TWITTER_NAME,
        'facebook_handle': settings.FACEBOOK_NAME,
        'google_plus_id': settings.GOOGLE_PLUS_ID,
        'actual_address': lab_addr_obj.address if lab_addr_obj else None,
        'api_url': f"{request.scheme}://{request.get_host()}/api/v2/",
    }