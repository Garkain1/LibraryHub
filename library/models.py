from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


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


class Category(models.Model):
    name = models.CharField(max_length=30, unique=True, verbose_name="Category Name")

    def __str__(self):
        return self.name


class Library(models.Model):
    name = models.CharField(max_length=100, verbose_name="Library Name")
    location = models.CharField(max_length=200, verbose_name="Location")
    site = models.URLField(null=True, blank=True, verbose_name="Website")

    def __str__(self):
        return self.name


class Member(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    ROLE_CHOICES = [
        ('Staff', 'Staff'),
        ('Reader', 'Reader'),
    ]

    first_name = models.CharField(max_length=50, verbose_name="First Name")
    last_name = models.CharField(max_length=50, verbose_name="Last Name")
    email = models.EmailField(unique=True, verbose_name="Email")
    gender = models.CharField(max_length=50, choices=GENDER_CHOICES, verbose_name="Gender")
    birth_date = models.DateField(verbose_name="Birth Date")
    age = models.IntegerField(validators=[MinValueValidator(6), MaxValueValidator(120)], verbose_name="Age")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, verbose_name="Role")
    active = models.BooleanField(default=True, verbose_name="Active")
    libraries = models.ManyToManyField(Library, related_name='members', verbose_name="Libraries")

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role})"


class Post(models.Model):
    title = models.CharField(max_length=255, unique_for_date='created_at', verbose_name="Title")
    body = models.TextField(verbose_name="Body")
    author = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='posts', verbose_name="Author")
    moderated = models.BooleanField(default=False, verbose_name="Moderated")
    library = models.ForeignKey(Library, on_delete=models.CASCADE, related_name='posts', verbose_name="Library")
    created_at = models.DateField(verbose_name="Created At")
    updated_at = models.DateField(auto_now=True, verbose_name="Updated At")

    def __str__(self):
        return self.title


class Book(models.Model):
    GENRE_CHOICES = [
        ('Fiction', 'Fiction'),
        ('Non-Fiction', 'Non-Fiction'),
        ('Science Fiction', 'Science Fiction'),
        ('Fantasy', 'Fantasy'),
        ('Mystery', 'Mystery'),
        ('Biography', 'Biography'),
    ]

    title = models.CharField(max_length=100, verbose_name="Title")
    author = models.ForeignKey(Author, null=True, on_delete=models.SET_NULL, verbose_name="Author")
    publishing_date = models.DateField(verbose_name="Publishing Date")
    summary = models.TextField(null=True, blank=True, verbose_name="Summary")
    genre = models.CharField(max_length=50, choices=GENRE_CHOICES, null=True, verbose_name="Genre")
    page_count = models.IntegerField(null=True, blank=True, validators=[MaxValueValidator(10000)],
                                     verbose_name="Page Count")
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL, related_name='books',
                                 verbose_name="Category")
    libraries = models.ManyToManyField(Library, related_name='books', verbose_name="Libraries")

    def __str__(self):
        return self.title


class Borrow(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='borrows', verbose_name="Member")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='borrows', verbose_name="Book")
    library = models.ForeignKey(Library, on_delete=models.CASCADE, related_name='borrows', verbose_name="Library")
    borrow_date = models.DateField(verbose_name="Borrow Date")
    return_date = models.DateField(verbose_name="Return Date")
    returned = models.BooleanField(default=False, verbose_name="Returned")

    def is_overdue(self):
        if self.returned:
            return False
        return self.return_date < timezone.now().date()

    def __str__(self):
        return f"{self.member} borrowed {self.book}"
