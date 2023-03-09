import factory
import factory.random
from culinary.models import Ingredient, Measure

factory.random.reseed_random("foodinfo")


class IngredientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Ingredient
        django_get_or_create = ("name",)

    name = factory.Sequence(lambda n: "test ingredient %d" % n)


class MeasureFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Measure
        django_get_or_create = ("name",)

    name = factory.Sequence(lambda n: "test measure %d" % n)
