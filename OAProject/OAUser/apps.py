from django.apps import AppConfig


# 继承自django自带的AppConfig类

class OauserConfig(AppConfig):
    # 如果没有指定主键类型，Django 将使用 BigAutoField类型作为默认主键类型
    default_auto_field = 'django.db.models.BigAutoField'
    # 应用程序的名称设置为 'OAUser'，在 URL 配置中有用
    name = 'OAUser'
