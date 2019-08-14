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
from . import tags
from django.conf import settings


tag_prefix = '{}-'.format(settings.TULI_TAG_PREFIX
    if hasattr(settings, 'TULI_TAG_PREFIX')
    else 'tuli')
prefix_len = len(tag_prefix)

def _should_catch(tag):
    global tag_prefix, prefix_len
    return tag[:prefix_len] == tag_prefix

class TuliParser(HTMLParser):

    def reset(self):
        super().reset()
        self._buffer = []
        self._output = None

    def get_output(self):
        if self._output is None:
            self._output = ''.join(self._buffer)
        return self._output

    def _add(self, in_str):
        self._buffer.append(in_str)

    def handle_starttag(self, tag, attrs):
        if _should_catch(tag):
            try:
                self._add(tags.tag(tag[5:]).start(dict(attrs)))
            except tags.TagNotFound as e:
                self._add("[Tag not found: {}]".format(
                    e.tag_name))
            except tags.MissingAttribute as e:
                self._add("[Missing attribute ({}) in {} tag.]".format(
                    e.attribute,
                    e.tag_name))
            except tags.TagError as e:
                self._add("[Error in {} tag: {}]".format(
                    e.tag_name,
                    e.message))
            except Exception as e:
                self._add("Unexpected error: {}: {}".format(str(type(e)), e))
        else:
            self._add(self.get_starttag_text())

    def handle_startendtag(self, tag, attrs):
        if _should_catch(tag):
            try:
                self._add(tags.tag(tag[5:]).closed_start(dict(attrs)))
            except tags.TagNotFound as e:
                self._add("[Unknown Tag: {}]".format(
                    e.tag_name))
            except tags.MissingAttribute as e:
                self._add("[Missing attribute ({}) in {} tag.]".format(
                    e.attribute,
                    e.tag_name))
            except tags.TagError as e:
                self._add("[Error in {} tag: {}]".format(
                    e.tag_name,
                    e.message))
        else:
            self._add(self.get_starttag_text())

    def handle_endtag(self, tag):
        if _should_catch(tag):
            try:
                self._add(tags.tag(tag[5:]).end())
            except tags.TagNotFound as e:
                self._add("[Unknown Tag: {}]".format(
                    e.tag_name))
        else:
            self._add('</{}>'.format(tag))

    def handle_data(self, data):
        self._add(data)
