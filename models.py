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
    file = models.FileField(upload_to=settings.LOKI_PATH)

    def __str__(self):
        return("{} (id: {})".format(
            self.file.name.replace(settings.LOKI_PATH+'/', ''),
            self.id if self.id != '' else '-',
        ))

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

    def parsed_content(self):
        chunks = str(self.content).split("<loki-")
        converted_chunks = [chunks[0]]
        for chunk in chunks[1:]:
            end = chunk.find('>')

            tokens = chunk[:end].split()
            tagname = tokens[0]

            # TODO: If other replacement tags are developed, implement
            #   a real lookup.
            if tagname != "media":
                replacement = "[Invalid Replacement:loki-{}]".format(tagname)
            else:
                attributes = {}
                for attr in tokens[1:]:
                    key, value = attr.split('=', 1)
                    if value[0] == '"':
                        quote_pos = value[1:].find('"')
                        value = value[1:quote_pos+1]
                    elif value[0] == '\'':
                        quote_pos = value[1:].find('\'')
                        value = value[1:quote_pos+1]
                    attributes[key] = value

                try:
                    media = Media.objects.get(id=attributes['id'])
                except Media.DoesNotExist:
                    replacement = "[Media not found]"
                else:
                    replacement = "<img src=\"{}\">".format(media.file.url)
            converted_chunks.append(replacement + chunk[end+1:])

        return "".join(converted_chunks)

    def __str__(self):
        return format(self.title)
