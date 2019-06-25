import datetime
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=48, db_index=True)),
                ('file', models.FileField(upload_to=settings.LOKI_PATH)),
                ('type', models.SmallIntegerField(choices=[(0, 'image'), (1, 'audio'), (2, 'video')])),
            ],
            options={'verbose_name': 'medium', 'verbose_name_plural': 'media'},
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
                ('content', models.TextField()),
                ('tags', models.ManyToManyField(to='loki.Tag', blank=True)),
            ],
        ),
    ]
