#from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import *
from buglist.views import landing, current_datetime, hours_ahead, hello, bug_list, mark_done
#from buglist.views import bug_list, mark_done
#from mysite.views import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^mark_done/(\d*)/$', 'buglist.views.mark_done'),
    url(r'^bug_action/(done|delete|onhold)/(\d*)/$', 'bug_action'),     
    url(r'^onhold_done/(onhold|done)/(on|off)/(\d*)/$', 'onhold_done'),
    url(r'^progress/(\d*)/$', 'progress'),

    url(r'^$', landing),
    url(r'^time/$', current_datetime),
   # unlimited hour adds
   # url(r'^time/plus/\d+/$', hours_ahead),
    
    # limits hour adds to 99 = two digits
    url(r'^time/plus/(\d{1,2})/$', hours_ahead),
   
    url(r'^list/$', bug_list),

    url(r'^hello/$',hello),
   
    # admin
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
