from django.urls import path
from . import views

app_name='books'

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('<int:book_pk>/detail/', views.detail, name='detail'),
    path('<int:book_pk>/update/', views.update, name='update'),
    path('<int:book_pk>/delete/', views.delete, name='delete'),
    path('<int:book_pk>/thread_create/', views.thread_create, name='thread_create'),
    path('<int:thread_pk>/thread_detail/', views.thread_detail, name='thread_detail'),
    path('<int:book_pk>/thread_update/<int:thread_pk>/', views.thread_update, name='thread_update'),
    path('<int:book_pk>/thread_delete/<int:thread_pk>/', views.thread_delete, name='thread_delete'),
    path('<int:thread_pk>/like/', views.like, name='like'),
] 
