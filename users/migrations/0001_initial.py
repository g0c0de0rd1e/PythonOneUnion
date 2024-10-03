# Generated by Django 3.2.10 on 2024-10-03 21:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feedback_name', models.CharField(max_length=50, verbose_name='Имя покупателя')),
                ('feedback_email', models.EmailField(max_length=254, verbose_name='Почта покупателя')),
                ('feedback_message', models.TextField(verbose_name='Текст')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
            ],
            options={
                'verbose_name': 'Обратная связь покупателя',
                'verbose_name_plural': 'Обратная связь покупателя',
            },
        ),
    ]
