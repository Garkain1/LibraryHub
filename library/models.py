from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Author(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="First name")
    last_name = models.CharField(max_length=100, verbose_name="Last name")
    birth_date = models.DateField(verbose_name="Birth date")
    profile = models.URLField(null=True, blank=True, verbose_name="Profile URL")
    deleted = models.BooleanField(default=False, verbose_name="Deleted",
                                  help_text="If checked, the author is considered removed from the list")
    rating = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name="Rating"
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Book(models.Model):
    title = models.CharField(max_length=100, verbose_name="Title")  # Название книги
    author = models.ForeignKey(Author, null=True, on_delete=models.SET_NULL, verbose_name="Author")  # Ссылка на автора
    publishing_date = models.DateField(verbose_name="Publishing Date")  # Дата публикации

    def __str__(self):
        return self.title
