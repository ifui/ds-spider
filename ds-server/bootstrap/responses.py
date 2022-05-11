from rest_framework.renderers import JSONRenderer


class ReponseRender(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        if renderer_context:
            result = dict()
            if data is None:
                result['success'] = True
            elif ('errorMessage' in data):
                result['success'] = False
                result['errorMessage'] = data['errorMessage']
                if ('errorData' in data):
                    result['errorData'] = data['errorData']
            else:
                result['success'] = True
                result['data'] = data

            # 返回JSON数据
            return super().render(result, accepted_media_type, renderer_context)
        else:
            return super().render(data, accepted_media_type, renderer_context)
