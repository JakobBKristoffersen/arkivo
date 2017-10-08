from django.views import generic
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, HttpResponseRedirect,render_to_response,redirect
from django.http import HttpResponse
from django.template import loader

from django.contrib.auth.models import User
from django.core import serializers
from django.template.context_processors import csrf
from django.template import RequestContext  # For CSRF
from django.forms.formsets import formset_factory, BaseFormSet
from django.forms import modelformset_factory, BaseModelFormSet, inlineformset_factory
from django.views.generic import ListView,CreateView,UpdateView

from .models import *
from .forms import *
from .tables import *

@login_required
def index(request):
    current_user = request.user
    company = current_user.userprofile.get_active_company
    return render(request, 'arkivo_app/index.html',{
        'title': "Frontpage",
        'nav_url': 'index',
        'company': company,
    })

@login_required
def CompanyShowDetail(request, edit=False):
    current_user = request.user
    company = current_user.userprofile.get_active_company()
    display_static = True
    updated = False

    # check if edit is allowed
    allow_edit = True

    arg = request.build_absolute_uri()

    if allow_edit and edit:
        display_static= False

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CompanyForm(request.POST,instance=company)

        # check whether it's valid:
        if form.is_valid():
            display_static = True
            if form.has_changed():
                form.save()
                updated = True


    # if a GET (or any other method) we'll create a blank form
    else:
        form = CompanyForm(instance=company)

    return render(request, 'arkivo_app/company/detail.html', {
        'nav_url': 'arkivo_app:company',
        'company': company,
        'form': form,
        'display_static': display_static,
        'allow_edit': allow_edit,
        'updated': updated,
        'arg': arg,
    })

@login_required
def CompanyEditDetail(request):
    return CompanyShowDetail(request, edit=True)

@login_required
def CompanySystemsShowList(request, edit=False, extra=0):
    current_user = request.user
    company = current_user.userprofile.get_active_company()

    display_static = True
    updated = False

    # check if edit is allowed
    allow_edit = False
    if current_user.has_perm('arkivo_app.change_companysystem'):
        allow_edit = True

    if allow_edit and edit:
        display_static = False

    systems = CompanySystem.objects.filter(company = company)
    CompanySystemFormSet = modelformset_factory(CompanySystem,exclude=('id','company'),can_delete=True,extra=extra)
    if request.method == 'POST':
        formset = CompanySystemFormSet(
            request.POST,request.FILES,
            queryset=CompanySystem.objects.filter(company = company))
        if formset.is_valid() and formset.has_changed():
            for form in formset:
                form.instance.company = company
            formset.save()
            updated = True
            display_static = True
    else:
        formset = CompanySystemFormSet(queryset=CompanySystem.objects.filter(company=company))

    table = CompanySystemTable(systems)

    return render(request, 'arkivo_app/company/systems.html',{
        'nav_url': 'arkivo_app:company_systems',
        'formset': formset,
        'company': company,
        'systems': systems,
        'display_static': display_static,
        'allow_edit': allow_edit,
        'updated': updated,
        'table': table
    })

@login_required
def CompanySystemsEditList(request):
    request.session['add_count'] = 0
    return CompanySystemsShowList(request,edit=True)

@login_required
def CompanySystemsAddList(request):
    extra_count = request.session.get('add_count', 0)+1
    request.session['add_count'] = extra_count
    return CompanySystemsShowList(request,edit=True, extra=extra_count)


@login_required
def CompanyProjectsShowList(request, edit=False, extra=0):
    current_user = request.user
    company = current_user.userprofile.get_active_company()

    display_static = True
    updated = False

    # check if edit is allowed
    allow_edit = False
    if current_user.has_perm('arkivo_app.change_project'):
        allow_edit = True

    if allow_edit and edit:
        display_static = False

    projects = Project.objects.filter(company = company)
    CompanyProjectFormSet = modelformset_factory(Project,exclude=('id','company'),can_delete=True,extra=extra)
    if request.method == 'POST':
        formset = CompanyProjectFormSet(
            request.POST,request.FILES,
            queryset=Project.objects.filter(company = company))
        if formset.is_valid():
            display_static = True
            if formset.has_changed():
                for form in formset:
                    form.instance.company = company
                formset.save()
                updated = True


    else:
        formset = CompanyProjectFormSet(queryset=Project.objects.filter(company=company))

    table = CompanyProjectTable(projects)

    return render(request, 'arkivo_app/company/projects.html',{
        'nav_url': 'arkivo_app:company_projects',
        'formset': formset,
        'company': company,
        'projects': projects,
        'display_static': display_static,
        'allow_edit': allow_edit,
        'updated': updated,
        'table': table
    })

@login_required
def CompanyProjectsEditList(request):
    request.session['add_count'] = 0
    return CompanyProjectsShowList(request,edit=True)


@login_required
def CompanyProjectsAddList(request):
    extra_count = request.session.get('add_count', 0)+1
    request.session['add_count'] = extra_count
    return CompanyProjectsShowList(request,edit=True, extra=extra_count)


@login_required
def CompanyUsersShowList(request, edit=False, extra=0):
    current_user = request.user
    company = current_user.userprofile.get_active_company()

    display_static = True
    updated = False

    # make session counter on extra (if user presses many times on add button)

    # check if edit is allowed
    allow_edit = False

    if allow_edit and edit:
        display_static = False

    users = UserCompany.get_company_users(company_id=company.pk)
    UserFormSet = modelformset_factory(UserProfile, exclude=('id', 'company'), can_delete=True, extra=extra)
    if request.method == 'POST':
        formset = UserFormSet(
            request.POST, request.FILES,
            queryset=users)
        if formset.is_valid() and formset.has_changed():
            for form in formset:
                form.instance.company = company
            formset.save()
            updated = True
            display_static = True
    else:
        formset = UserFormSet(queryset=users)

    table = CompanyUserTable(users)

    return render(request, 'arkivo_app/company/users.html', {
        'nav_url': 'arkivo_app:company_users',
        'company': company,
        'formset': formset,
        'users': users,
        'display_static': display_static,
        'allow_edit': allow_edit,
        'updated': updated,
        'table': table
    })


@login_required
def SurveyShow(request, project_name, section_name='', category_name= ''):
    current_user = request.user
    company = current_user.userprofile.get_active_company()
    project = Project.objects.get(company = company, name = project_name, active = True)
    if not project:
        redirect('arkivo_app:index');

    survey = Survey.objects.get(project = project)

    # Get section
    qs = SurveySection.objects.filter(survey_template=survey.survey_template, name = section_name)
    if not qs:
        qs = SurveySection.objects.filter(survey_template=survey.survey_template)

    section = qs.first()

    # Get current category
    qs = QuestionCategory.objects.filter(survey_template=survey.survey_template, survey_section=section, name =category_name)
    if not qs:
        qs = QuestionCategory.objects.filter(survey_template=survey.survey_template, survey_section=section)

    category = qs.first()

    return render(request, 'arkivo_app/survey/survey.html', {
        'nav_url': 'arkivo_app:company_users',
        'company': company,
        'project': project,
        'survey':  survey,
        'section': section,
        'category': category,
        'section_name': section_name,
    })

