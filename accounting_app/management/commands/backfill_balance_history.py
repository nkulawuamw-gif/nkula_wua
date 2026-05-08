from django.core.management.base import BaseCommand
from accounting_app.models import Beneficiary, BalanceHistory, Invoice, Payment, OpeningBalance
from decimal import Decimal
from datetime import date


class Command(BaseCommand):
    help = 'Backfill balance history for all existing beneficiaries'

    def handle(self, *args, **options):
        self.stdout.write('Clearing existing balance history...')
        BalanceHistory.objects.all().delete()

        beneficiaries = Beneficiary.objects.all()
        self.stdout.write(f'Processing {beneficiaries.count()} beneficiaries...')

        for ben in beneficiaries:
            entries = []

            for ob in OpeningBalance.objects.filter(beneficiary=ben):
                entries.append(BalanceHistory(
                    beneficiary=ben,
                    transaction_type='opening_balance',
                    transaction_date=date(ob.fiscal_year, 1, 1),
                    description=f"Opening Balance FY {ob.fiscal_year}",
                    reference_number=f"FY{ob.fiscal_year}",
                    debit=ob.amount,
                    credit=Decimal('0.00'),
                    fiscal_year=ob.fiscal_year,
                    notes=ob.notes,
                    created_by=ob.created_by,
                    created_at=ob.created_at,
                ))

            for inv in Invoice.objects.filter(beneficiary=ben).order_by('issue_date', 'created_at'):
                desc = f"Invoice {inv.invoice_number}"
                if inv.created_by:
                    desc += f" - created by {inv.created_by.username}"
                entries.append(BalanceHistory(
                    beneficiary=ben,
                    transaction_type='invoice',
                    transaction_date=inv.issue_date,
                    description=desc,
                    reference_number=inv.invoice_number,
                    debit=inv.total_amount,
                    credit=Decimal('0.00'),
                    fiscal_year=inv.issue_date.year,
                    created_by=inv.created_by,
                    created_at=inv.created_at,
                ))

            for pmt in Payment.objects.filter(beneficiary=ben).order_by('payment_date', 'created_at'):
                inv_ref = pmt.invoice.invoice_number if pmt.invoice else ''
                desc = f"Payment of {pmt.amount}"
                if inv_ref:
                    desc += f" for {inv_ref}"
                if pmt.created_by:
                    desc += f" - by {pmt.created_by.username}"
                entries.append(BalanceHistory(
                    beneficiary=ben,
                    transaction_type='payment',
                    transaction_date=pmt.payment_date,
                    description=desc,
                    reference_number=pmt.reference or inv_ref,
                    debit=Decimal('0.00'),
                    credit=pmt.amount,
                    fiscal_year=pmt.payment_date.year,
                    created_by=pmt.created_by,
                    created_at=pmt.created_at,
                ))

            entries.sort(key=lambda e: (e.transaction_date, e.created_at))

            running = Decimal('0.00')
            for e in entries:
                running = running + e.debit - e.credit
                e.running_balance = running

            BalanceHistory.objects.bulk_create(entries)
            self.stdout.write(f'  {ben.name}: {len(entries)} entries created')

        self.stdout.write(self.style.SUCCESS('Done! Balance history backfilled successfully.'))
