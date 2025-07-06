from django.conf import settings


# noinspection PyUnusedLocal
def noindex_context(request) -> dict[str, bool]:
    return {"NOINDEX": settings.NOINDEX}
