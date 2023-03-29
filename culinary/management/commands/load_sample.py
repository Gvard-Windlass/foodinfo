from django.core.management.base import BaseCommand

from test.factories import (
    IngredientFactory,
    IngredientUsageFactory,
    RecipeFactory,
    UserFactory,
    FridgeFactory,
    MeasureFactory,
    ConversionFactory,
)


class Command(BaseCommand):
    help = "load data using factoryboy fixtures"

    def _add_ingredients_to_recipe(self, ingredients, measure, recipe):
        for ingr in ingredients:
            IngredientUsageFactory.create(
                ingredient=ingr, measure=measure, recipe=recipe
            )

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

        measures = MeasureFactory.create_batch(3)
        for i in range(len(measures)):
            ConversionFactory.create(utensil=measures[i], ingredient=staff_ingrs[i])

        recipes = RecipeFactory.create_batch(3)
        self._add_ingredients_to_recipe(staff_ingrs[:5], measures[0], recipes[0])
        self._add_ingredients_to_recipe(staff_ingrs[5:10], measures[1], recipes[1])
        self._add_ingredients_to_recipe(staff_ingrs[10:15], measures[2], recipes[2])

        print("Import complete")
