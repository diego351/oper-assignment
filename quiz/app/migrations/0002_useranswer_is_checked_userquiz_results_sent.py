# Generated by Django 4.2.3 on 2023-07-08 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='useranswer',
            name='is_checked',
            field=models.BooleanField(null=True),
        ),
        migrations.AddField(
            model_name='userquiz',
            name='results_sent',
            field=models.BooleanField(default=False),
        ),
    ]