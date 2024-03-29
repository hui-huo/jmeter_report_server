## 🌴 背景

JMeter 是测试工作中常用的一款工具，除了压测还可以用来做接口自动化的测试。从事测试多年，接口自动化也做过很多的尝试，有时候所在项目迭代较快，平常没有足够的时间 编写自动化测试脚本，但又想在日常测试中加入自动化来提高点效率，JMeter 是一个不错的选择。
缺点就是官方没有提高好的测试报告（相信很多人都是颜值控 😂），于是就自己写了款适配 JMeter 的测试报告。[在线体验](http://1.116.137.209:8000/dashboard "效果体验")

## 📎 实现

在实现方案上借鉴了 Grafana 收集压测数据的方式，自己实现了一个用来收集测试数据的 JMeter 后端监听器插件，当测试完成后，将测试数据通过 API 的形式发送到测试服务端，服务端把测试数据保存到数据库。

### 技术栈

前端 React + Antd | 后端 Django REST framework | Python 3.8+

<img src="https://files.mdnice.com/user/25329/8ff683b1-4e1f-4a52-b131-24b8564d6d57.png" alt="_huihuo" width="600" height="450" />

## 📌 安装配置

### 第一步：通过 docker 启动服务

虽然属于前后分离的项目，但为了简化使用已经将前端静态文件打包到了后端项目中，且制作好了 docker 镜像，直接从 dockerhub 拉取到本地启动即可。

```
# 下载镜像
1. docker pull huihuo21/jmeter-report
# 启动容器
2. docker run -d -p 8000:8000 huihuo21/jmeter-report
# 页面访问
3. 浏览器访问`http://{服务ip}:8000
```

以上启动容器的方式默认使用的是内置数据库`sqlite`，若指定外部数据库(仅支持`mysql`)则需要通过传入数据库配置参数来启动：

```
# HOST 和 PORT 可选，默认`localhost`, `3306`
docker run -d -p 8000:8000 \
-e DB_NAME=数据库名称 \
-e DB_USER=用户名 \
-e DB_PASSWORD=密码 \
-e DB_HOST=IP \
-e DB_PORT=端口 \
huihuo21/jmeter-report
```

### 第二步：安装 JMeter 后端监听器插件

JMeter 版本`5.4.3`，JKD-11 (JDK8 应该可用，未测试)

1. 下载插件：[JMeter-Backend-Listener](https://github.com/hui-huo/JMeter-Backend-Listener/releases)
2. 安装插件：jar 文件放置在`{JMeter主目录}/lib/ext`下。
3. 配置参数：
   ![](https://files.mdnice.com/user/25329/07494619-83ea-49f8-b484-93d755acfa40.png)

## 🔎 预览说明

### 测试看板

![](https://files.mdnice.com/user/25329/66eecb06-bd72-4e99-801f-ad660ecfc3b5.png)

看板页面分三部分，最上面一行是最近一次测试的概括信息；中间两个图表，左边图标是测试历史柱状图，右边是测试通过率的曲线图，① 处是快速筛选时间范围按钮，W 表示周、M 表示月、Q 表示一季度；
② 处标签表示当前看板数据的范围（因最初设计考虑到多项目使用）③ 可以对项目和环境进行筛选。

### 测试报告

![](https://files.mdnice.com/user/25329/623131fc-30bc-4f72-8bd9-c10b9fc2d719.png)

报告页面则展示所有的测试记录，有两处需要说明：

① 报告的最初设计是尽量简单，没有做权限控制，所以第一个版本没有删除功能，因有小伙伴反馈需要删除功能，所以增加了删除，但为了降低误操作的可能，页面做了处理默认不展示删除按钮，需要通过 url 增加传参`?show=delete`来显示删除按钮。

② 构建方式在使用中无须设置，是根据 JMeter 所执行的平台来自动显示，除 Linux 平台是自动构建，其他平台都是手动构建方式。

### 测试详情

![](https://files.mdnice.com/user/25329/77bcd14a-fac6-4f24-9078-357e04463e14.png)

详情页中用例列表可以根据所属模块、测试场景、用例名称、测试结果做筛选和搜索，且字段都做了超长截断和浮层完整显示。

## ✏️ JMeter 用例编写
所属模块建议从业务角度来命名，也可以按照微服务功能划分命名，场景名称则是某个业务流程，比如商城系统中：订单模块-下单流程，订单模块-退货流程等。
### 单接口测试

![](https://files.mdnice.com/user/25329/82c0c03f-0b58-4e90-b719-f57c31bee378.png)

对于单接口测试的用例组织形式如上图所示：线程组名称=所属模块名称，事务控制器名称=场景名称，请求名=用例名；请求使用事务控制器包裹，事务控制器必须勾选`Generate parent sample`选项。（事务控制器非必须）

### 串联接口测试

![](https://files.mdnice.com/user/25329/51e577f9-8fcc-4a1b-811c-2e6dd93d5570.png)

相对单接口，串联接口的测试特殊点在于 如果中间某个环节的接口测试失败了，后续的接口就不需要继续测试。故目前在 JMeter 中摸索出了两种方式，在上图的方式中，模块名和场景名都在线程组名称中给出且使用`|`分隔（两边可以有空格已做处理)，线程组勾选`停止线程`配置，注意不是停止测试！
另一种方式在 jmx 示例文件（项目根目录下jmeter_repoter.jmx）中有注释说明，可以下载测试尝试下，个人推荐前者。

### 其他注意项

#### 测试计划

测试计划中建议勾选`独立运行每个线程组`选项，不勾选的情况下每个线程组都会自动一个线程，优点是并发执行时间短，缺点是测试用例列表显示无序，因为是多线程同时执行的。

#### 用例和场景

接口测试一般分为两种：一种是单接口测试，如对同一个接口做正向或者异常的传参，通常这种接口测试之间没有相互依赖关系，其中一个测试失败不影响另一个测试的执行；另一种则是串联场景的接口测试，通常是组织多个接口来测试某个场景，接口之间存在关联关系，如某个接口的入参依赖前一个接口的出参。为了方便，此报告会将每一个 http 请求视为一个用例，场景数只做统计展示。


#### 插件工具分享
第一个：
[BlazeMeter | The Continuous Testing Platform](https://chrome.google.com/webstore/detail/blazemeter-the-continuous/mbopgmdnpcbohhpnfglgohlbhfongabi)
这个chrome插件用来快速录制接口生成可执行的JMX文件。

第二个：[Convert HAR, XML, Selenium, PCAP and JSON to JMX format](https://converter.blazemeter.com/)。


## 🏄 交流群

二维码会经常过期，可以加我个人微信: `_huihuo`，拉你入群。

<img src="https://files.mdnice.com/user/25329/510e20fe-2c77-4b5f-b05d-c36332551a7f.png" alt="_huihuo" width="300" height="300" />


## 0610更新
- 去除数据库字段长度限制
- 新增测试报告删除功能
- 拆分出测试场景字段
- 优化用例基本信息样式

## 0813更新
- 修复通过率精度问题
- 优化用例列表序号显示