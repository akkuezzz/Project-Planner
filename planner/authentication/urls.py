from django.urls import path

from . import views

urlpatterns = [
    
    # path('login/', obtain_auth_token),

    path('login/', views.LoginView.as_view()),

    path('register/',views.RegisterView.as_view())


]