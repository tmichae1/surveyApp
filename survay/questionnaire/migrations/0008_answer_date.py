# Generated by Django 3.0.5 on 2021-02-20 00:08

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0007_question_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
