from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class MyModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False, auto_created=True)
    updated_at = models.DateTimeField(auto_now=True, editable=False, auto_created=True)
    hidden_fields = ['']

    class Meta:
        abstract = True

    def get_display_field(self, field_name):
        f = self[field_name]
        t = {'label': f.verbose_name,
             'value': getattr(self, f.name)}
        return t

    def get_display_detail(self):
        t = {'fields': []}
        for f in self._meta.get_fields(include_hidden=False):
            if (not f.auto_created) and (not any(f.name in s for s in self.hidden_fields)):
                try:
                    t['fields'].append({'label': f.verbose_name,
                                        'value': getattr(self, f.name)
                                        })
                except AttributeError:
                    pass
                    # Needs a way to display many_to_many fields.
        return t

    def get_display_list(self):
        pass


class CompanySizeRange(MyModel):
    size_from = models.PositiveIntegerField()
    size_to = models.PositiveIntegerField()

    def __str__ (self):
        return self.size_from.__str__() + "-" + self.size_to.__str__() + " Employees"


class Company(MyModel):
    name = models.CharField(max_length=255, unique=True, verbose_name="Company Name")
    addr_street = models.TextField(max_length=255, verbose_name="Street")
    addr_zip_code = models.PositiveIntegerField(verbose_name="ZIP Code")
    addr_city = models.CharField(max_length=255, verbose_name="City")
    addr_country = models.CharField(max_length=30, verbose_name="Country")
    vat_no = models.CharField(max_length=15, null=False, verbose_name="VAT No.")  # What is max length really?
    website = models.URLField(max_length=255, verbose_name="Website")
    company_size_range = models.ForeignKey(CompanySizeRange, on_delete=models.CASCADE, verbose_name="Company Size")
    invoice_mail = models.EmailField(max_length=255, verbose_name="Invoice E-mail")
    invoice_conctact_name = models.CharField(max_length=255, verbose_name="Invoice Contact Name")

    def __str__ (self):
        return self.name

    class Meta:
        default_permissions = ('add', 'change', 'delete', 'view')

    def get_active_projects(self):
        return Project.objects.filter(company_id = self.pk,active = True)


