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
    path('', views.index, name="loki-software-home"),
    path('projects/', views.project_list, name="loki-software-project-list"),
    path('projects/<slug:project>/',
        views.project,
        name="loki-software-project-show"),
    path(
        'projects/<slug:project>/downloads/',
        views.download_list,
        {
            'component': '',
        },
    ),
    path(
        'projects/<slug:project>/downloads/v<int:major>.<int:minor>.<int:patch><str:prerelease>',
        views.download,
        {
            'component': '',
        },
    ),
    path(
        'projects/<slug:project>/downloads/<slug:component>-v<int:major>.<int:minor>.<int:patch>',
        views.download,
        {
            'prerelease': '',
        },
    ),
    path(
        'projects/<slug:project>/downloads/<slug:component>-v<int:major>.<int:minor>.<int:patch><str:prerelease>',
        views.download,
        {
        },
    ),
    path(
        'projects/<slug:project>/downloads/<slug:component>',
        views.download_list,
        {
        },
    ),
    path(
        'projects/<slug:project>/downloads/v<int:major>.<int:minor>.<int:patch>',
        views.download,
        {
            'component': '',
            'prerelease': '',
        },
    ),
]
