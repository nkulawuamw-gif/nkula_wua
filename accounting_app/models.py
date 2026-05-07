from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ("admin", "Administrator"),
        ("manager", "Manager"),
        ("accountant", "Accountant"),
        ("viewer", "Viewer"),
    ]
    
    CURRENCY_CHOICES = [
        ("MWK", "Malawi Kwacha (K)"),
        ("USD", "US Dollar ($)"),
        ("EUR", "Euro (€)"),
        ("GBP", "British Pound (£)"),
        ("ZAR", "South African Rand (R)"),
        ("ZMW", "Zambian Kwacha (ZK)"),
        ("BWP", "Botswana Pula (P)"),
        ("TZS", "Tanzanian Shilling (TSh)"),
        ("KES", "Kenyan Shilling (KSh)"),
        ("UGX", "Ugandan Shilling (USh)"),
        ("NGN", "Nigerian Naira (₦)"),
        ("GHS", "Ghanaian Cedi (₵)"),
        ("INR", "Indian Rupee (₹)"),
        ("CNY", "Chinese Yuan (¥)"),
        ("JPY", "Japanese Yen (¥)"),
        ("AUD", "Australian Dollar (A$)"),
        ("CAD", "Canadian Dollar (C$)"),
        ("CHF", "Swiss Franc (CHF)"),
        ("AED", "UAE Dirham (د.إ)"),
        ("SAR", "Saudi Riyal (﷼)"),
    ]
    
    SMS_PROVIDER_CHOICES = [
        ("twilio", "Twilio"),
        ("africastalking", "Africa's Talking"),
        ("bulksms", "BulkSMS"),
        ("msg91", "MSG91"),
        ("none", "No SMS (Demo Mode)"),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="admin")
    company_name = models.CharField(max_length=255, blank=True)
    last_activity = models.DateTimeField(null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    tax_id = models.CharField(max_length=50, blank=True)
    currency = models.CharField(max_length=10, choices=CURRENCY_CHOICES, default="MWK")
    
    sms_provider = models.CharField(max_length=30, choices=SMS_PROVIDER_CHOICES, default="none")
    sms_api_key = models.CharField(max_length=255, blank=True)
    sms_api_secret = models.CharField(max_length=255, blank=True)
    sms_sender_id = models.CharField(max_length=20, blank=True)
    
    whatsapp_number = models.CharField(max_length=20, blank=True, help_text="WhatsApp number with country code (e.g., 265991234567)")
    whatsapp_message = models.CharField(max_length=255, default="Hello! I would like to inquire about your services.")
    enable_whatsapp_chat = models.BooleanField(default=True)
    
    WHATSAPP_VERIFIED_CHOICES = [
        ("pending", "Pending"),
        ("verified", "Verified"),
        ("expired", "Expired"),
    ]
    whatsapp_status = models.CharField(max_length=20, choices=WHATSAPP_VERIFIED_CHOICES, default="pending")
    whatsapp_session_token = models.CharField(max_length=500, blank=True, help_text="WhatsApp Web session token")
    whatsapp_qr_code = models.TextField(blank=True, help_text="Base64 QR code for WhatsApp Web")
    
    THEME_CHOICES = [
        ("light", "Light"),
        ("dark", "Dark"),
    ]
    ACCENT_COLOR_CHOICES = [
        ("primary", "Blue (Default)"),
        ("success", "Green"),
        ("danger", "Red"),
        ("warning", "Orange"),
        ("info", "Cyan"),
        ("purple", "Purple"),
    ]
    
    theme = models.CharField(max_length=10, choices=THEME_CHOICES, default="light")
    accent_color = models.CharField(max_length=20, choices=ACCENT_COLOR_CHOICES, default="primary")
    sidebar_color = models.CharField(max_length=20, default="#1a1a2e")
    ticker_color = models.CharField(max_length=20, default="#1a1a2e")
    header_color = models.CharField(max_length=20, default="#0d6efd")
    
    TITLE_ANIMATION_CHOICES = [
        ("none", "None"),
        ("underline", "Underline"),
        ("logo", "Logo Effect"),
        ("fade", "Fade In"),
        ("fadeslide", "Fade Slide"),
        ("gradient", "Gradient"),
        ("pulse", "Pulse"),
    ]
    title_animation = models.CharField(max_length=20, choices=TITLE_ANIMATION_CHOICES, default="gradient")

    can_access_dashboard = models.BooleanField(default=True, help_text="Can access the dashboard")
    can_view_beneficiaries = models.BooleanField(default=True, help_text="Can view beneficiaries")
    can_edit_beneficiaries = models.BooleanField(default=False, help_text="Can edit beneficiaries")
    can_delete_beneficiaries = models.BooleanField(default=False, help_text="Can delete beneficiaries")
    can_view_invoices = models.BooleanField(default=True, help_text="Can view invoices")
    can_edit_invoices = models.BooleanField(default=False, help_text="Can create/edit invoices")
    can_delete_invoices = models.BooleanField(default=False, help_text="Can delete invoices")
    can_view_payments = models.BooleanField(default=True, help_text="Can view payments")
    can_edit_payments = models.BooleanField(default=False, help_text="Can record payments")
    can_delete_payments = models.BooleanField(default=False, help_text="Can delete payments")
    can_view_expenses = models.BooleanField(default=True, help_text="Can view expenses")
    can_edit_expenses = models.BooleanField(default=False, help_text="Can create/edit expenses")
    can_delete_expenses = models.BooleanField(default=False, help_text="Can delete expenses")
    can_view_reports = models.BooleanField(default=True, help_text="Can view reports")
    can_export_reports = models.BooleanField(default=False, help_text="Can export reports")
    can_view_journal = models.BooleanField(default=False, help_text="Can view journal entries")
    can_edit_journal = models.BooleanField(default=False, help_text="Can create/edit journal entries")
    can_view_budgets = models.BooleanField(default=False, help_text="Can view budgets")
    can_edit_budgets = models.BooleanField(default=False, help_text="Can create/edit budgets")
    can_delete_budgets = models.BooleanField(default=False, help_text="Can delete budgets")
    can_manage_users = models.BooleanField(default=False, help_text="Can manage users")
    can_access_settings = models.BooleanField(default=False, help_text="Can access system settings")
    can_communicate = models.BooleanField(default=False, help_text="Can send communications (SMS/WhatsApp)")
    can_view_employees = models.BooleanField(default=False, help_text="Can view employee records")
    can_edit_employees = models.BooleanField(default=False, help_text="Can manage employees")
    can_access_management = models.BooleanField(default=False, help_text="Can access management section (schemes, trustees, etc.)")

    def __str__(self):
        return self.user.username
    
    def get_currency_symbol(self):
        symbols = {
            "MWK": "K", "USD": "$", "EUR": "€", "GBP": "£", "ZAR": "R",
            "ZMW": "ZK", "BWP": "P", "TZS": "TSh", "KES": "KSh", "UGX": "USh",
            "NGN": "₦", "GHS": "₵", "INR": "₹", "CNY": "¥", "JPY": "¥",
            "AUD": "A$", "CAD": "C$", "CHF": "CHF", "AED": "د.إ", "SAR": "﷼",
        }
        return symbols.get(self.currency, self.currency)
    
    def is_admin(self):
        return self.role == "admin" or (
            self.can_access_dashboard and self.can_edit_beneficiaries and self.can_delete_beneficiaries
            and self.can_edit_invoices and self.can_delete_invoices and self.can_edit_payments
            and self.can_delete_payments and self.can_edit_expenses and self.can_delete_expenses
            and self.can_manage_users and self.can_access_settings
        )

    def is_manager(self):
        return self.role in ["admin", "manager"] or (
            self.can_edit_beneficiaries and self.can_delete_beneficiaries
            and self.can_edit_invoices and self.can_edit_payments
        )

    def is_accountant(self):
        return self.role in ["admin", "manager", "accountant"] or (
            self.can_view_beneficiaries and self.can_edit_beneficiaries
            and self.can_view_invoices and self.can_edit_invoices
            and self.can_view_payments and self.can_edit_payments
        )

    def can_view(self):
        return self.can_access_dashboard or self.can_view_beneficiaries or self.can_view_invoices

    def can_edit(self):
        return (self.role in ["admin", "manager", "accountant"] or
                self.can_edit_beneficiaries or self.can_edit_invoices or
                self.can_edit_payments or self.can_edit_expenses)

    def can_delete(self):
        return (self.role in ["admin", "manager"] or
                self.can_delete_beneficiaries or self.can_delete_invoices or
                self.can_delete_payments or self.can_delete_expenses)
    
    def has_settings_access(self):
        return self.role == "admin" or self.can_access_settings

    def has_user_management_access(self):
        return self.role == "admin" or self.can_manage_users


class Account(models.Model):
    ACCOUNT_TYPES = [
        ("asset", "Asset"),
        ("liability", "Liability"),
        ("equity", "Equity"),
        ("revenue", "Revenue"),
        ("expense", "Expense"),
    ]
    name = models.CharField(max_length=100)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    parent = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, related_name="children")
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["code"]

    def __str__(self):
        return f"{self.code} - {self.name}"

    def get_nature(self):
        if self.account_type in ["asset", "expense"]:
            return "debit"
        return "credit"


