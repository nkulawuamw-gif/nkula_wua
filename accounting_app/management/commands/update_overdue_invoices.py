from django.core.management.base import BaseCommand
from django.utils import timezone
from accounting_app.models import Invoice


class Command(BaseCommand):
    help = 'Auto-detect and update overdue invoices based on due date'

    def handle(self, *args, **options):
        today = timezone.now().date()
        
        # Find invoices past due date that aren't already marked as overdue or paid/cancelled
        overdue_invoices = Invoice.objects.filter(
            due_date__lt=today,
            status__in=["sent", "viewed", "partial"]
        )
        
        count = overdue_invoices.count()
        
        if count > 0:
            overdue_invoices.update(status="overdue")
            self.stdout.write(
                self.style.SUCCESS(f'Successfully updated {count} invoices to overdue status')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS('No invoices need to be updated to overdue status')
            )
