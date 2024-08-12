
from import_export import resources
from import_export.fields import Field


class MyUserResourceMixin(resources.ModelResource):

    username = Field(attribute='username', column_name='Логин')
    first_name = Field(attribute='first_name', column_name='Имя')
    last_name = Field(attribute='last_name', column_name='Фамилия')
    middle_name = Field(attribute='middle_name', column_name='Отчество')
    snils = Field(attribute='snils', column_name='СНИЛС')