class Beneficiary(models.Model):
    BENEFICIARY_TYPE_CHOICES = [
        ("private", "Private"),
        ("communal", "Communal"),
    ]
    SCHEME_CHOICES = [
        ("Mangale", "Mangale"),
        ("Nkala", "Nkala"),
        ("Dodza", "Dodza"),
        ("Milala", "Milala"),
    ]
    name = models.CharField(max_length=255)
    beneficiary_type = models.CharField(max_length=20, choices=BENEFICIARY_TYPE_CHOICES, default="private")
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    village = models.CharField(max_length=100, blank=True)
    scheme = models.CharField(max_length=50, choices=SCHEME_CHOICES, blank=True)
    country = models.CharField(max_length=100, blank=True)
    tax_id = models.CharField(max_length=50, blank=True)
    household_count = models.PositiveIntegerField(default=0, help_text="Number of households served")
    total_bill = models.DecimalField(max_digits=12, decimal_places=2, default=0, help_text="Total amount invoiced")
    total_paid = models.DecimalField(max_digits=12, decimal_places=2, default=0, help_text="Total amount paid")
    total_outstanding = models.DecimalField(max_digits=12, decimal_places=2, default=0, help_text="Outstanding balance")
    credit_limit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_terms = models.IntegerField(default=30, help_text="Payment terms in days")
    tap_installed_date = models.DateField(null=True, blank=True, help_text="Date when tap was installed")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Normalize beneficiary_type to lowercase
        if self.beneficiary_type:
            self.beneficiary_type = self.beneficiary_type.lower()
        if self.pk:
            self.total_bill = sum(invoice.total_amount for invoice in self.invoices.all())
            self.total_paid = sum(payment.amount for payment in self.payments.all())
            self.total_outstanding = self.total_bill - self.total_paid
        super().save(*args, **kwargs)
        if self.pk:
            self.total_bill = sum(invoice.total_amount for invoice in self.invoices.all())
            self.total_paid = sum(payment.amount for payment in self.payments.all())
            self.total_outstanding = self.total_bill - self.total_paid
            models.Model.save(self, update_fields=['total_bill', 'total_paid', 'total_outstanding'])

    def recalculate_totals(self):
        self.total_bill = sum(invoice.total_amount for invoice in self.invoices.all())
        self.total_paid = sum(payment.amount for payment in self.payments.all())
        self.total_outstanding = self.total_bill - self.total_paid
        models.Model.save(self, update_fields=['total_bill', 'total_paid', 'total_outstanding'])
    
    def is_overdue_account(self):
        return self.total_outstanding > self.credit_limit and self.credit_limit > 0
    
    def has_overdue_invoices(self):
        return self.invoices.filter(
            due_date__lt=timezone.now().date(),
            status__in=['sent', 'viewed', 'partial', 'overdue']
        ).exists()
    
    def get_overdue_invoices_count(self):
        return self.invoices.filter(
            due_date__lt=timezone.now().date(),
            status__in=['sent', 'viewed', 'partial', 'overdue']
        ).count()
    
    def get_opening_balance(self, fiscal_year):
        balance = self.opening_balances.filter(fiscal_year=fiscal_year).first()
        return balance.amount if balance else Decimal('0.00')
    
    def get_total_balance_with_opening(self, fiscal_year):
        return self.get_opening_balance(fiscal_year) + self.total_outstanding
    
    def get_unpaid_invoices_count(self):
        return self.invoices.filter(
            status__in=['sent', 'viewed', 'partial', 'overdue']
        ).count()
    
    def get_unpaid_invoices(self):
        return self.invoices.filter(
            status__in=['sent', 'viewed', 'partial', 'overdue']
        )
    
    def get_unpaid_invoices_total(self):
        unpaid = self.get_unpaid_invoices()
        return sum(invoice.total_amount for invoice in unpaid)


