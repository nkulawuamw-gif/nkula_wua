from django.contrib import admin
from .models import (
    UserProfile, Account, Beneficiary, Vendor, Invoice, InvoiceItem,
    Expense, ExpenseItem, JournalEntry, JournalEntryLine, Payment, TaxRate, 
    Budget, ActivityLog, Report, OpeningBalance, YearEndRollover, Scheme, 
    Village, VillagePopulation, BoardOfTrustees, GeneralAssemblyMember, Employee, GalleryImage, Service, LandingPageSettings
)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "company_name", "phone"]
    search_fields = ["user__username", "company_name"]


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ["code", "name", "account_type", "balance", "is_active"]
    list_filter = ["account_type", "is_active"]
    search_fields = ["code", "name"]
    ordering = ["code"]


@admin.register(Beneficiary)
class BeneficiaryAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "phone", "village", "scheme", "household_count", "total_bill", "total_paid", "is_active"]
    list_filter = ["is_active", "scheme"]
    search_fields = ["name", "email"]
    readonly_fields = ["total_bill", "total_paid", "total_outstanding"]


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "phone", "city", "is_active"]
    list_filter = ["is_active", "country"]
    search_fields = ["name", "email"]


class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 1


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ["invoice_number", "beneficiary", "household_count", "cost_per_unit", "total_amount", "status"]
    list_filter = ["status", "beneficiary"]
    search_fields = ["invoice_number", "beneficiary__name"]
    readonly_fields = ["tax_amount", "total_amount"]
    date_hierarchy = "issue_date"
    inlines = [InvoiceItemInline]


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ["beneficiary", "amount", "payment_date", "payment_method", "invoice"]
    list_filter = ["payment_method", "payment_date"]
    search_fields = ["invoice__invoice_number", "beneficiary__name"]


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ["expense_number", "vendor", "amount", "expense_date", "is_paid"]
    list_filter = ["is_paid", "expense_date"]
    search_fields = ["expense_number", "vendor__name"]
    date_hierarchy = "expense_date"


@admin.register(ExpenseItem)
class ExpenseItemAdmin(admin.ModelAdmin):
    list_display = ["description", "expense", "quantity", "unit_price", "category"]
    list_filter = ["category"]
    search_fields = ["description"]


class JournalEntryLineInline(admin.TabularInline):
    model = JournalEntryLine
    extra = 1


@admin.register(JournalEntry)
class JournalEntryAdmin(admin.ModelAdmin):
    list_display = ["entry_number", "date", "description", "is_posted"]
    list_filter = ["is_posted", "date"]
    search_fields = ["entry_number", "description"]
    inlines = [JournalEntryLineInline]


@admin.register(TaxRate)
class TaxRateAdmin(admin.ModelAdmin):
    list_display = ["name", "rate", "is_active"]
    list_filter = ["is_active"]


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ["start_date", "end_date", "total_amount", "line_count"]
    list_filter = ["start_date"]
    search_fields = ["start_date", "end_date", "notes"]


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ["user", "action", "model_name", "timestamp"]
    list_filter = ["action", "model_name"]
    search_fields = ["user__username"]
    date_hierarchy = "timestamp"
    readonly_fields = ["user", "action", "model_name", "object_id", "description", "ip_address", "timestamp"]


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ["name", "report_type", "from_date", "to_date", "created_by"]
    list_filter = ["report_type", "is_saved"]
    search_fields = ["name"]
    date_hierarchy = "created_at"
    readonly_fields = ["total_invoiced", "total_payments", "total_expenses", "balance_to_collect", "net_income", "created_by", "created_at", "updated_at"]


@admin.register(OpeningBalance)
class OpeningBalanceAdmin(admin.ModelAdmin):
    list_display = ["beneficiary", "fiscal_year", "amount"]
    list_filter = ["fiscal_year"]
    search_fields = ["beneficiary__name"]


@admin.register(YearEndRollover)
class YearEndRolloverAdmin(admin.ModelAdmin):
    list_display = ["fiscal_year", "rollover_date", "total_clients", "total_opening_balance"]
    list_filter = ["fiscal_year"]
    readonly_fields = ["created_at"]


@admin.register(Scheme)
class SchemeAdmin(admin.ModelAdmin):
    list_display = ["code", "name", "is_active"]
    list_filter = ["is_active"]
    search_fields = ["name", "code"]


@admin.register(Village)
class VillageAdmin(admin.ModelAdmin):
    list_display = ["name", "scheme", "household_count", "is_active"]
    list_filter = ["scheme", "is_active"]
    search_fields = ["name"]


@admin.register(VillagePopulation)
class VillagePopulationAdmin(admin.ModelAdmin):
    list_display = ["village", "population", "recorded_date"]
    list_filter = ["village"]
    search_fields = ["village__name"]


@admin.register(BoardOfTrustees)
class BoardOfTrusteesAdmin(admin.ModelAdmin):
    list_display = ["name", "title", "contact", "village", "scheme_present"]
    list_filter = ["scheme_present"]
    search_fields = ["name", "village__name"]


@admin.register(GeneralAssemblyMember)
class GeneralAssemblyMemberAdmin(admin.ModelAdmin):
    list_display = ["name", "contact", "village", "scheme_present"]
    list_filter = ["scheme_present"]
    search_fields = ["name", "village__name"]


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ["name", "position", "contact", "employee_type", "is_active"]
    list_filter = ["employee_type", "is_active"]
    search_fields = ["name", "position"]


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ["title", "is_active", "uploaded_at"]
    list_filter = ["is_active"]
    search_fields = ["title"]
    date_hierarchy = "uploaded_at"


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ["title", "is_active", "order"]
    list_filter = ["is_active"]
    search_fields = ["title"]
    list_editable = ["order"]


@admin.register(LandingPageSettings)
class LandingPageSettingsAdmin(admin.ModelAdmin):
    list_display = ["primary_color", "is_active", "updated_at"]
    list_filter = ["is_active"]