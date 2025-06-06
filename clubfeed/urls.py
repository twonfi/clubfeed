from django.contrib import admin
from django.urls import path, include
from allauth.account.decorators import secure_admin_login

admin.autodiscover()
admin.site.login = secure_admin_login(admin.site.login)

urlpatterns = [
    path('admin/', admin.site.urls),

    # allauth
    path('accounts/', include('allauth.urls')),

    # ClubFeed
    path('clubs/',
        include('viewer.urls')),
    path('create/', include('creator.urls')),
    path('', include('home.urls'))
]

# Error handlers
handler404 = 'core.views.handler_404'
