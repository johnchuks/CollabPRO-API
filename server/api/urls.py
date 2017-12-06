from django.conf.urls import url
from api import views
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_jwt.views import obtain_jwt_token


urlpatterns = [
    url(r'^auth/token/$', obtain_jwt_token),
    url(r'^user/$', views.CreateUserView.as_view(), name="Create User"),
    url(r'^profile/$', views.CreateUserProfileView.as_view(), name="Create Skill"),
    url(r'^skill/$', views.CreateSkillSetView.as_view(), name="Create Skill"),
    url(r'^project/$', views.CreateProjectView.as_view(), name="Create Project"),
    url(r'^team/$', views.CreateTeamView.as_view(), name="Create Team"),
    url(r'^profile/(?P<pk>[0-9]+)/$',
        views.UserProfileDetailsView.as_view(), name="Update, Get, Delete"),
    url(r'^skill/(?P<pk>[0-9]+)/$',
        views.SkillSetDetailsView.as_view(), name="Get"),
    url(r'^project/(?P<pk>[0-9]+)/$',
        views.ProjectDetailsView.as_view(), name='Update, Get and Delete'),
    url(r'^team/(?P<pk>[0-9]+)/$',
        views.TeamDetailsView.as_view(), name='Update, Get and Delete')

]

urlpatterns = format_suffix_patterns(urlpatterns)
