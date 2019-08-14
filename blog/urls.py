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

from django.urls import path
from . import views

urlpatterns = [
    path('', views.Index, name='tuli-blog-index'),
    path('posts/', views.PostList, name='tuli-blog-post-list'),
    path('posts/<slug>', views.Post, name='tuli-blog-post'),
    path('tags/', views.TagList, name='tuli-blog-tag-list'),
    path('tags/<slug>', views.Tag, name='tuli-blog-tag'),
]
