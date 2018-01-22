from django.conf import settings
from django.contrib.sites.models import Site


def business(request):
    return {
        'business_hours': getattr(settings, 'BUSINESS_HOURS', lambda :'')(),
        'brand': getattr(settings, 'BRAND_NAME', '')
    }


def theme(request):
    if Site._meta.installed:
        site = Site.objects.get_current(request)
        ctx = ({
            "SITE_NAME": site.name,
            "SITE_DOMAIN": site.domain
        })

        return ctx
    return {}