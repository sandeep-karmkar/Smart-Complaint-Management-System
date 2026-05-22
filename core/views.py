from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Complaint
from .forms import ComplaintForm


# ================= HOME =================

def home(request):

    return render(request, 'home.html')


# ================= DASHBOARD =================

@login_required
def dashboard(request):

    complaints = Complaint.objects.filter(
        user=request.user
    )

    total_complaints = complaints.count()

    pending_complaints = complaints.filter(
        status='Pending'
    ).count()

    inprogress_complaints = complaints.filter(
        status='In Progress'
    ).count()

    resolved_complaints = complaints.filter(
        status='Resolved'
    ).count()

    return render(request, 'dashboard.html', {

        'total_complaints': total_complaints,

        'pending_complaints': pending_complaints,

        'inprogress_complaints': inprogress_complaints,

        'resolved_complaints': resolved_complaints,

    })


# ================= REGISTER =================

def register(request):

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        # Prevent duplicate usernames

        if User.objects.filter(username=username).exists():

            return render(request, 'register.html', {
                'error': 'Username already exists'
            })

        User.objects.create_user(
            username=username,
            password=password
        )

        messages.success(
            request,
            'Account created successfully 🎉'
        )

        return redirect('/login/')

    return render(request, 'register.html')


# ================= LOGIN =================

def user_login(request):

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            messages.success(
                request,
                'Login successful 🚀'
            )

            return redirect('/dashboard/')

        else:

            return render(request, 'login.html', {
                'error': 'Invalid credentials'
            })

    return render(request, 'login.html')


# ================= LOGOUT =================

def user_logout(request):

    logout(request)

    return redirect('/login/')


# ================= ADD COMPLAINT =================

@login_required
def add_complaint(request):

    if request.method == 'POST':

        form = ComplaintForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            complaint = form.save(commit=False)

            complaint.user = request.user

            complaint.save()

            messages.success(
                request,
                'Complaint submitted successfully 🎉'
            )

            return redirect('/dashboard/')

    else:

        form = ComplaintForm()

    return render(request, 'add_complaint.html', {
        'form': form
    })


# ================= VIEW COMPLAINTS =================

@login_required
def view_complaints(request):

    search_query = request.GET.get('search')

    complaints = Complaint.objects.filter(
        user=request.user
    )

    if search_query:

        complaints = complaints.filter(
            title__icontains=search_query
        )

    return render(request, 'view_complaints.html', {

        'complaints': complaints

    })


# ================= DELETE COMPLAINT =================

@login_required
def delete_complaint(request, id):

    complaint = Complaint.objects.get(
        id=id,
        user=request.user
    )

    complaint.delete()

    messages.success(
        request,
        'Complaint deleted successfully 🗑️'
    )

    return redirect('/view/')