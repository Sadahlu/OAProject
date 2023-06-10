import random
from . import forms
from OAUser.models import Users, Income, Pay
# render() 函数用于渲染 templates,并返回 HttpResponse 对象，locals()函数返回当前作用域(函数)中的变量，传给要渲染的html模板
# redirect() 函数:重定向到新的URL(页面跳转),返回 HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import redirect
from pymysql import DatabaseError
from django.db import transaction
import time
from pyecharts.charts import Bar
from pyecharts import options


# Create views
# request对象代表一个HTTP请求(包含请求的大部分信息),可以直接在视图函数使用。
# request.method: POST DELETE GET PUT
# 会话消息字典键：'is_login' 'user_uid' 'user_uname'(login时已创建)


# 主页面/index/，根据用户是否登录来决定显示登录页还是主页面,request.session.get() 方法从会话中读取一个键对应的值。
def index(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    return render(request, 'login/index.html')


# 个人信息页面/personal/
def personal(request):
    uid_nums = request.session['user_uid']
    user_list = Users.objects.get(uid=uid_nums)
    return render(request, 'login/personal-info.html', {"user": user_list})


# 主页面根据POST类型是收入or支出，跳转到/income/页面 or /pay/页面
def insertRecord(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    # 根据post请求实例化一个收入表单
    income_form = forms.IncomeForm(request.POST)
    if income_form.is_valid():
        # 表单如果有效，获取（记录）信息（cleaned_data 是字典,包含此表单的所有字段）
        iType = income_form.cleaned_data.get('iType')
        iMoney = income_form.cleaned_data.get('iMoney')
        iRemark = income_form.cleaned_data.get('iRemark')
        iTime = income_form.cleaned_data.get('iTime')
        # 调用django中表的objects.create（）方法，如果是收入添加到收入表，如果是支出添加到支出表中
        if iType == "收入":
            Income.objects.create(iType=iType,
                                  iMoney=iMoney,
                                  iRemark=iRemark,
                                  iTime=iTime)
        else:
            Pay.objects.create(pType=iType,
                               pMoney=iMoney,
                               pRemark=iRemark,
                               pTime=iTime)
    if iType == "收入":
        return redirect('/income/')
    else:
        return redirect('/pay/')


# 收入页面/income/
def income(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    # 搜索功能
    key = request.GET.get("key")
    if key is None:
        # 返回所有记录
        new_list = Income.objects.all()
    else:
        # 返回搜索记录,__contains实现模糊匹配
        new_list = Income.objects.filter(iRemark__contains=key)

    # 分页
    # 获取GET请求中的page参数:
    page = request.GET.get("page")
    # 如果page不存在,则默认为1:
    if page is None:
        page = 1
    # 如果存在（当前页）,则强制转换为int类型:
    else:
        page = int(page)
    # 收入条数 除10并向上取整（整除+1）
    page_count = (len(new_list) - 1) // 10 + 1
    # page_count 转换为可迭代对象
    page_count = range(1, page_count + 1)
    # 根据page和每页记录数,对new_list进行,获取第page页的数据
    new_list = new_list[page * 10 - 10: page * 10]
    # locals()返回当前函数中的变量，作为context传给要渲染的html模板
    return render(request, 'login/income.html', locals())


def update_income(request):
    update_id = request.GET.get("iId")
    if request.method == "POST":
        # 暂时记录
        new_type = request.POST.get('iType')
        new_money = request.POST.get('iMoney')
        new_remark = request.POST.get('iRemark')
        new_time = request.POST.get('iTime')
        # 在收入表中获取匹配的单个记录，并对这个对象进行更新
        update_obj = Income.objects.get(iId=update_id)
        update_obj.iType = new_type
        update_obj.iMoney = new_money
        update_obj.iRemark = new_remark
        update_obj.iTime = new_time
        # 保存该条收入
        update_obj.save()
        return redirect('/income/')
    # 还没POST新数据时，将ret（记录该条收入信息）作为context传给要渲染的update_income.html
    ret = Income.objects.get(iId=update_id)
    return render(request, 'login/update_income.html', {'ret': ret})


def del_income(request):
    # 获取iId
    income_id = request.GET.get("iId")
    # 在Income表中找到该条收入并删除
    Income.objects.filter(iId=income_id).delete()
    # 重新跳转到收入页面
    return redirect('/income/')


def pay(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    key = request.GET.get("key")
    if key is None:
        new_list1 = Pay.objects.all()
    else:
        new_list1 = Pay.objects.filter(pRemark__contains=key)
    # 分页
    # 获取GET请求中的page参数:
    page = request.GET.get("page")
    # 默认为1
    if page is None:
        page = 1
    else:
        page = int(page)
    # 1-总页数的可迭代对象
    page_count = (len(new_list1) - 1) // 10 + 1
    page_count = range(1, page_count + 1)
    # 切片截取当页的支付数据
    new_list1 = new_list1[page * 10 - 10: page * 10]
    return render(request, 'login/pay.html', locals())


def update_pay(request):
    edit_id = request.GET.get("pId")
    if request.method == "POST":
        # 暂时存储
        new_ptype = request.POST.get('pType')
        new_pmoney = request.POST.get('pMoney')
        new_premark = request.POST.get('pRemark')
        new_ptime = request.POST.get('pTime')
        # 在Pay表中获取该对象并更新数据
        edit_obj = Pay.objects.get(pId=edit_id)
        edit_obj.pType = new_ptype
        edit_obj.pMoney = new_pmoney
        edit_obj.pRemark = new_premark
        edit_obj.pTime = new_ptime
        edit_obj.save()
        return redirect('/pay/')
    # 还没POST新数据时，将reet（记录该条支出信息）作为context传给要渲染的update_pay.html
    reet = Pay.objects.get(pId=edit_id)
    return render(request, 'login/update_pay.html', {'reet': reet})


def del_pay(request):
    pay_id = request.GET.get("pId")
    Pay.objects.filter(pId=pay_id).delete()
    return redirect('/pay/')


def chart(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    # 横坐标，表示日期
    x = []
    # 纵坐标
    y1 = []
    y2 = []
    # 最近十五天的总收入和总支出
    s1 = []
    s2 = []

    i_dir = {}
    p_dir = {}

    time_sprite = time.time()  # 返回当前时间的时间戳（1970纪元后经过的浮点秒数）
    time_sprite -= 14 * 24 * 60 * 60  # 当前时间减去14天
    for i in range(15):
        # 得到当前的年月日信息
        local = time.localtime(time_sprite)
        year = local.tm_year
        month = local.tm_mon
        day = local.tm_mday
        #
        date_str = "%d-%02d-%02d" % (year, month, day)

        # 最近15天的每天的值都初始化为0
        i_dir[date_str] = 0
        p_dir[date_str] = 0

        # 日期一天天叠加，并存在x中
        x.append(date_str)
        time_sprite += 24 * 60 * 60

    # 获取收入表里面的所有信息
    income_list = Income.objects.all()
    for item in income_list:
        # 获取每条收入的日期
        time_str = str(item.iTime)
        # 判断收入日期是否在最近15天内，若在，则计算当天收入金额总和
        if time_str in i_dir:
            i_dir[time_str] += item.iMoney
    # 获取支出表里面的所有信息
    pay_list = Pay.objects.all()
    for item in pay_list:
        # 获取每条支出的日期
        time_str = str(item.pTime)
        # 判断支出日期是否在最近15天内，若在，则计算当天支出金额总和
        if time_str in p_dir:
            p_dir[time_str] += item.pMoney

    for day in x:
        # 近15天，每个日期的总收入/支出添加到y1/y2
        y1.append(float(i_dir[day]))
        y2.append(float(p_dir[day]))
    # 实例化一个条形图
    bar = Bar()
    # add_xaxis() 是添加x轴数据到条形图(bar chart)的方法
    bar.add_xaxis(xaxis_data=x)
    # add_yaxis（）是添加y轴数据到条形图(bar chart)的方法
    bar.add_yaxis(series_name='收入', y_axis=y1)
    bar.add_yaxis(series_name='支出', y_axis=y2)
    # 添加options，用bar的set_global_opts（）方法设置条形图全局标题
    bar.set_global_opts(title_opts=options.TitleOpts(title='最近15天的收入与支出'))
    # bar.render()方法生成HTML文件
    bar.render('temp.html')
    # 将 html 字符串按照 "</body>" 进行切分，取切分结果的第一个元素作为新的 html 字符串（只提取 HTML 代码的主体部分）
    html = ""
    with open("temp.html") as f:
        html = f.read()
    html = html.split("</body>")[0]

    # 读取HTML并更新收入和支出的总计
    s1 += y1  # 最近十五天的总收入
    s2 += y2  # 最近十五天的总支出

    # 为饼图创建数据
    names = ['收入', sum(s1)]
    values = ['支出', sum(s2)]
    data = []
    for name, value in names, values:
        datadict = {
            'name': name,
            'value': value
        }
        data.append(datadict)
    return render(request, 'login/chart.html', locals())

# 视图对数据库进行多项更改，并且修改个人信息时希望确保全部成功或全部失败时，防止提交部分更改（仅影响数据库），数据的一致性和完整性
# 修改个人信息
@transaction.atomic
def UpdatePro(request):
    # 接收输入参数(更新)
    uame = request.GET.get('uname')
    upwd = request.GET.get('upwd')
    uemail = request.GET.get('uemail')
    utel = request.GET.get('utel')

    try:
        # __exact精确匹配的比较运算符，first()方法来获取第一个符合条件的用户对象
        user = Users.objects.filter(uname__exact=uame).first()
        user.uname = uame
        user.upwd = upwd
        user.uemail = uemail
        user.utel = utel
        # 保存
        user.save()
    # 捕捉数据库连接失败，操作错误
    except DatabaseError as e:
        print(e)

    return redirect("/personal/")


def login(request):
    if request.session.get('is_login', None):  # 不允许重复登录
        return redirect('/index/')
    if request.method == 'POST':
        # 实例化一个表单类forms.UserForm,并传入请求的POST数据
        login_form = forms.UserForm(request.POST)
        message = '请检查填写的内容！'
        # is_valid() 方法验证表单数据是否有效
        if login_form.is_valid():
            # 表单如果有效，获取用户名密码（cleaned_data 是字典,包含此表单的所有字段）
            uname = login_form.cleaned_data.get('uname')
            upwd = login_form.cleaned_data.get('upwd')
            # 从用户表中获取用户名为uname的单个记录（有则传给user）
            try:
                user = Users.objects.get(uname=uname)
            except:
                message = '用户不存在！'
                return render(request, 'login/login.html', locals())

            if user.upwd == upwd:
                request.session['is_login'] = True
                request.session['user_uid'] = user.uid
                request.session['user_uname'] = user.uname
                return redirect('/index/')
            else:
                message = '密码不正确！'
                return render(request, 'login/login.html', locals())
        else:
            return render(request, 'login/login.html', locals())

    # 否则实例化一个空登录表单（请求方式是GET时）, 并把表单数据传给登录模板, 渲染登录表单。
    login_form = forms.UserForm()
    return render(request, 'login/login.html', locals())


def register(request):
    if request.session.get('is_login', None):
        return redirect('/login/')

    if request.method == 'POST':
        # 通过POST请求的数据实例化一个注册表单
        register_form = forms.RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():
            uname = register_form.cleaned_data.get('uname')
            upwd1 = register_form.cleaned_data.get('upwd1')
            upwd2 = register_form.cleaned_data.get('upwd2')
            uemail = register_form.cleaned_data.get('uemail')
            utel = register_form.cleaned_data.get('utel')
            usex = register_form.cleaned_data.get('usex')

            if upwd1 != upwd2:
                message = '两次输入的密码不同！'
                return render(request, 'login/register.html', locals())
            else:
                # 将其添加到用户表，filter()会返回所有匹配的记录（过滤）
                same_name_user = Users.objects.filter(uname=uname)
                if same_name_user.exists():
                    message = '用户名已经存在'
                    return render(request, 'login/register.html', locals())
                same_email_user = Users.objects.filter(uemail=uemail)
                if same_email_user.exists():
                    message = '该邮箱已经被注册了！'
                    return render(request, 'login/register.html', locals())
                print(uname, upwd1, uemail, utel, usex)
                Users.objects.create(uname=uname,
                                     upwd=upwd1,
                                     uemail=uemail,
                                     utel=utel,
                                     usex=usex)
                return redirect('/login/')
        else:
            return render(request, 'login/register.html', locals())
    # 否则实例化一个空注册表单（请求方式是GET时）, 并把注册表单的数据传给 注册模板,
    register_form = forms.RegisterForm()
    return render(request, 'login/register.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说，跳转到登陆页面
        return redirect("/login/")
    request.session.flush()
    # 即清除请求的会话
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return redirect("/login/")
