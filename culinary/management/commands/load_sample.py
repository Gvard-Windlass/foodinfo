from django.core.management.base import BaseCommand

from test.factories import IngredientFactory, UserFactory


class Command(BaseCommand):
    help = "load data using factoryboy fixtures"

    def handle(self, *args, **kwargs):
        staff_user = UserFactory.create()
        staff_user.is_staff = True
        staff_user.save()
        user1 = UserFactory.create()
        user2 = UserFactory.create()

        IngredientFactory.create_batch(21, user_id=staff_user.id)
        IngredientFactory.create_batch(5, user_id=user1.id)
        IngredientFactory.create_batch(5, user_id=user2.id)
