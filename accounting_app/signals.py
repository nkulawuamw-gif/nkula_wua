from django.db.models.signals import post_save, post_delete, post_migrate, pre_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from decimal import Decimal
from .models import UserProfile, Account, Beneficiary, Invoice, Payment, BeneficiaryHistory, BalanceHistory, OpeningBalance

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance, role='admin' if instance.is_superuser else 'viewer')

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'userprofile'):
        instance.userprofile.save()

@receiver(post_migrate)
def create_default_accounts(sender, **kwargs):
    if sender.name != 'accounting_app':
        return
    
    default_accounts = [
        {"name": "Penalty Fees", "code": "4001", "account_type": "revenue", "description": "Revenue from penalty fees"},
        {"name": "Connection Fees", "code": "4002", "account_type": "revenue", "description": "Revenue from connection fees"},
        {"name": "Other Services Fees", "code": "4003", "account_type": "revenue", "description": "Revenue from other services"},
    ]
    
    for acc in default_accounts:
        Account.objects.get_or_create(
            code=acc["code"],
            defaults={
                "name": acc["name"],
                "account_type": acc["account_type"],
                "description": acc["description"]
            }
        )


@receiver(pre_save, sender=Beneficiary)
def cache_old_beneficiary(sender, instance, **kwargs):
    """Cache old values before save to detect changes"""
    if instance.pk:
        try:
            instance._old_values = Beneficiary.objects.filter(pk=instance.pk).values().first()
        except:
            instance._old_values = None
    else:
        instance._old_values = None


@receiver(post_save, sender=Beneficiary)
def log_beneficiary_save(sender, instance, created, **kwargs):
    user = getattr(instance, 'created_by', None)
    if created:
        BeneficiaryHistory.objects.create(
            beneficiary=instance,
            user=user,
            action="created",
            description=f"Beneficiary '{instance.name}' was created"
        )
    else:
        action = "updated"
        old_values = getattr(instance, '_old_values', None)
        if old_values:
            track_fields = ['name', 'beneficiary_type', 'phone', 'email', 'village', 'scheme', 'country',
                           'tax_id', 'household_count', 'credit_limit', 'payment_terms', 'tap_installed_date', 'is_active']
            for field in track_fields:
                old_val = old_values.get(field)
                new_val = getattr(instance, field)
                if old_val != new_val:
                    BeneficiaryHistory.objects.create(
                        beneficiary=instance,
                        user=user,
                        action="updated",
                        field_name=field,
                        old_value=str(old_val) if old_val is not None else '',
                        new_value=str(new_val) if new_val is not None else '',
                        description=f"Field '{field}' changed from '{old_val}' to '{new_val}'"
                    )





@receiver(post_save, sender=Payment)
def update_invoice_status_on_payment(sender, instance, created, **kwargs):
    if not created:
        return
    
    invoice = instance.invoice
    if invoice:
        invoice.update_payment_status()


@receiver(post_delete, sender=Payment)
def log_payment_delete(sender, instance, **kwargs):
    if instance.invoice:
        instance.invoice.update_payment_status()



# ─── Balance History Signals ────────────────────────────────────────────────

def recalculate_running_balance(beneficiary_id):
    entries = BalanceHistory.objects.filter(beneficiary_id=beneficiary_id).order_by('transaction_date', 'created_at')
    running = Decimal('0.00')
    for entry in entries:
        running = running + entry.debit - entry.credit
        if entry.running_balance != running:
            BalanceHistory.objects.filter(pk=entry.pk).update(running_balance=running)


@receiver(post_save, sender=Invoice)
def balance_history_invoice_save(sender, instance, created, **kwargs):
    desc = f"Invoice {instance.invoice_number}"
    if instance.created_by:
        desc += f" - created by {instance.created_by.username}"

    BalanceHistory.objects.update_or_create(
        beneficiary=instance.beneficiary,
        transaction_type='invoice',
        transaction_date=instance.issue_date,
        description=desc,
        defaults={
            'reference_number': instance.invoice_number,
            'debit': instance.total_amount,
            'credit': Decimal('0.00'),
            'fiscal_year': instance.issue_date.year,
            'created_by': instance.created_by,
        }
    )
    recalculate_running_balance(instance.beneficiary_id)


@receiver(post_delete, sender=Invoice)
def balance_history_invoice_delete(sender, instance, **kwargs):
    BalanceHistory.objects.filter(
        beneficiary=instance.beneficiary,
        transaction_type='invoice',
        reference_number=instance.invoice_number,
    ).delete()
    recalculate_running_balance(instance.beneficiary_id)


@receiver(post_save, sender=Payment)
def balance_history_payment_save(sender, instance, created, **kwargs):
    invoice_ref = instance.invoice.invoice_number if instance.invoice else ''
    desc = f"Payment of {instance.amount}"
    if invoice_ref:
        desc += f" for {invoice_ref}"
    if instance.created_by:
        desc += f" - by {instance.created_by.username}"

    BalanceHistory.objects.update_or_create(
        beneficiary=instance.beneficiary,
        transaction_type='payment',
        transaction_date=instance.payment_date,
        description=desc,
        defaults={
            'reference_number': instance.reference or invoice_ref,
            'debit': Decimal('0.00'),
            'credit': instance.amount,
            'fiscal_year': instance.payment_date.year,
            'created_by': instance.created_by,
        }
    )
    recalculate_running_balance(instance.beneficiary_id)


@receiver(post_delete, sender=Payment)
def balance_history_payment_delete(sender, instance, **kwargs):
    BalanceHistory.objects.filter(
        beneficiary=instance.beneficiary,
        transaction_type='payment',
        created_at=instance.created_at,
        credit=instance.amount,
    ).delete()
    recalculate_running_balance(instance.beneficiary_id)


@receiver(post_save, sender=OpeningBalance)
def balance_history_opening_save(sender, instance, created, **kwargs):
    desc = f"Opening Balance FY {instance.fiscal_year}"
    from datetime import date
    transaction_date = date(instance.fiscal_year, 1, 1)

    BalanceHistory.objects.update_or_create(
        beneficiary=instance.beneficiary,
        transaction_type='opening_balance',
        fiscal_year=instance.fiscal_year,
        defaults={
            'transaction_date': transaction_date,
            'description': desc,
            'reference_number': f"FY{instance.fiscal_year}",
            'debit': instance.amount,
            'credit': Decimal('0.00'),
            'notes': instance.notes,
            'created_by': instance.created_by,
        }
    )
    recalculate_running_balance(instance.beneficiary_id)


@receiver(post_delete, sender=OpeningBalance)
def balance_history_opening_delete(sender, instance, **kwargs):
    BalanceHistory.objects.filter(
        beneficiary=instance.beneficiary,
        transaction_type='opening_balance',
        fiscal_year=instance.fiscal_year,
    ).delete()
    recalculate_running_balance(instance.beneficiary_id)
