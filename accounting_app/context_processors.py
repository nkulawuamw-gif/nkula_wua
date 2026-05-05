from django.apps import apps
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

def user_currency(request):
    currency = {}
    if request.user.is_authenticated:
        if hasattr(request.user, 'userprofile'):
            currency['user_currency'] = request.user.userprofile.currency
    return currency

def user_theme(request):
    theme = {}
    if request.user.is_authenticated:
        if hasattr(request.user, 'userprofile'):
            theme['user_theme'] = request.user.userprofile.theme
    return theme

def get_latest_populations():
    from accounting_app.models import Village
    from accounting_app.models import VillagePopulation
    
    villages = Village.objects.filter(is_active=True)
    populations = []
    for village in villages:
        latest = village.population_records.order_by('-recorded_date').first()
        if latest:
            populations.append(latest)
    return populations

def online_users(request):
    online = {}
    if request.user.is_authenticated:
        now = timezone.now()
        five_minutes_ago = now - timedelta(minutes=5)
        
        users = User.objects.filter(is_active=True)
        online_users_list = []
        for u in users:
            if hasattr(u, 'userprofile'):
                last_active = u.userprofile.last_activity
                if last_active and last_active >= five_minutes_ago:
                    online_users_list.append({
                        'id': u.id,
                        'username': u.username,
                        'last_activity': last_active
                    })
        
        online['users_online'] = online_users_list
        online['online_count'] = len(online_users_list)
    return online

def menu_counts(request):
    counts = {}
    if request.user.is_authenticated:
        try:
            from accounting_app.models import Beneficiary, Invoice, Payment, Expense, Vendor, Account, Budget
            from accounting_app.models import BoardOfTrustees, GeneralAssemblyMember, Employee
            from accounting_app.models import Scheme, Village
            from accounting_app.models import CommunicationLog
            
            if request.user.userprofile.can_edit:
                counts['beneficiaries'] = Beneficiary.objects.filter(is_active=True).count()
                counts['invoices'] = Invoice.objects.exclude(status='cancelled').count()
                counts['expenses'] = Expense.objects.all().count()
                counts['payments'] = Payment.objects.all().count()
                counts['vendors'] = Vendor.objects.filter(is_active=True).count()
                counts['accounts'] = Account.objects.filter(is_active=True).count()
                counts['budgets'] = Budget.objects.all().count()
            
            # Scheme Overall counts
            counts['total_population'] = sum(vp.population for vp in get_latest_populations())
            counts['trustees'] = BoardOfTrustees.objects.all().count()
            counts['general_assembly'] = GeneralAssemblyMember.objects.all().count()
            counts['employees'] = Employee.objects.filter(is_active=True).count()
            counts['schemes'] = Scheme.objects.filter(is_active=True).count()
            
            # Communication counts
            counts['sms'] = CommunicationLog.objects.filter(communication_type='sms').count()
            counts['voice_call'] = CommunicationLog.objects.filter(communication_type='voice_call').count()
            counts['video_call'] = CommunicationLog.objects.filter(communication_type='video_call').count()
            counts['whatsapp'] = CommunicationLog.objects.filter(communication_type='whatsapp').count()
            
            # User message unread count
            try:
                from accounting_app.models import UserMessage
                counts['total_unread'] = UserMessage.objects.filter(recipient=request.user, is_read=False).count()
            except Exception:
                counts['total_unread'] = 0
            
        except Exception as e:
            pass
    return {'menu_counts': counts}