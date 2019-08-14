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

import tuli.models
from . import settings


class License(models.Model):
    name = models.CharField(max_length=55)
    abbreviation = models.CharField(max_length=12)
    url = models.URLField()

    def __str__(self):
        return self.name


class Platform(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Format(models.Model):
    name = models.CharField(max_length=50)
    suffix = models.CharField(max_length=20)

    def __str__(self):
        return ("{} ({})").format(self.name, self.suffix)


class Project(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
    description = models.CharField(max_length=250)
    overview = tuli.models.ContentField()

    def main_component(self):
        try:
            return self._main_component
        except AttributeError:
            try:
                self._main_component = self.component_set.filter(name="")[0]
            except IndexError:
                self._main_component = None
            return self._main_component

    def components(self):
        return self.component_set.filter(~models.Q(name=''))

    def __str__(self):
        return self.name


class Component(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=True)
    slug = models.SlugField(max_length=50, blank=True)
    description = models.CharField(max_length=250, blank=True)
    repo = models.URLField(blank=True)
    tracker = models.URLField(blank=True)
    license = models.ForeignKey(License, null=True, on_delete=models.PROTECT)

    def latest(self):
        try:
            return self._latest
        except AttributeError:
            try:
                self._latest = self.release_set.filter(prerelease="").order_by('major', 'minor', 'patch')[0]
            except IndexError:
                self._latest = None
            return self._latest

    def __str__(self):
        return ("{}: {}").format(self.project.name, self.name
            if self.name != ""
            else "[*]")

    class Meta:
        unique_together = ('project', 'name')


class Release(models.Model):
    component = models.ForeignKey(Component, on_delete=models.CASCADE)
    date = models.DateField(default=date.today)
    major = models.IntegerField()
    minor = models.IntegerField()
    patch = models.IntegerField()
    prerelease = models.CharField(max_length=20, blank=True)
    revoked = models.BooleanField(default=False)

    def version(self):
        return ("{}.{}.{}{}").format(self.major, self.minor, self.patch, self.prerelease)

    def __str__(self):
        return ("{} v{}.{}.{}{}").format(self.component, self.major, self.minor, self.patch, self.prerelease)

def upload(inst, filename):
    return "{}/{}{}/v{}/{}".format(
        settings.TULI_SWCAT_DIR,
        inst.release.component.project.slug,
        ''  if inst.release.component.slug == ''
            else "/{}".format(inst.release.component.slug),
        inst.release.version(),
        filename)

# These are here to avoid a migration if upload
# # needs to diverge for source and binary packages.
upload_source = upload
upload_binary = upload

class SourcePackage(models.Model):
    release = models.ForeignKey(Release, on_delete=models.CASCADE)
    format = models.ForeignKey(Format, on_delete=models.PROTECT)
    file = models.FileField(upload_to=upload_source)

class BinaryPackage(models.Model):
    release = models.ForeignKey(Release, on_delete=models.CASCADE)
    platform = models.ForeignKey(Platform, on_delete=models.PROTECT)
    format = models.ForeignKey(Format, on_delete=models.PROTECT)
    file = models.FileField(upload_to=upload_binary)
