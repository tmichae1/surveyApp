# Generated by Django 3.0.5 on 2021-02-24 19:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0014_auto_20210224_1905'),
    ]

    operations = [
        migrations.RenameField(
            model_name='answer',
            old_name='surevy_token',
            new_name='survey_token',
        ),
    ]
