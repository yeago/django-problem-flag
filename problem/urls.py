from django.conf.urls.defaults import *

urlpatterns = patterns('problem.views',
   url('^problem-flags/(?P<content_type>\d+)/(?P<object_pk>\d+)/add/$','form',name="problem_flag_form"),
   url('^problem-flags/(?P<content_type>\d+)/(?P<object_pk>\d+)/$','flag',name="problem_flag"),
   url('^problem-flags/(?P<content_type>\d+)/(?P<object_pk>\d+)/delete/$','delete',name="problem_flag_delete"),
   url('^problem-flags/(?P<content_type>\d+)/(?P<object_pk>\d+)/resolve/$','resolve',name="problem_flag_resolve"),
   url('^problem-flags/$','list',name="problem_flag_list"),
)

