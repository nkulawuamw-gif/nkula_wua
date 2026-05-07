from django.contrib import admin
from .models import (
    UserProfile, Account, Beneficiary, Vendor, Invoice, InvoiceItem,
    Expense, ExpenseItem, JournalEntry, JournalEntryLine, Payment, TaxRate, 
    Budget, ActivityLog, Report, OpeningBalance, YearEndRollover, Scheme, 
    Village, VillagePopulation, BoardOfTrustees, GeneralAssemblyMember, Employee, GalleryImage, Service, LoginSession, DeletedRecord
)


class RestrictedModelAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        if request.user.is_superuser:
            return True
        if hasattr(request.user, 'userprofile'):
            return request.user.userprofile.role in ('admin', 'manager')
        return False

    def has_view_permission(self, request, obj=None):
        return self.has_module_permission(request)

    def has_add_permission(self, request):
        return self.has_module_permission(request)

    def has_change_permission(self, request, obj=None):
        return self.has_module_permission(request)

    def has_delete_permission(self, request, obj=None):
        return self.has_module_permission(request)


@admin.register(UserProfile)
class UserProfileAdmin(RestrictedModelAdmin):
    list_display = ["user", "company_name", "phone"]
    search_fields = ["user__username", "company_name"]


@admin.register(Account)
class AccountAdmin(RestrictedModelAdmin):
    list_display = ["code", "name", "account_type", "balance", "is_active"]
    list_filter = ["account_type", "is_active"]
    search_fields = ["code", "name"]
    ordering = ["code"]


@admin.register(Beneficiary)
class BeneficiaryAdmin(RestrictedModelAdmin):
    list_display = ["name", "email", "phone", "village", "scheme", "household_count", "total_bill", "total_paid", "is_active"]
    list_filter = ["is_active", "scheme"]
    search_fields = ["name", "email"]
    readonly_fields = ["total_bill", "total_paid", "total_outstanding"]


@admin.register(Vendor)
class VendorAdmin(RestrictedModelAdmin):
    list_display = ["name", "email", "phone", "city", "is_active"]
    list_filter = ["is_active", "country"]
    search_fields = ["name", "email"]


class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 1


@admin.register(Invoice)
class InvoiceAdmin(RestrictedModelAdmin):
    list_display = ["invoice_number", "beneficiary", "household_count", "cost_per_unit", "total_amount", "status"]
    list_filter = ["status", "beneficiary"]
    search_fields = ["invoice_number", "beneficiary__name"]
    readonly_fields = ["tax_amount", "total_amount"]
    date_hierarchy = "issue_date"
    inlines = [InvoiceItemInline]


@admin.register(Payment)
class PaymentAdmin(RestrictedModelAdmin):
    list_display = ["beneficiary", "amount", "payment_date", "payment_method", "invoice"]
    list_filter = ["payment_method", "payment_date"]
    search_fields = ["invoice__invoice_number", "beneficiary__name"]


@admin.register(Expense)
class ExpenseAdmin(RestrictedModelAdmin):
    list_display = ["expense_number", "vendor", "amount", "expense_date", "is_paid"]
    list_filter = ["is_paid", "expense_date"]
    search_fields = ["expense_number", "vendor__name"]
    date_hierarchy = "expense_date"


@admin.register(ExpenseItem)
class ExpenseItemAdmin(RestrictedModelAdmin):
    list_display = ["description", "expense", "quantity", "unit_price", "category"]
    list_filter = ["category"]
    search_fields = ["description"]


class JournalEntryLineInline(admin.TabularInline):
    model = JournalEntryLine
    extra = 1


@admin.register(JournalEntry)
class JournalEntryAdmin(RestrictedModelAdmin):
    list_display = ["entry_number", "date", "description", "is_posted"]
    list_filter = ["is_posted", "date"]
    search_fields = ["entry_number", "description"]
    inlines = [JournalEntryLineInline]


@admin.register(TaxRate)
class TaxRateAdmin(RestrictedModelAdmin):
    list_display = ["name", "rate", "is_active"]
    list_filter = ["is_active"]


@admin.register(Budget)
class BudgetAdmin(RestrictedModelAdmin):
    list_display = ["start_date", "end_date", "total_amount", "line_count"]
    list_filter = ["start_date"]
    search_fields = ["start_date", "end_date", "notes"]


