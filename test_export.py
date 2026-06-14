import django, os, sys, json
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'accounting_project.settings')
django.setup()

from django.test import RequestFactory
from django.contrib.auth.models import User
from accounting_app.views import export_beneficiaries_full

factory = RequestFactory()
user = User.objects.first()
request = factory.get('/beneficiaries/export/full/')
request.user = user

response = export_beneficiaries_full(request)
data = json.loads(response.content)

print(f'Version: {data["version"]}')
print(f'Exported by: {data["exported_by"]}')
print(f'Beneficiaries count: {len(data["beneficiaries"])}')

b0 = data['beneficiaries'][0]
print(f'First beneficiary: {b0["fields"]["name"]} (PK: {b0["pk"]})')
print(f'  Invoices: {len(b0["invoices"])}')
print(f'  Payments: {len(b0["payments"])}')
print(f'  Opening balances: {len(b0["opening_balances"])}')
print(f'  Balance history: {len(b0["balance_history"])}')
print(f'  History entries: {len(b0["history"])}')
print(f'  Status logs: {len(b0["status_logs"])}')

for b in data['beneficiaries']:
    for inv in b['invoices']:
        if inv['items']:
            print(f'Beneficiary "{b["fields"]["name"]}": Invoice {inv["fields"]["invoice_number"]} has {len(inv["items"])} items')
            print(f'  Item fields: {json.dumps(inv["items"][0]["fields"], default=str)[:200]}')
            break
    else:
        continue
    break

for b in data['beneficiaries']:
    for pay in b['payments']:
        pay_fields = {k: v for k, v in pay['fields'].items() if not k.endswith('_id') or v}
        print(f'Beneficiary "{b["fields"]["name"]}": Payment fields: {json.dumps(pay_fields, default=str)[:300]}')
        break
    else:
        continue
    break

print('Export test PASSED')
