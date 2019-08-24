# Generated by Django 2.2.4 on 2019-08-23 06:41

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Название источника', max_length=512)),
                ('kind', models.CharField(choices=[('vk', 'ВКонтакте')], max_length=36)),
                ('url', models.URLField(help_text='Ссылка')),
                ('active', models.BooleanField(default=True)),
                ('last_check_at', models.DateTimeField(blank=True, help_text='Время последней проверки', null=True)),
                ('frequency', models.PositiveIntegerField(help_text='Частота Проверок')),
            ],
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_at', models.DateTimeField(auto_created=True, auto_now_add=True)),
                ('url', models.URLField(help_text='Ссылка на текст')),
                ('text', models.TextField(help_text='Текст')),
                ('report', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict)),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='zritel.Source')),
            ],
        ),
    ]
