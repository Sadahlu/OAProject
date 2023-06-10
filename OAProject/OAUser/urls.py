from django.contrib import admin
from django.urls import path, include
from OAUser import views
urlpatterns = (
    path('index/', views.index, name='index'),
    path('insertRecord/', views.insertRecord, name='insertRecord'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('personal/', views.personal, name='personal'),
    path('UpdatePro/', views.UpdatePro, name='UpdatePro'),
    path('income/', views.income, name='income'),
    path('pay/', views.pay, name='pay'),
    path('chart/', views.chart, name='chart'),
    path('update_income/', views.update_income, name='update_income'),
    path('del_income/', views.del_income, name='del_income'),
    path('del_pay/', views.del_pay, name='del_pay'),
    path('update_pay/', views.update_pay, name='update_pay'),
    # Django 内置的一个 URL 配置，提供了生成和验证验证码所需的视图和模板。
    path('captcha/', include("captcha.urls")),

)

# 导入url，并关联view

