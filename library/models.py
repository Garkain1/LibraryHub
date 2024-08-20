from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    profile = models.URLField(null=True, blank=True)  # Профиль автора
    deleted = models.BooleanField(default=False)  # Поле для пометки автора как удаленного
    rating = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
