# Generated by Django 4.2.6 on 2023-10-18 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training_materials', '0002_summarizeddocument_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='summarizeddocument',
            name='image_url',
            field=models.URLField(blank=True, max_length=500, null=True),
        ),
    ]