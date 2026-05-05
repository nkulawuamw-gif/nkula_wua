from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not hasattr(request.user, 'userprofile'):
            return redirect('login')
        if not request.user.userprofile.can_access_settings():
            messages.error(request, "You don't have permission to access this page.")
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper


def manager_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not hasattr(request.user, 'userprofile'):
            return redirect('login')
        if not request.user.userprofile.is_manager():
            messages.error(request, "You don't have permission to perform this action.")
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper


def accountant_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not hasattr(request.user, 'userprofile'):
            return redirect('login')
        if not request.user.userprofile.is_accountant():
            messages.error(request, "You don't have permission to perform this action.")
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper


def can_edit_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not hasattr(request.user, 'userprofile'):
            return redirect('login')
        if not request.user.userprofile.can_edit():
            messages.error(request, "You don't have permission to edit.")
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper


def can_delete_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not hasattr(request.user, 'userprofile'):
            return redirect('login')
        if not request.user.userprofile.can_delete():
            messages.error(request, "You don't have permission to delete.")
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper


def user_management_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not hasattr(request.user, 'userprofile'):
            return redirect('login')
        if not request.user.userprofile.can_manage_users():
            messages.error(request, "You don't have permission to manage users.")
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper
