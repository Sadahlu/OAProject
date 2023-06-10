from django.db import models


# 继承自 models.Model 的类,
# 可使用YourModel.objects.all() 获取所有记录,YourModel.objects.create() 创建记录,
# YourModel.objects.get() 获取单个记录，YourModel.objects.filter()会返回所有匹配的记录
# 用户表
class Users(models.Model):
    uid = models.AutoField(primary_key=True, auto_created=True)
    uname = models.CharField(max_length=30)
    upwd = models.CharField(max_length=30, unique=True)
    usex = models.CharField(max_length=30)
    uemail = models.EmailField()
    utel = models.BigIntegerField()


# 收入表
class Income(models.Model):
    iId = models.AutoField(primary_key=True)
    iType = models.CharField(max_length=30)  # 类型（借入、收入）
    iMoney = models.DecimalField(max_digits=10, decimal_places=2)  # 金额
    iRemark = models.CharField(max_length=55)  # 备注
    iTime = models.DateField()  # 时间


# 支出表
class Pay(models.Model):
    pId = models.AutoField(primary_key=True)
    pType = models.CharField(max_length=30)  # 类型（借出、支出）
    pMoney = models.DecimalField(max_digits=10, decimal_places=2)  # 金额
    pRemark = models.CharField(max_length=55)  # 备注
    pTime = models.DateField()  # 时间