class Vendor(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    tax_id = models.CharField(max_length=50, blank=True)
    payment_terms = models.IntegerField(default=30, help_text="Payment terms in days")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Invoice(models.Model):
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("sent", "Sent"),
        ("viewed", "Viewed"),
        ("paid", "Paid"),
        ("partial", "Partial"),
        ("overdue", "Overdue"),
        ("cancelled", "Cancelled"),
    ]
    invoice_number = models.CharField(max_length=50, unique=True)
    beneficiary = models.ForeignKey(Beneficiary, on_delete=models.CASCADE, related_name="invoices")
    issue_date = models.DateField(default=timezone.now)
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    household_count = models.PositiveIntegerField(default=0, help_text="Number of households")
    cost_per_unit = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Cost per household")
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    notes = models.TextField(blank=True)
    terms = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_bulk = models.BooleanField(default=False, help_text="Created via bulk invoice creation")
    bulk_group_id = models.CharField(max_length=50, blank=True, null=True, help_text="Group ID for bulk created invoices")

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.invoice_number

    def calculate_totals(self):
        subtotal = self.household_count * self.cost_per_unit
        self.tax_amount = subtotal * (self.tax_rate / 100)
        self.total_amount = subtotal + self.tax_amount - self.discount
        self.save()
        self.update_payment_status()
        self.beneficiary.recalculate_totals()
    
    def update_payment_status(self):
        """Auto-update invoice status based on payments"""
        balance = self.balance()
        if balance < 0:
            self.status = 'paid'  # Has brought forward
        elif balance == 0:
            self.status = 'paid'  # No balance
        else:
            amount_paid = self.total_paid()
            if amount_paid > 0:
                self.status = 'partial'  # Has balance
            models.Model.save(self, update_fields=['status'])

    def amount_paid(self):
        return sum(payment.amount for payment in self.payments.all())
    
    def amount_due(self):
        return self.total_amount - self.amount_paid()
    
    def total_paid(self):
        return self.payments.aggregate(total=models.Sum('amount'))['total'] or 0
    
    def balance(self):
        return self.total_amount - self.total_paid()
    
    def is_fully_paid(self):
        """Check if invoice is fully paid"""
        return self.amount_due() <= 0
    
    def payment_status_display(self):
        """Return human-readable payment status"""
        balance = self.balance()
        if balance > 0:
            return "Has Balance"
        elif balance < 0:
            return "Has Brought Forward"
        else:
            return "No Balance"
    
    def payment_percentage(self):
        """Return percentage of invoice that has been paid"""
        if self.total_amount > 0:
            return (self.amount_paid() / self.total_amount) * 100
        return 0


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="items")
    description = models.CharField(max_length=255)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=12, decimal_places=2)

    def save(self, *args, **kwargs):
        self.total = self.quantity * self.unit_price
        super().save(*args, **kwargs)
        self.invoice.calculate_totals()

    def __str__(self):
        return self.description


