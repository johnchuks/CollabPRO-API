from django.conf.urls import url
from api import views
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
  url(r'^user/$', views.CreateUserView.as_view(), name="Create"),
  url(r'^profile/$', views.CreateUserProfileView.as_view(), name="Create"),
  url(r'^profile/(?P<pk>[0-9]+)/$', views.UserProfileDetailsView.as_view(), name="Update, Get, Delete")
]

urlpatterns = format_suffix_patterns(urlpatterns)

