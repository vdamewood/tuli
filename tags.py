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

from django.template import loader
from loki.models import Image


class TagNotFound(Exception):
    def __init__(self, tag_name):
        self.tag_name = tag_name


class MissingAttribute(Exception):
    def __init__(self, tag_name, attribute):
        self.tag_name = tag_name
        self.attribute = attribute


class TagError(Exception):
    def __init__(self, tag_name, message):
        self.tag_name = tag_name
        self.message = message

class LinkError(Exception):
    def __init__(self, package, target, message):
        self.package = package
        self.target = target
        self.message = message

class LinkTargetNotFound(Exception):
    def __init__(self, package, target):
        self.package = package
        self.target = target

class Tag:
    def start(self, attributes):
        raise NotImplementedError

    def closed_start(self, attributes):
        raise NotImplementedError

    def end(self):
        raise NotImplementedError


class ClosedTag(Tag):
    def closed_start(self, attributes):
        return self.closed_start(attributes)

    def end(self):
        return ''

_link_list = {}

class LinkTag(Tag):
    def _get_link(self, target_str):
        global _link_list
        pkg, target = target_str.split(":", 1)
        return _link_list[pkg](target)
    def start(self, attributes):
        try:
            target = self._get_link(attributes['target'])
        except LinkTargetNotFound as e:
            return "[Link target {}:{} not found.]".format(e.package, e.target)
        except LinkError as e:
            return "[Link error in package {} for target {}: {}]" \
                .format(e.package, e.target, e.message)
        else:
            return '<a href="{}">'.format(target['url'])
    def closed_start(self, attributes):
        try:
            target = self._get_link(attributes['target'])
        except LinkTargetNotFound as e:
            return "[Link target {}:{} not found.]".format(e.package, e.target)
        except LinkError as e:
            return "[Link error in package {} for target {}: {}]" \
                .format(e.package, e.target, e.message)
        else:
            return '<a href="{}">{}</a>'.format(target['url'], target['title'])
    def end(self):
        return '</a>'


class ImageTag(ClosedTag):
    def start(self, attributes):
        try:
            image = Image.objects.get(lookup=attributes['lookup'])
        except KeyError:
            raise MissingAttribute('image', 'lookup')
        except Image.DoesNotExist:
            raise TagError('image',
                "Image \"{}\" not found".format(attributes['lookup']))
        else:
            tpl = loader.get_template('loki/image.html')
            ctx = {}
            ctx['files'] = image.imagefile_set.order_by('sequence')
            try:
                ctx['caption'] = attributes['caption']
            except KeyError:
                pass
            return tpl.render(ctx)

_tag_list = {
    'image': ImageTag(),
    'link': LinkTag(),
}

def tag(tag_name):
    try:
        return _tag_list[tag_name]
    except KeyError:
        raise TagNotFoundError(tag_name)

def register_link(name, callback):
    _link_list[name] = callback
