import factory
import factory.random
from django.contrib.auth.models import User
from allauth.account.models import EmailAddress
from culinary.models import (
    Ingredient,
    IngredientUsage,
    Measure,
    Fridge,
    Recipe,
    UtensilConversion,
)
from tags.models import Tag, TagCategory

factory.random.reseed_random("foodinfo")


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ("username",)

    username = factory.Sequence(lambda n: "user %d" % n)
    password = factory.Sequence(lambda n: "Bk7^31&3LDXt%d" % n)
    email = factory.Sequence(lambda n: "test%d@example.com" % n)

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        manager = cls._get_manager(model_class)
        return manager.create_user(*args, **kwargs)


class EmailFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EmailAddress
        django_get_or_create = ("email",)

    user_id = 1
    email = UserFactory.email
    verified = True
    primary = True


class IngredientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Ingredient
        django_get_or_create = ("name",)

    name = factory.Sequence(lambda n: "test ingredient %d" % n)
    user_id = 1


class MeasureFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Measure
        django_get_or_create = ("name",)

    name = factory.Sequence(lambda n: "test measure %d" % n)


class FridgeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Fridge
        django_get_or_create = ("name",)

    name = factory.Sequence(lambda n: "test fridge %d" % n)
    user_id = 1

    @factory.post_generation
    def shelf(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for item in extracted:
                self.shelf.add(item)


class ConversionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UtensilConversion
        django_get_or_create = ("utensil", "ingredient")

    standard_value = factory.Faker("pyfloat", positive=True)
    utensil = factory.SubFactory(MeasureFactory)
    ingredient = factory.SubFactory(IngredientFactory)


class RecipeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Recipe
        django_get_or_create = ("title",)

    title = factory.Sequence(lambda n: "test recipe %d" % n)
    portions = factory.Faker("pyint", min_value=1)
    total_time = factory.Faker("time")
    instructions = factory.Faker("paragraph", nb_sentences=10)
    author_id = 1

    calories = factory.Faker("pyfloat", min_value=1, max_value=350)
    proteins = factory.Faker("pyfloat", min_value=1, max_value=350)
    fats = factory.Faker("pyfloat", min_value=1, max_value=350)
    carbs = factory.Faker("pyfloat", min_value=1, max_value=350)

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for item in extracted:
                self.tags.add(item)


class IngredientUsageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = IngredientUsage

    amount = factory.Faker("pyfloat", positive=True)
    ingredient = factory.SubFactory(IngredientFactory)
    measure = factory.SubFactory(MeasureFactory)
    recipe = factory.SubFactory(RecipeFactory)


class TagCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TagCategory

    name = factory.Sequence(lambda n: "test tag category %d" % n)


class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tag

    label = factory.Sequence(lambda n: "tag %d" % n)
    category = factory.SubFactory(TagCategoryFactory)
