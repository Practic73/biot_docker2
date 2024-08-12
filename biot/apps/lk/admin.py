from django.contrib import admin

from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget

from users.models import CustomUser
from users.import_fields import MyUserResourceMixin
from .models import Group, Person


class GroupMixin():
    group_number = Field(attribute='group_number',
                         column_name='Номер группы')

    program_training = Field(attribute='program_training',
                             column_name='Программа обучения')

    start_date = Field(attribute='start_date',
                       column_name='Дата начала обучения')

    end_date = Field(attribute='end_date',
                     column_name='Дата окончания обучения')


class GroupResource(resources.ModelResource, GroupMixin):

    class Meta:
        model = Group
        import_id_fields = ('group_number',)
        skip_unchanged = True
        report_skipped = True

        # export_order = (
        #     'grup_number',
        #     #'program_training',
        #     'start_date',
        #     #'start_date2',
        #     #'end_date',
        # )


class GroupAdmin(ImportExportModelAdmin):
    resource_classes = [GroupResource]
    search_fields = ('group_number',)
    list_display = (
            'group_number',
            'program_training',
            'start_date',
            'end_date',
    )
    fields = [
            'group_number',
            'program_training',
            'start_date',
            'end_date',
    ]


class PersonResource(MyUserResourceMixin, GroupMixin):

    person = Field(
        column_name='СНИЛС',
        attribute='person',
        widget=ForeignKeyWidget(CustomUser, field='snils'))

    uid = Field(attribute='uid',
                column_name='UID студента')

    group = Field(
        column_name='Номер группы',
        attribute='group',
        widget=ForeignKeyWidget(Group, field='group_number'))
    
    start_date_person = Field(attribute='start_date_person',
                              column_name='Дата начала обучения')   

    def before_import_row(self, row, **kwargs):
        group = row["Номер группы"]
        program_training = row['Программа обучения']
        start_date = row['Дата начала обучения']
        end_date = row['Дата окончания обучения']
        Group.objects.get_or_create(
                                group_number=group,
                                defaults={
                                    'group_number': group,
                                    'program_training': program_training,
                                    'start_date': start_date,
                                    'end_date': end_date,
                                    }
        )

        first_name = row['Имя']
        last_name = row['Фамилия']
        middle_name = row['Отчество']
        snils = row['СНИЛС']
        CustomUser.objects.get_or_create(
                                snils=snils,
                                defaults={
                                    "snils": snils,
                                    'first_name': first_name,
                                    'last_name': last_name,
                                    'middle_name': middle_name,
                                    'is_verification': True,
                                    }
        )

    def before_save_instance(self, instance, using_transactions, dry_run):
        try:
            person = Person.objects.get(uid=instance.uid)
            if person and person.start_date_person:
                instance.start_date_person = person.start_date_person
                if instance.group != person.group.group_number:
                    if not person.previous_groups:
                        instance.previous_groups = person.group.group_number
                    else:
                        instance.previous_groups = (
                            f'{person.previous_groups},'
                            f'{person.group.group_number}'
                        )

        except Person.DoesNotExist:
            pass

    class Meta:
        model = Person
        import_id_fields = ('uid',)
        skip_unchanged = True
        report_skipped = True

        # export_order = (
        #     'person',
        #     'student_uid',
        #     'group',
        # )


class PersonAdmin(ImportExportModelAdmin):
    resource_classes = [PersonResource]

    list_display = [

        'person',
        'uid',
        'status',
        'start_date_person',
        'end_date_person',
        'group',
        'previous_groups',
    ]

    fields = [
        'person',
        'uid',
        'previous_groups',
        'group',
        ('start_date_person', 'end_date_person'),
    ]
    search_fields = ('person__last_name', 'group__group_number',)


admin.site.register(Group, GroupAdmin)
admin.site.register(Person, PersonAdmin)