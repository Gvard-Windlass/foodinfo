import factory
import factory.random
from django.contrib.auth.models import User
from culinary.models import Ingredient, Measure

factory.random.reseed_random("foodinfo")


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ("username",)

    username = "gvard"
    password = "Bk7^31&3LDXt"
    email = "test@example.com"

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        manager = cls._get_manager(model_class)
        return manager.create_user(*args, **kwargs)


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
