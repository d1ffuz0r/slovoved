from django.urls import path

from website import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('slovoved/', views.SlovovedView.as_view(), name='slovoved'),
    path('weboved/', views.WebovedView.as_view(), name='weboved'),
    path('saitoved/', views.SaitovedView.as_view(), name='saitoved-sources'),
    path('saitoved/<slug:slug>/', views.RecordsView.as_view(), name='saitoved-records'),
    path('api/validate/', views.WordValidationView.as_view()),
    path('api/loadurl/', views.LoadUrlView.as_view()),
]
