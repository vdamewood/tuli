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

from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.urls import reverse

_licenses = [
    ('BSD(2C)', '2-clause BSD License',
        'https://opensource.org/licenses/BSD-2-Clause'),
    ('BSD(3C)', '3-clause BSD License',
        'https://opensource.org/licenses/BSD-3-Clause'),
    ('MIT', 'MIT License',
        'https://opensource.org/licenses/MIT'),
    ('ISC', 'ISC License',
        'https://opensource.org/licenses/ISC'),
    ('zlib', 'zlib/libpng License',
        'https://opensource.org/licenses/Zlib'),
    ('APL2', 'Apache License version 2.0',
        'http://apache.org/licenses/LICENSE-2.0'),
    ('MPL2', 'Mozilla Public License version 2.0',
        'https://www.mozilla.org/en-US/MPL/2.0/'),
    ('LGPLv2.1', 'GNU Lesser General Public License version 2.1',
        'https://www.gnu.org/licenses/lgpl-2.1.html'),
    ('LGPLv2.1+', 'GNU Lesser General Public License version 2.1 or later',
        'https://www.gnu.org/licenses/lgpl-2.1.html'),
    ('LGPLv3', 'GNU Lesser General Public License version 3.0',
        'https://www.gnu.org/licenses/lgpl-3.0.en.html'),
    ('LGPLv3+', 'GNU Lesser General Public License version 3.0 or later',
        'https://www.gnu.org/licenses/lgpl-3.0.en.html'),
    ('GPLv2', 'GNU General Public License version 2.0',
        'https://www.gnu.org/licenses/gpl-2.0.html'),
    ('GPLv2+', 'GNU General Public License version 2.0 or later',
        'https://www.gnu.org/licenses/gpl-2.0.html'),
    ('GPLv3', 'GNU General Public License version 3.0',
        'https://www.gnu.org/licenses/gpl-3.0.html'),
    ('GPLv3+', 'GNU General Public License version 3.0 or later',
        'https://www.gnu.org/licenses/gpl-3.0.html'),
]

_formats = [
    ('7zip Archive', '.7z'),
    ('Debian Package', '.deb'),
    ('macOS Disk Image', '.dmg'),
    ('macOS Package', '.pkg'),
    ('RPM Package', '.rpm'),
    ('Tape Archive', '.tar'),
    ('Tape Archive, gzip-compressed', '.tar.gz'),
    ('Tape Archive, bzip2-compressed', '.tar.bz2'),
    ('Tape Archive, xz-compressed', '.tar.xz'),
    ('Windows Installer', '.msi'),
    ('Zip Archive', '.zip'),
]


def add_default_data(sender, **kwargs):
    License = kwargs['apps'].get_model('swcat', 'License')
    if License.objects.count() == 0:
        for abbreviation, name, url in _licenses:
            new_license = License()
            new_license.name = name
            new_license.abbreviation = abbreviation
            new_license.url = url
            new_license.save()
    Format = kwargs['apps'].get_model('swcat', 'Format')
    if Format.objects.count() == 0:
        for name, suffix in _formats:
            new_format = Format()
            new_format.name = name
            new_format.suffix = suffix
            new_format.save()

def _link_lookup(target):
    kind, slug = target.split(":", 1)
    if kind != 'project':
        from tuli.tags import LinkError
        raise LinkError('swcat', target, "Invalid target type: {}".format(kind))

    try:
        from .models import Project
        my_proj = Project.objects.get(slug=slug)
    except Project.DoesNotExist as e:
        from tuli.tags import LinkTargetNotFound
        raise LinkTargetNotFound('swcat', target)
    else:
        return {
            "url": reverse('tuli-swcat-project', args=(my_proj.slug,)),
            "title": my_proj.name,
        }


class SwcatConfig(AppConfig):
    name = 'tuli.swcat'
    verbose_name = 'Tuli Software Catalog'
    def ready(self):
        post_migrate.connect(add_default_data, sender=self)
        from tuli.tags import register_link
        register_link('swcat', _link_lookup)
