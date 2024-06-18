
from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field

from .models import CustomUser


class MyUserResource(resources.ModelResource):
    username = Field(attribute='username', column_name='Логин')
    first_name = Field(attribute='first_name', column_name='Имя')
    last_name = Field(attribute='last_name', column_name='Фамилия')
    middle_name = Field(attribute='middle_name', column_name='Отчество')
    snils = Field(attribute='snils', column_name='СНИЛС')

    # def __init__(self, is_verification):
    #     self.is_verification = is_verification

    def before_save_instance(self, instance, using_transactions, dry_run):
        instance.is_verification = True

    class Meta:
        model = CustomUser
        import_id_fields = ('snils',)
        skip_unchanged = True
        report_skipped = True
        fields = (
            'last_name',
            'first_name',
            'middle_name',
            'snils',
        )
        export_order = ('snils', 'last_name', 'first_name', 'middle_name',)


class MyUserAdmin(ImportExportModelAdmin):
    resource_classes = (MyUserResource,)
    search_fields = ('last_name', 'snils',)
    list_display = (
        'username',
        'snils',
        'last_name',
        'first_name',
        'middle_name',
        # 'birthday',
        'is_verification',
        'is_active',
    )
    # В листе что можно редактировать прямо в колонке
    # list_editable = (
    #     'is_verification',
    # )
    fields = [
        ('password', 'username'),
        ('last_name', 'first_name'),
        'middle_name',
        'birthday',
        ('snils', 'is_verification'),
        'address',
        ('date_joined', 'last_login'),
        'groups',
        ('is_active', 'is_staff'),
    ]


admin.site.register(CustomUser, MyUserAdmin)
