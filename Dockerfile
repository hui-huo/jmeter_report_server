# 指定镜像源
FROM python:3.9-slim-buster

# 设置环境变量
ARG DB_NAME
ARG DB_USER
ARG DB_PASSWORD
ARG DB_HOST
ARG DB_PORT
ENV DB_NAME=$DB_NAME
ENV DB_USER=$DB_USER
ENV DB_PASSWORD=$DB_PASSWORD
ENV DB_HOST=$DB_HOST
ENV DB_PORT=$DB_PORT

# 将当前目录复制到镜像中
COPY . /app

# 设置工作目录
WORKDIR /app

# 安装依赖
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ --trusted-host mirrors.cloud.aliyuncs.com --default-timeout=60 --no-cache-dir -r requirements.txt

# 运行 migrate 命令
RUN python manage.py makemigrations app && python manage.py migrate app

# 启动应用
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]