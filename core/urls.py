from django.urls import path
from core.views import UploadCSVView, OutputCSVView

urlpatterns = [
    path('upload/', UploadCSVView.as_view()),
    path('output/', OutputCSVView.as_view()),
]
