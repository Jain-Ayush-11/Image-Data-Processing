from django.urls import path
from core.views import UploadCSVView

urlpatterns = [
    path('upload/', UploadCSVView.as_view()),
]
