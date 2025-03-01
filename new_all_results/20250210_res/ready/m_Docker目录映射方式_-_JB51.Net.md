# Docker目录映射方式

更新时间：2024年11月02日 09:32:03   
作者：普通网友  

总结了一些常用的Docker命令,包括查看、停止、重启和删除容器等操作,帮助用户更好地管理容器

---

### 目录

- [Docker目录映射](#docker目录映射)
- [docker常用命令](#docker常用命令)
- [目录映射](#目录映射)
- [实战过程](#实战过程)
- [总结](#总结)

## Docker目录映射

### docker常用命令

1. `docker ps // 查看所有正在运行容器`
2. `docker stop containerId // containerId 是容器的ID`
3. `docker ps -a // 查看所有容器`
4. `docker ps -a -q // 查看所有容器ID`
5. `docker stop $(docker ps -a -q) // stop停止所有容器`
6. `docker rm $(docker ps -a -q) // remove删除所有容器`
7. `docker restart 容器id // 重启容器`
8. `docker run -d -p 8008:80 --name nginx-name nginx:1.1.1 // 启动一个新docker实例(nginx:1.1.1是版本号)`

### 目录映射

**实例：**

1. `docker run -p 8079:80 --name nginx-test --privileged=true -v /testdocker/default.conf:/etc/nginx/conf.d/default.conf -v /testdocker/html:/usr/share/nginx/html -d nginx:1.14`

**命令解读：**

- `-p`: 指定端口映射，格式为：主机(宿主)端口:容器端口
- `--privileged=true`: 关闭安全权限，否则你容器操作文件夹没有权限
- `-v`: 挂载目录为：主机目录:容器目录，在创建前容器是没有指定目录时，docker容器会自己创建

### 实战过程

在服务器添加一个测试文件夹，放置nginx测试用例需要的nginx.conf配置文件，和一个默认页面index.html如图：

![实战过程图](//img.jbzj.com/file_images/article/202411/2024110209294114.png)

**执行：**

1. `docker run -p 8079:80 --name nginx-test --privileged=true -v /testdocker/default.conf:/etc/nginx/conf.d/default.conf -v /testdocker/html:/usr/share/nginx/html -d nginx:1.14`

成功后如图：

![成功执行图](//img.jbzj.com/file_images/article/202411/2024110209294115.png)

- 测试挂载的目录文件是否可用：直接修改index.html内容后，直接成功生效。
- 修改default.conf 文件需要重启容器：`docker restart 容器id` 才能生效。

## 总结

以上为个人经验，希望能给大家一个参考，也希望大家多多支持脚本之家。

原文链接：[Docker目录映射方式](https://blog.csdn.net/m0_54850825/article/details/126616172)  
本文来自互联网用户投稿，该文观点仅代表作者本人，不代表本站立场。本站仅提供信息存储空间服务，不拥有所有权，不承担相关法律责任。如若内容造成侵权/违法违规/事实不符，请将相关资料发送至 reterry123@163.com 进行投诉反馈，一经查实，立即处理！