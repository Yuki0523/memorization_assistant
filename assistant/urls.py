from django.urls import path

from . import views

app_name = 'assistant'
urlpatterns = [
    path('', views.TopView.as_view(), name='top'),
    path('registration/', views.RegistrationView.as_view(), name='registration'),
    path('review/', views.ReviewView.as_view(), name='review'),
    path('review/create_record/', views.CreateReviewRecordView.as_view(), name='create_review_record'),
    path('register/list/', views.RegisterListView.as_view(), name='register_list'),
    path('register/<int:pk>/detail/', views.RegisterDetailView.as_view(), name='register_detail'),
    path('register/<int:pk>/update/', views.UpdateRegisterView.as_view(), name='update_register'),
    path('register/<int:pk>/delete/', views.DeleteRegisterView.as_view(), name='delete_register'),
    path('review_record/<int:pk>/update/', views.UpdateReviewRecordView.as_view(),
         name='update_review_record'),
    path('review_record/<int:pk>/delete/', views.DeleteReviewRecordView.as_view(),
         name='delete_review_record'),
]
