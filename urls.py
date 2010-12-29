from django.conf.urls.defaults import *
from django.conf import settings

from django.views.generic.simple import direct_to_template

from account.openid_consumer import PinaxConsumer

from django.contrib import admin
admin.autodiscover()

import os

urlpatterns = patterns('',
    # Main pages.
    url(r'^$', "pages.index.views.index", name="index"),
    url(r'^home/$', "pages.home.views.index", name="home"),
    url(r'^activities/', include('pages.view_activities.urls')),
    url(r'^energy/', include('pages.energy.urls')),
    url(r'^help/', include('pages.help.urls')),
    url(r'^news/', include('pages.news.urls')),
    url(r'^profile/', include('pages.view_profile.urls')),
    url(r'^m/', include('pages.mobile.urls')),
    
    # Component views.
    url(r'^account/cas/login/$', 'components.django_cas.views.login'),
    url(r'^account/cas/logout/$', 'components.django_cas.views.logout'),
    url(r'^avatar/', include('components.makahiki_avatar.urls')),
    url(r'^setup/', include('components.setup_wizard.urls')),
    url(r'^resources/', include('components.resources.urls')),
    url(r'^themes/', include('components.makahiki_themes.urls')),
    
    # 3rd party
    (r'^frontendadmin/', include('frontendadmin.urls')),
    (r'^attachments/', include('attachments.urls')),
    (r'^sentry/', include('sentry.urls')),
    
    # pinax provided
    (r'^account/', include('account.urls')),
    (r'^admin/(.*)', admin.site.root),
    # (r'^notifications/', include('notification.urls')),
)

if settings.SERVE_MEDIA:
    urlpatterns += patterns('',
        (r'^site_media/', include('staticfiles.urls')),
    )
