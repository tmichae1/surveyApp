# Generated by Django 3.0.5 on 2021-02-24 19:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0017_remove_answer_surevy_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='survey_token',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='questionnaire.SurveyToken'),
            preserve_default=False,
        ),
    ]