class Payment(models.Model):
    PAYMENT_METHODS = [
        ("cash", "Cash"),
        ("bank_transfer", "Bank Transfer"),
        ("credit_card", "Credit Card"),
        ("check", "Check"),
        ("mobile_money", "Mobile Money"),
        ("other", "Other"),
    ]
    invoice = models.ForeignKey(Invoice, on_delete=models.SET_NULL, related_name="payments", null=True, blank=True)
    beneficiary = models.ForeignKey(Beneficiary, on_delete=models.CASCADE, related_name="payments")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True, related_name="payments", help_text="Chart of accounts category for this payment")
    payment_date = models.DateField(default=timezone.now)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default="bank_transfer")
    reference = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_bulk = models.BooleanField(default=False, help_text="Created via bulk payment")
    bulk_group_id = models.CharField(max_length=50, blank=True, null=True, help_text="Group ID for bulk payments")
    is_brought_forward = models.BooleanField(default=False, help_text="Payment brought forward from previous period")

    def __str__(self):
        if self.invoice:
            return f"Payment {self.amount} for {self.invoice.invoice_number}"
        return f"Payment {self.amount} for {self.beneficiary.name}"

    def save(self, *args, **kwargs):
        if self.beneficiary:
            self.beneficiary.recalculate_totals()
        super().save(*args, **kwargs)
        if self.invoice:
            self.invoice.update_payment_status()

    def delete(self, *args, **kwargs):
        beneficiary = self.beneficiary
        account = self.account
        amount = self.amount
        invoice = self.invoice
        super().delete(*args, **kwargs)
        if beneficiary:
            beneficiary.recalculate_totals()
        if account:
            account.balance -= amount
            account.save()
        if invoice:
            invoice.update_payment_status()


class Expense(models.Model):
    expense_number = models.CharField(max_length=50, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, blank=True, related_name="expenses")
    description = models.TextField(blank=True, default="")
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    expense_date = models.DateField(default=timezone.now)
    receipt = models.ImageField(upload_to="receipts/", blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    payment_date = models.DateField(blank=True, null=True)
    account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True, related_name="expenses")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.expense_number} - {self.description[:30]}"
    
    def calculate_total(self):
        return sum(item.amount for item in self.items.all())
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class ExpenseItem(models.Model):
    CATEGORY_CHOICES = [
        ("travel", "Travel"),
        ("utilities", "Utilities"),
        ("supplies", "Supplies"),
        ("rent", "Rent"),
        ("salaries", "Salaries"),
        ("marketing", "Marketing"),
        ("insurance", "Insurance"),
        ("taxes", "Taxes"),
        ("professional_services", "Professional Services"),
        ("equipment", "Equipment"),
        ("other", "Other"),
    ]
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE, related_name="items")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField()
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.category} - {self.description[:20]}: {self.amount}"
    
    def save(self, *args, **kwargs):
        self.amount = self.quantity * self.unit_price
        super().save(*args, **kwargs)


class JournalEntry(models.Model):
    entry_number = models.CharField(max_length=50, unique=True)
    date = models.DateField(default=timezone.now)
    description = models.CharField(max_length=255)
    is_posted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date", "-created_at"]

    def __str__(self):
        return self.entry_number

    def total_debit(self):
        return sum(line.debit for line in self.lines.all())

    def total_credit(self):
        return sum(line.credit for line in self.lines.all())

    def is_balanced(self):
        return self.total_debit() == self.total_credit()


class JournalEntryLine(models.Model):
    journal_entry = models.ForeignKey(JournalEntry, on_delete=models.CASCADE, related_name="lines")
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    debit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    credit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    memo = models.CharField(max_length=255, blank=True)

    def save(self, *args, **kwargs):
        if self.debit > 0 and self.credit > 0:
            raise ValueError("A line cannot have both debit and credit")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.account.name}: Dr {self.debit} / Cr {self.credit}"


class TaxRate(models.Model):
    name = models.CharField(max_length=100)
    rate = models.DecimalField(max_digits=5, decimal_places=2)
    is_active = models.BooleanField(default=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.rate}%)"


class Budget(models.Model):
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-start_date"]

    def __str__(self):
        return f"Budget {self.start_date} to {self.end_date}"

    @property
    def total_amount(self):
        return sum(line.total for line in self.lines.all())

    def line_count(self):
        return self.lines.count()


class BudgetLine(models.Model):
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, related_name="lines")
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="budget_lines")
    description = models.CharField(max_length=255, blank=True)
    quantity = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.account.name} - {self.total}"

    @property
    def total(self):
        return self.quantity * self.unit_price


class ActivityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=100)
    model_name = models.CharField(max_length=100)
    object_id = models.PositiveIntegerField(null=True)
    description = models.TextField()
    ip_address = models.GenericIPAddressField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.user} - {self.action} - {self.model_name}"


class BeneficiaryHistory(models.Model):
    ACTION_CHOICES = [
        ("created", "Created"),
        ("updated", "Updated"),
        ("deleted", "Deleted"),
    ]
    beneficiary = models.ForeignKey(Beneficiary, on_delete=models.CASCADE, related_name="history")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    field_name = models.CharField(max_length=100, blank=True)
    old_value = models.TextField(blank=True)
    new_value = models.TextField(blank=True)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.beneficiary.name} - {self.action} - {self.field_name}"


class BeneficiaryStatusLog(models.Model):
    STATUS_CHOICES = [
        ("activated", "Activated"),
        ("deactivated", "Deactivated"),
    ]
    beneficiary = models.ForeignKey(Beneficiary, on_delete=models.CASCADE, related_name="status_logs")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    changed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-changed_at"]

    def __str__(self):
        return f"{self.beneficiary.name} - {self.status} - {self.changed_at}"


