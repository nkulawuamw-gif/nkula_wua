from django import forms
from django.forms import inlineformset_factory
from django.forms.models import BaseModelFormSet
from django.contrib.auth.models import User
from .models import (
    Account, Beneficiary, Vendor, Invoice, InvoiceItem, Expense, ExpenseItem,
    JournalEntry, JournalEntryLine, Budget, BudgetLine, UserProfile,
    Scheme, Village, VillagePopulation,
    BoardOfTrustees, GeneralAssemblyMember, Employee, Report
)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["company_name", "phone", "address", "tax_id", "currency", "sms_provider", "sms_api_key", "sms_api_secret", "sms_sender_id", "whatsapp_number", "whatsapp_message", "enable_whatsapp_chat", "theme", "accent_color", "sidebar_color"]


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ["username", "email", "password"]


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ["name", "account_type", "code", "description", "parent", "is_active"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
        }


class BeneficiaryForm(forms.ModelForm):
    class Meta:
        model = Beneficiary
        fields = ["name", "beneficiary_type", "phone", "village", "scheme", "country", "tax_id", "household_count", "credit_limit", "payment_terms", "is_active"]
        exclude = ["total_bill", "total_paid", "total_outstanding"]
        widgets = {
            "name": forms.TextInput(attrs={"required": "required"}),
            "beneficiary_type": forms.Select(attrs={"required": "required"}),
            "village": forms.TextInput(attrs={"required": "required"}),
            "scheme": forms.Select(attrs={"required": "required"}),
            "household_count": forms.NumberInput(attrs={"required": "required", "min": "0"}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = True
        self.fields['beneficiary_type'].required = True
        self.fields['village'].required = True
        self.fields['scheme'].required = True
        self.fields['household_count'].required = True


class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ["name", "email", "phone", "address", "city", "country", "tax_id", "payment_terms"]
        widgets = {
            "address": forms.Textarea(attrs={"rows": 3}),
        }


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ["beneficiary", "invoice_number", "issue_date", "due_date", "household_count", "cost_per_unit", "tax_rate", "discount", "notes", "terms", "status"]
        widgets = {
            "issue_date": forms.DateInput(attrs={"type": "date"}),
            "due_date": forms.DateInput(attrs={"type": "date"}),
            "notes": forms.Textarea(attrs={"rows": 3}),
            "terms": forms.Textarea(attrs={"rows": 2}),
        }


class InvoiceItemForm(forms.ModelForm):
    class Meta:
        model = InvoiceItem
        fields = ["description", "quantity", "unit_price"]


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ["vendor", "description", "expense_date", "receipt", "account"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 2}),
            "expense_date": forms.DateInput(attrs={"type": "date"}),
        }
        labels = {
            "vendor": "Vendor (Optional)",
            "account": "Account (Optional)",
            "description": "General Description (Optional)",
        }


class ExpenseItemForm(forms.ModelForm):
    class Meta:
        model = ExpenseItem
        fields = ["category", "description", "quantity", "unit_price"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 2}),
        }


class PaymentForm(forms.Form):
    beneficiary = forms.ModelChoiceField(queryset=Beneficiary.objects.filter(is_active=True).order_by('name'), label="Beneficiary Name")
    payment_date = forms.DateField(label="Payment Date", widget=forms.DateInput(attrs={'type': 'date'}))
    amount = forms.DecimalField(label="Paid Amount", min_value=0)
    account = forms.ModelChoiceField(queryset=Account.objects.filter(is_active=True, account_type='revenue').order_by('code'), label="Paid For")
    payment_method = forms.ChoiceField(choices=[
        ("cash", "Cash"),
        ("bank_transfer", "Bank Transfer"),
        ("mobile_money", "Mobile Money"),
        ("other", "Other"),
    ])
    reference = forms.CharField(label="Reference", required=False, max_length=100)
    notes = forms.CharField(label="Notes", required=False, widget=forms.Textarea(attrs={'rows': 2}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['account'].empty_label = "-- Select Account --"


class JournalEntryForm(forms.ModelForm):
    class Meta:
        model = JournalEntry
        fields = ["entry_number", "date", "description"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
        }


class JournalEntryLineForm(forms.ModelForm):
    class Meta:
        model = JournalEntryLine
        fields = ["account", "debit", "credit", "memo"]


class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ["start_date", "end_date", "notes"]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "end_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "notes": forms.Textarea(attrs={"rows": 2, "class": "form-control"}),
        }


class BudgetLineForm(forms.ModelForm):
    class Meta:
        model = BudgetLine
        fields = ["account", "description", "quantity", "unit_price"]
        widgets = {
            "account": forms.Select(attrs={"class": "form-select"}),
            "description": forms.TextInput(attrs={"class": "form-control"}),
            "quantity": forms.NumberInput(attrs={"class": "form-control", "step": "1"}),
            "unit_price": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
        }


BudgetLineFormSet = inlineformset_factory(
    Budget, BudgetLine, form=BudgetLineForm,
    extra=1, can_delete=True,
)


class SchemeForm(forms.ModelForm):
    class Meta:
        model = Scheme
        fields = ["name", "description", "is_active"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 2}),
        }


class VillageForm(forms.ModelForm):
    class Meta:
        model = Village
        fields = ["scheme", "name", "household_count", "description", "is_active"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 2}),
        }


class VillagePopulationForm(forms.ModelForm):
    class Meta:
        model = VillagePopulation
        fields = ["village", "population", "recorded_date", "notes"]
        widgets = {
            "recorded_date": forms.DateInput(attrs={"type": "date"}),
            "notes": forms.Textarea(attrs={"rows": 2}),
        }


class BulkPopulationUpdateForm(forms.Form):
    def __init__(self, *args, **kwargs):
        villages = kwargs.pop('villages', [])
        super().__init__(*args, **kwargs)
        for village in villages:
            self.fields[f'population_{village.id}'] = forms.IntegerField(
                label=village.name,
                min_value=0,
                required=False,
                initial=village.get_population()
            )


class BoardOfTrusteesForm(forms.ModelForm):
    class Meta:
        model = BoardOfTrustees
        fields = ["name", "sex", "village", "scheme_present", "title", "contact"]
        widgets = {
            "contact": forms.TextInput(attrs={"placeholder": "e.g. +265991234567"}),
        }


class GeneralAssemblyMemberForm(forms.ModelForm):
    class Meta:
        model = GeneralAssemblyMember
        fields = ["name", "sex", "village", "scheme_present", "title", "contact"]
        widgets = {
            "contact": forms.TextInput(attrs={"placeholder": "e.g. +265991234567"}),
        }


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ["name", "sex", "village", "scheme_present", "contact", "employee_type", "position", "department", "salary", "date_recruited", "date_dismissed", "is_active"]
        widgets = {
            "contact": forms.TextInput(attrs={"placeholder": "e.g. +265991234567"}),
            "date_recruited": forms.DateInput(attrs={"type": "date"}),
            "date_dismissed": forms.DateInput(attrs={"type": "date"}),
            "salary": forms.NumberInput(attrs={"min": "0", "step": "0.01"}),
        }


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ["name", "report_type", "from_date", "to_date"]
        widgets = {
            "from_date": forms.DateInput(attrs={"type": "date"}),
            "to_date": forms.DateInput(attrs={"type": "date"}),
        }
