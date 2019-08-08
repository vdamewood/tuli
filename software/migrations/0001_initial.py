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
                ('overview', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Component',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='software.Project')),
                ('name', models.CharField(max_length=50, blank=True)),
                ('slug', models.SlugField(blank=True)),
                ('description', models.CharField(blank=True, max_length=250)),
                ('repo', models.URLField(blank=True)),
                ('tracker', models.URLField(blank=True)),
                ('license', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='software.License')),
            ],
        ),
        migrations.CreateModel(
            name='Release',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('component', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='software.Component')),
                ('date', models.DateField(default=datetime.date.today)),
                ('major', models.IntegerField()),
                ('minor', models.IntegerField()),
                ('patch', models.IntegerField()),
                ('prerelease', models.CharField(blank=True, max_length=20)),
                ('revoked', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Download',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='SourcePackage',
            fields=[
                ('download_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='software.Download')),
                ('release', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='software.Release')),
                ('format', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='software.Format')),
            ],
            bases=('software.Download',),
        ),
        migrations.CreateModel(
            name='BinaryPackage',
            fields=[
                ('download_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='software.Download')),
                ('release', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='software.Release')),
                ('platform', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='software.Platform')),
                ('format', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='software.Format')),
            ],
            bases=('software.Download',),
        ),
        migrations.CreateModel(
            name='SupportPackage',
            fields=[
                ('download_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='software.Download')),
                ('description', models.CharField(max_length=250)),
                ('format', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='software.Format')),
                ('release', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='software.Release')),
            ],
            bases=('software.download',),
        ),
        migrations.AlterUniqueTogether(
            name='component',
            unique_together={('project', 'name')},
        )
    ]
