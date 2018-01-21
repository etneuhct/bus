from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from authentification.views import GoogleOauth
from authentification.views import GoogleOauthFailed
from authentification.views import GoogleOauthSucceed
from profiles.views import SignupView
from . import views


urlpatterns = [
    url(r'^$', views.HomePage.as_view(), name='home'),
    url(r'^about/$', views.AboutPage.as_view(), name='about'),
    url(r'^users/', include('profiles.urls', namespace='profiles')),
    url(r'^admin/', include(admin.site.urls)),
    url(r"^account/signup/$", SignupView.as_view(), name="account_signup"),
    # redirect unneeded/unused social accounts page to settings page
    url(r"account/social/accounts/", RedirectView.as_view(url='/account/settings/')),
    url(r"^account/", include("account.urls")),
    url(r"^connexion/oauth", GoogleOauth.as_view(), name='google_oauth'),
    url(r"^connexion/success", GoogleOauthSucceed.as_view(), name='google_oauth'),
    url(r"^connexion/fail", GoogleOauthFailed.as_view(), name='google_oauth')
]

# User-uploaded files like profile pics need to be served in development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Include django debug toolbar if DEBUG is on
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
