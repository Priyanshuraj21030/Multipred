from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('bmi', views.bmi, name='bmi'),
    path('diabetes', views.diabetes, name='diabetes'),
    path('breastcancer', views.breastcancer, name='breastcancer'),
]