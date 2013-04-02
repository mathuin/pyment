from django.core.management.base import NoArgsCommand
from cart import cart
from pyment import settings


class Command(NoArgsCommand):
    help = 'Delete shopping cart items more than %d days old' % settings.SESSION_AGE_DAYS

    def handle_noargs(self, **options):
        cart.remove_old_cart_items()
