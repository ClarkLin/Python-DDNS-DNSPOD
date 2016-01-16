#Python-DDNS-DNSPOD

##编写脚本目的
最近尝试使用VNC进行远程控制，但由于VNC Server是使用ADSL拨号上网，重启拨号或断网后IP变更，无法使用IP进行连接。所以想到结合[DNSpod.cn](http://www.dnspod.cn)的域名解析服务，使用子域名来代替IP从而连接VNC Server。

##编写环境
系统环境: Mac OSX 10.10.5  
软件环境: PyCharm 4.5; Python 2.7.10; 

##参考网站
DNSPOD官方API参考: https://github.com/DNSPod/dnspod-python  
Python脚本实现DNSPod DNS动态解析域名: http://www.jb51.net/article/61146.htm		  

##软件原理
不停检查adsl用户当前ip地址是否与dnspod账户里子域名的A记录一致，如果不一致则更新域名的A记录，如果没有子域名记录则添加。

##使用说明
由于检测更新的是子域名，当初的构想是用子域名来命名脚本名称。例如主域名为domain.com，子域名为adsl1.domain.com，则脚本名称为adsl1.pyw。而另一台机只需把脚本名字改为adsl2.pyw再运行，就会自动生成一个新的子域名A记录：adsl2.domain.com --> xx.xx.xx.xx

所以只要修改脚本名称为子域名，并需要修改脚本里面以下地方即可工作：  

```python
username = 'Your Email Here'  
password = 'Your Password Here'  
domain = [u'Your Maindomain Here']  
```

“Your Email Here”改为你的dnspod账号；  
“Your Password Here”改为你的dnspod账号密码；  
“Your Maindomain Here”改为你需要修改A记录的主域名，就像上面例子的domain.com


脚本修改后便可以通过

```sh
python subdomain.pyw
```
开始运行此程序。完成更新后便可以通过 adsl1.domain.com来访问VNC Server。

##配置开机启动
###linux 环境下
配置/etc/rc.local文件，在最后加入  

```sh
/usr/bin/python /script_path/subdomain.pyw &
```
让脚本随系统启动时后台运行。

###windows 环境下
添加脚本快捷方式，把脚本快捷方式放入 开始-》程序-》启动 文件夹中，让脚本随开机启动时运行。（也可以制作vbs文件启动运行，但自己还未编写。）

##存在问题和展望：
这个程序是本人在网上参考各方面资料东拼西凑编写的，也算是本人第一个python小程序，还存在一些问题，还请大家见笑和给出宝贵的意见。  
1. 暂时只在winXP和Macbook上面做过测试，其他系统可以有bug。  
2. 使用子域名作为脚本这个方法还有待改善，其实可以通过ConfigParser读取配置文件获取子域名，dnspod账号等信息。但自己还是觉一个文件能解决的问题暂时不用两个文件处理。  
3. 暂时想到以上两点，有空再补。