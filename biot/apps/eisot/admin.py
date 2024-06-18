from django.contrib import admin
from import_export import fields, resources
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget
from users.models import CustomUser

from .models import ReestrOt


class ReestrOtAdminResource(resources.ModelResource):
    reestr_number = Field(attribute='reestr_number',
                          column_name='Номер в реестре')
    reestr_date = Field(attribute='reestr_date',
                        column_name='Дата внесения в реестр')
    reestr_number = Field(attribute='reestr_number',
                          column_name='Номер в реестре')
    reestr_id_packet = Field(attribute='reestr_id_packet',
                             column_name='Id пакета')
    is_sistem = Field(attribute='is_sistem',
                      column_name='В системе')
    position_at_work = Field(attribute='position_at_work',
                             column_name='Должность')
    employer = Field(attribute='employer',
                     column_name='Наименование работодателя')
    employer_inn = Field(attribute='employer_inn',
                         column_name='ИНН организации проводившей обучение')
    program = Field(attribute='program',
                    column_name='Программа обучения')
    prot_number = Field(attribute='prot_number',
                        column_name='Номер протокола')
    prot_date = Field(attribute='prot_date',
                      column_name='Дата проверки знаний')
    result = Field(attribute='result',
                   column_name='Результат')

    author = fields.Field(
        column_name='СНИЛС',
        attribute='author',
        widget=ForeignKeyWidget(CustomUser, field='snils'))

    class Meta:
        model = ReestrOt
        import_id_fields = ('reestr_number',)
        skip_unchanged = True
        report_skipped = True

        export_order = (
            'reestr_number',
            'reestr_date',
            'reestr_id_packet',
            'is_sistem',
            'author',
            'position_at_work',
            'employer',
            'employer_inn',
            'program',
            'result',
            'prot_number',
            'prot_date',
        )


class ReestrOtAdmin(ImportExportModelAdmin):
    resource_classes = [ReestrOtAdminResource]
    search_fields = ('author__last_name',)
    list_display = (
        'reestr_number',
        'reestr_date',
        'reestr_id_packet',
        'is_sistem',
        'author',
        'employer',
        'position_at_work',
        'program',
    )

    fields = [
        ('reestr_number', 'reestr_date'),
        ('reestr_id_packet', 'is_sistem'),
        ('author', 'position_at_work'),
        ('employer', 'employer_inn'),
        'program',
        'result',
        ('prot_number', 'prot_date'),
    ]


admin.site.register(ReestrOt, ReestrOtAdmin)