class OpeningBalance(models.Model):
    beneficiary = models.ForeignKey(Beneficiary, on_delete=models.CASCADE, related_name="opening_balances")
    fiscal_year = models.IntegerField()
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, help_text="Balance brought forward from previous year")
    notes = models.TextField(blank=True, help_text="Notes about this opening balance")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["beneficiary", "fiscal_year"]
        ordering = ["-fiscal_year"]

    def __str__(self):
        return f"{self.beneficiary.name} - FY {self.fiscal_year}: {self.amount}"


class YearEndRollover(models.Model):
    fiscal_year = models.IntegerField(unique=True)
    rollover_date = models.DateField()
    total_clients = models.IntegerField(default=0)
    total_opening_balance = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-fiscal_year"]

    def __str__(self):
        return f"Year-End Rollover {self.fiscal_year}"


class Scheme(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_total_population(self):
        return sum(vp.population for vp in self.village_populations.all())


class Village(models.Model):
    scheme = models.ForeignKey(Scheme, on_delete=models.CASCADE, related_name="villages")
    name = models.CharField(max_length=100)
    household_count = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]
        unique_together = ["scheme", "name"]

    def __str__(self):
        return f"{self.name} ({self.scheme.name})"

    def get_population(self):
        latest = self.population_records.order_by('-recorded_date').first()
        return latest.population if latest else 0


class VillagePopulation(models.Model):
    village = models.ForeignKey(Village, on_delete=models.CASCADE, related_name="population_records")
    population = models.PositiveIntegerField(default=0)
    recorded_date = models.DateField(default=timezone.now)
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-recorded_date"]

    def __str__(self):
        return f"{self.village.name}: {self.population} ({self.recorded_date})"


SCHEME_CHOICES = [
    ("Mangale", "Mangale"),
    ("Dodza", "Dodza"),
    ("Nkala", "Nkala"),
    ("Milala", "Milala"),
]

SEX_CHOICES = [
    ("M", "Male"),
    ("F", "Female"),
]


class BoardOfTrustees(models.Model):
    TITLE_CHOICES = [
        ("Chairperson", "Chairperson"),
        ("Vice Chairperson", "Vice Chairperson"),
        ("Secretary", "Secretary"),
        ("Vice Secretary", "Vice Secretary"),
        ("Treasurer", "Treasurer"),
        ("Member", "Member"),
    ]
    
    name = models.CharField(max_length=255)
    sex = models.CharField(max_length=10, choices=SEX_CHOICES)
    village = models.CharField(max_length=100)
    scheme_present = models.CharField(max_length=50, choices=SCHEME_CHOICES)
    title = models.CharField(max_length=50, choices=TITLE_CHOICES, blank=True)
    contact = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class GeneralAssemblyMember(models.Model):
    TITLE_CHOICES = [
        ("Chairperson", "Chairperson"),
        ("Vice Chairperson", "Vice Chairperson"),
        ("Secretary", "Secretary"),
        ("Vice Secretary", "Vice Secretary"),
        ("Treasurer", "Treasurer"),
        ("Member", "Member"),
    ]
    
    name = models.CharField(max_length=255)
    sex = models.CharField(max_length=10, choices=SEX_CHOICES)
    village = models.CharField(max_length=100)
    scheme_present = models.CharField(max_length=50, choices=SCHEME_CHOICES)
    title = models.CharField(max_length=50, choices=TITLE_CHOICES, blank=True)
    contact = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Employee(models.Model):
    EMPLOYEE_TYPE_CHOICES = [
        ("full_time", "Full Time"),
        ("part_time", "Part Time"),
        ("contract", "Contract"),
        ("casual", "Casual"),
    ]
    
    PENSION_RATE = Decimal('0.10')
    
    name = models.CharField(max_length=255)
    sex = models.CharField(max_length=10, choices=SEX_CHOICES)
    village = models.CharField(max_length=100)
    scheme_present = models.CharField(max_length=50, choices=SCHEME_CHOICES)
    contact = models.CharField(max_length=50, blank=True)
    employee_type = models.CharField(max_length=20, choices=EMPLOYEE_TYPE_CHOICES, default="full_time")
    position = models.CharField(max_length=100, blank=True)
    department = models.CharField(max_length=100, blank=True)
    salary = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    date_recruited = models.DateField(null=True, blank=True, verbose_name="Starting Date")
    date_dismissed = models.DateField(null=True, blank=True, verbose_name="End Date")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
    
    def get_days_worked(self):
        from django.utils import timezone
        if not self.date_recruited:
            return 0
        end = self.date_dismissed if self.date_dismissed else timezone.now().date()
        return (end - self.date_recruited).days
    
    def get_daily_salary(self):
        if self.salary and self.salary > 0:
            return self.salary / 30
        return Decimal('0.00')
    
    def get_pension_amount(self):
        days_worked = self.get_days_worked()
        daily_salary = self.get_daily_salary()
        if days_worked > 0 and daily_salary > 0:
            return daily_salary * days_worked * self.PENSION_RATE
        return Decimal('0.00')


class EmployeeSalary(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="salaries")
    salary = models.DecimalField(max_digits=12, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True, help_text="Leave empty if currently active")
    pension_rate = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('10.00'), help_text="Pension rate percentage")
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        ordering = ["-start_date"]
        unique_together = ["employee", "start_date"]
    
    def __str__(self):
        return f"{self.employee.name} - {self.salary} ({self.start_date} to {self.end_date or 'Present'})"
    
    def get_daily_salary(self):
        if self.salary and self.salary > 0:
            return self.salary / 30
        return Decimal('0.00')
    
    def get_days_in_period(self):
        from django.utils import timezone
        end = self.end_date if self.end_date else timezone.now().date()
        return (end - self.start_date).days
    
    def calculate_pension(self):
        days = self.get_days_in_period()
        if days > 0:
            return self.get_daily_salary() * days * (self.pension_rate / 100)
        return Decimal('0.00')


