# IIS 10.0 详细错误 - 404.0 - Not Found

### HTTP 错误 404.0 - Not Found

#### 您要找的资源已被删除、已更名或暂时不可用。

#### 最可能的原因:

-   指定的目录或文件在 Web 服务器上不存在。
-   URL 拼写错误。
-   某个自定义筛选器或模块(如 URLScan)限制了对该文件的访问。

#### 可尝试的操作:

-   在 Web 服务器上创建内容。
-   检查浏览器 URL。
-   创建跟踪规则以跟踪此 HTTP 状态代码的失败请求，并查看是哪个模块在调用 SetStatus。有关为失败的请求创建跟踪规则的详细信息，请单击[此处](http://go.microsoft.com/fwlink/?LinkID=66439)。

#### 详细错误信息:

模块

   IIS Web Core

通知

   MapRequestHandler

处理程序

   StaticFile

错误代码

   0x80070002

请求的 URL

   http://127.0.0.1:8010/n/20120919/45111.html

物理路径

   D:\Webs\httpdocwww\n\20120919\45111.html

登录方法

   匿名

登录用户

   匿名

#### 详细信息:

此错误表明文件或目录在服务器上不存在。请创建文件或目录并重新尝试请求。

[查看详细信息 »](https://go.microsoft.com/fwlink/?LinkID=62293&IIS70Error=404,0,0x80070002,17763)