from django.db import models
from django.utils.timezone import now

# Create your models here.
class Hitas(models.Model):
    jew_data = models.TextField(unique=True, null=False, blank=False)
    chumash = models.TextField()
    tehillim = models.TextField()
    tanya = models.TextField()
    hayom_yoma = models.TextField()
    rambam = models.TextField()
    moshiach = models.TextField()
    created_date = models.DateTimeField(default=now, editable=False)