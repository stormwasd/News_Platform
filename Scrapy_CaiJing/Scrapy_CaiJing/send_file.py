from urllib3 import encode_multipart_formdata
import requests
from tenacity import *
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def retry_on_result(result):
    return result.result()


def if_retry(result):
   return result['code'] != 1


@retry(stop=stop_after_attempt(3),
       retry_error_callback=retry_on_result,
       retry=retry_if_result(if_retry))
def send_file(file_name, file_url='', upload_url='', headers=None, **kwargs):
    """
    返回的字典中code为 1 时才代表上传成功，其他全部是失败
    :param file_name：文件的名称
    :param file_url：文件的url，可以是本地路径也可以是http连接
    :param upload_url: 文件上传接口的url
    :param headers: 图片请求的headers
    """
    if not file_url.startswith('http'):
        my_file = Path(file_url)
        if my_file.is_file():
            return send_local_file(file_name, file_url, upload_url)
        return {
            'code': 2,
            'msg': '不是一个常规的url地址',
            'data': {}
        }
    url = upload_url  # 请求的接口地址
    err = {
            'code': 2,
            'msg': '文件下载失败',
            'data': {}
        }

    img = None
    try:
        img = requests.get(file_url, headers=headers, **kwargs)
        
    except Exception as e:
        logger.warning('%s 文件下载失败', file_name)
        return err

    if not img or (not img.content):
        logger.warning('%s 文件下载失败', file_name)
        return err
    file = {
        "file": (file_name, img.content),  # 引号的file是接口的字段，后面的是文件的名称、文件的内容
        # "key": "value",  # 如果接口中有其他字段也可以加上
    }

    encode_data = encode_multipart_formdata(file)

    file_data = encode_data[0]
    # b'--c0c46a5929c2ce4c935c9cff85bf11d4\r\nContent-Disposition: form-data; name="file"; filename="1.txt"\r\nContent-Type: text/plain\r\n\r\n...........--c0c46a5929c2ce4c935c9cff85bf11d4--\r\n

    headers_from_data = {
        "Content-Type": encode_data[1]
    }

    response = requests.post(url=url, headers=headers_from_data, data=file_data).json()
    return response


@retry(stop=stop_after_attempt(3),
       retry_error_callback=retry_on_result,
       retry=retry_if_result(if_retry))
def send_local_file(file_name, file_url='', upload_url=''):
        """
        本地文件上传接口
        :param file_name:
        :param file_url:
        :param upload_url:
        :param headers:
        :return:
        """
        with open(file_url, mode="rb") as f:  # 打开文件
            file = {
                "file": (file_name, f.read()),  # 引号的file是接口的字段，后面的是文件的名称、文件的内容
                # "key": "value",  # 如果接口中有其他字段也可以加上
            }

            encode_data = encode_multipart_formdata(file)

            file_data = encode_data[0]
            # b'--c0c46a5929c2ce4c935c9cff85bf11d4\r\nContent-Disposition: form-data; name="file"; filename="1.txt"\r\nContent-Type: text/plain\r\n\r\n...........--c0c46a5929c2ce4c935c9cff85bf11d4--\r\n

            headers_from_data = {
                "Content-Type": encode_data[1]
            }

            response = requests.post(url=upload_url, headers=headers_from_data, data=file_data).json()
            return response