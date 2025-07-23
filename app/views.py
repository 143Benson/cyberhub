from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Service, ServiceRequest
from django.views.decorators.http import require_GET, require_POST
from django.db.models import Q, Count, Sum
from datetime import date




@login_required
def dashboard(request):
    categories = Service.CATEGORY_CHOICES
    return render(request, 'dashboard.html', {'categories': categories})

@login_required
@require_GET
def dashboard_stats(request):
    if not request.user.is_superuser:
        return JsonResponse({'error': 'Forbidden'}, status=403)
    stats = {
        'active_services': Service.objects.filter(is_active=True).count(),
        'completed_requests': ServiceRequest.objects.filter(
            status='completed',
            requested_date__date=date.today()
        ).count(),
        'pending_requests': ServiceRequest.objects.filter(
            status='pending',
            user=request.user
        ).count(),
        'daily_revenue': ServiceRequest.objects.filter(
            status='completed',
            requested_date__date=date.today()
        ).aggregate(total=Sum('service__price'))['total'] or 0,
        'notifications': request.user.notifications.unread().count() if hasattr(request.user, 'notifications') else 0
    }
    return JsonResponse(stats)

@login_required
@require_GET
def service_list(request):
    search_query = request.GET.get('search', '')
    category = request.GET.get('category', '')
    
    services = Service.objects.filter(is_active=True)
    
    if search_query:
        services = services.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    if category:
        services = services.filter(category=category)
    
    service_data = []
    for service in services:
        service_data.append({
            'id': service.id,
            'name': service.name,
            'category': service.get_category_display(),
            'description': service.description,
            'icon': service.icon,
            'price_display': f"KSh {service.price:.0f}",
            'price': float(service.price)
        })
    
    return JsonResponse({'services': service_data})

@csrf_exempt
@login_required
@require_POST
def request_service(request):
    service_id = request.POST.get('service_id')
    try:
        service = Service.objects.get(id=service_id, is_active=True)
        ServiceRequest.objects.create(
            user=request.user,
            service=service,
            status='pending'
        )
        return JsonResponse({'success': True})
    except Service.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Service not found'}, status=404)
def login_view(request):
    username_or_email = ''
    error = None
    
    if request.method == 'POST':
        username_or_email = request.POST.get('username')
        password = request.POST.get('password')
        is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
        
        # Try to authenticate with username first
        user = authenticate(request, username=username_or_email, password=password)
        # If authentication with username fails, try with email
        if user is None:
            try:
                user_with_email = User.objects.get(email=username_or_email)
                user = authenticate(request, username=user_with_email.username, password=password)
            except User.DoesNotExist:
                pass
        if user is not None:
            auth_login(request, user)
            if is_ajax:
                return JsonResponse({'success': True, 'redirect_url': '/dashboard/'})
            messages.success(request, 'Login successful!')
            return redirect('dashboard')
        else:
            error = 'Invalid username,email or password.'
            if is_ajax:
                return JsonResponse({'success': False, 'error': error}, status=400)
    return render(request, 'app/index.html', {
        'username': username_or_email,
        'error': error
    })
def register_view(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Validate passwords match
        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')

        # Check if username exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('register')

        # Check if email exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return redirect('register')

        try:
            # Create user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1,
                first_name=full_name.split()[0] if full_name else '',
                last_name=' '.join(full_name.split()[1:]) if full_name and len(full_name.split()) > 1 else ''
            )
            user.save()
            auth_login(request, user)            
            messages.success(request, 'Registration successful! Welcome to CyberHub Kenya')
            return redirect('dashboard')
            
        except Exception as e:
            messages.error(request, f'Error during registration: {str(e)}')
            return redirect('register')

    return render(request, 'app/register.html')
@login_required(login_url='login')
def dashboard(request):
    services = Service.objects.filter(is_active=True)
    categories = Service.CATEGORY_CHOICES
    return render(request, 'app/dashboard.html', {'services': services, 'categories': categories})

def logout_view(request):
    auth_logout(request)
    messages.info(request, 'Logged out successfully.')
    return redirect('login')

def check_username(request):
    username = request.GET.get('username', '').strip()
    exists = False
    if username:
        exists = User.objects.filter(username=username).exists()
    return JsonResponse({'exists': exists})

@csrf_exempt
def check_email(request):
    email = request.GET.get('email', '').strip()
    exists = False
    if email:
        exists = User.objects.filter(email=email).exists()
    return JsonResponse({'exists': exists})

@csrf_exempt
def check_phone(request):
    phone = request.GET.get('phone', '').strip()
    exists = False
    # If phone is stored in User or UserProfile, check here. For now, always return False.
    return JsonResponse({'exists': exists})

def index(request):
    return render(request, 'app/index.html')
