from django.db import models
from users.models import WORKitUser as User
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=60)
    description = models.TextField()

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        # Return the category name capitalized
        return self.name.capitalize()


class Location(models.Model):
    place = models.CharField(max_length=255, unique=True)

    def __str__(self):
        # Return the location name capitalized
        return self.place.capitalize()


class Task(models.Model):
    name = models.CharField(max_length=255)
    task_description = models.TextField(blank=True)  # Optional description for the task
    slug = models.SlugField(max_length=255, unique=True, blank=True)  # Unique slug for the task
    amount = models.PositiveIntegerField()  # Amount must be a positive integer
    location = models.ForeignKey(Location, on_delete=models.PROTECT)  # Location of the task
    extra_location_info = models.TextField(blank=True)  # Additional optional info about the location
    categories = models.ManyToManyField(Category, related_name="tasks")  # Categories related to the task
    employer = models.ForeignKey(User, on_delete=models.CASCADE)  # User who created the task
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the task was created
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp when the task was last updated
    bids = models.ManyToManyField(User, related_name="bids")


    def save(self, *args, **kwargs):
        if self.slug != slugify(f"{self.name.lower()}-{self.pk}", allow_unicode=True):
            self.slug = slugify(f"{self.name.lower()}-{self.pk}", allow_unicode=True)
        self.name = self.name.title()  # Capitalize the task name for display
        super().save(*args, **kwargs)  # Call the parent class's save method

    def __str__(self):
        # Return a string representation of the task including employer's name
        return f"{self.name}"
