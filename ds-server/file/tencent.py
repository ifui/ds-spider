import datetime
import os
import shutil
from django.conf import settings
from qcloud_cos import CosS3Client, CosConfig

from qcloud_cos.cos_threadpool import SimpleThreadPool


def tencent_client():
    """返回腾讯云COS对象

    """
    region = settings.COS_REDION
    secret_id = settings.COS_SECRED_ID
    secret_key = settings.COS_SECRET_KEY

    config = CosConfig(Region=region, SecretId=secret_id,
                       SecretKey=secret_key)
    client = CosS3Client(config)

    return client


def tencent_get_presigned_url(filename):
    """生成预签名URL

    @params
      - filename (string, required) - 文件名
    """
    client = tencent_client()
    bucket = settings.COS_BUCKET

    key = "{0}{1}.zip".format(settings.COS_ARCHIVE_FULL_PATH, str(filename))
    disposition = "attachment; filename={0}.zip".format(filename)
    expired = settings.COS_URL_EXPIRED

    url = client.get_presigned_url(
        Method='GET',
        Bucket=bucket,
        Key=key,
        Params={
            'response-content-disposition': disposition  # 下载时保存为指定的文件
        },
        Expired=int(expired)
    )

    return url


def tencent_object_exists(filename):
    """判断对象是否存在

    """

    client = tencent_client()
    bucket = settings.COS_BUCKET
    archive_full_path = settings.ARCHIVE_FULL_PATH
    key = "{0}/{1}.zip".format(archive_full_path, str(filename))

    response = client.object_exists(
        Bucket=bucket,
        Key=key)

    return response


def tencent_create_path_list(start_time, end_time):
    """根据时间范围生成对应路径数组

    """
    source_list = []

    client = tencent_client()
    bucket = settings.COS_BUCKET

    datepath_list = []
    archive_path = settings.ARCHIVE_PATH

    for i in range((end_time - start_time).days + 1):
        _date = start_time + datetime.timedelta(days=i)
        _path = "{0}{1}".format(archive_path, _date.strftime('%Y/%m/%d/'))
        datepath_list.append(_path)

    for path in datepath_list:
        _res = client.list_objects(
            Bucket=bucket,
            Prefix=path)
        # 判断对象是否存在
        if 'Contents' in _res:
            for content in _res['Contents']:
                source_list.append(content['Key'])

    return source_list


def tencent_download_file(filename, path_list):
    """下载并压缩

    @params
      - filename (string, required) - 文件名
      - path_list (dict, required) - 路径数组
    """
    # 临时路径 eg: ds-server/tmp/filename
    local_tmp_dir = os.path.join(settings.BASE_DIR, 'tmp', filename)

    # 如果本地目录结构不存在，递归创建
    if not os.path.exists(os.path.dirname(local_tmp_dir + '/')):
        os.makedirs(os.path.dirname(local_tmp_dir + '/'))

    pool = SimpleThreadPool()
    client = tencent_client()
    bucket = settings.COS_BUCKET

    for path in path_list:
        if str(path).endswith("/"):
            continue
        # 一维化保存路径
        _save_path = local_tmp_dir + '/' + os.path.basename(path)
        # 使用线程池方式下载文件
        pool.add_task(client.download_file, bucket, path, _save_path)

    pool.wait_completion()
    # 打包
    zip_filename = shutil.make_archive(
        local_tmp_dir + '/' + filename, 'zip', local_tmp_dir)
    return zip_filename


def tencent_upload(filename):
    """上传函数

    @params
      - filename (string, required) - 文件名
    """
    client = tencent_client()
    bucket = settings.COS_BUCKET
    cos_archive_full_path = settings.COS_ARCHIVE_FULL_PATH
    expires = settings.COS_URL_EXPIRED

    key = cos_archive_full_path + os.path.basename(filename)

    response = client.upload_file(
        Bucket=bucket,
        Key=key,
        LocalFilePath=filename,
        Expires=expires
    )

    return response
