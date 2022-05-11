import datetime
import os
import zipfile
from django.conf import settings
from rest_framework.exceptions import ValidationError


def check_request_datetime(request):
    """检查请求中的日期状态

    @params
        - request 
    """

    # 对日期进行格式化，防止用户随意下载文件
    if 'start_time' in request.data:
        req_start_time = request.data['start_time']
    elif 'start_time' in request.query_params:
        req_start_time = request.query_params['start_time']
    else:
        raise ValidationError('start_time is required')

    if 'end_time' in request.data:
        req_end_time = request.data['end_time']
    elif 'end_time' in request.query_params:
        req_end_time = request.query_params['end_time']
    else:
        req_end_time = req_start_time

    # 日期格式化格式
    dateformat = settings.ARCHIVE_DATETIME_FORMAT
    # 开始日期
    start_time = datetime.datetime.strptime(req_start_time, dateformat)
    # 结束日期
    end_time = datetime.datetime.strptime(req_end_time, dateformat)

    return start_time, end_time


def take_filename(start_time, end_time):
    """生成打包文件名

    @params
        - start_time (string, required) - 开始日期 eg: 20220214
        - end_time (string) - 结束日期 eg: 20220214
    """
    # 日期格式化格式
    dateformat = settings.ARCHIVE_DATETIME_FORMAT

    if start_time == end_time:
        filename = "{0}".format(start_time.strftime(dateformat))
    else:
        filename = "{0}_{1}".format(start_time.strftime(
            dateformat), end_time.strftime(dateformat))

    return filename


def create_path_list(start_time, end_time):
    """根据传入的时间范围生成路径数组

    @params
        - start_time (datetime, required) - 开始日期 datetime对象
        - end_time (datetime) - 结束日期 datetime对象
    """

    # 回传路径数组
    source_list = []
    # 临时根据时间生成的路径数组，可按自己需求更改响应规则
    datepath_list = []
    archive_path = settings.ARCHIVE_PATH

    for i in range((end_time - start_time).days + 1):
        _date = start_time + datetime.timedelta(days=i)
        _path = "{0}{1}".format(archive_path, _date.strftime('%Y/%m/%d/'))
        datepath_list.append(_path)

    for path in datepath_list:
        # 判断文件夹是否存在
        if os.path.isdir(path):
            source_list.append(path)

    return source_list


def make_archive(list_path, filename):
    """按照传入的路径数组对进行打包压缩

    @params
        - list_path (array, required) - 路径数组
        - filename (filename) - 文件地址
    """
    if not os.path.exists(os.path.dirname(filename)):  # 判断文件夹是否存在如果不存在则创建
        os.makedirs(os.path.dirname(filename))
    zf = zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED)
    zf_root_dir = os.path.basename(os.path.splitext(filename)[0])

    for path in list_path:
        for dirpath, dirnames, filenames in os.walk(path):
            for file in filenames:
                # 将文件打包到根目录
                zf.write(os.path.join(dirpath, file),
                         zf_root_dir + '/' + file)

    zf.close()

    return filename
