import functools
import traceback

from django.db import transaction
from django.http import JsonResponse
from rest_framework import status

JSON_DUMPS_PARAMS = {
    'ensure_ascii': False
}


def ret(json_object, status=status.HTTP_200_OK):
    """ Отдает JSON с правильным HTTP заголовком и в читаемом
    в браузере виде в случае с кириллицей"""
    return JsonResponse(
        json_object,
        status=status,
        safe=not isinstance(json_object, list),
        json_dumps_params=JSON_DUMPS_PARAMS
    )


def error_response(exception):
    """Форматирует HTTP ответ с описанием ошибки и Tracebak'ом"""
    res = {'errorMessage': str(exception),
           'traceback': traceback.format_exc()}
    return ret(res, status=400)


def base_view(fn):
    """Декоратор для всех вьюшек, обрабатываент исключения"""
    @functools.wraps(fn)
    def inner(request, *args, **kwargs):
        try:
            with transaction.atomic():
                return fn(request, *args, **kwargs)
        except Exception as e:
            return error_response(e)
    return inner
