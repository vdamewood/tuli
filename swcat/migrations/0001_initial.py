# Copyright 2019 Vincent Damewood
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime
from django.db import migrations, models
import django.db.models.deletion

import loki.models

class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='License',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=55)),
                ('abbreviation', models.CharField(max_length=12)),
                ('url', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Platform',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('separator', models.CharField(default='-', max_length=1)),
                ('filename', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Format',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('suffix', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('slug', models.SlugField()),
                ('description', models.CharField(max_length=250)),
                ('overview', loki.models.ContentField()),
            ],
        ),
        migrations.CreateModel(
            name='Component',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='swcat.Project')),
                ('name', models.CharField(max_length=50, blank=True)),
                ('slug', models.SlugField(blank=True)),
                ('description', models.CharField(blank=True, max_length=250)),
                ('repo', models.URLField(blank=True)),
                ('tracker', models.URLField(blank=True)),
                ('license', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='swcat.License')),
            ],
        ),
        migrations.CreateModel(
            name='Release',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('component', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='swcat.Component')),
                ('date', models.DateField(default=datetime.date.today)),
                ('major', models.IntegerField()),
                ('minor', models.IntegerField()),
                ('patch', models.IntegerField()),
                ('prerelease', models.CharField(blank=True, max_length=20)),
                ('revoked', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='SourcePackage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to=loki.swcat.models.upload)),
                ('release', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='swcat.Release')),
                ('format', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='swcat.Format')),
            ],
        ),
        migrations.CreateModel(
            name='BinaryPackage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to=loki.swcat.models.upload)),
                ('release', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='swcat.Release')),
                ('platform', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='swcat.Platform')),
                ('format', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='swcat.Format')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='component',
            unique_together={('project', 'name')},
        )
    ]
