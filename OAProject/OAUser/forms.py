from django import forms
from captcha.fields import CaptchaField

# UserForm类，继承自django自带的Form类


class UserForm(forms.Form):
    # CharField：指定字段类型是字符
    # label：字段显示的名称
    # form-control 类能够很好的规范和整齐你的表单样式，让输入框具有 Bootstrap 中默认的风格。

    # widget：指定widget（表单元素），这里选择forms.Text会渲染为Input<input type="text" class="form-control">
    # attrs：给文本输入框添加样式，这里类名是form - control，输入框占位提示为Username，自动获取焦点（用户可以直接开始输入,无需额外点击。）
    uname = forms.CharField(label="用户名", max_length=128,
                            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Username", 'autofocus': ''}))
    # 选择forms.PassWordInput会渲染为<input type="password" class="form-control">，输入内容是密码样式,而不是明文。
    upwd = forms.CharField(label="密码", max_length=256,
                           widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "Password"}))
    # 验证码字段，CaptchaField类型
    captcha = CaptchaField(label='验证码')


class RegisterForm(forms.Form):
    gender = (
        ('male', "男"),
        ('female', "女"),
    )
    uname = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    upwd1 = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    upwd2 = forms.CharField(label="确认密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    # EmailField:指定字段类型是 EmailField（会验证用户输入的是否是合法的email格式）,用来接受email地址。
    # EmailInput会渲染为 < input type = "email"  class="form-control">
    uemail = forms.EmailField(label="邮箱地址", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    utel = forms.CharField(label="电话号码", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    # choices实现下拉选择, 接受"男"或"女"两个值。
    usex = forms.ChoiceField(label='性别', choices=gender)
    captcha = CaptchaField(label='验证码')


class IncomeForm(forms.Form):
    iType = forms.CharField(label="类型", max_length=30)  # 类型（借入、收入）
    # DecimalField 表示这是一个接受十进制浮点数的字段。
    # max_digits指定最多可以输入10个数字,decimal_places指定小数点后最多保留2位小数
    iMoney = forms.DecimalField(label="金额", max_digits=10, decimal_places=2)  # 金额
    iRemark = forms.CharField(label="备注", max_length=55)  # 备注
    # 设置最小允许日期和当前日期
    iTime = forms.DateField(label="时间")  # 时间


class PayForm(forms.Form):
    pType = forms.CharField(label="类型", max_length=30)  # 类型（借出、支出）
    pMoney = forms.DecimalField(label="金额", max_digits=10, decimal_places=2)  # 金额
    pRemark = forms.CharField(label="备注", max_length=55)  # 备注
    # 设置最小允许日期和当前日期
    pTime = forms.DateField(label="时间")  # 时间
