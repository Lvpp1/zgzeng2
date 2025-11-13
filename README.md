## 帮助信息

使用`python oneforall.py --help`

```
D:\yd_project>python3 run.py --help

      __                                     __               .___
_/  |_  ____   ____   ____  ____   _____/  |_   ___.__. __| _/
\   __\/ __ \ /    \_/ ___\/ __ \ /    \   __\ <   |  |/ __ |
 |  | \  ___/|   |  \  \__\  ___/|   |  \  |    \___  / /_/ |
 |__|  \___  >___|  /\___  >___  >___|  /__|    / ____\____ |
           \/     \/     \/    \/     \/        \/         \/




    获取各单位评分情况:              python run.py -c
    获取展示各二级单位 ID:           python run.py -s
    获取各单位实名用户终端:           python run.py -i
    获取安装御点全量数据详情:         python run.py -a
    获取未处理风险涉及的终端:         python run.py -g
    获取未修复漏洞涉及的终端:         python run.py -v
    获取网络攻击涉及终端详情:         python run.py -n 20240101 20240102

usage: run.py [-h] [-c] [-s] [-a] [-g] [-v] [-i] [-n START_DATE END_DATE]

腾讯御点各数据获取参数

optional arguments:
  -h, --help            show this help message and exit
  -c, --core            获取各单位评分情况
  -s, --show            展示各二级单位ID
  -a, --all             获取全集团安装御点的用户详情
  -g, --virus           获取未处理风险涉及的终端
  -v, --vuls            获取未修复漏洞涉及的终端
  -i, --installdetail   获取各单位实名用户终端
  -n START_DATE END_DATE, --GetAttack START_DATE END_DATE
                        获取网络攻击涉及终端详情 参数格式:20241001, 例如python run.py -n 20241001 20241001
```

数据获取存储位置

![image-20241016113500467](C:\Users\ABC\AppData\Roaming\Typora\typora-user-images\image-20241016113500467.png)

![image-20241016113513005](C:\Users\ABC\AppData\Roaming\Typora\typora-user-images\image-20241016113513005.png)# zgzeng

