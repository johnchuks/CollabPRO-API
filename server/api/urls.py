from django.conf.urls import url
from api import views
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_jwt.views import obtain_jwt_token


urlpatterns = [
    url(r'^auth/token/$', obtain_jwt_token),
    url(r'^user/$', views.CreateUserView.as_view(), name="create_user"),
    url(r'^login/$', views.LoginView.as_view(), name="login_user"),
    url(r'^profile/$', views.CreateUserProfileView.as_view(), name="create_userprofile"),
    url(r'^skill/$', views.CreateSkillSetView.as_view(), name="create_skill"),
    url(r'^project/$', views.CreateProjectView.as_view(), name="create_project"),
    url(r'^team/$', views.CreateTeamView.as_view(), name="create_team"),
    url(r'^profile/(?P<pk>[0-9]+)/$',
        views.UserProfileDetailsView.as_view(), name="update_get_delete_userprofile"),
    url(r'^skill/(?P<pk>[0-9]+)/$',
        views.SkillSetDetailsView.as_view(), name="update_get_delete_skill"),
    url(r'^project/(?P<pk>[0-9]+)/$',
        views.ProjectDetailsView.as_view(), name='update_get_delete_project'),
    url(r'^team/(?P<pk>[0-9]+)/$',
        views.TeamDetailsView.as_view(), name='update_get_delete_team')

]

urlpatterns = format_suffix_patterns(urlpatterns)
