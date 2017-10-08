from django.conf.urls import url, include

from . import views

app_name = 'arkivo_app'
urlpatterns = [
    url(r'^settings/projects/add/', views.CompanyProjectsAddList, name='company_projects_add'),
    url(r'^settings/projects/edit/', views.CompanyProjectsEditList, name='company_projects_edit'),
    url(r'^settings/projects/', views.CompanyProjectsShowList, name='company_projects'),
    url(r'^settings/users/add/', views.CompanyUsersShowList, name='company_users_add'),
    url(r'^settings/users/edit/', views.CompanyUsersShowList, name='company_users_edit'),
    url(r'^settings/users/', views.CompanyUsersShowList, name='company_users'),
    url(r'^settings/systems/add/', views.CompanySystemsAddList, name='company_systems_add'),
    url(r'^settings/systems/edit/', views.CompanySystemsEditList, name='company_systems_edit'),
    url(r'^settings/systems/', views.CompanySystemsShowList, name='company_systems'),
    url(r'^settings/edit/', views.CompanyEditDetail, name='company_edit'),
    url(r'^settings/', views.CompanyShowDetail, name='company'),
    url(r'^(?P<project_name>[^/]+)/survey/$',views.SurveyShow, name = 'survey'),
    url(r'^(?P<project_name>[^/]+)/survey/(?P<section_name>[^/]+)/$', views.SurveyShow, name= 'survey_sec'),
    url(r'^(?P<project_name>.+)/survey/(?P<section_name>[^/].+)/(?P<category_name>[^/].+)/$', views.SurveyShow, name= 'survey_sec_cat'),
    url(r'^$', views.index, name='index'),
]


urlpatterns += [
    url(r'^accounts/', include('django.contrib.auth.urls')),
]

