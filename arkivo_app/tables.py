import django_tables2 as tables
from .models import *

class CompanySystemTable(tables.Table):
    class Meta:
        model = CompanySystem
        exclude = ('id','updated_at','created_at','company')
        attrs = {'class': 'table table-responsive table-hover'}



class CompanyUserTable(tables.Table):
    Name = tables.Column(accessor='user.get_full_name',verbose_name='Name')
    Email = tables.EmailColumn(accessor='user.email')
    Active = tables.BooleanColumn(accessor='user.is_active',)
    Role = tables.ManyToManyColumn(accessor='user.groups',verbose_name='Role')

    class Meta:
        model = UserProfile
        exclude = ('id','updated_at','created_at','company','user',)
        attrs = {'class': 'table table-responsive table-hover'}


class CompanyProjectTable(tables.Table):
    survey_template = tables.Column(accessor='survey_template.name', verbose_name='Survey Template')

    class Meta:
        model = Project
        exclude = ('id', 'updated_at', 'created_at', 'company')
        attrs = {'class': 'table table-responsive table-hover'}
