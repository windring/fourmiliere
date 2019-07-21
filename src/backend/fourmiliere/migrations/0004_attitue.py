# Generated by Django 2.2 on 2019-07-20 18:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fourmiliere', '0003_post'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attitue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attitude', models.IntegerField()),
                ('pid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fourmiliere.Post')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]