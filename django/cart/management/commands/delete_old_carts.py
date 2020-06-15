from django.core.management.base import BaseCommand
from cart import cart
from pyment import settings


class Command(BaseCommand):
    help = "Delete shopping cart items more than %d days old" % settings.SESSION_AGE_DAYS

    def handle_noargs(self, **options):
        cart.remove_old_cart_items()
