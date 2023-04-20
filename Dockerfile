# 指定镜像源
FROM python:3.9-slim-buster

# 将当前目录复制到镜像中
COPY . /app

# 设置工作目录
WORKDIR /app

# 安装依赖
RUN pip3 install -i http://mirrors.cloud.aliyuncs.com/pypi/simple/ --trusted-host mirrors.cloud.aliyuncs.com --default-timeout=60 --no-cache-dir -r requirements.txt
RUN #pip install --no-cache-dir -r requirements.txt

# 运行 migrate 命令
RUN python manage.py makemigrations app
RUN python manage.py migrate app

# 启动应用
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]