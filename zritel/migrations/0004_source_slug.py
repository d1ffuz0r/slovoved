# Generated by Django 2.2.4 on 2019-09-10 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zritel', '0003_auto_20190907_1723'),
    ]

    operations = [
        migrations.AddField(
            model_name='source',
            name='slug',
            field=models.CharField(default='', help_text='Путь', max_length=512),
            preserve_default=False,
        ),
    ]
