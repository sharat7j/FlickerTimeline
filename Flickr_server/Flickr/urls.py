from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from Flickr import settings

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:`
    # url(r'^$', 'Flickr.views.home', name='home'),
    # url(r'^Flickr/', include('Flickr.foo.urls')),

    url (r'^tagSearch/?$', 'Flickr.views.landing',name='landing' ),
    url(r'^tagSearchTag/?$','Flickr.views.search',name='search'),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    url(r'^admin/',include(admin.site.urls))


    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^tag/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()
if settings.DEBUG:
    urlpatterns += patterns('django.contrib.staticfiles.views',
        url(r'^static/(?P<path>.*)$', 'serve'),
    )
