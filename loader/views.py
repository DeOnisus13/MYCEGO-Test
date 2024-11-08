import requests
from django.core.cache import cache
from django.http import HttpResponseBadRequest
from django.shortcuts import render

from loader.services import get_data


def home(request):
    """
    View-функция для отображения главной страницы.
    """
    return render(request, "home.html")


def items(request):
    """
    View-функция для отображения страницы загрузки файлов.
    Получает public_url (public_key) из запроса с главной страницы.
    """
    if request.method == "POST":
        public_url = request.POST.get("public_url")
        # Сохраняем public_url в сессию для
        request.session['public_url'] = public_url

        # Ищем данные в кэше
        cache_key = f"items_data_{public_url}"
        cache_data = cache.get(cache_key)

        if not cache_data:
            # Если данные не найдены в кэше, делаем запрос и кэшируем
            api_url = f"https://cloud-api.yandex.net/v1/disk/public/resources/download?public_key={public_url}"
            try:
                data = get_data(public_url)

                # Получаем ссылку для загрузки
                response = requests.get(api_url)
                response.raise_for_status()
                download_url = response.json().get("href")  # Получаем прямую ссылку на файл

                # Создаём структуру данных для кэша
                cache_data = {
                    "items": [data] if data.get("items") is None else data["items"],
                    "download_url": download_url,
                }
                cache.set(cache_key, cache_data, 60)

            except TypeError:
                return HttpResponseBadRequest(
                    "Нет такого адреса. Вернитесь на страницу поиска и введите правильный url.")

        return render(request, "items_list.html", cache_data)

    else:
        return HttpResponseBadRequest("Разрешены только POST запросы.")
