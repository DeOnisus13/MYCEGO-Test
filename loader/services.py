from datetime import datetime

import requests


def get_data(public_link: str, limit=20, offset=0) -> dict:
    """
    Функция для получения словаря с нужными параметрами из запроса к публичному ресурсу на Я.Диске.
    """
    url = f"https://cloud-api.yandex.net/v1/disk/public/resources"
    params = {
        "public_key": public_link,
        "limit": limit,
        "offset": offset,
    }
    response = requests.get(url, params=params)
    response_json = response.json()

    if response_json.get("_embedded") is None:
        result = {
            "file_dl_link": response_json.get("file"),
            "size": f'{(response_json.get("size") // 1024) if response_json.get("size") else "-"} Kb',
            "media_type": response_json.get("media_type"),
            "preview": response_json.get("preview"),
            "type": response_json.get("type"),
            "mime_type": response_json.get("mime_type").split("/")[-1] if response_json.get("mime_type") else None,
            "name_file": response_json.get("name"),
            "created": revert_time(response_json.get("created")),
        }

    else:
        items_list = response_json["_embedded"].get("items")
        items_list_final = []

        for item in items_list:
            items = {
                "name_file": item.get("name"),
                "created": revert_time(item.get("created")),
                "size": f'{(item.get("size") // 1024) if item.get("size") else "-"} Kb',
                "mime_type": item.get("mime_type").split("/")[-1] if item.get("mime_type") else None,
                "file_dl_link": item.get("file"),
                "media_type": item.get("media_type"),
                "preview": item.get("preview"),
                "type": item.get("type"),
            }
            items_list_final.append(items)

        result = {
            "total": response_json["_embedded"].get("total"),
            "name_dir": response_json.get("name"),
            "created_dir": revert_time(response_json.get("created")),
            "type_dir": response_json.get("type"),
            "items": items_list_final
        }
    return result


def revert_time(input_time: str) -> str:
    """
    Функция для приведения строки с датой и временем к удобочитаемому виду.
    """
    date_obj = datetime.fromisoformat(input_time)
    formatted_date = date_obj.strftime("%d.%m.%Y")
    return formatted_date
