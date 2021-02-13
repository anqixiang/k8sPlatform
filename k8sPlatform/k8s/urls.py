from django.urls import path,re_path,include
from k8s import views

urlpatterns = [
    re_path('^node/$', views.node, name="node"),
]