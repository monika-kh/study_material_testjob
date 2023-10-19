from django.db import models
        
class SummarizedDocument(models.Model):
    original_document = models.FileField(upload_to='documents/')
    summarized_text = models.TextField()
    questions = models.JSONField()
    application_design = models.TextField(default = "")
    image_url = models.URLField(max_length=500, null=True, blank=True)

    
    def __str__(self):
        return self.original_document.name

    