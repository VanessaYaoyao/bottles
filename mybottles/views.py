from django.shortcuts import render, redirect
# Create your views here.
from mybottles.models import bottle_user, bottles, finders, EmailVerifyRecord
from .forms import BottleUserForm, RegisterForm, ForgetForm
from django.core import serializers
from django.http import JsonResponse, HttpResponse
from django.core.serializers.json import json
from bottles.settings import EMAIL_FROM
from random import Random
from django.core.mail import send_mail
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage


def index(request):
    return render(request, 'index.html')


def login(request):
    if request.method == 'POST':
        login_form = BottleUserForm(request.POST)
        error = '验证码输入错误！'
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = bottle_user.objects.get(username=username)
                if user.is_active == 0:
                    error = '您尚未激活，请前往邮箱验证!'
                    email = user.email
                    send_email_code(email, 'register')
                    return render(request, 'login.html', locals())
                else:
                    if user.password == password:
                        request.session['is_login'] = True
                        request.session['user_id'] = user.id
                        request.session['user_name'] = user.username
                        return redirect('index')
                    else:
                        error = '密码输入错误！'
                        return render(request, 'login.html', locals())
            except:
                error = '用户名不存在！'
                return render(request, 'login.html', locals())

    login_form = BottleUserForm()
    return render(request, 'login.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        return redirect("index")
    else:
        request.session.flush()
        return redirect('index')


def personal_center(request):
    username = request.session.get('user_name')
    user = bottle_user.objects.get(username=username)
    user_dict = {'user': user}
    return render(request, 'personal_center.html', user_dict)


def edit_information(request):
    username = request.session.get('user_name')
    user = bottle_user.objects.get(username=username)
    avatar = request.FILES.get('avatar')
    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')
        sex = request.POST.get('sex')

        if name and description and sex:
            user.sex = sex
            user.description = description
            user.name = name
            user.avatar = avatar
            user.save()
            return redirect('personal_center')
        else:
            error = {'error': '填写的内容不能为空！'}
            return render(request, 'edit_information.html', error)
    else:
        return render(request, 'edit_information.html')


def change_password(request):
    username = request.session.get('user_name')
    user = bottle_user.objects.get(username=username)
    real_password = user.password
    if request.method == "POST":
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')
        if old_password == '' or new_password1 == '' or new_password2 == '':
            error = {'error': '填写内容不能为空！'}
            return render(request, 'change_password.html', error)
        else:
            if new_password2 != new_password1:
                error = {'error': '两次密码不相同！'}
                return render(request, 'change_password.html', error)
            else:
                if old_password != real_password:
                    error = {'error': '旧密码填写错误！'}
                    return render(request, 'change_password.html', error)
                else:
                    user.password = new_password1
                    user.save()
                    return redirect('personal_center')
    else:
        return render(request, 'change_password.html')


def salvage(request):
    return render(request, 'salvage.html')


def throw_one(request):
    if request.method == "POST":
        content = request.POST.get('content')
        if content == '':
            error = {'error': '请输入内容！'}
            return render(request, 'throw_one.html', error)
        else:
            owner = request.session.get('user_name')
            bottles.objects.create(content=content, owner=owner)
            return redirect('salvage')
    else:
        return render(request, 'throw_one.html')


def find_one(request):
    if request.method == "POST":
        reply = request.POST.get('reply')
        if reply == '':
            error = {'error': '回复内容不能为空！'}
            return render(request, 'find_one.html', error)
        else:
            replier = request.session.get('user_name')
            rand_ids = request.session.get('rand_ids')
            find_bottles = bottles.objects.get(id__in=rand_ids)
            find_bottles.reply = reply
            find_bottles.replier = replier
            find_bottles.is_replied = 1
            find_bottles.save()
            return redirect('salvage')
    else:
        username = request.session.get('user_name')
        import random
        count = bottles.objects.all().values('id')
        count_list = list(count)
        all_bottle_id = []  # 所有瓶子的id
        for i in count_list:
            id = i['id']
            all_bottle_id.append(id)

        found = finders.objects.filter(finder=username).values('thebottle_id')
        found_list = list(found)
        found_bottle_id = []  # 已被该用户捞起的瓶子的id
        for j in found_list:
            id = j['thebottle_id']
            found_bottle_id.append(id)

        replied = bottles.objects.filter(is_replied=1).values('id')
        replied_list = list(replied)
        replied_bottle_id = []  # 已被回复的瓶子id
        for i in replied_list:
            id = i['id']
            replied_bottle_id.append(id)

        owned = bottles.objects.filter(owner=username).values('id')
        owned_list = list(owned)
        owned_bottled_id = []  # 该用户自己扔出的瓶子id
        for i in owned_list:
            id = i['id']
            owned_bottled_id.append(id)

        id_list = []  # 在所有的瓶子中去除1已被回复的2该用户自己的3该用户捞起过的
        for m in all_bottle_id:
            if (m not in found_bottle_id) and (m not in replied_bottle_id) and (m not in owned_bottled_id):
                id_list.append(m)

        if id_list:
            rand_ids = random.sample(id_list, 1)
            find_bottle = bottles.objects.get(id__in=rand_ids)
            request.session['content'] = find_bottle.content
            request.session['rand_ids'] = rand_ids
            finders.objects.create(finder=username, thebottle=find_bottle)
            return render(request, 'find_one.html')
        else:
            return render(request, 'find_none.html')



def mybottles(request):
    username = request.session.get('user_name')

    mythrow = bottles.objects.filter(owner=username).values('id', 'content', 'reply', 'replier')
    throw_num = 1
    for i in mythrow:
        i['throw_num']=throw_num
        throw_num+=1
    myreply = bottles.objects.filter(replier=username).values('content', 'reply', 'owner')
    reply_num = 1
    for i in myreply:
        i['reply_num']=reply_num
        reply_num+=1
    myfind = finders.objects.filter(finder=username).values('thebottle__content', 'thebottle__owner')
    find_num = 1
    for i in myfind:
        i['find_num']= find_num
        find_num+=1
    whole = list(mythrow)+list(myreply)+list(myfind)

    paginator = Paginator(whole, 6)

    if request.method == "GET":
        page = request.GET.get('page')
        try:
            whole= paginator.page(page)
        except (PageNotAnInteger,InvalidPage,EmptyPage):
            # 有错误, 返回第一页。
            whole = paginator.page(1)
    return render(request, 'mybottles.html', locals())


def bottle_delete(request, id):
    norely_bottle = bottles.objects.get(id=id)
    norely_bottle.delete()
    return redirect('mybottle')


def its_profile(request, username):
    user = bottle_user.objects.get(username=username)
    user_dict = {'user': user}
    return render(request, 'its_profile.html', user_dict)


def random_str(randomlength=8):
    randomstr = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        randomstr += chars[random.randint(0, length)]
    return randomstr


def send_email_code(email, send_type):
    code = random_str()
    email_record = EmailVerifyRecord()
    # 将给用户发的信息保存在数据库中
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()
    send_title = ''
    send_body = ''
    # 如果为注册类型
    if send_type == "register":
        send_title = "注册激活链接"
        send_body = "请点击下面的链接激活你的账号:http://127.0.0.1:8000/mybottles/activate/{0}".format(code)
        # 发送邮件
        send_mail(send_title, send_body, EMAIL_FROM, [email])
    if send_type == 'forget':
        send_title = "重置密码链接"
        send_body = "请点击下面的链接重置密码:http://127.0.0.1:8000/mybottles/reset_password/{0}".format(code)
        # 发送邮件
        send_mail(send_title, send_body, EMAIL_FROM, [email])


def activate(request, code):
    if code:
        email_ver_list = EmailVerifyRecord.objects.filter(code=code)
        if email_ver_list:
            email_ver = email_ver_list[0]
            email = email_ver.email
            user = bottle_user.objects.get(email=email)
            user.is_active = 1
            user.save()
            return redirect('login')


def reset_password(request, code):
    if code:
        if request.method == 'POST':
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            if password1 != password2:
                error = {'error': '两次输入的密码不相同！'}
                return render(request, 'reset_password.html', locals())
            else:
                email_ver_list = EmailVerifyRecord.objects.filter(code=code)
                if email_ver_list:
                    email_ver = email_ver_list[0]
                    email = email_ver.email
                    user = bottle_user.objects.get(email=email)
                    user.password = password1
                    user.save()
                    return redirect('login')
        else:
            return render(request, 'reset_password.html', locals())


def register(request):
    if request.session.get('is_login', None):
        # 登录状态不允许注册。
        return redirect("/index/")
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        description = request.POST.get('description')
        avatar = request.FILES.get('avatar')
        message = "请检查填写的内容！"
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            sex = register_form.cleaned_data['sex']
            name = register_form.cleaned_data['name']
            if password1 != password2:
                message = "两次输入的密码不同！"
                return render(request, 'register.html', locals())
            else:
                same_name_user = bottle_user.objects.filter(username=username)
                same_email = bottle_user.objects.filter(email=email)
                if same_name_user:
                    message = '用户已经存在，请重新选择用户名！'
                    return render(request, 'register.html', locals())
                if same_email:
                    message = '该邮箱已被注册！'
                    return render(request, 'register.html', locals())
                new_user = bottle_user.objects.create()
                new_user.username = username
                new_user.name = name
                new_user.password = password1
                new_user.description = description
                new_user.sex = sex
                new_user.email = email
                new_user.is_active = 0
                new_user.avatar = avatar
                new_user.save()
                send_email_code(email, 'register')

                return HttpResponse('请前往邮箱验证!')
    register_form = RegisterForm()
    return render(request, 'register.html', locals())


def forget_password(request):
    if request.method == 'POST':
        forget_form = ForgetForm(request.POST)
        message = '验证码填写错误！'
        if forget_form.is_valid():
            email = forget_form.cleaned_data['email']
            user = bottle_user.objects.filter(email=email)
            if user:
                send_email_code(email, 'forget')
                return HttpResponse('请前往邮箱验证！')
            else:
                message = '该邮箱尚未注册！'
                return render(request, 'forget_password.html', locals())
    forget_form = ForgetForm()
    return render(request, 'forget_password.html', locals())
