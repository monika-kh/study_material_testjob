from django.urls import path
from .views import PDFSummaryAPIView



urlpatterns = [
    # Other URL patterns
    path('generate_summary/', PDFSummaryAPIView.as_view(), name='generate_summary'),
    # path('get_summary_list/', PDFSummaryAPIView.as_view(), name='get_summary_list'),
    # path('get_summary/<int:pk>', PDFSummaryAPIView.as_view(), name='get_summary')
    
]
