from django.core.management.base import BaseCommand

from test.factories import TagFactory, TagCategoryFactory


class Command(BaseCommand):
    help = "load tags using factoryboy fixtures"

    def handle(self, *args, **kwargs):
        categories = TagCategoryFactory.create_batch(3)
        for category in categories:
            TagFactory.create_batch(5, category=category)

        print("Import complete")
