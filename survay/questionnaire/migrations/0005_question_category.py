# Generated by Django 3.0.5 on 2021-02-18 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0004_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='category',
            field=models.CharField(default=0, max_length=40),
            preserve_default=False,
        ),
    ]