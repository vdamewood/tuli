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

from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.Index, name='tuli-swcat-index'),
    path('projects/', views.ProjectList, name='tuli-swcat-project-list'),
    path('projects/<slug:project>/',
        views.Project,
        name="tuli-swcat-project"),
    path(
        'projects/<slug:project>/downloads/',
        views.DownloadList,
        {
            'component': '',
        },
    ),
    path(
        'projects/<slug:project>/downloads/v<int:major>.<int:minor>.<int:patch><str:prerelease>',
        views.Download,
        {
            'component': '',
        },
    ),
    path(
        'projects/<slug:project>/downloads/<slug:component>-v<int:major>.<int:minor>.<int:patch>',
        views.Download,
        {
            'prerelease': '',
        },
    ),
    path(
        'projects/<slug:project>/downloads/<slug:component>-v<int:major>.<int:minor>.<int:patch><str:prerelease>',
        views.Download,
        {
        },
    ),
    path(
        'projects/<slug:project>/downloads/<slug:component>',
        views.DownloadList,
        {
        },
    ),
    path(
        'projects/<slug:project>/downloads/v<int:major>.<int:minor>.<int:patch>',
        views.Download,
        {
            'component': '',
            'prerelease': '',
        },
    ),
]
