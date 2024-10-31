# Generated by Django 5.1.1 on 2024-10-30 12:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0004_remove_messageboard_responses'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messagecategory',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='MessageCategory', to='models.category'),
        ),
        migrations.AlterField(
            model_name='response',
            name='message',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='MessageResponse', to='models.messageboard'),
        ),
    ]