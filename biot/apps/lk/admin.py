#from readline import redisplay
from django.contrib import admin
#from datetime import date

from import_export import fields, resources
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget

from users.models import CustomUser
from .models import Group, Person


class GroupResource(resources.ModelResource):

    grup_number = Field(attribute='grup_number',
                        column_name='Номер группы')
    
    program_training = Field(attribute='program_training',
                             column_name='Программа обучения')

    # start_date = Field(attribute='start_date',
    #                    column_name='Дата начала строка')
    start_date = Field(attribute='start_date',
                       column_name='Дата начала обучения')

    end_date = Field(attribute='end_date',
                     column_name='Дата окончания обучения')
    

                        #widget=DateWidget(format='%Y-%m-%d')

    # value = self.widget.clean(value, row=data, **kwargs)
    # def after_import_row(self, row, row_result, **kwargs):
    #     self.start_date2 = date.fromisoformat(self.start_date)
        # if getattr(row_result.original, "start_date2") is None \
        #     and 
        # if getattr(row_result.instance, "start_date2") is not None:
        #     self.start_date2 = date.today()
          # import value is different from stored value.
          # exec custom workflow..

    class Meta:
        model = Group
        # store_instance = True
        import_id_fields = ('grup_number',)
        skip_unchanged = True
        report_skipped = True
        # widgets = {
        #     'start_date2': {'format': '%Y.%m.%d'},
        # }
        # exclude = ('program_training',
        #            'start_date2',
        #            'end_date',
        #            #'start_date2',
        # )

        # export_order = (
        #     'grup_number',
        #     #'program_training',
        #     'start_date',
        #     #'start_date2',
        #     #'end_date',
        # )


class GroupAdmin(ImportExportModelAdmin):
    resource_classes = [GroupResource]
    search_fields = ('grup_number',)
    list_display = (
            'grup_number',
            'program_training',
            'start_date',
            'end_date',
    )
    #filter_horizontal = ('groups',)
    fields = [
            'grup_number',
            'program_training',
            'start_date',
            'end_date',
    ]


class PersonResource(resources.ModelResource):

    # person = fields.Field(
    #     column_name='СНИЛС',
    #     attribute='person',
    #     widget=ForeignKeyWidget(CustomUser, field='snils'))
    
    uid = Field(attribute='uid',
                column_name='UID студента')
    
    groups = fields.Field(
        column_name='Номер группы',
        attribute='groups',
        widget=ManyToManyWidget(Group, separator=',', field='grup_number')
    )

    program_training = Field(attribute='program_training',
                             column_name='Программа обучения')

    start_date = Field(attribute='start_date',
                       column_name='Дата начала обучения')

    end_date = Field(attribute='end_date',
                     column_name='Дата окончания обучения')

    def before_import_row(self, row, **kwargs):
        groups = row["Номер группы"]
        program_training = row['Программа обучения']
        start_date = row['Дата начала обучения']
        end_date = row['Дата окончания обучения']
        #uid = row["UID студента"]
        Group.objects.get_or_create(
                                grup_number=groups,
                                defaults={
                                    "grup_number": groups,
                                    'program_training': program_training,
                                    'start_date': start_date,
                                    'end_date': end_date,
                                    }
        )
        #p=Person.objects.get(uid=uid)

    # def before_save_instance(self, instance, using_transactions, dry_run):
    #     # instance.is_verification = True
    #     instance.groups.add('111111')

    # def after_save_instance(self, instance, using_transactions, dry_run):
    #     instance.groups.clear()

    def save_m2m(self, obj, row, using_transactions, dry_run):
        uid = row["UID студента"]
        group = row["Номер группы"]
        fk_group = Group.objects.get(grup_number=group)
        peron_groups = Person.objects.get(uid=uid).groups
        peron_groups.add(fk_group)

        
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

    def get_groups(self, groups):
        # list(Group.objects.filter(groups=groups))
        qs = Group.objects.filter(groups=groups).last()
        return qs
    get_groups.short_description = "Группа"

    list_display = [

        #'person',
        'uid',
        'status',
        'start_date',
        'end_date',
        'get_groups',
        #'groups'
    ]
    #list_select_related = ('groups',)
    #filter_horizontal = ('groups',)
    fields = [
        #'person',
        'uid',
        'groups',
    ]

    #raw_id_fields = ('groups',)
    #filter_horizontal = ('groups',)
    autocomplete_fields = ('groups',)
    #list_select_related = ['groups', ]

    
    # @redisplay(description='Группы')


admin.site.register(Group, GroupAdmin)
admin.site.register(Person, PersonAdmin)