from django.contrib import admin
# Register your models here.
from mybottles.models import *


class RegistersFilter(admin.SimpleListFilter):
    title = '账户状态'
    parameter_name = 'is_active'

    def lookups(self, request, model_admin):
        return (
            ('0', '未激活'),
            ('1', '已激活'),
        )

    def queryset(self, request, queryset):
        if self.value() == '0':
            return queryset.filter(is_active='0')
        elif self.value() == '1':
            return queryset.filter(is_active='1')


class SexFilter(admin.SimpleListFilter):
    title = "性别"
    parameter_name = 'sex'

    def lookups(self, request, model_admin):
        return (
            ('0', '女'),
            ('1', '男'),
        )

    def queryset(self, request, queryset):
        if self.value() == '0':
            return queryset.filter(sex='0')
        elif self.value() == '1':
            return queryset.filter(sex='1')


@admin.register(bottle_user)
class Registers(admin.ModelAdmin):
    list_display = ['username', 'email', 'name', 'is_active']
    search_fields = ('username', 'email')
    actions_selection_counter = True
    list_filter = (RegistersFilter, SexFilter)
    actions = ['is_active0', 'is_active1']

    def is_active0(self, request, queryset):
        row_updated = queryset.update(is_active=0)
        self.message_user(request, '修改了{}条字段'.format(row_updated))

    is_active0.short_description = '冻结账号'

    def is_active1(self, request, queryset):
        row_updated = queryset.update(is_active=1)
        self.message_user(request, '修改了{}条字段'.format(row_updated))

    is_active1.short_description = '激活账号'


class ReplyFilter(admin.SimpleListFilter):
    title = '是否被回复'
    parameter_name = 'is_replied'

    def lookups(self, request, model_admin):
        return (
            ('0', '未回复'),
            ('1', '已回复'),
        )

    def queryset(self, request, queryset):
        if self.value() == '0':
            return queryset.filter(is_replied='0')
        elif self.value() == '1':
            return queryset.filter(is_replied='1')


@admin.register(bottles)
class Bottles(admin.ModelAdmin):
    list_display = ['content', 'owner', 'reply', 'replier']
    search_fields = ('owner', 'replier')
    actions_selection_counter = True
    list_filter = (ReplyFilter,)
