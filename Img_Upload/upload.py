"""
@Description :
@File        : upload
@Project     : Img_Upload
@Time        : 2022/4/8 15:00
@Author      : LiHouJian
@Software    : PyCharm
@issue       :
@change      :
@reason      :
"""

from flask import Flask, jsonify
from flask import request
import os
from datetime import datetime
import random

# 路径配置
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)


# 上传图片接口
@app.route("/upload", methods=["POST"])
def upload():
    # 获取文件列表
    f = request.files.get('file')
    # 返回文件列表
    refile = []
    # 生成随机数
    randomNum = random.randint(0, 100)
    # 生成文件名,以及保存文件
    filename = datetime.now().strftime("%Y%m%d%H%M%S") + "_" + str(randomNum) + '.' + 'jpg'
    file_path = basedir + '/static/file/' + filename
    f.save(file_path)
    # 配置成对应外网访问的连接
    my_host = "http://127.0.0.1:5000"
    new_path_file = my_host + '/static/file/' + filename
    refile.append(new_path_file)
    data = {"msg": "success", "url": refile}
    payload = jsonify(data)
    return payload, 200


if __name__ == "__main__":
    app.run(debug=True)
