# 1.在项目根目录中创建一个名为asgi.py的文件，并定义一个名为application的ASGI应用程序对象
# 与旧版的WSGI协议不同，ASGI可以处理异步（执行某个操作时不会阻塞当前线程的代码，它可以在等待某些操作完成的同时执行其他操作）
# 和长连接请求（在长连接请求中，客户端和服务器之间建立的连接可以在多次请求和响应之间重复使用，直到客户端主动关闭连接）
# 2.还未配置
import os

from django.core.asgi import get_asgi_application

# 设置了DJANGO_SETTINGS_MODULE环境变量，指定Django应该使用哪个settings模块
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
# 定义了一个名为application的ASGI应用程序对象，它使用get_asgi_application()函数从settings.py文件中获取Django应用程序对象
application = get_asgi_application()
