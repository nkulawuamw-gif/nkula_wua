import json
import re
import logging
from decimal import Decimal
from datetime import date, datetime
from django.conf import settings
from django.utils import timezone

logger = logging.getLogger(__name__)


def _parse_date(value):
    if not value:
        return None
    if isinstance(value, date):
        return value
    value = str(value).strip()
    for fmt in ("%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y"):
        try:
            return datetime.strptime(value, fmt).date()
        except ValueError:
            continue
    raise ValueError(f"Cannot parse date: {value}")


def _fmt_date(d):
    if isinstance(d, date):
        return d.strftime("%d/%m/%Y")
    return str(d)


class GroqAIService:
    BASE_URL = "https://api.groq.com/openai/v1"

    def __init__(self, user=None):
        self.api_key = settings.GROQ_API_KEY
        self.model_name = settings.GROQ_MODEL
        self.user = user
        self.client = None
        self._init_client()

    def _init_client(self):
        if not self.api_key or self.api_key == 'your-groq-api-key-here':
            self.client = None
            return
        try:
            from openai import OpenAI
            self.client = OpenAI(
                api_key=self.api_key,
                base_url=self.BASE_URL
            )
        except Exception as e:
            logger.error(f"Failed to initialize Groq client: {e}")
            self.client = None

    def is_available(self):
        return self.client is not None and self.api_key and self.api_key != 'your-groq-api-key-here'

    def _get_system_prompt(self):
        return """You are an AI assistant for the Nkula Water Users Association (WUA) management system.
You help staff with three main tasks:

1. **Generating Reports** - Query financial data and present summaries
2. **Creating Invoices** - Create invoices for beneficiaries
3. **Creating Payments** - Record payments from beneficiaries

## Database Schema

### Beneficiary
- Fields: id, name, beneficiary_type (private/communal/town), phone, village, scheme (Mangale/Nkala/Dodza/Milala), household_count, total_bill, total_paid, total_outstanding, is_active

### Invoice
- Fields: id, invoice_number, beneficiary_id, issue_date, due_date, household_count, cost_per_unit, tax_rate, tax_amount, discount, total_amount, status (draft/sent/paid/partial/overdue/cancelled), notes, created_by_id

### Payment
- Fields: id, beneficiary_id, invoice_id (nullable), amount, payment_date, payment_method (cash/bank_transfer/mobile_money/credit_card/check/other), reference, notes, account_id, created_by_id

### Account (Chart of Accounts)
- Fields: id, name, account_type (asset/liability/equity/revenue/expense), code, description

### Scheme
- Fields: id, name, description, is_active

## How to respond

When a user asks to CREATE or RECORD something:
1. First ask for any missing required information
2. Only include the JSON action block when ALL required fields are provided by the user. If you need to ask a follow-up question, just respond with text — do NOT include any JSON block.
   For invoice creation (required: beneficiary_name, household_count, cost_per_unit):
    ```json
    {"action": "create_invoice", "data": {"beneficiary_name": "...", "household_count": X, "cost_per_unit": X, "due_date": "DD/MM/YYYY", ...}}
    ```
    For payment creation (required: beneficiary_name, amount):
    ```json
    {"action": "create_payment", "data": {"beneficiary_name": "...", "amount": X, "payment_method": "...", "payment_date": "DD/MM/YYYY", ...}}
    ```

When a user asks to GENERATE or VIEW a report:
- Only include a JSON action block when the user has specified what report they want. If you need to ask which report type, don't include a JSON block.
- Use ONE of these exact report_type values:
  - `"financial"` for financial summary (income, expenses, payments)
  - `"beneficiary_balances"` for beneficiaries with outstanding balances (alias: "outstanding_balances")
  - `"overdue"` for overdue invoices report
  Example:
  ```json
  {"action": "generate_report", "data": {"report_type": "financial", "from_date": "DD/MM/YYYY", "to_date": "DD/MM/YYYY"}}
  ```
  For beneficiary balances, no dates needed:
  ```json
  {"action": "generate_report", "data": {"report_type": "beneficiary_balances"}}
  ```

When a user asks a general question (help, capabilities, etc.):
- Respond conversationally without any JSON action block

Always be helpful, concise, and professional. Default currency is MWK (Malawi Kwacha).
Current date is: """ + _fmt_date(timezone.now().date()) + """

CRITICAL: Use DD/MM/YYYY format for all dates. Never include a JSON action block in a response that is asking a follow-up question — the system will attempt to execute it immediately and fail if data is missing."""

    def chat(self, message, conversation_history=None):
        if not self.is_available():
            return {
                "type": "error",
                "message": "Groq AI is not configured. Ask the administrator to set the GROQ_API_KEY in the .env file. Get a free key at https://console.groq.com/keys"
            }

        try:
            messages = []
            messages.append({"role": "system", "content": self._get_system_prompt()})

            if conversation_history:
                for msg in conversation_history[-20:]:
                    role = "user" if msg.get("role") == "user" else "assistant"
                    messages.append({"role": role, "content": msg.get("text", "")})

            messages.append({"role": "user", "content": message})

            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=0.2,
                max_tokens=2048,
            )

            reply = response.choices[0].message.content.strip()

            action = self._extract_action(reply)
            clean_reply = self._remove_action_block(reply)

            return {
                "type": "response",
                "message": clean_reply,
                "action": action
            }

        except Exception as e:
            logger.error(f"Groq API error: {e}", exc_info=True)
            return {
                "type": "error",
                "message": f"AI service error: {str(e)}. Please check your API key and try again."
            }

    def _extract_action(self, text):
        pattern = r'```json\s*(\{.*\})\s*```'
        match = re.search(pattern, text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1))
            except json.JSONDecodeError:
                return None
        return None

    def _remove_action_block(self, text):
        return re.sub(r'```json\s*\{.*\}\s*```', '', text, flags=re.DOTALL).strip()

    def execute_action(self, action):
        if not action or "action" not in action:
            return {"success": False, "message": "No action to execute"}

        action_type = action.get("action")
        data = action.get("data", {})

        try:
            if action_type == "create_invoice":
                return self._execute_create_invoice(data)
            elif action_type == "create_payment":
                return self._execute_create_payment(data)
            elif action_type == "generate_report":
                return self._execute_generate_report(data)
            else:
                return {"success": False, "message": f"Unknown action: {action_type}"}
        except Exception as e:
            logger.error(f"Action execution error: {e}", exc_info=True)
            return {"success": False, "message": f"Error executing action: {str(e)}"}

    def _execute_create_invoice(self, data):
        from .models import Beneficiary, Invoice

        beneficiary_name = data.get("beneficiary_name", "")
        if not beneficiary_name:
            return {"success": False, "message": "Beneficiary name is required"}

        beneficiaries = Beneficiary.objects.filter(
            name__icontains=beneficiary_name, is_active=True
        )
        if not beneficiaries.exists():
            return {"success": False, "message": f"No active beneficiary found matching '{beneficiary_name}'"}
        if beneficiaries.count() > 1:
            names = [b.name for b in beneficiaries[:5]]
            return {"success": False, "message": f"Multiple beneficiaries found: {', '.join(names)}. Please be more specific."}

        beneficiary = beneficiaries.first()
        household_count = int(data.get("household_count") or beneficiary.household_count or 1)
        cost_per_unit = float(data.get("cost_per_unit") or 0)
        tax_rate = float(data.get("tax_rate") or 0)
        discount = float(data.get("discount") or 0)
        notes = data.get("notes", "")

        if not cost_per_unit:
            return {"success": False, "message": "Cost per unit is required"}

        today = timezone.now().date()
        issue_date = _parse_date(data.get("issue_date")) or today
        due_date = _parse_date(data.get("due_date")) or issue_date

        prefix = f"INV-{today.strftime('%Y%m%d')}"
        last_invoice = Invoice.objects.filter(invoice_number__startswith=prefix).order_by('-invoice_number').first()
        if last_invoice:
            last_num = int(last_invoice.invoice_number.split('-')[-1])
            new_num = last_num + 1
        else:
            new_num = 1
        invoice_number = f"{prefix}-{new_num:04d}"

        subtotal = household_count * cost_per_unit
        tax_amount = subtotal * (tax_rate / 100)
        total_amount = subtotal + tax_amount - discount

        invoice = Invoice.objects.create(
            invoice_number=invoice_number,
            beneficiary=beneficiary,
            issue_date=issue_date,
            due_date=due_date,
            household_count=household_count,
            cost_per_unit=cost_per_unit,
            tax_rate=tax_rate,
            tax_amount=tax_amount,
            discount=discount,
            total_amount=total_amount,
            notes=notes,
            created_by=self.user
        )


        beneficiary.recalculate_totals()

        return {
            "success": True,
            "message": f"Invoice {invoice_number} created successfully for {beneficiary.name} - Total: {total_amount}",
            "invoice_id": invoice.pk,
            "invoice_number": invoice_number,
            "beneficiary": beneficiary.name,
            "total_amount": float(total_amount)
        }

    def _execute_create_payment(self, data):
        from .models import Beneficiary, Payment, Account

        beneficiary_name = data.get("beneficiary_name", "")
        if not beneficiary_name:
            return {"success": False, "message": "Beneficiary name is required"}

        beneficiaries = Beneficiary.objects.filter(
            name__icontains=beneficiary_name, is_active=True
        )
        if not beneficiaries.exists():
            return {"success": False, "message": f"No active beneficiary found matching '{beneficiary_name}'"}
        if beneficiaries.count() > 1:
            names = [b.name for b in beneficiaries[:5]]
            return {"success": False, "message": f"Multiple beneficiaries found: {', '.join(names)}. Please be more specific."}

        beneficiary = beneficiaries.first()
        amount = float(data.get("amount") or 0)
        if amount <= 0:
            return {"success": False, "message": "Payment amount must be greater than zero"}

        payment_method = data.get("payment_method", "cash")
        payment_date = _parse_date(data.get("payment_date")) or timezone.now().date()
        reference = data.get("reference", "")
        notes = data.get("notes", "")

        account_name = data.get("account_name", "")
        account = None
        if account_name:
            accounts = Account.objects.filter(name__icontains=account_name, is_active=True)
            if accounts.exists():
                account = accounts.first()
        if not account:
            account = Account.objects.filter(account_type='revenue', is_active=True).first()

        payment = Payment.objects.create(
            beneficiary=beneficiary,
            amount=amount,
            payment_date=payment_date,
            payment_method=payment_method,
            reference=reference,
            notes=notes,
            account=account,
            created_by=self.user
        )

        if account:
            account.balance = (account.balance or 0) + amount
            account.save()

        beneficiary.recalculate_totals()


        return {
            "success": True,
            "message": f"Payment of {amount} recorded successfully for {beneficiary.name}",
            "payment_id": payment.pk,
            "beneficiary": beneficiary.name,
            "amount": float(amount)
        }

    def _execute_generate_report(self, data):
        from .models import Invoice, Payment, Expense, Beneficiary
        from django.db.models import Sum

        today = timezone.now().date()
        report_type = data.get("report_type", "financial")
        try:
            from_date = _parse_date(data.get("from_date")) or today.replace(month=1, day=1)
            to_date = _parse_date(data.get("to_date")) or today
        except (ValueError, TypeError):
            from_date = today.replace(month=1, day=1)
            to_date = today

        normalized_type = report_type.replace(" ", "_").lower()
        if normalized_type in ("financial", "income_statement", "profit_loss"):
            invoices = Invoice.objects.filter(issue_date__gte=from_date, issue_date__lte=to_date)
            payments = Payment.objects.filter(payment_date__gte=from_date, payment_date__lte=to_date)
            expenses = Expense.objects.filter(expense_date__gte=from_date, expense_date__lte=to_date)

            total_invoiced = invoices.aggregate(total=Sum('total_amount'))['total'] or 0
            total_payments = payments.aggregate(total=Sum('amount'))['total'] or 0
            total_expenses = expenses.aggregate(total=Sum('amount'))['total'] or 0
            balance_to_collect = float(total_invoiced) - float(total_payments)
            net_income = float(total_payments) - float(total_expenses)

            return {
                "success": True,
                "message": f"Financial Report ({_fmt_date(from_date)} to {_fmt_date(to_date)})",
                "report": {
                    "from_date": _fmt_date(from_date),
                    "to_date": _fmt_date(to_date),
                    "total_invoiced": float(total_invoiced),
                    "total_payments": float(total_payments),
                    "total_expenses": float(total_expenses),
                    "balance_to_collect": balance_to_collect,
                    "net_income": net_income,
                    "invoice_count": invoices.count(),
                    "payment_count": payments.count(),
                    "expense_count": expenses.count(),
                }
            }

        elif normalized_type in ("beneficiary_balances", "outstanding_balances", "balances"):
            beneficiaries = Beneficiary.objects.filter(is_active=True, total_outstanding__gt=0)
            data_list = []
            for b in beneficiaries:
                data_list.append({
                    "name": b.name,
                    "scheme": b.scheme,
                    "village": b.village,
                    "total_bill": float(b.total_bill),
                    "total_paid": float(b.total_paid),
                    "balance": float(b.total_outstanding),
                })
            data_list.sort(key=lambda x: x['balance'], reverse=True)

            return {
                "success": True,
                "message": f"Beneficiary Balances Report - {len(data_list)} beneficiaries with outstanding balances",
                "report": {
                    "type": "beneficiary_balances",
                    "count": len(data_list),
                    "beneficiaries": data_list[:50],
                }
            }

        elif normalized_type in ("overdue", "overdue_invoices"):
            overdue_invoices = Invoice.objects.filter(status="overdue")
            inv_data = []
            for inv in overdue_invoices:
                inv_data.append({
                    "number": inv.invoice_number,
                    "beneficiary": inv.beneficiary.name,
                    "total": float(inv.total_amount),
                    "due_date": _fmt_date(inv.due_date),
                })

            return {
                "success": True,
                "message": f"Overdue Invoices Report - {overdue_invoices.count()} overdue invoices",
                "report": {
                    "type": "overdue",
                    "count": overdue_invoices.count(),
                    "invoices": inv_data[:50],
                }
            }

        else:
            return {"success": False, "message": f"Unknown report type: {report_type}. Supported types: financial, beneficiary_balances, overdue"}
