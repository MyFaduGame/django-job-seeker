from django.urls import path
from . import views
app_name='accounts'

urlpatterns = [
    path('signup/employer/', views.employer_signup, name='employer_signup'),
    path('signup/seeker/', views.jobseeker_signup, name='jobseeker_signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]