class Report(models.Model):
    REPORT_TYPES = [
        ("financial", "Financial Report"),
        ("scheme", "Scheme Performance Report"),
        ("expense", "Expense Report"),
        ("client", "Client Report"),
    ]
    
    name = models.CharField(max_length=255)
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    from_date = models.DateField()
    to_date = models.DateField()
    
    total_invoiced = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_payments = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_expenses = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    balance_to_collect = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    net_income = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    
    additional_data = models.JSONField(default=dict, blank=True)
    
    is_saved = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.report_type}) - {self.from_date} to {self.to_date}"


class CommunicationLog(models.Model):
    COMMUNICATION_TYPES = [
        ("sms", "SMS"),
        ("voice_call", "Voice Call"),
        ("video_call", "Video Call"),
        ("whatsapp", "WhatsApp"),
    ]
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("sent", "Sent"),
        ("delivered", "Delivered"),
        ("failed", "Failed"),
    ]
    communication_type = models.CharField(max_length=20, choices=COMMUNICATION_TYPES)
    recipient = models.CharField(max_length=255, help_text="Phone number or recipient name")
    recipient_beneficiary = models.ForeignKey(Beneficiary, on_delete=models.SET_NULL, null=True, blank=True, related_name="communications")
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    sent_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="communications_sent")
    sent_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-sent_at"]

    def __str__(self):
        return f"{self.communication_type} to {self.recipient} - {self.sent_at.strftime('%Y-%m-%d %H:%M')}"


class UserMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-sent_at"]
        indexes = [
            models.Index(fields=["sender", "recipient", "-sent_at"]),
        ]

    def __str__(self):
        return f"{self.sender.username} -> {self.recipient.username} at {self.sent_at.strftime('%H:%M')}"

    @staticmethod
    def get_conversation(user1, user2):
        return UserMessage.objects.filter(
            (models.Q(sender=user1) & models.Q(recipient=user2)) |
            (models.Q(sender=user2) & models.Q(recipient=user1))
        ).order_by("sent_at")

    @staticmethod
    def get_unread_count(user, other_user=None):
        if other_user:
            return UserMessage.objects.filter(sender=other_user, recipient=user, is_read=False).count()
        return UserMessage.objects.filter(recipient=user, is_read=False).count()

    @staticmethod
    def get_conversations_for_user(user):
        from django.db.models import Max, Q, Count
        conversations = UserMessage.objects.filter(
            Q(sender=user) | Q(recipient=user)
        ).values(
            "sender", "recipient"
        ).annotate(
            last_message_time=Max("sent_at"),
            message_count=Count("id")
        ).order_by("-last_message_time")
        return conversations


class UserCall(models.Model):
    CALL_TYPES = [
        ("voice", "Voice Call"),
        ("video", "Video Call"),
    ]
    STATUS_CHOICES = [
        ("ringing", "Ringing"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
        ("missed", "Missed"),
        ("ended", "Ended"),
    ]
    caller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="calls_made")
    callee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="calls_received")
    call_type = models.CharField(max_length=10, choices=CALL_TYPES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="ringing")
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    duration = models.IntegerField(default=0, help_text="Duration in seconds")
    caller_offer = models.TextField(blank=True, default="")
    callee_answer = models.TextField(blank=True, default="")
    caller_ice = models.TextField(blank=True, default="")
    callee_ice = models.TextField(blank=True, default="")

    class Meta:
        ordering = ["-started_at"]

    def __str__(self):
        return f"{self.call_type} {self.caller.username} -> {self.callee.username} ({self.status})"


class GalleryImage(models.Model):
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='gallery/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return self.title or f"Gallery Image {self.id}"


class Service(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='services/')
    caption = models.CharField(max_length=255, blank=True, help_text="Short caption explaining the picture")
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0, help_text="Order of display (lower numbers appear first)")
    
    class Meta:
        ordering = ['order', 'title']
    
    def __str__(self):
        return self.title


class LoginSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='login_sessions')
    session_key = models.CharField(max_length=40, db_index=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True, help_text="Browser and device information")
    device_info = models.CharField(max_length=255, blank=True, help_text="Parsed device/OS/browser info")
    login_time = models.DateTimeField(auto_now_add=True)
    logout_time = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-login_time']

    def __str__(self):
        return f"{self.user.username} - {self.login_time}"

    @staticmethod
    def parse_user_agent(user_agent):
        if not user_agent:
            return "Unknown Device"
        
        device = "Unknown OS"
        browser = "Unknown Browser"
        
        if "Windows" in user_agent:
            if "Windows NT 10.0" in user_agent:
                device = "Windows 10/11"
            elif "Windows NT 6.3" in user_agent:
                device = "Windows 8.1"
            elif "Windows NT 6.1" in user_agent:
                device = "Windows 7"
            else:
                device = "Windows"
        elif "Macintosh" in user_agent or "Mac OS X" in user_agent:
            device = "macOS"
        elif "Linux" in user_agent:
            device = "Linux"
        elif "Android" in user_agent:
            version = ""
            for part in user_agent.split(';'):
                if 'Android' in part:
                    version = part.strip()
                    break
            device = f"Android ({version})"
        elif "iPhone" in user_agent or "iPad" in user_agent:
            device = "iOS (iPhone/iPad)"
        elif "Mobile" in user_agent:
            device = "Mobile Device"
        
        if "Edg/" in user_agent:
            browser = "Microsoft Edge"
        elif "Chrome/" in user_agent and "Safari/" in user_agent and "Edg/" not in user_agent:
            browser = "Google Chrome"
        elif "Firefox/" in user_agent:
            browser = "Mozilla Firefox"
        elif "Safari/" in user_agent and "Chrome/" not in user_agent:
            browser = "Safari"
        elif "Opera" in user_agent or "OPR/" in user_agent:
            browser = "Opera"
        
        if "Mobile" in user_agent and "iPad" not in user_agent:
            return f"{device} (Mobile) - {browser}"
        return f"{device} - {browser}"


