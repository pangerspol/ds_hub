# Generated by Django 5.1.4 on 2025-02-18 00:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_client_folder_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='client',
            old_name='folder_id',
            new_name='expense_folder_id',
        ),
        migrations.AddField(
            model_name='client',
            name='lexviamail_folder_id',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name='client',
            name='main_folder_id',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]
