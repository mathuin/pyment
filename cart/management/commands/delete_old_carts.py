from django.core.management.base import NoArgsCommand
from cart import cart

class Command(NoArgsCommand):
    help = "Delete shopping cart items more than SESSION_AGE_DAYS days old"
    def handle_noargs(self, **options):
        cart.remove_old_cart_items()

