from django.urls import path
from recommendation import views

app_name='recommendation'

urlpatterns=[
    path('',views.index,name='index'),
]
