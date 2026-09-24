from django.conf import settings


def support(request):
    """Expose only a configured support number, never a hardcoded contact."""
    number = str(settings.WHATSAPP_SUPPORT_NUMBER).strip()
    valid = number.isascii() and number.isdigit() and 7 <= len(number) <= 15
    return {'whatsapp_support_number': number if valid else ''}
