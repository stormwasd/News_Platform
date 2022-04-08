from flask import Flask, jsonify
from werkzeug.utils import secure_filename
from flask import request
import os
from datetime import datetime
import random

# 路径配置
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)


# 上传图潘test接口
@app.route("/upload", methods=["POST"])
def upload():
    # 获取文件列表
    f = request.files.get('file')
    # 返回文件列表
    refile = []
    # 获取安全文件名
    filename = secure_filename(f.filename)
    # 生成随机数
    randomNum = random.randint(0, 100)
    # 生成文件名,以及保存文件
    filename = datetime.now().strftime("%Y%m%d%H%M%S") + "_" + str(randomNum) + '.' + filename.rsplit('.', 1)[1]
    file_path = basedir + '/static/file/' + filename
    f.save(file_path)
    # 配置成对应外网访问的连接
    my_host = "http://175.24.172.64:5000"
    new_path_file = my_host + '/static/file/' + filename
    refile.append(new_path_file)
    data = {"msg": "success", "url": refile}
    payload = jsonify(data)
    return payload, 200


if __name__ == "__main__":
    app.run(debug=True)
