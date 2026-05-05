from django.core.management.base import BaseCommand
from accounting_app.models import Beneficiary, Invoice, Payment
from django.db.models import Sum
from decimal import Decimal


class Command(BaseCommand):
    help = 'Recalculate all beneficiary totals (total_bill, total_paid, total_outstanding)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--beneficiary_id',
            type=int,
            help='Recalculate totals for specific beneficiary ID',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be updated without saving',
        )

    def handle(self, *args, **options):
        beneficiary_id = options.get('beneficiary_id')
        dry_run = options.get('dry_run', False)

        if beneficiary_id:
            beneficiaries = Beneficiary.objects.filter(id=beneficiary_id)
        else:
            beneficiaries = Beneficiary.objects.all()

        updated_count = 0

        for beneficiary in beneficiaries:
            # Calculate total bill from invoices
            total_bill = beneficiary.invoices.aggregate(
                total=Sum('total_amount')
            )['total'] or Decimal('0.00')

            # Calculate total paid from payments
            total_paid = beneficiary.payments.aggregate(
                total=Sum('amount')
            )['total'] or Decimal('0.00')

            # Calculate outstanding
            total_outstanding = total_bill - total_paid

            # Check if update needed
            if (beneficiary.total_bill != total_bill or
                beneficiary.total_paid != total_paid or
                beneficiary.total_outstanding != total_outstanding):

                self.stdout.write(f"\nBeneficiary: {beneficiary.name} (ID: {beneficiary.id})")
                self.stdout.write(f"  total_bill: {beneficiary.total_bill} -> {total_bill}")
                self.stdout.write(f"  total_paid: {beneficiary.total_paid} -> {total_paid}")
                self.stdout.write(f"  total_outstanding: {beneficiary.total_outstanding} -> {total_outstanding}")

                if not dry_run:
                    beneficiary.total_bill = total_bill
                    beneficiary.total_paid = total_paid
                    beneficiary.total_outstanding = total_outstanding
                    beneficiary.save(update_fields=['total_bill', 'total_paid', 'total_outstanding'])
                    updated_count += 1
                    self.stdout.write(self.style.SUCCESS("  Updated!"))
            else:
                self.stdout.write(f"Beneficiary: {beneficiary.name} - OK")

        self.stdout.write(self.style.SUCCESS(
            f"\n{'Would update' if dry_run else 'Updated'} {updated_count} beneficiaries"
        ))
