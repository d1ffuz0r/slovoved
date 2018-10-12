from django.urls import path

from website import views

urlpatterns = [
    path('', views.IndexView.as_view()),
    path('slovoved/', views.SlovovedView.as_view()),
    path('api/validate/', views.WordValidationView.as_view()),
]
