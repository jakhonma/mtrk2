from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget
from authentication.models import User
from main.models import Information
from helper.models import Fond, Category, Mtv, Region, Language, Format


class FondForeignKeyWidget(ForeignKeyWidget):
    def clean(self, value, row=None, **kwargs):
        department_name = str(row['department']).strip()
        fond_name = str(row["fond"]).strip()
        try:
            fond = Fond.objects.get(
                name=fond_name,
                department__name=department_name
            )
        except Fond.DoesNotExist:
            raise ValueError(f"Category {fond_name} does not exist in the database.")
        if fond is not None:
            return fond
        else:
            return None


class CategoryParentForeignKeyWidget(ForeignKeyWidget):

    def clean(self, value, row=None, **kwargs):
        parent_name = row['parent']
        category_name = row["category"]
        fond_name = row["fond"]
        department_name = str(row["department"]).strip()
        try:
            fond = Fond.objects.get(
                name=fond_name,
                department__name=department_name
            )
            category = Category.objects.get(
                name=category_name,
                fond=fond
            )
            if parent_name is not None:
                return Category.objects.get(
                    name=parent_name,
                    parent=category
                )
            elif category_name is not None:
                return category
            else:
                return None
        except Category.DoesNotExist:
            raise ValueError(f"Category {category_name} does not exist in the database.")


class InformationAdminResource(resources.ModelResource):
    def __init__(self, user=None, *args, **kwargs):
        super().__init__()
        self.user = user

    fond = fields.Field(
        column_name='fond',
        attribute='fond',
        widget=FondForeignKeyWidget(
            model=Fond,
            field='name'
        )
    )

    category = fields.Field(
        column_name='category',
        attribute='category',
        widget=CategoryParentForeignKeyWidget(
            model=Category,
            field='name'
        )
    )

    employee = fields.Field(
        column_name='emp',
        attribute='employee',
        widget=ForeignKeyWidget(
            User,
            field='username'
        )
    )

    mtv = fields.Field(
        column_name='mtv',
        attribute='mtv',
        widget=ManyToManyWidget(Mtv, field='name')
    )
    region = fields.Field(
        column_name='region',
        attribute='region',
        widget=ManyToManyWidget(Region, field='name')
    )
    language = fields.Field(
        column_name='language',
        attribute='language',
        widget=ManyToManyWidget(Language, field='name')
    )
    format = fields.Field(
        column_name='format',
        attribute='format',
        widget=ManyToManyWidget(Format, field='name')
    )

    def before_import_row(self, row, **kwargs):
        self.employee = kwargs['user']
        mtv_name = str(row["mtv"]).strip()
        region_name = str(row["region"]).strip()
        language_name = str(row["language"]).strip()
        format_name = str(row["format"]).strip()

        if "," in mtv_name:
            mtv_list = mtv_name.split(',')
            for item in mtv_list:
                Mtv.objects.get(name=item)
        elif mtv_name == 'None':
            pass
        else:
            Mtv.objects.get(name=mtv_name)

        if "," in region_name:
            region_list = region_name.split(',')
            for item in region_list:
                Region.objects.get(name=item)
            # for item in range(len(region_name)-1):
            #     if region_name[item] == ',':
            #         Region.objects.get(name=region)
            #         region = ''
            #     if count == len(region_name)-1:
            #         Region.objects.get(name=region)
            #         region = ''
            #     region += region_name[item]
            #     count +=1
        elif region_name == 'None':
            pass
        else:
            Region.objects.get(name=region_name)

        if ',' in language_name:
            lst = language_name.split(',')
            for item in lst:
                Language.objects.get(name=item)
        elif language_name == 'None':
            pass
        else:
            Language.objects.get(name=language_name)

        if ',' in format_name:
            format_list = format_name.split(',')
            for item in format_list:
                Format.objects.get(name=item)
        elif format_name == 'None':
            pass
        else:
            Format.objects.get(name=format_name)

    def save_instance(
        self, instance, is_create, using_transactions=True, dry_run=False
    ):
        instance.employee = self.employee
        super().save_instance(instance, is_create, using_transactions, dry_run)

    class Meta:
        model = Information
        fields = [
            'fond', 'category', 'mtv', 'region', 'language', 'format', 'id', 'title',
            'mtv_index', 'location_on_server', 'color', 'material', 'duration',
            'year', 'month', 'day', 'restoration', 'confidential', 'brief_data',
            'summary', 'is_serial'
        ]
