from django.db import models
from django.db.models import CheckConstraint, UniqueConstraint, Q
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

from tags.models import Tag


class CaloryInfo(models.Model):
    calories = models.FloatField(
        null=True,
        help_text="number of calories in kcal per 100 grams",
        validators=[MinValueValidator(0.0)],
    )
    proteins = models.FloatField(
        null=True,
        help_text="amount of proteins in kcal per 100 grams",
        validators=[MinValueValidator(0.0)],
    )
    fats = models.FloatField(
        null=True,
        help_text="amount of fats in kcal per 100 grams",
        validators=[MinValueValidator(0.0)],
    )
    carbs = models.FloatField(
        null=True,
        help_text="amount of carbs in kcal per 100 grams",
        validators=[MinValueValidator(0.0)],
    )

    class Meta:
        constraints = [
            CheckConstraint(check=Q(calories__gte=0.0), name="%(class)s calories >= 0"),
            CheckConstraint(check=Q(proteins__gte=0.0), name="%(class)s proteins >= 0"),
            CheckConstraint(check=Q(fats__gte=0.0), name="%(class)s fats >= 0"),
            CheckConstraint(check=Q(carbs__gte=0.0), name="%(class)s carbs >= 0"),
        ]
        abstract = True


class Ingredient(CaloryInfo):
    class IngredientCategory(models.TextChoices):
        Fruits = "Fruits"
        Vegetables = "Vegetables"
        Meat = "Meat"
        Poultry = "Poultry"
        Fish = "Fish"
        Seafood = "Seafood"
        Milk = "Milk"
        Eggs = "Eggs"
        Baking = "Baking"
        Grains = "Grains"
        Beans = "Beans"
        Seasonings = "Seasonings"
        Spices = "Spices"
        Sauces = "Sauces"
        Alcohol = "Alcohol"
        Liquids = "Liquids"
        Other = "Other"

    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    category = models.CharField(
        choices=IngredientCategory.choices,
        default=IngredientCategory.Other,
        max_length=50,
    )

    def __str__(self) -> str:
        return self.name


class Fridge(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shelf = models.ManyToManyField(Ingredient)

    def __str__(self) -> str:
        return self.name


class Measure(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self) -> str:
        return self.name


class UtensilConversion(models.Model):
    standard_value = models.FloatField(
        validators=[MinValueValidator(0.0)], help_text="conversion value in grams"
    )
    utensil = models.ForeignKey(Measure, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            CheckConstraint(
                check=Q(standard_value__gte=0.0), name="standard_value >= 0"
            ),
            UniqueConstraint(
                fields=["utensil", "ingredient"],
                name="utensil and ingredient combination must be unique",
            ),
        ]


class Recipe(CaloryInfo):
    title = models.CharField(max_length=150)
    thumbnail = models.ImageField(upload_to="", null=True, blank=True)
    favorites = models.ManyToManyField(User, related_name="favorites")
    portions = models.PositiveSmallIntegerField()
    total_time = models.TimeField()
    instructions = models.TextField()

    author = models.ForeignKey(User, on_delete=models.PROTECT)
    tags = models.ManyToManyField(Tag)

    def __str__(self) -> str:
        return self.title


class IngredientUsage(models.Model):
    amount = models.FloatField()
    ingredient = models.ForeignKey(Ingredient, on_delete=models.PROTECT)
    measure = models.ForeignKey(Measure, on_delete=models.PROTECT)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
