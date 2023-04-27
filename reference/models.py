import datetime

from django.db import models


class Reference(models.Model):
    """
    Модель справочника.

    Fields:
        - code (CharField): уникальный код справочника
        - name (CharField): наименование справочника
        - description (TextField): описание справочника

    Методы:
        - __str__: возвращает наименование справочника
        - get_current_version: возвращает текущую версию справочника
    """
    code = models.CharField(max_length=100, unique=True, verbose_name='Уникальный код справочника')
    name = models.CharField(max_length=300, verbose_name='Наименование справочника')
    description = models.TextField(verbose_name='Описание справочника')

    def __str__(self):
        return self.name

    def get_current_version(self):
        """
        Возвращает текущую версию справочника.

        :returns:
            - версия справочника (ReferenceVersion), если версия существует и её дата начала действия меньше или равна текущей дате
            - None, если версия не существует или её дата начала действия больше текущей даты
        """
        versions = ReferenceVersion.objects.filter(
            reference=self, start_date__lte=datetime.date.today()
        ).order_by('-start_date')
        if versions.exists():
            return versions.first()
        else:
            return None


class ReferenceVersion(models.Model):
    """
    Модель версии справочника.

    Fields:
        - reference (ForeignKey): ссылка на справочник
        - version (CharField): версия справочника
        - start_date (DateField): дата начала действия версии

    Meta:
        - unique_together: уникальность записей по комбинации полей reference и start_date

    Методы:
        - __str__: возвращает версию справочника
    """
    reference = models.ForeignKey(Reference, on_delete=models.PROTECT, verbose_name='Внешний ключ на справочник')
    version = models.CharField(max_length=50, verbose_name='Версия справочника')
    start_date = models.DateField(verbose_name='Дата начала действия версии')

    class Meta:
        unique_together = ('reference', 'start_date')

    def __str__(self):
        return self.version


class ReferenceElement(models.Model):
    """
    Модель элемента справочника.

    Fields:
        - version (ForeignKey): ссылка на версию справочника
        - code (CharField): код элемента справочника
        - value (CharField): значение элемента справочника

    Meta:
        - unique_together: уникальность записей по комбинации полей version и code

    Методы:
        - __str__: возвращает код элемента справочника
    """
    version = models.ForeignKey(ReferenceVersion, on_delete=models.PROTECT,
                                verbose_name='Внешний ключ на версию справочника')
    code = models.CharField(max_length=100, verbose_name='Код элемента справочника')
    value = models.CharField(max_length=300, verbose_name='Значение элемента справочника')

    class Meta:
        unique_together = ('version', 'code')

    def __str__(self):
        return self.code
