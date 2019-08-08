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

from django.contrib import admin
from . import models

admin.site.register(models.License)
admin.site.register(models.Platform)
admin.site.register(models.Format)

class ComponentInline(admin.StackedInline):
    prepopulated_fields = {"slug": ("name",)}
    model = models.Component

@admin.register(models.Project)
class ProjectAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ComponentInline]


class SourcePackageInline(admin.TabularInline):
    fields = ('format', 'filename')
    model = models.SourcePackage

class BinaryPackageInline(admin.TabularInline):
    fields = ('format', 'platform', 'filename')
    model = models.BinaryPackage

class SupportPackageInline(admin.TabularInline):
    fields = ('format', 'description', 'filename')
    model = models.SupportPackage


@admin.register(models.Release)
class ReleaseAdmin(admin.ModelAdmin):
    inlines = [
        SourcePackageInline,
        BinaryPackageInline,
        SupportPackageInline,
    ]
