# Generated by Django 3.0.5 on 2021-02-19 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0006_remove_question_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='category',
            field=models.CharField(default=0, max_length=50),
            preserve_default=False,
        ),
    ]
