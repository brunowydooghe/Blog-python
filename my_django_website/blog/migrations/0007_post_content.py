# Generated by Django 3.1.1 on 2020-09-24 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20200924_1132'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='content',
            field=models.TextField(default=-1.0),
            preserve_default=False,
        ),
    ]
