from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [    
    path('projects/', views.ProjectList.as_view()),
    path('projects/<int:pk>/', views.ProjectDetail.as_view()),
    path('pledges/', views.PledgeList.as_view()),
    path('projects/<int:pk>/delete/', views.ProjectDelete.as_view(), name='project-delete'),
    path('pledges/<int:pk>/delete/', views.PledgeDelete.as_view(), name='pledge-delete'),
]

urlpatterns = format_suffix_patterns(urlpatterns)

