# serializers.py
from rest_framework import serializers
from .models import SummarizedDocument


class SummarizedDocumentSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField(method_name="get_title")

    class Meta:
        model = SummarizedDocument
        fields = ("id", "title", "original_document", "summarized_text", "questions", "image_url", "application_design")

    def get_title(self, instance):
        return (
            instance.original_document.name.split("/")[1]
            .replace("_", " ")
            .replace(".pdf", "")
        )
