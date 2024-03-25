from django.db import models

class GenderChoices(models.TextChoices):
    """ Choices for genders """
    HOMBRE = 'Hombre', 'Hombre'
    MUJER = 'Mujer', 'Mujer'
    OTRO = 'Otro', 'Otro'