from datetime import timezone
from django.db import models


class GeneralModel(models.Model):
    """ This class is used to define the common fields for all models """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True
    
    def delete(self, using=None, keep_parents=False):
        self.deleted_at = timezone.now()
        self.is_active = False
        self.save()