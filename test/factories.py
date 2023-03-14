import factory
import factory.random
from django.contrib.auth.models import User
from culinary.models import Ingredient, Measure, Fridge

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
