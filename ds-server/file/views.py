import os
from django.conf import settings
from django.http import FileResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.exceptions import APIException
from file.tencent import tencent_get_presigned_url, tencent_object_exists, tencent_upload
from file.utils import check_request_datetime, create_path_list, make_archive, take_filename


@api_view(['POST'])
def download_file(request):
    """直接下载服务器文件

    @params
        - start_time (string, required) - 开始日期 eg: 20220214
        - end_time (string) - 结束日期 eg: 20220214
        - is_overwrite (boolean) - 是否覆盖原文件
    """

    [start_time, end_time] = check_request_datetime(request)
    filename = take_filename(start_time, end_time)
    # 打包文件地址
    archive_full_path = settings.ARCHIVE_FULL_PATH
    archive_filepath = archive_full_path + filename + '.zip'

    is_overwrite = bool('is_overwrite' in request.query_params)
    is_exist = os.path.exists(archive_filepath)

    # 判断是否需要覆盖文件
    if is_overwrite == True or is_exist != True:
        # 进行打包操作
        list_path = create_path_list(start_time, end_time)
        make_archive(list_path, archive_filepath)

    response = FileResponse(open(archive_filepath, 'rb'))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename={}.zip'.format(
        filename)

    return response


@api_view(['POST'])
def tencent_download(request):
    """下载腾讯云COS文件存储

    @params
        - start_time (string, required) - 开始日期 eg: 20220214
        - end_time (string) - 结束日期 eg: 20220214
        - is_overwrite (boolean) - 是否覆盖原文件
    """

    [start_time, end_time] = check_request_datetime(request)
    filename = take_filename(start_time, end_time)

    is_overwrite = bool('is_overwrite' in request.data)
    is_exist = tencent_object_exists(filename)

    # 判断是否需要覆盖文件
    if is_overwrite == True or is_exist != True:
        try:
            # 打包文件地址
            archive_full_path = settings.ARCHIVE_FULL_PATH
            archive_filepath = archive_full_path + filename + '.zip'
            # 首先进行打包操作
            list_path = create_path_list(start_time, end_time)
            make_archive(list_path, archive_filepath)
            # 上传指定打包
            tencent_upload(archive_filepath)
            # 生成预定义URL进行分发
            url = tencent_get_presigned_url(filename)
        except:
            raise APIException('打包失败，请联系管理员解决')
    else:
        url = tencent_get_presigned_url(filename)

    expired = settings.COS_URL_EXPIRED

    return Response({
        'url': url,
        'expired': int(expired)
    })
