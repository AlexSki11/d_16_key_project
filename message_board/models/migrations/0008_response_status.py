# Generated by Django 5.1.1 on 2024-12-26 01:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0007_alter_messagecategory_category_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='response',
            name='status',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]