class DeletedRecord(models.Model):
    model_name = models.CharField(max_length=100, help_text="Name of the model (e.g., Beneficiary)")
    object_id = models.CharField(max_length=100, help_text="Original ID of the deleted object")
    data = models.TextField(help_text="Serialized JSON data of the deleted record")
    deleted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='deleted_records')
    deleted_at = models.DateTimeField(auto_now_add=True)
    recovered = models.BooleanField(default=False)
    recovered_at = models.DateTimeField(null=True, blank=True)
    recovery_note = models.TextField(blank=True)

    class Meta:
        ordering = ['-deleted_at']

    def __str__(self):
        return f"{self.model_name} #{self.object_id} (deleted: {self.deleted_at})"

    def recover(self):
        from django.apps import apps
        import json
        model = apps.get_model('accounting_app', self.model_name.lower())
        if not model:
            return False
        
        data = json.loads(self.data)
        
        related_fields = []
        for field in model._meta.get_fields():
            if field.is_relation and hasattr(field, 'to'):
                related_fields.append(field.name)
        
        for field in related_fields:
            if field in data:
                del data[field]
        
        try:
            obj = model.objects.create(**data)
            self.recovered = True
            self.recovered_at = timezone.now()
            self.save(update_fields=['recovered', 'recovered_at'])
            return obj
        except Exception:
            return False


