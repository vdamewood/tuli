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

class Image(models.Model):
    lookup = models.CharField(max_length=48, db_index=True)

    def __str__(self):
        return(self.lookup)

class ImageFile(models.Model):
    image = models.ForeignKey(Image, models.CASCADE)
    file = models.ImageField(upload_to=settings.LOKI_PATH, height_field="height", width_field="width")
    height = models.PositiveSmallIntegerField()
    width = models.PositiveSmallIntegerField()

    def url(self):
        return self.file.url

    class Meta:
        get_latest_by = ('image', '-width', '-height')

class Content:
    def __init__(self, raw):
        self._raw = raw
        self._parsed = None
        self._plain = None
    def parse(self):
        if self._parsed is None:
            from .parser import LokiParser
            p = LokiParser()
            p.feed(self._raw)
            p.close()
            self._parsed = p.get_output()
        return self._parsed
    def plain(self):
        raise NotImplementedError()
    def __str__(self):
        return self._raw

class ContentField(models.TextField):
    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        elif isinstance(value, str):
            return Content(value)
        else:
            raise TypeError()
    def to_python(self, value):
        if isinstance(value, Content) or value is None:
            return value
        elif isinstance(value, str):
            return Content(value)
        else:
            raise TypeError()
    def get_prep_value(self, value):
        if isinstance(value, Content):
            return str(value)
        elif isinstance(value, str) or value is None:
            return value
        else:
            raise TypeError("Type {} not supported.".format(type(value)))
