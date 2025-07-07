from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sites.shortcuts import get_current_site
from django.db.utils import OperationalError
from django.views.i18n import JavaScriptCatalog
from allauth.account.decorators import secure_admin_login

try:
    site = get_current_site(None)
    admin.site.site_header = f"{site.name} administration"
    admin.site.site_title = f"{site.name} site admin"
except OperationalError:
    pass

admin.autodiscover()
admin.site.login = secure_admin_login(admin.site.login)

urlpatterns = [
    path("admin/", admin.site.urls),
    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    re_path(r"^comments/", include('django_comments_xtd.urls')),
    # tz_detect
    path("_tz_detect/", include("tz_detect.urls")),
    # avatar
    path("avatar/", include("avatar.urls")),
    # allauth
    path("accounts/", include("allauth.urls")),
    # martor
    path("_martor/", include("martor.urls")),
    # ClubFeed
    path("clubs/", include("clubs.urls")),
    path("create/", include("creator.urls")),
    path("users/", include("users.urls")),
    path("", include("home.urls")),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )

# Error handlers
handler404 = "core.views.handler_404"
