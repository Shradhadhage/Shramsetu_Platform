from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile, Job
from django.contrib.auth.models import User
from .forms import ProfileUpdateForm
# services/views.py
from django.db.models import Q  # <--- Add this line!

# --- BASIC PAGES ---
def home_view(request):
    return render(request, 'index.html')

def about_view(request):
    return render(request, 'about.html')

def services_view(request):
    return render(request, 'services.html')

def projects_view(request):
    return render(request, 'projects.html')

# --- AUTHENTICATION ---
def auth_view(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        email = request.POST.get('email')
        password = request.POST.get('password')
        selected_role = request.POST.get('role')

        if action == 'register':
            full_name = request.POST.get('full_name')
            # Check if user already exists
            if User.objects.filter(username=email).exists():
                return render(request, 'index.html', {'error': 'User already exists.'})
            
            user = User.objects.create_user(username=email, email=email, password=password)
            user.first_name = full_name
            user.save()
            Profile.objects.create(user=user, role=selected_role)
            login(request, user)
            return redirect('dashboard')

        elif action == 'login':
            user = authenticate(request, username=email, password=password)
            if user is not None:
                user_profile = get_object_or_404(Profile, user=user)
                if user_profile.role == selected_role:
                    login(request, user)
                    return redirect('dashboard')
                else:
                    return render(request, 'index.html', {'error': 'Invalid role for this account.'})
            else:
                return render(request, 'index.html', {'error': 'Invalid email or password.'})
                
    return redirect('home')

def logout_view(request):
    logout(request)
    return redirect('home')

# --- MAIN DASHBOARD (Unified) ---
@login_required
def dashboard_view(request):
    user_profile = get_object_or_404(Profile, user=request.user)
    
    # --- CUSTOMER VIEW ---
    if user_profile.role == 'customer':
        search_query = request.GET.get('search', '')
        available_workers = Profile.objects.filter(role='worker')
        
        if search_query:
            available_workers = available_workers.filter(
                Q(skill__icontains=search_query) | Q(location__icontains=search_query)
            )

        # Get requests sent BY this customer
        my_requests = Job.objects.filter(customer=request.user).order_by('-created_at')

        return render(request, 'services/customer_dashboard.html', {
            'profile': user_profile,
            'workers': available_workers,
            'my_requests': my_requests,
            'search_query': search_query,
        })
    
    # --- WORKER VIEW ---
    else:
        # Get requests sent TO this worker
        incoming_jobs = Job.objects.filter(worker=request.user, status='pending').order_by('-created_at')
        # Get jobs this worker has already accepted
        accepted_jobs = Job.objects.filter(worker=request.user, status='accepted')

        return render(request, 'services/worker_dashboard.html', {
            'profile': user_profile,
            'incoming_jobs': incoming_jobs,
            'accepted_jobs': accepted_jobs,
        })

# ADD THIS TO HANDLE THE BUTTONS
def update_job_status(request, job_id, action):
    job = get_object_or_404(Job, id=job_id, worker=request.user)
    if action == 'accept':
        job.status = 'accepted'
    elif action == 'decline':
        job.status = 'declined'
    job.save()
    return redirect('dashboard')
# services/views.py
@login_required
def messages_view(request):
    user_profile = get_object_or_404(Profile, user=request.user)
    
    # 1. Start with the relevant jobs based on role
    if user_profile.role == 'worker':
        notifications = Job.objects.filter(worker=request.user)
    else:
        notifications = Job.objects.filter(customer=request.user)

    # 2. Filter for all active statuses and use select_related to speed up page loading
    # We include 'declined' and 'rejected' to be safe
    notifications = notifications.filter(
        Q(status='pending') | 
        Q(status='accepted') | 
        Q(status='declined') | 
        Q(status='rejected')
    ).select_related('worker__profile', 'customer__profile').order_by('-id')

    return render(request, 'services/dashboard_messages.html', {
        'notifications': notifications,
        'profile': user_profile,
    })
# --- JOB ACTIONS ---

@login_required
def hire_worker(request, worker_id):
    if request.method == 'POST':
        # worker_id is the ID of the Profile model
        worker_profile = get_object_or_404(Profile, id=worker_id)
        
        Job.objects.create(
            customer=request.user,
            worker=worker_profile.user,
            title=f"Request from {request.user.first_name}",
            description="General labor request",
            budget=0,
            status='pending'
        )
        messages.success(request, "Hire request sent successfully!")
        return redirect('dashboard')

@login_required
def accept_job(request, job_id):
    if request.method == 'POST':
        job = get_object_or_404(Job, id=job_id, worker=request.user)
        job.status = 'accepted'
        job.save()
        messages.success(request, "Job accepted!")
    return redirect('dashboard')

@login_required
def reject_job(request, job_id):
    if request.method == 'POST':
        job = get_object_or_404(Job, id=job_id, worker=request.user)
        job.status = 'rejected'
        job.save()
        messages.info(request, "Job declined.")
    return redirect('dashboard')


@login_required
def settings_view(request):
    user_profile = get_object_or_404(Profile, user=request.user)

    if request.method == 'POST':
        # 1. Capture the data
        new_name = request.POST.get('full_name')
        new_phone = request.POST.get('phone')
        new_location = request.POST.get('location')
        new_skill = request.POST.get('skill')

        # 2. Update the User Model (Name)
        if new_name:
            request.user.first_name = new_name
            request.user.save()

        # 3. Update the Profile Model
        user_profile.phone = new_phone
        user_profile.location = new_location
        
        if user_profile.role == 'worker':
            user_profile.skill = new_skill
        
        user_profile.save()
        
        # 4. Add a success message and redirect
        messages.success(request, "Your changes have been saved!")
        return redirect('settings') 

    return render(request, 'services/dashboard_settings.html', {'profile': user_profile})

@login_required
def job_detail(request, job_id):
    """Detailed view for a specific job."""
    job = get_object_or_404(Job, id=job_id)
    return render(request, 'services/job_detail.html', {'job': job})

import openai # You'll need to pip install openai
from django.http import JsonResponse

def chatbot_api(request):
    user_message = request.GET.get('message')
    # Call OpenAI API here using your API Key
    # response = openai.ChatCompletion.create(...)
    return JsonResponse({'reply': "This is where the AI response would go"})

