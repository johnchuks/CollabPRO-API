from django.conf.urls import url
from user_profile import views

urlpatterns = [
  url(r'^$', views.index, name='index')
]
