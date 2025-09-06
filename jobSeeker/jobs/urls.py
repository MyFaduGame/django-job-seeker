from django.urls import path
from . import views

app_name = 'jobs'

urlpatterns = [
    path('employer/dashboard/', views.employer_dashboard, name='employer_dashboard'),
    path('employer/job/create/', views.create_job, name='create_job'),
    path('employer/job/<uuid:pk>/edit/', views.edit_job, name='edit_job'),
    path('employer/job/<uuid:job_pk>/applications/', views.view_applications, name='view_applications'),
    path('employer/application/<int:app_pk>/status/', views.change_application_status, name='change_application_status'),

    path('', views.job_list, name='list'),
    path('job/<uuid:pk>/<slug:slug>/', views.job_detail, name='detail'),
    path('job/<uuid:pk>/apply/', views.apply_job, name='apply'),
    path('my/applications/', views.my_applications, name='my_applications'),
]
