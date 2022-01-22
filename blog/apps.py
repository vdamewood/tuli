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
from django.urls import reverse

def _link_lookup(target):
    kind, slug = target.split(":", 1)
    if kind != 'post':
        from tuli.tags import LinkError
        raise LinkError('blog', target, "Invalid target type: {}".format(kind))

    try:
        from .models import Post
        my_post = Post.objects.get(slug=slug)
    except Post.DoesNotExist as e:
        from tuli.tags import LinkTargetNotFound
        raise LinkTargetNotFound('blog', target)
    else:
        return {
            "url": reverse('tuli-blog-post', args=(my_post.slug,)),
            "title": my_post.title,
        }


class BlogConfig(AppConfig):
    name = 'tuli.blog'
    verbose_name = "Tuli Blog"
    default_auto_field = 'django.db.models.AutoField'
    def ready(self):
        from tuli.tags import register_link
        register_link('blog', _link_lookup)
