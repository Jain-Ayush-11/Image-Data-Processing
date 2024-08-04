from django.urls import path
from core.views import UploadCSVView, OutputCSVView, WebhookView

urlpatterns = [
    path('upload/', UploadCSVView.as_view()),
    path('output/', OutputCSVView.as_view()),
    path('webhook/', WebhookView.as_view(), name='webhook'),
]
