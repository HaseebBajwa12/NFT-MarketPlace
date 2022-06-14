# Generated by Django 4.0 on 2022-02-08 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EmailTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('forgot-password', 'Forgot Password'), ('user-activation', 'User Activation'), ('activation-confirmation', 'Activation Confirmation')], max_length=100)),
                ('subject', models.CharField(max_length=250)),
                ('body', models.TextField()),
            ],
        ),
    ]