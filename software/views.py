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

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from .models import Project

def index(request):
    return redirect(reverse('loki-software-project-list'))

def project_list(request):
    return render(request,
        "loki/index.html",
        {
            "projects": Project.objects.order_by('name')
        }
    )

def project(request, project):
    return render(request,
        "loki/project.html",
        {
            "project": get_object_or_404(Project, slug=project)
        }
    )

def download_list(request, project, component):
    return HttpResponse("Downloads for: «{}»-«{}»".format(project, component))

def download(request, project, component, major, minor, patch, prerelease):
    return HttpResponse("Download: «{}»-«{}»-«{}»-«{}»-«{}»-«{}»".format(project, component, major, minor, patch, prerelease))
