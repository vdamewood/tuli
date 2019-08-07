import datetime
from django.conf import settings
from django.db import migrations, models

import loki.blog.models

class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lookup', models.CharField(db_index=True, max_length=48)),
            ],
        ),
        migrations.CreateModel(
            name='ImageFile',
            options={
                'unique_together': {('image', 'sequence')},
                'get_latest_by': ('image', 'sequence'),
            },
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to=settings.LOKI_PATH)),
                ('width', models.SmallIntegerField()),
                ('image', models.ForeignKey(on_delete=models.deletion.CASCADE, to='blog.Image')),
                ('sequence', models.SmallIntegerField()),
            ],
        ),
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
                ('content', loki.blog.models.ContentField()),
                ('tags', models.ManyToManyField(to='blog.Tag', blank=True)),
            ],
        ),
    ]
