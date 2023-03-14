from django.core.management.base import BaseCommand

from test.factories import IngredientFactory, UserFactory, FridgeFactory


class Command(BaseCommand):
    help = "load data using factoryboy fixtures"

    def handle(self, *args, **kwargs):
        staff_user = UserFactory.create()
        staff_user.is_staff = True
        staff_user.save()
        user1 = UserFactory.create()
        user2 = UserFactory.create()

        staff_ingrs = IngredientFactory.create_batch(21, user_id=staff_user.id)
        user1_ingrs = IngredientFactory.create_batch(5, user_id=user1.id)
        user2_ingrs = IngredientFactory.create_batch(5, user_id=user2.id)

        FridgeFactory.create(user_id=staff_user.id, shelf=staff_ingrs)
        FridgeFactory.create(user_id=user1.id, shelf=user1_ingrs)
        FridgeFactory.create(user_id=user2.id, shelf=user2_ingrs)
