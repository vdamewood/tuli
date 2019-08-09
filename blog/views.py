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

from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from . import models as m

def Index(request):
    return render(request, 'loki/blog/index.html', {
        'posts': m.Post.objects.order_by('created'),
        'tags': m.Tag.objects.order_by('name'),
    })

def PostList(request):
    return redirect('loki-blog-index')

def Post(request, slug):
    p = get_object_or_404(m.Post, slug=slug)
    return render(request, 'loki/blog/post.html', {'post': p})

def TagList(request):
    return redirect('loki-blog-index')

def Tag(request, slug):
    return render(request, 'loki/blog/tag.html', {
        'tag': get_object_or_404(m.Tag, slug=slug),
    })
