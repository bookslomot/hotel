import functools


from django.db import transaction
from django.http import JsonResponse
from django.views import View


from my_exeptions.exeptions_fun.exeptions_views import error_response, JSON_DUMPS_PARAMS


def base_view(fn):
    """ Декоратор для всех вьюшек, обрабатывает исключение"""
    @functools.wraps(fn)
    def inner(request, *args, **kwargs):
        try:
            with transaction.atomic():
                return fn(request, *args, **kwargs)
        except Exception as e:
            return error_response(e)

    return inner


class BaseView(View):
    """Базовый класс для всех вьюшек, обрабатывает исключения"""

    def dispatch(self, request, *args, **kwargs):
        try:
            response = super().dispatch(request, *args, **kwargs)
        except Exception as e:
            return self._response({'errorMessage': e.message}, status=400)

        if isinstance(response, (dict, list)):
            return self._response(response)
        else:
            return response

    @staticmethod
    def _response(data, *, status=200):
        return JsonResponse(
            data,
            status=status,
            safe=not isinstance(data, list),
            json_dumps_params=JSON_DUMPS_PARAMS
        )

