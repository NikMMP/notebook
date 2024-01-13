import datetime
import json
import mimetypes
import os

import dropbox
import requests
from allauth.socialaccount.providers.oauth.client import OAuthError
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, FileResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

from .forms import FileForm
from .models import File
from .utils import get_file_category, get_file_size
from django.views import View
from django.utils.decorators import method_decorator
from .dropbox_work import DropBoxServer, refresh_token, app_key, app_secret


@method_decorator(login_required, name="dispatch")
class upload(View):
    template_name = "files/upload.html"

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = FileForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        # print(request.POST)
        form = FileForm(request.POST, request.FILES)
        # print(request.FILES)
        # print(form.is_valid())
        if form.is_valid():
            file = form.save(commit=False)
            if file.path:
                # Отримуємо категорію за допомогою get_file_category
                category = get_file_category(file.path.name)
                file.category = category
                file.orig_name = "origname"
                # Зберігаємо файл
                file.user = request.user
                file.save()
                # Шлях до файлу на Dropbox та локального файлу
                dropbox_path = f'/{category}/{file.path.name}'
                local_path = os.path.join(settings.MEDIA_ROOT, file.path.name)
                # print(local_path + "-->>" + dropbox_path)
                # print(file.path.name + "-->>" + dropbox_path)

                size = get_file_size(local_path)
                file.size = size
                file.dropbox_path = dropbox_path
                file.save()
            # Завантаження файла на Dropbox
                dbx = DropBoxServer(refresh_token=refresh_token,
                                    app_key=app_key, app_secret=app_secret)
                dbx.connect()
                dbx.backup(local_path, dropbox_path)
            return redirect(to="files:files")
        else:
            return render(request, self.template_name, {"title": "Files", "form": form})

# Функція відображення файлів


class files_list(View):
    template_name = 'files/files.html'

    def get(self, request, *args, **kwargs):
        files_ = (
            File.objects.filter(user=request.user).all()
            if request.user.is_authenticated
            else []
        )
        return render(request, self.template_name, {"files": files_})


@method_decorator(login_required, name="dispatch")
class remove(View):
    def get(self, request, file_id):
        dbx = DropBoxServer(refresh_token=refresh_token,
                            app_key=app_key, app_secret=app_secret)
        dbx.connect()
        file_to_delete = File.objects.filter(
            user=request.user, pk=file_id).first()
        dbx.delete(file_to_delete.dropbox_path)
        File.objects.filter(
            user=request.user, pk=file_id).delete()
        return redirect(to='files:files')


@method_decorator(login_required, name="dispatch")
class download(View):
    def get(self, request, file_id):
        dbx = DropBoxServer(refresh_token=refresh_token,
                            app_key=app_key, app_secret=app_secret)
        dbx.connect()
        file_to_download = File.objects.filter(
            user=request.user, pk=file_id).first()
        local_path = os.path.join(
            settings.MEDIA_ROOT, file_to_download.orig_name)
        dbx.download(local_path, file_to_download.dropbox_path)
        return redirect(to='files:files')

# скачування фвйлів
# @login_required()
# def download(request, file_id):
#     dbx = get_access_dbx(request)
#     if isinstance(dbx, (HttpResponseRedirect, type(None))):
#         print(f'INSTANCE ::::::::::::::: {dbx}')
#         return redirect(to='files:dropbox_oauth')

#     file = File.objects.filter(pk=file_id).first()

#     dbx.files_download_to_file(os.path.join(
#         settings.MEDIA_ROOT, file.orig_name), file.dropbox_path)
#     local_path = os.path.join(settings.MEDIA_ROOT, file.orig_name)

#     content_type, _ = mimetypes.guess_type(local_path)
#     if content_type is None:
#         content_type = 'application/octet-stream'

#     response = FileResponse(open(local_path, 'rb'), content_type=content_type)
#     response['Content-Disposition'] = f'attachment; filename="{file.orig_name}"'
#     return response


# відображення файлів
@login_required()
def show(request, file_id):
    dbx = get_access_dbx(request)
    if isinstance(dbx, (HttpResponseRedirect, type(None))):
        print(f'INSTANCE ::::::::::::::: {dbx}')
        return redirect(to='files:dropbox_oauth')

    file = File.objects.filter(pk=file_id).first()
    if file.orig_name.split('.')[1] not in ('html', 'htm', 'txt', 'xml', 'json', 'svg', 'jpg', 'jpeg', 'png,' 'gif',
                                            'bmp', 'css', 'js', 'webm', 'pdf', 'mp3', 'wav'):
        return redirect(to="files:files")
    dbx.files_download_to_file(os.path.join(
        settings.MEDIA_ROOT, file.orig_name), file.dropbox_path)
    local_path = os.path.join(settings.MEDIA_ROOT, file.orig_name)

    response = FileResponse(open(local_path, 'rb'))
    return response


# Функція редагування файлів
@login_required()
def edit(request, file_id):
    if request.method == 'POST':
        description = request.POST.get('description')
        File.objects.filter(pk=file_id).first().update(description=description)
        return redirect(to='files:files')

    file = File.objects.filter(pk=file_id).first()
    return render(request, "files/edit.html",
                  context={"title": "Files", "file": file})

# Функція перегляду інфо про файл


def detail(request, file_id):
    if request.method == 'GET':
        description = request.GET.get('description')
        category = request.GET.get('category')

    file = File.objects.filter(pk=file_id).first()
    return render(request, "files/detail.html",
                  context={"title": "Files", "file": file})
