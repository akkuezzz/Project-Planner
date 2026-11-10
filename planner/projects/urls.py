from django.urls import path

from . import views

urlpatterns = [

    path ('projects/',views.ProjectListCreateView.as_view()),

    path('projects/<str:uuid>/',views.ProjectRetriveUpdateDestoryView.as_view())
    

]