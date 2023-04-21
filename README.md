# JMeter Report

![](https://img.shields.io/badge/JMeter-green)
[![](https://img.shields.io/github/last-commit/hui-huo/jmeter_report_server)](https://github.com/hui-huo/jmeter_report_server)

基于Antd+DRF开发的一款JMeter测试报告服务，用于在JMeter接口测试中使用。


## 🌴 背景
JMeter是测试工作中常用的一款工具，除了压测还可以用来做接口自动化的测试。

从事测试多年，接口自动化也做过很多的尝试，有时候所在项目迭代较快，平常没有足够的时间
编写自动化测试脚本，但又想在日常测试中加入自动化来提高点效率，JMeter是一个不错的选择。
缺点就是官方没有提高好的测试报告（相信很多人都是颜值控😂），于是就有了这款适配JMeter的测试报告。

虽然功能比较简单，但已满足基本日常需求。

## 📌 安装

### 一、Docker

1. `docker pull huihuo21/jmeter-report`
2. `docker run -d -p 8000:8000 huihuo21/jmeter-report`
3. 浏览器访问`http://{服务ip}:8000`

### 二、本地构建
1. 克隆代码：`git clone https://github.com/hui-huo/jmeter_report_server.git`
2. 安装依赖：`pip install -r requirements.txt `
3. 生成数据表：`python manage.py makemigrations app`
4. 创建数据表：`python manage.py migrate app`
5. 启动服务：`python manage.py runserver`

## 👏 JMeter
插件使用(测试数据收集)：[JMeter-Backend-Listener](https://github.com/hui-huo/JMeter-Backend-Listener)

## 🔎 预览

#### 测试看板
![report](https://files.mdnice.com/user/25329/5919ebec-6bda-4717-a308-52a2428d1154.png)

#### 测试详情
![detail](https://files.mdnice.com/user/25329/5f6b4198-d6c0-40a9-8111-1666448b2d5a.png)

## 交流群
二维码会经常过期，可以加我个人微信: `xuechaoluan`，拉你入群。

<img src="https://files.mdnice.com/user/25329/b940a9df-f86a-40f9-ba15-f79fba7585b6.png" alt="_huihuo" width="300" height="300" />




