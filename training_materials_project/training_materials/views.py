from django.conf import settings
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .models import SummarizedDocument
from .serializers import SummarizedDocumentSerializer
from rest_framework import status
from .utils import (
    generate_questions,
    get_summary,
    get_image,
    count_pdf_pages,
    generate_system_design,
    generate_application
)

class PDFSummaryAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)    
    
    def post(self, request):
        pdf_file = request.data["pdf_file"]
        try:
            pages = count_pdf_pages(pdf_file)
            summary = get_summary(pdf_file, pages)
            system_design_text = generate_system_design(summary)

            questions = generate_questions(summary)
            
            image = get_image(summary)
            app = generate_application(summary)
            summarized_doc = SummarizedDocument(
                original_document=pdf_file,
                summarized_text=system_design_text,
                questions=questions,
                image_url=image,
                application_design=app
            )
            summarized_doc.save()

            serializer = SummarizedDocumentSerializer(summarized_doc)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return e

    def get(self, request, pk=None):
        if pk is not None:
            try:
                obj = SummarizedDocument.objects.get(pk=pk)
                serializer = SummarizedDocumentSerializer(obj)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except SummarizedDocument.DoesNotExist:
                return Response(
                    {"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND
                )
        else:
            queryset = SummarizedDocument.objects.all().order_by('-id')
            serializer = SummarizedDocumentSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
