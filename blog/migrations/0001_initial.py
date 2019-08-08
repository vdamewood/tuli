import datetime
from django.conf import settings
from django.db import migrations, models

import loki.models

class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, unique=True)),
                ('slug', models.SlugField(unique=True)),
                ('created', models.DateField(default=datetime.date.today)),
                ('edited', models.DateField(auto_now=True)),
                ('content', loki.models.ContentField()),
                ('tags', models.ManyToManyField(to='blog.Tag', blank=True)),
            ],
        ),
    ]
