# Generated by Django 5.1.5 on 2025-05-02 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hsabackend', '0008_job_quote_s3_link_job_quote_sign_pin_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='quote_status',
            field=models.CharField(choices=[('not-created-yet', 'not-created-yet'), ('created', 'created'), ('approved', 'approved'), ('denied', 'denied')], default='not-created-yet', max_length=50),
        ),
    ]
