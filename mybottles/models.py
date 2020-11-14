from django.db import models
class bottle_user(models.Model):

    gender = (
        ('1', '男'),
        ('0', '女'),
    )

    username = models.CharField(max_length=128,default='用户名',verbose_name='用户名')
    password = models.CharField(max_length=256,verbose_name='密码')
    email = models.EmailField(verbose_name='邮箱')
    name = models.CharField(max_length=128,default='昵称',verbose_name='昵称')
    sex = models.IntegerField(choices=gender,verbose_name='性别',default=1)
    description = models.TextField(max_length=100,default='简介',verbose_name='简介')
    is_active = models.IntegerField(default=1,verbose_name='是否激活')
    avatar = models.ImageField(upload_to='avatar/%Y%m%d/', blank=True)

class bottles(models.Model):
    content = models.TextField(max_length=128,default='漂流瓶内容',verbose_name='漂流瓶内容')
    reply = models.TextField(max_length=128,blank=True,verbose_name='回复')
    owner = models.CharField(max_length=128,default='扔瓶子的人',verbose_name='扔瓶子的人')
    replier = models.CharField(max_length=128,blank=True,verbose_name='回复的人')
    is_replied = models.IntegerField(default=0, verbose_name='是否被回复')

class finders(models.Model):
    finder = models.CharField(max_length=128,default='打捞起瓶子的人')
    thebottle = models.ForeignKey(bottles,on_delete=models.CASCADE)


class EmailVerifyRecord(models.Model):
    # 验证码
    code = models.CharField(max_length=20, verbose_name=u"验证码")
    email = models.EmailField(max_length=50, verbose_name=u"邮箱")
    # 包含注册验证和找回验证
    send_type = models.CharField(verbose_name=u"验证码类型", max_length=10,
                                 choices=(("register", u"注册"), ("forget", u"找回密码")))
