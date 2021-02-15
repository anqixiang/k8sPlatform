from django.urls import path,re_path,include
from workload import views

urlpatterns = [
    re_path('^deployment/$', views.deployment, name="deployment"),
    re_path('^deployment_api/$', views.deployment_api, name="deployment_api"),
    re_path('^daemonset/$', views.daemonset, name="daemonset"),
    re_path('^daemonset_api/$', views.daemonset_api, name="daemonset_api"),
]