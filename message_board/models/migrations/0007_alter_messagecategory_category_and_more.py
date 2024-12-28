# Generated by Django 5.1.1 on 2024-12-23 23:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0006_alter_messageboard_message_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messagecategory',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='models.category'),
        ),
        migrations.AlterField(
            model_name='messagecategory',
            name='message',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='models.messageboard'),
        ),
    ]