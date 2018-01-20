## 北京小客车指标结果查询
* 本程序是基于 python3写成,需要安装python3。
* 需要安装一些依赖

```
pip install pyquery
pip install requests
pip install urllib
```

* 需要在脚本中下面的变量替换成自己的用户名密码，[点我注册打码兔](http://dama2.com/Index/register)

```
dmtuser='输入打码兔用户名'
dmtpassword='请输入打码兔密码'
phone='北京摇号平台手机号'
password='北京摇号平台密码'
```

脚本是需要自动输入验证码，如果需要手动自己输入验证码。需要修改代码,具体看bjhjyd.py。


脚本执行方式

```
python3 bjhjyd.py
```
结果
![结果](https://raw.githubusercontent.com/liuyongqing1/bjhjyd/master/result.png)