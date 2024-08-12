
from django.contrib import admin

from import_export.admin import ImportExportModelAdmin

from .models import CustomUser
from .import_fields import MyUserResourceMixin


class MyUserResource(MyUserResourceMixin):

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
        #'birthday',
        'is_verification',
        'is_active',
        'role'
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
        #'groups', 'role',
        ('is_active', 'is_staff'),
    ]


admin.site.register(CustomUser, MyUserAdmin)