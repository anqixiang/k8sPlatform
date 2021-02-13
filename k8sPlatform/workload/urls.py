from django.urls import path,re_path,include
from workload import views

urlpatterns = [
    re_path('^deployment/$', views.deployment, name="deployment"),
]