@admin.register(ActivityLog)
class ActivityLogAdmin(RestrictedModelAdmin):
    list_display = ["user", "action", "model_name", "timestamp"]
    list_filter = ["action", "model_name"]
    search_fields = ["user__username"]
    date_hierarchy = "timestamp"
    readonly_fields = ["user", "action", "model_name", "object_id", "description", "ip_address", "timestamp"]


@admin.register(Report)
class ReportAdmin(RestrictedModelAdmin):
    list_display = ["name", "report_type", "from_date", "to_date", "created_by"]
    list_filter = ["report_type", "is_saved"]
    search_fields = ["name"]
    date_hierarchy = "created_at"
    readonly_fields = ["total_invoiced", "total_payments", "total_expenses", "balance_to_collect", "net_income", "created_by", "created_at", "updated_at"]


@admin.register(OpeningBalance)
class OpeningBalanceAdmin(RestrictedModelAdmin):
    list_display = ["beneficiary", "fiscal_year", "amount"]
    list_filter = ["fiscal_year"]
    search_fields = ["beneficiary__name"]


@admin.register(YearEndRollover)
class YearEndRolloverAdmin(RestrictedModelAdmin):
    list_display = ["fiscal_year", "rollover_date", "total_clients", "total_opening_balance"]
    list_filter = ["fiscal_year"]
    readonly_fields = ["created_at"]


@admin.register(Scheme)
class SchemeAdmin(RestrictedModelAdmin):
    list_display = ["code", "name", "is_active"]
    list_filter = ["is_active"]
    search_fields = ["name", "code"]


@admin.register(Village)
class VillageAdmin(RestrictedModelAdmin):
    list_display = ["name", "scheme", "household_count", "is_active"]
    list_filter = ["scheme", "is_active"]
    search_fields = ["name"]


@admin.register(VillagePopulation)
class VillagePopulationAdmin(RestrictedModelAdmin):
    list_display = ["village", "population", "recorded_date"]
    list_filter = ["village"]
    search_fields = ["village__name"]


@admin.register(BoardOfTrustees)
class BoardOfTrusteesAdmin(RestrictedModelAdmin):
    list_display = ["name", "title", "contact", "village", "scheme_present"]
    list_filter = ["scheme_present"]
    search_fields = ["name", "village__name"]


@admin.register(GeneralAssemblyMember)
class GeneralAssemblyMemberAdmin(RestrictedModelAdmin):
    list_display = ["name", "contact", "village", "scheme_present"]
    list_filter = ["scheme_present"]
    search_fields = ["name", "village__name"]


@admin.register(Employee)
class EmployeeAdmin(RestrictedModelAdmin):
    list_display = ["name", "position", "contact", "employee_type", "is_active"]
    list_filter = ["employee_type", "is_active"]
    search_fields = ["name", "position"]


@admin.register(GalleryImage)
class GalleryImageAdmin(RestrictedModelAdmin):
    list_display = ["title", "is_active", "uploaded_at"]
    list_filter = ["is_active"]
    search_fields = ["title"]
    date_hierarchy = "uploaded_at"


@admin.register(Service)
class ServiceAdmin(RestrictedModelAdmin):
    list_display = ["title", "is_active", "order"]
    list_filter = ["is_active"]
    search_fields = ["title"]
    list_editable = ["order"]


@admin.register(LoginSession)
class LoginSessionAdmin(RestrictedModelAdmin):
    list_display = ["user", "ip_address", "device_info", "login_time", "logout_time", "is_active"]
    list_filter = ["is_active", "login_time"]
    search_fields = ["user__username", "ip_address"]
    readonly_fields = ["user", "session_key", "ip_address", "user_agent", "device_info", "login_time", "logout_time"]
    date_hierarchy = "login_time"


@admin.register(DeletedRecord)
class DeletedRecordAdmin(RestrictedModelAdmin):
    list_display = ["model_name", "object_id", "deleted_by", "deleted_at", "recovered"]
    list_filter = ["model_name", "recovered", "deleted_at"]
    search_fields = ["model_name", "object_id", "deleted_by__username"]
    readonly_fields = ["model_name", "object_id", "data", "deleted_by", "deleted_at", "recovered", "recovered_at"]
    date_hierarchy = "deleted_at"
