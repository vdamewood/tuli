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

from datetime import date
from django.db import models
from django.conf import settings

class Media(models.Model):
    IMAGE = 0
    AUDIO = 1
    VIDEO = 2
    type_choices = [
        (IMAGE, "image"),
        (AUDIO, "audio"),
        (VIDEO, "video"),
    ]
    name = models.CharField(max_length=48, db_index=True)
    file = models.FileField(upload_to=settings.LOKI_PATH)
    type = models.SmallIntegerField(choices=type_choices)

    def type_name(self):
        return Media.type_choices[self.type][1]

    def __str__(self):
        return("{} (id: {})".format(
            self.name,
            self.id if self.id is not None else '-'))
    class Meta:
        verbose_name = "medium"
        verbose_name_plural = "media"


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return format(self.name)


class Post(models.Model):
    title = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    created = models.DateField(default=date.today)
    edited = models.DateField(auto_now=True)
    content = models.TextField()
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return format(self.title)
