from django.core.management.base import NoArgsCommand
from inventory.models import Jar
from pyment import settings
from datetime import datetime, timedelta
from django.utils.timezone import utc

class Command(NoArgsCommand):
    help = "Delete inactive jars more than INACTIVE_JAR_AGE_DAYS days old"
    def handle_noargs(self, **options):
        self.stdout.write('Removing inactive jars\n')
        # calculate date of INACTIVE_JAR_AGE_DAYS days ago
        remove_before = datetime.utcnow().replace(tzinfo=utc) + timedelta(days=-settings.INACTIVE_JAR_AGE_DAYS)
        old_jars = Jar.objects.filter(is_active=False,updated_at__lt=remove_before)
        num_jars = str(len(old_jars))
        old_jars.delete()
        self.stdout.write('%s jars were removed\n' % num_jars)
