```
yd_project
|   .idea
|   __pycache__
|   code_dir     	缓存识别的图片验证码
|   common          各个模块需要公用的逻辑代码，包括登录代码，装饰器等
|   data     		输出的各类数据
|   docs			docs文档说明
|   logs			工具运行的日志
|   moudle    		各个数据统计的功能模块
|   company			集团各个单位
|   CooperativeUnits合作单位
|  	README.md       文档说明
|   UnitInfo.txt 	unitid.py结果存储文件
|   requirements.txt 依赖项
|   run.py     		 工具入口
|   temp     		 缓存请求headers
|	unitid.py		 获取各个单位的id
+---common
|   login_demo.py	 登录逻辑
|   my_logging.py    日志配置
|   temp.py          装饰器，用于登录
|   unit.py

+---data 数据存储路径
|       Core 各单位评分情况存储
|       FullDate  安装御点全量数据详情
|       InstalltionDetail 各单位实名用户终端
|       NetworkAttackDetail 网络攻击涉及终端详情
|       VirusDetail 未处理风险涉及的终端
|       VulDetail 未修复漏洞涉及的终端
|       __init__.py
+---moudle 
|   |       Display.py
|   |       FullData.py
|   |       GetCore.py
|   |       GetNetworkAttackDetail.py
|   |       GetVirusDate.py
|   |      	GetVulDate.py
|   |		InstalltionDetail.py

```

