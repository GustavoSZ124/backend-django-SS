
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from api.views import DocumentView, TranslationView

urlpatterns = [
    path('documents',DocumentView.as_view()),
    path('documents/<int:id>',DocumentView.as_view()),
    path('translations',TranslationView.as_view()),
    path('translations/<int:id>',TranslationView.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)