from django.urls import path

from . import views

app_name = 'assistant'
urlpatterns = [
    path('', views.TopView.as_view(), name='top'),
    path('registration/', views.RegistrationView.as_view(), name='registration'),
    path('review/', views.ReviewView.as_view(), name='review'),
    path('review/record/', views.RecordReviewView.as_view(), name='record_review'),
    path('list/', views.RegisterListView.as_view(), name='register_list'),
]
