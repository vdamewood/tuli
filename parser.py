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

from html.parser import HTMLParser as HTMLParser
from django.template import loader
from loki.models import Media

class _CustomTagError(Exception):
    def __init__(self, msg):
        self.message = msg

def _media(attributes, end):
    try:
        media = Media.objects.get(name=attributes['name'])
    except KeyError:
        raise _CustomTagError("Name required in media tag")
    except Media.DoesNotExist:
        raise _CustomTagError("Media not found")
    else:
        tpl = loader.get_template("loki/intext-{}.html".format(media.type_name()))
        ctx = {}
        ctx["src"] = media.file.url
        for attr in ['height', 'width', 'caption']:
            try:
                ctx[attr] = attributes[attr]
            except KeyError:
                pass
        return tpl.render(ctx)

# Some custom tags will not have end tags, or end tags won't matter.
# These all can share a single, null end tag implementation.
def _null_end_tag():
    return ''

_s = {
    "media": _media,
}

_e = {
    "media": _null_end_tag,
}

class LokiParser(HTMLParser):
    def reset(self):
        super(LokiParser, self).reset()
        self._buffer = []
        self._output = None

    def get_output(self):
        if self._output is None:
            self._output = ''.join(self._buffer)
        return self._output

    def _add(self, in_str):
        self._buffer.append(in_str)

    def handle_starttag(self, tag, attrs):
        if tag[:5] == "loki-":
            try:
                self._add(_s[tag[5:]](dict(attrs), False))
            except _CustomTagError as e:
                self._add("[Error: {}]".format(e.message))
        else:
            self._add(self.get_starttag_text())

    def handle_startendtag(self, tag, attrs):
        if tag[:5] == "loki-":
            try:
                self._add(_s[tag[5:]](dict(attrs), True))
            except _CustomTagError as e:
                self._add("[Error: {}]".format(e.message))
        else:
            self._add(self.get_starttag_text())

    def handle_endtag(self, tag):
        if tag[:5] == "loki-":
            try:
                self._add(_e[tag[5:]](dict(attrs)))
            except _CustomTagError as e:
                self._add("[Error: {}]".format(e.message))
        else:
            self._add('</{}>'.format(tag))

    def handle_data(self, data):
        self._add(data)

def convert(in_str):
    p = LokiParser()
    p.feed(in_str)
    p.close()
    return p.get_output()
