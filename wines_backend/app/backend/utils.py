from rest_framework.pagination import PageNumberPagination
from rest_framework import status as http_status, status
from collections import Iterable, Sequence, defaultdict
from rest_framework.views import exception_handler
from rest_framework.renderers import JSONRenderer


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)
    # Now add the HTTP status code to the response.
    if response is not None:
        # pprint(vars(response))
        if 'code' in response.data:
            del response.data['code']
        if 'messages' in response.data:
            del response.data['messages']
        code = response.status_code
        code_text = 'error'
        description = 'Error occured while processing request.'
        data = {}
        # LET THE SHIT BEGIN.
        if isinstance(response.data, Sequence):
            if len(response.data) > 0:
                response.data = response.data[0]
        elif 'detail' in response.data:
            description = response.data['detail']
            code_text = response.data['detail'].code
            data = {'detail': description}
            del response.data['detail']
        # THE SHIT MUST GO ON.
        else:
            detail_key = next(iter(response.data))
            if isinstance(response.data[detail_key], Iterable):
                description = str(response.data[detail_key][0])
                if hasattr(response.data[detail_key][0], 'code'):
                    code_text = response.data[detail_key][0].code
            else:
                description = str(response.data[detail_key])
                if hasattr(response.data[detail_key], 'code'):
                    code_text = response.data[detail_key].code
            data[detail_key] = description
            data['code'] = code_text
            del response.data[detail_key]
        response.data['status'] = 'error'
        response.data['code'] = code
        response.data['code_text'] = code_text
        response.data['message'] = description
        response.data['data'] = data
    return response


class CustomJsonRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        res = renderer_context.pop('response')
        if res.exception or res.status_code == status.HTTP_400_BAD_REQUEST:
            return super(CustomJsonRenderer, self).render(data, accepted_media_type, renderer_context)
        if not renderer_context:
            renderer_context = defaultdict()
        # pop not used params
        renderer_context.pop('view', None)
        renderer_context.pop('args', None)
        renderer_context.pop('kwargs', None)
        renderer_context.pop('request', None)

        renderer_context.setdefault('message', 'OK')
        renderer_context.setdefault('status', 'success')
        renderer_context.setdefault('code_text', 'success')
        renderer_context.setdefault('code', http_status.HTTP_200_OK)

        response = self.custom_response(data=data, **renderer_context)
        return super(CustomJsonRenderer, self).render(response, accepted_media_type, renderer_context)

    @staticmethod
    def custom_response(status, code, code_text, message, data=None):
        return {
            'status': status, 'code': code,
            'code_text': code_text, 'message': message,
            'data': data or {},
        }


class StandardSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        response = super(StandardSetPagination, self).get_paginated_response(data)
        response.data['total_pages'] = self.page.paginator.num_pages
        return response
