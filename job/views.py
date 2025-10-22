from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Job, Application
from .forms import JobPostForm
from .forms import ApplicationForm
from django.core.mail import send_mail
from django.conf import settings

def job_list(request):
    jobs = Job.objects.all().order_by('-created_at')
    for job in jobs:
        job.applications = Application.objects.filter(job=job).select_related('applicant')
    applications = None
    if request.user.is_authenticated:
        applications = Application.objects.filter(applicant=request.user)
    return render(request, 'job/jobs.html', {
        'jobs': jobs,
        'applications': applications
    })

@login_required
def job_post_create(request):
    if request.method == 'POST':
        form = JobPostForm(request.POST, request.FILES)
        if form.is_valid():
            job = form.save(commit=False)
            job.posted_by = request.user
            job.save()
            messages.success(request, "Job posted successfully.")
            return redirect('job:job_list')
    else:
        form = JobPostForm()
    return render(request, 'job/job_post_form.html', {'form': form})


@login_required
def job_apply(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    if Application.objects.filter(job=job, applicant=request.user).exists():
        messages.error(request, "You have already applied for this job.")
        return redirect('job:job_list')
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user
            application.status = 'pending'
            application.save()
            messages.success(request, "Application submitted successfully.")
            return redirect('job:job_list')
    else:
        form = ApplicationForm()
    return render(request, 'job/job_apply_form.html', {'form': form, 'job': job})

@login_required
def job_delete(request, job_id):
    job = get_object_or_404(Job, id=job_id, posted_by=request.user)
    job.delete()
    messages.success(request, "Job deleted successfully.")
    return redirect('job:job_list')

@login_required
def job_application_manage(request, application_id):
    application = get_object_or_404(Application, id=application_id, job__posted_by=request.user)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        old_status = application.status
        
        if action in ['accept', 'reject']:
            application.status = 'accepted' if action == 'accept' else 'rejected'
            application.save()
            
            messages.success(request, f"Application {application.status} successfully!")
        else:
            messages.error(request, "Invalid action.")
        
        return redirect('job:my_post_job_applications')
    
    return render(request, 'job/application_manager.html', {'application': application})


@login_required
def my_job_applications(request):
    applications = Application.objects.filter(applicant=request.user).select_related('job')
    return render(request, 'job/my_applications.html', {'applications': applications})

# Post Owner: View all applications to jobs posted by the current user
def my_post_job_applications(request):
    """View all applications to jobs posted by the current user"""
    applications = Application.objects.filter(job__posted_by=request.user).select_related('job', 'applicant')
    return render(request, 'job/my_post_applications.html', {'applications': applications})