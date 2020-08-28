from django.urls import path

from . import views

app_name = 'assistant'
urlpatterns = [
    path('', views.TopView.as_view(), name='top'),
    path('registration/', views.RegistrationView.as_view(), name='registration'),
    path('review/', views.ReviewView.as_view(), name='review'),
    path('review/record/', views.RecordReviewView.as_view(), name='record_review'),
    path('list/', views.RegisterListView.as_view(), name='register_list'),
    path('list/<int:pk>/', views.RegisterDetailView.as_view(), name='register_detail'),
    path('list/<int:pk>/update/', views.RegisterUpdateView.as_view(), name='register_update'),
    path('list/<int:pk>/update/delete', views.RegisterDeleteView.as_view(), name='register_delete'),
    path('list/review_record/<int:pk>/update/', views.ReviewRecordUpdateView.as_view(), name='review_record_update'),
    path('list/review_record/<int:pk>/update/delete', views.ReviewRecordDeleteView.as_view(), name='review_record_delete'),
]
