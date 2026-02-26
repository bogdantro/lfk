from django.db import models
from django.utils import timezone


class Sponsor(models.Model):
    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to="sponsors/")
    website = models.URLField(blank=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Team(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Player(models.Model):

    POSITION_CHOICES = [
        ("GK", "Keeper"),
        ("DF", "Forsvar"),
        ("MF", "Midtbane"),
        ("FW", "Angrep"),
    ]

    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="players")

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    jersey_number = models.PositiveIntegerField()
    position = models.CharField(max_length=5, choices=POSITION_CHOICES)

    date_of_birth = models.DateField()

    height = models.PositiveIntegerField(blank=True, null=True, help_text="Height in cm")
    weight = models.PositiveIntegerField(blank=True, null=True, help_text="Weight in kg")

    image = models.ImageField(upload_to="players/")
    bio = models.TextField(blank=True)

    sponsor = models.ForeignKey(Sponsor, on_delete=models.SET_NULL, null=True, blank=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["jersey_number"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def age(self):
        today = timezone.now().date()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )