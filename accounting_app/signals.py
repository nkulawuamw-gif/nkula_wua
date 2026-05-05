from django.db.models.signals import post_save, post_delete, post_migrate, pre_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import UserProfile, Account, Beneficiary, Invoice, Payment, Expense, Vendor, BeneficiaryHistory

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


def log_activity(user, action, model_name, object_id, description, request=None):
    from .models import ActivityLog
    ip_address = None
    if request:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[0]
        else:
            ip_address = request.META.get('REMOTE_ADDR')
    
    ActivityLog.objects.create(
        user=user,
        action=action,
        model_name=model_name,
        object_id=object_id,
        description=description,
        ip_address=ip_address
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
        action = "created"
        log_activity(user=user, action=action, model_name="Beneficiary", object_id=instance.pk,
                    description=f"Beneficiary '{instance.name}' was created")
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
            track_fields = ['name', 'beneficiary_type', 'phone', 'village', 'scheme', 'country',
                           'tax_id', 'household_count', 'credit_limit', 'payment_terms', 'is_active']
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
        log_activity(user=user, action=action, model_name="Beneficiary", object_id=instance.pk,
                    description=f"Beneficiary '{instance.name}' was updated")


@receiver(post_delete, sender=Beneficiary)
def log_beneficiary_delete(sender, instance, **kwargs):
    BeneficiaryHistory.objects.create(
        beneficiary=instance,
        user=None,
        action="deleted",
        description=f"Beneficiary '{instance.name}' was deleted"
    )
    log_activity(
        user=None,
        action="deleted",
        model_name="Beneficiary",
        object_id=instance.pk,
        description=f"Beneficiary '{instance.name}' was deleted"
    )


@receiver(post_save, sender=Invoice)
def log_invoice_save(sender, instance, created, **kwargs):
    action = "created" if created else "updated"
    log_activity(
        user=getattr(instance, 'created_by', None),
        action=action,
        model_name="Invoice",
        object_id=instance.pk,
        description=f"Invoice '{instance.invoice_number}' was {action}"
    )


@receiver(post_delete, sender=Invoice)
def log_invoice_delete(sender, instance, **kwargs):
    log_activity(
        user=None,
        action="deleted",
        model_name="Invoice",
        object_id=instance.pk,
        description=f"Invoice '{instance.invoice_number}' was deleted"
    )


@receiver(post_save, sender=Payment)
def log_payment_save(sender, instance, created, **kwargs):
    action = "created" if created else "updated"
    log_activity(
        user=getattr(instance, 'created_by', None),
        action=action,
        model_name="Payment",
        object_id=instance.pk,
        description=f"Payment of {instance.amount} for '{instance.beneficiary.name}' was {action}"
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
    log_activity(
        user=None,
        action="deleted",
        model_name="Payment",
        object_id=instance.pk,
        description=f"Payment of {instance.amount} was deleted"
    )
    if instance.invoice:
        instance.invoice.update_payment_status()


@receiver(post_save, sender=Expense)
def log_expense_save(sender, instance, created, **kwargs):
    action = "created" if created else "updated"
    log_activity(
        user=getattr(instance, 'created_by', None),
        action=action,
        model_name="Expense",
        object_id=instance.pk,
        description=f"Expense '{instance.expense_number}' was {action}"
    )


@receiver(post_delete, sender=Expense)
def log_expense_delete(sender, instance, **kwargs):
    log_activity(
        user=None,
        action="deleted",
        model_name="Expense",
        object_id=instance.pk,
        description=f"Expense '{instance.expense_number}' was deleted"
    )


@receiver(post_save, sender=Vendor)
def log_vendor_save(sender, instance, created, **kwargs):
    action = "created" if created else "updated"
    log_activity(
        user=None,
        action=action,
        model_name="Vendor",
        object_id=instance.pk,
        description=f"Vendor '{instance.name}' was {action}"
    )


@receiver(post_delete, sender=Vendor)
def log_vendor_delete(sender, instance, **kwargs):
    log_activity(
        user=None,
        action="deleted",
        model_name="Vendor",
        object_id=instance.pk,
        description=f"Vendor '{instance.name}' was deleted"
    )


@receiver(post_save, sender=Account)
def log_account_save(sender, instance, created, **kwargs):
    action = "created" if created else "updated"
    log_activity(
        user=None,
        action=action,
        model_name="Account",
        object_id=instance.pk,
        description=f"Account '{instance.name}' ({instance.code}) was {action}"
    )


@receiver(post_delete, sender=Account)
def log_account_delete(sender, instance, **kwargs):
    log_activity(
        user=None,
        action="deleted",
        model_name="Account",
        object_id=instance.pk,
        description=f"Account '{instance.name}' ({instance.code}) was deleted"
    )
