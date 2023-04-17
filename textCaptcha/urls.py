from django.urls import path

#
from . import views
#

urlpatterns = [
    path('generateCaptcha/', views.generateCaptcha, name='generateCaptcha'),
    path('recognizeCaptcha/', views.recognizeCaptcha, name='recognizeCaptcha'),
]