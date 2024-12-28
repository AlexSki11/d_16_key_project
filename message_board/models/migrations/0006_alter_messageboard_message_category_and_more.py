# Generated by Django 5.1.1 on 2024-12-23 23:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0005_alter_messagecategory_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messageboard',
            name='message_category',
            field=models.ManyToManyField(through='models.MessageCategory', to='models.category', verbose_name='categories'),
        ),
        migrations.AlterField(
            model_name='messagecategory',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='models.category'),
        ),
    ]
