from django.urls import path

from . import views

urlpatterns = [

    path ('projects/',views.ProjectListCreateView.as_view()),
    path('projects/<str:uuid>/',views.ProjectRetriveUpdateDestoryView.as_view()),
    path ('assigned-projects/',views.AssignedProjectListCreateView.as_view()),
    path('assigned-projects/<str:uuid>/',views.AssignedProjectRetriveUpdateDestoryView.as_view()),
    path ('tasks/',views.TaskListCreateView.as_view()),
    path('tasks/<str:uuid>/',views.TaskProjectRetriveUpdateDestoryView.as_view()),
    path('create-tasks-ai/<str:uuid>/',views.TaskcreatewithAi.as_view()),

]