class LandingPageSettings(models.Model):
    primary_color = models.CharField(max_length=7, default='#0984e3', help_text="Primary color (hex code like #0984e3)")
    secondary_color = models.CharField(max_length=7, default='#00b894', help_text="Secondary color (hex code like #00b894)")
    hero_gradient_start = models.CharField(max_length=7, default='#0f1923', help_text="Hero section gradient start color")
    hero_gradient_mid = models.CharField(max_length=7, default='#1a2a3a', help_text="Hero section gradient middle color")
    hero_gradient_end = models.CharField(max_length=7, default='#0984e3', help_text="Hero section gradient end color")
    navbar_bg = models.CharField(max_length=7, default='#0f1923', help_text="Navbar background color")
    section_bg_light = models.CharField(max_length=7, default='#f5f6fa', help_text="Light section background color")
    text_primary = models.CharField(max_length=7, default='#1e272e', help_text="Primary text color")
    text_secondary = models.CharField(max_length=7, default='#636e72', help_text="Secondary text color")
    cta_gradient_start = models.CharField(max_length=7, default='#0984e3', help_text="CTA section gradient start")
    cta_gradient_end = models.CharField(max_length=7, default='#00b894', help_text="CTA section gradient end")
    whatsapp_color = models.CharField(max_length=7, default='#25D366', help_text="WhatsApp icon color")
    is_active = models.BooleanField(default=True, help_text="Use these settings (only one should be active)")
    updated_at = models.DateTimeField(auto_now=True)

    site_name = models.CharField(max_length=100, default='Nkula WUA', help_text="Site name shown in navbar")
    hero_title = models.CharField(max_length=200, default='Nkula Water Users Association (WUA)', help_text="Main hero heading")
    hero_title_highlight = models.CharField(max_length=200, default='Good and Quality Water for All', help_text="Highlighted text in hero (span)")
    hero_subtitle = models.CharField(max_length=200, default='Good and Quality Water for All', help_text="Hero subtitle (h2)")
    hero_description = models.TextField(default='Nkula Water Users Association is a community-based institution established under the Government of Malawi with African Development Bank (ADB) support to enhance safe, sustainable, and reliable water access in communities.', help_text="Hero paragraph description")
    about_title = models.CharField(max_length=100, default='About Us', help_text="About section title")
    about_subtitle = models.CharField(max_length=100, default='Who We Are', help_text="About section subtitle")
    about_content = models.TextField(default='Nkula Water Users Association (WUA) is a community-based institution established in 2013 under the Government of Malawi with financial support from the African Development Bank (ADB). Our purpose is to empower communities to take full responsibility in water management and support community development initiatives.\n\nWe work with local leaders and community members to ensure water schemes are properly managed, protected, and maintained for the benefit of all.', help_text="About section paragraphs (use \\n\\n for new paragraphs)")
    vision_title = models.CharField(max_length=100, default='Vision, Mission & Values', help_text="Vision section title")
    vision_subtitle = models.CharField(max_length=100, default='Our guiding principles', help_text="Vision section subtitle")
    vision_text = models.TextField(default='Good and quality water for all.', help_text="Vision statement")
    mission_text = models.TextField(default='Empowering the community, promoting good health, and adapting and mitigating the effects of climate change through sustainable water management.', help_text="Mission statement")
    values_text = models.TextField(default='Transparency and Accountability\nHonesty\nTeamwork', help_text="Core values (one per line)")
    location_title = models.CharField(max_length=100, default='Our Location', help_text="Location section title")
    location_subtitle = models.CharField(max_length=100, default='Where We Operate', help_text="Location section subtitle")
    location_address = models.CharField(max_length=300, default='Matandika Village, T/A Nkula, Machinga District, Malawi', help_text="Physical address")
    location_description = models.TextField(default='We serve multiple villages through our managed schemes and catchment areas.', help_text="Location description")
    contact_phone = models.CharField(max_length=30, default='+265 982 960 373', help_text="Contact phone number")
    contact_email = models.CharField(max_length=100, default='nkulawuamw@gmail.com', help_text="Contact email")
    contact_whatsapp = models.CharField(max_length=30, default='+265 982 960 373', help_text="WhatsApp number (with country code, no +)")
    contact_whatsapp_raw = models.CharField(max_length=30, default='265982960373', help_text="WhatsApp number raw format for link (e.g. 265982960373)")
    projects_title = models.CharField(max_length=100, default='Projects & Achievements', help_text="Projects section title")
    projects_subtitle = models.CharField(max_length=100, default='Our Progress', help_text="Projects section subtitle")
    projects_intro = models.TextField(default='Nkula WUA is committed to improving water availability and sustainability by supporting:', help_text="Projects intro text")
    projects_items = models.TextField(default='Water scheme rehabilitation\nCommunity capacity building\nWater point monitoring\nHygiene and sanitation awareness\nCatchment protection programs', help_text="Project items (one per line)")
    projects_outro = models.TextField(default='We believe safe water is the foundation of a healthy and productive community.', help_text="Projects closing text")
    cta_title = models.CharField(max_length=200, default='Join Us in Building Sustainable Water Access', help_text="Call-to-action heading")
    cta_description = models.TextField(default='Nkula WUA invites partners, community members, and stakeholders to support the mission of providing safe and sustainable water. Together we can protect our water sources and improve lives.', help_text="Call-to-action description")
    footer_text = models.TextField(default='Nkula Water Users Association (WUA)\nGood and Quality Water for All.\n2026 Nkula Water Users Association. All Rights Reserved.\nDesigned for Community Water Development and Sustainability.', help_text="Footer lines (one per line)")

    water_sources_title = models.CharField(max_length=100, default='Our Water Sources', help_text="Water Sources section title")
    water_sources_subtitle = models.TextField(default='Water infrastructure and natural sources sustaining our communities', help_text="Water Sources subtitle")
    water_sources_images = models.TextField(default='intake.png|Water Intake System\nintake 3.png|Intake Infrastructure\npipes.png|Water Distribution Pipes\npulmbers.png|Plumbers at Work\nplumbers survey.png|Survey Work\nmilala survey.png|Milala Scheme Survey', help_text="Image file names and captions (filename|caption per line)")

    news_title = models.CharField(max_length=100, default='News & Updates', help_text="News section title")
    news_subtitle = models.CharField(max_length=100, default='Latest Updates', help_text="News section subtitle")
    news_content = models.TextField(default='Meeting announcements\nScheme maintenance updates\nCommunity sanitation campaigns\nTraining and awareness programs', help_text="News items (one per line)")
    news_intro = models.TextField(default='Stay updated with the latest activities and announcements from Nkula WUA.', help_text="News intro text")

    meeting_objectives_title = models.CharField(max_length=100, default='Meeting Objectives', help_text="Meeting Objectives section title")
    meeting_objectives_subtitle = models.CharField(max_length=100, default='Our Regular Meeting Goals', help_text="Meeting Objectives subtitle")
    meeting_objectives_intro = models.TextField(default='Our regular meetings are aimed at:', help_text="Meeting intro text")
    meeting_objectives_items = models.TextField(default='Discussing ways to improve the performance of water schemes\nReviewing completed activities\nIdentifying challenges faced in the schemes\nPlanning solutions and community action strategies', help_text="Meeting objective items (one per line)")

    schemes_title = models.CharField(max_length=100, default='Our Water Schemes', help_text="Schemes section title")
    schemes_subtitle = models.CharField(max_length=100, default='Schemes and Catchment Areas', help_text="Schemes subtitle")
    schemes_list = models.TextField(default='Mangale Scheme|Serving communities with reliable water access\nNkala Scheme|Managed water infrastructure for local villages\nDodza Scheme|Sustainable water solutions for the community\nMilala Scheme|Clean water access for thousands of residents', help_text="Schemes (name|description per line)")

    villages_title = models.CharField(max_length=100, default='Villages Under Nkula WUA', help_text="Villages section title")
    villages_subtitle = models.CharField(max_length=100, default='Communities Served', help_text="Villages subtitle")
    villages_list = models.TextField(default='Mangale Scheme|GVH Lipongo,Ndanje,Maoni,M\'balaka\nNkala Scheme|GVH Chingoli,Nthipo\nDodza Scheme|GVH Mtambo,Masanjala\nMilala Scheme|GVH Mkalawire,Mpango,Chimwayi,Mlawe', help_text="Villages grouped by scheme (scheme|village1,village2 per line)")

    gallery_title = models.CharField(max_length=100, default='Gallery', help_text="Gallery section title")
    gallery_subtitle = models.CharField(max_length=200, default='Photos of water infrastructure, intakes, pipes, and field work', help_text="Gallery subtitle")

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"Landing Page Settings (Updated: {self.updated_at})"

    def save(self, *args, **kwargs):
        if self.is_active:
            LandingPageSettings.objects.filter(is_active=True).exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)