class CompanySystem(MyModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, verbose_name="Name")
    reception = models.BooleanField(verbose_name="Modtagelse")
    registration = models.BooleanField(verbose_name="Registration")
    storage = models.BooleanField(verbose_name="Storage")
    deletion = models.BooleanField(verbose_name="Deletion")
    passing = models.BooleanField(verbose_name="Passing")
    system_location = models.CharField(max_length=20, choices=(('INTERNAL', 'Internal'), ('EXTERNAL', 'External')),
                                       verbose_name="System Location")
    active = models.BooleanField(verbose_name="Active")

    class Meta:
        unique_together = ('company', 'name',)

    def __str__ (self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def get_active_company(self):
        qs = UserCompany.objects.filter(user=self.user, view_active=True)
        if not qs:
            qs = UserCompany.objects.filter(user=self.user)
        return qs.first().company


class UserCompany(MyModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    view_active = models.BooleanField(default=True)

    def get_company_users(company_id):
        return UserCompany.objects.filter(company_id = company_id, user__is_superuser = False)

# PROJECT

class SurveyTemplate(MyModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Project(MyModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, verbose_name='Project')
    active = models.BooleanField()
    survey_template = models.ForeignKey(SurveyTemplate, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('company', 'name',)

    def __str__(self):
        return self.name

    def get_surveys(self):
        return Survey.objects.filter(project_id=self.pk)


# SURVEY FORM
class Survey(MyModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    survey_template = models.ForeignKey(SurveyTemplate, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_sections(self):
        return SurveySection.objects.filter(survey_template=self.survey_template).order_by('order')



@receiver(post_save, sender=Project)
def save_project_survey(sender, instance, created, raw, using, update_fields,**kwargs):
    if instance and created:
        s = Survey.objects.create(project = instance, survey_template = instance.survey_template)
        s.name = "Survey"
        s.save()


class SurveySection(MyModel):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=1000, null=True, blank=True)
    survey_template = models.ForeignKey(SurveyTemplate, on_delete=models.CASCADE)
    order = models.IntegerField(default=1)

    def __str__(self):
        return self.name

    def get_categories(self):
        return QuestionCategory.objects.filter(survey_template=self.survey_template, survey_section_id=self.pk).order_by('order')

    def get_shown_categories(self):
        return QuestionCategory.objects.filter(survey_template=self.survey_template, survey_section_id=self.pk, show=True).order_by('order')

@receiver(post_save, sender=SurveySection)
def save_survey_section_top_category(sender, instance, created, raw, using, update_fields,**kwargs):
    if instance and created:
        c = QuestionCategory.objects.create(survey_section = instance, survey_template = instance.survey_template, order=1)
        c.name = "Default Category"
        c.show = False
        c.save()


# Question ##
class QuestionCategory(MyModel):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=1000, null=True, blank=True)
    survey_template = models.ForeignKey(SurveyTemplate, on_delete=models.CASCADE)
    survey_section = models.ForeignKey(SurveySection, on_delete=models.CASCADE)
    order = models.IntegerField(default=1)
    show = models.BooleanField(default=True)

    def __str__(self):
        return self.survey_section.name + ">>" + self.name

    def get_questions(self):
        return Question.objects.filter(survey_template = self.survey_template, category_id=self.pk).order_by('order')


def validate_list(value):
    """takes a text value and verifies that there is at least one comma """
    values = value.split(',')
    if len(values) < 2:
        raise ValidationError(
            "The selected field requires an associated list of choices. Choices must contain more than one item.")


class Question(MyModel):
    TEXT = 'text'
    RADIO = 'radio'
    SELECT = 'select'
    SELECT_MULTIPLE = 'select-multiple'
    INTEGER = 'integer'

    QUESTION_TYPES = (
        (TEXT, 'Text'),
        (RADIO, 'Radio'),
        (SELECT, 'Select'),
        (SELECT_MULTIPLE, 'Select Multiple'),
        (INTEGER, 'Integer'),
    )

    survey_template = models.ForeignKey(SurveyTemplate, on_delete=models.CASCADE)

    text = models.TextField()
    order = models.IntegerField(default=1)
    required = models.BooleanField(default=True)
    category = models.ForeignKey(QuestionCategory, blank=True, null=True)
    question_type = models.CharField(max_length=30, choices=QUESTION_TYPES, verbose_name='Question Type')
    description = models.TextField(max_length=1000, null=True, blank=True)
    help_text = models.CharField(max_length=255, null=True, blank=True)
    # the choices field is only used if the question type has choices
    choices = models.TextField(blank=True, null=True,
                               help_text='if the question type is "radio," "select," or "select multiple" provide a '
                                         'comma-separated list of options for this question .')

    def get_choices(self):
        """ parse the choices field and return a tuple formatted appropriately
        for the 'choices' argument of a form widget."""
        choices = self.choices.split(',')
        choices_list = []
        for c in choices:
            c = c.strip()
            choices_list.append((c, c))
        choices_tuple = tuple(choices_list)
        return choices_tuple

    def __str__(self):
        return self.text

class Response(MyModel):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)


class AnswerBase(MyModel):
    question = models.ForeignKey(Question)
    response = models.ForeignKey(Response)


# these type-specific answer models use a text field to allow for flexible
# field sizes depending on the actual question this answer corresponds to. any
# "required" attribute will be enforced by the form.
class AnswerText(AnswerBase):
    body = models.TextField(blank=True, null=True)


class AnswerRadio(AnswerBase):
    body = models.TextField(blank=True, null=True)


class AnswerSelect(AnswerBase):
    body = models.TextField(blank=True, null=True)


class AnswerSelectMultiple(AnswerBase):
    body = models.TextField(blank=True, null=True)


class AnswerInteger(AnswerBase):
    body = models.IntegerField(blank=True, null=True)
