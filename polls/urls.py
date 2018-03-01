from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('create/', views.create_question, name='create'),
    # path('<int:pk>/delete/', views.QuestionDelete.as_view(), name='delete'),
    path('<int:question_id>/delete/', views.delete_question, name='delete'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('my_polls/', views.my_polls, name='my_polls'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]