# Generated by Django 5.2.1 on 2025-07-05 02:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0003_clubimage_uploader'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clubimage',
            name='alt',
            field=models.CharField(blank=True, help_text='Describe this image for screen reader users and if the image cannot load correctly.', max_length=255, verbose_name='Alternative description'),
        ),
    ]
