from django.urls import path

from . import views

app_name = 'remoteshifts'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<slug:pk>/shifts/', views.UserDetailView.as_view(), name='user_shifts'),
    path('<slug:uid>/shifts/fixed/create/', views.FixedRemoteShiftCreateView.as_view(), name='fixed_shift_create'),
    path('<slug:uid>/shifts/fixed/<int:pk>/', views.FixedRemoteShiftUpdateView.as_view(), name='fixed_shift_update'),
    path('<slug:uid>/shifts/fixed/<int:pk>/delete/', views.FixedRemoteShiftDeleteView.as_view(), name='fixed_shift_delete'),
    path('<slug:uid>/shifts/scheduled/create/', views.ScheduledRemoteShiftCreateView.as_view(), name='scheduled_shift_create'),
    path('<slug:uid>/shifts/scheduled/<int:pk>/', views.ScheduledRemoteShiftUpdateView.as_view(), name='scheduled_shift_update'),
]
