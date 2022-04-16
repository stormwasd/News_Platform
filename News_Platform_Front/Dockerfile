# 基于的基础镜像
FROM python:3.7

# 代码添加到code文件夹
ADD ./package /code

# 设置code文件夹为工作目录
WORKDIR /code

# 安装支持
RUN pip3 install -i https://pypi.doubanio.com/simple/ -r requirements.txt

# 启动命令
CMD ["python", "/code/Front_end/run.py"]