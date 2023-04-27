import datetime

from django.db import models


class Reference(models.Model):
    code = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=300)
    description = models.TextField()

    def __str__(self):
        return self.name

    def get_current_version(self):
        versions = ReferenceVersion.objects.filter(
            reference=self, start_date__lte=datetime.date.today()
        ).order_by('-start_date')
        if versions.exists():
            return versions.first()
        else:
            return None


class ReferenceVersion(models.Model):
    reference = models.ForeignKey(Reference, on_delete=models.CASCADE)
    version = models.CharField(max_length=50)
    start_date = models.DateField()

    class Meta:
        unique_together = ('reference', 'start_date')

    def __str__(self):
        return self.version


class ReferenceElement(models.Model):
    version = models.ForeignKey(ReferenceVersion, on_delete=models.CASCADE)
    code = models.CharField(max_length=100)
    value = models.CharField(max_length=300)

    class Meta:
        unique_together = ('version', 'code')

    def __str__(self):
        return self.code
