from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import *
# Register your models here.

admin.site.register(CompanySizeRange)

class CompanySystemsAdmin(admin.TabularInline):
	model = CompanySystem
	extra = 1

class CompanyAdmin(admin.ModelAdmin):
	inlines = [CompanySystemsAdmin]


admin.site.register(Company,CompanyAdmin)

# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class UserProfileInline(admin.StackedInline):
	model = UserProfile
	can_delete = False
	verbose_name_plural = 'Profile'


class UserCompanyInline(admin.TabularInline):
	model = UserCompany
	extra = 0
	can_delete = False



# Define a new User admin
class UserAdmin(BaseUserAdmin):
	inlines = (UserProfileInline, UserCompanyInline)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

class SurveyInline(admin.TabularInline):
	model = Survey
	extra = 0

class ProjectAdmin(admin.ModelAdmin):
	inlines = [SurveyInline]


class SurveySectionInline(admin.TabularInline):
	model = SurveySection
	ordering = ('order',)
	extra = 0

class QuestionCategoryInline(admin.TabularInline):
	model = QuestionCategory
	ordering = ('order',)
	extra = 0

class QuestionInline(admin.StackedInline):
	model = Question
	ordering = ('order',)
	extra = 0

class SurveyTemplateAdmin(admin.ModelAdmin):
	inlines = [SurveySectionInline,QuestionCategoryInline, QuestionInline]


class AnswerBaseInline(admin.TabularInline):
	fields = ('question', 'body')
	readonly_fields = ()
	extra = 0


class AnswerTextInline(AnswerBaseInline):
	model= AnswerText


class AnswerRadioInline(AnswerBaseInline):
	model= AnswerRadio


class AnswerSelectInline(AnswerBaseInline):
	model= AnswerSelect


class AnswerSelectMultipleInline(AnswerBaseInline):
	model= AnswerSelectMultiple


class AnswerIntegerInline(AnswerBaseInline):
	model= AnswerInteger


class ResponseAdmin(admin.ModelAdmin):
	#list_display = ('interview_uuid', 'interviewer', 'created')
	inlines = [AnswerTextInline, AnswerRadioInline, AnswerSelectInline, AnswerSelectMultipleInline, AnswerIntegerInline]
	# specifies the order as well as which fields to act on
	readonly_fields = ( 'created_at', 'updated_at')


admin.site.register(SurveyTemplate, SurveyTemplateAdmin)
admin.site.register(Response, ResponseAdmin)
admin.site.register(Project,ProjectAdmin)

