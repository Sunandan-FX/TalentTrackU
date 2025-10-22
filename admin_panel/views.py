from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from job.models import Job, Application
from user.models import UserProfile
from research_paper.models import ResearchPaper
from internship.models import Internship
from django.db.models import Count, Q
from datetime import datetime, timedelta
from django.contrib import messages
from django.http import JsonResponse
import json

def superuser_required(view_func):
    return user_passes_test(
        lambda u: u.is_active and u.is_superuser,
        login_url='/admin/login/'
    )(view_func)

@superuser_required
def admin_dashboard(request):
    # Get statistics
    total_users = User.objects.count()
    total_jobs = Job.objects.count()
    total_applications = Application.objects.count()
    total_papers = ResearchPaper.objects.count()
    total_internships = Internship.objects.count()
    
    # Recent activity (last 7 days)
    week_ago = datetime.now() - timedelta(days=7)
    recent_users = User.objects.filter(date_joined__gte=week_ago).count()
    recent_jobs = Job.objects.filter(created_at__gte=week_ago).count()
    recent_applications = Application.objects.filter(applied_at__gte=week_ago).count()
    
    # User roles distribution
    role_distribution = UserProfile.objects.values('role').annotate(count=Count('role'))
    
    # Application status distribution
    app_status_distribution = Application.objects.values('status').annotate(count=Count('status'))
    
    # Recent users
    recent_user_list = User.objects.select_related('user_profile').order_by('-date_joined')[:5]
    
    # Recent applications
    recent_applications_list = Application.objects.select_related('job', 'applicant').order_by('-applied_at')[:5]
    
    # ✅ FIXED: Define context variable properly
    context = {
        'total_users': total_users,
        'total_jobs': total_jobs,
        'total_applications': total_applications,
        'total_papers': total_papers,
        'total_internships': total_internships,
        'recent_users': recent_users,
        'recent_jobs': recent_jobs,
        'recent_applications': recent_applications,
        'role_distribution': role_distribution,
        'app_status_distribution': app_status_distribution,
        'recent_user_list': recent_user_list,
        'recent_applications_list': recent_applications_list,
    }
    
    return render(request, 'admin_panel/dashboard.html', context)

@superuser_required
def admin_users(request):
    users = User.objects.select_related('user_profile').all().order_by('-date_joined')
    return render(request, 'admin_panel/users.html', {'users': users})

@superuser_required
def admin_edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        role = request.POST.get('role')
        is_active = request.POST.get('is_active') == 'on'
        
        # Update user
        user.username = username
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.is_active = is_active
        user.save()
        
        # Update user profile
        if hasattr(user, 'user_profile'):
            user.user_profile.role = role
            user.user_profile.save()
        
        messages.success(request, f"User {username} updated successfully!")
        return redirect('admin_panel:admin_users')
    
    return render(request, 'admin_panel/edit_user.html', {'user_obj': user})

@superuser_required
def admin_delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        username = user.username
        user.delete()
        messages.success(request, f"User {username} deleted successfully!")
        return redirect('admin_panel:admin_users')
    
    return render(request, 'admin_panel/delete_confirm.html', {
        'object': user,
        'object_type': 'user',
        'cancel_url': 'admin_panel:admin_users'
    })

@superuser_required
def admin_jobs(request):
    jobs = Job.objects.select_related('posted_by').all().order_by('-created_at')
    return render(request, 'admin_panel/jobs.html', {'jobs': jobs})

@superuser_required
def admin_edit_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    
    if request.method == 'POST':
        job.title = request.POST.get('title')
        job.company = request.POST.get('company')
        job.description = request.POST.get('description')
        job.location = request.POST.get('location')
        job.salary = request.POST.get('salary')
        job.save()
        
        messages.success(request, f"Job '{job.title}' updated successfully!")
        return redirect('admin_panel:admin_jobs')
    
    return render(request, 'admin_panel/edit_job.html', {'job': job})

@superuser_required
def admin_delete_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    
    if request.method == 'POST':
        job_title = job.title
        job.delete()
        messages.success(request, f"Job '{job_title}' deleted successfully!")
        return redirect('admin_panel:admin_jobs')
    
    return render(request, 'admin_panel/delete_confirm.html', {
        'object': job,
        'object_type': 'job',
        'cancel_url': 'admin_panel:admin_jobs'
    })

@superuser_required
def admin_applications(request):
    applications = Application.objects.select_related('job', 'applicant').all().order_by('-applied_at')
    return render(request, 'admin_panel/applications.html', {'applications': applications})

@superuser_required
def admin_edit_application(request, application_id):
    application = get_object_or_404(Application, id=application_id)
    
    if request.method == 'POST':
        status = request.POST.get('status')
        cover_letter = request.POST.get('cover_letter')
        
        application.status = status
        application.cover_letter = cover_letter
        application.save()
        
        messages.success(request, f"Application updated successfully!")
        return redirect('admin_panel:admin_applications')
    
    return render(request, 'admin_panel/edit_application.html', {'application': application})

@superuser_required
def admin_delete_application(request, application_id):
    application = get_object_or_404(Application, id=application_id)
    
    if request.method == 'POST':
        application.delete()
        messages.success(request, "Application deleted successfully!")
        return redirect('admin_panel:admin_applications')
    
    return render(request, 'admin_panel/delete_confirm.html', {
        'object': application,
        'object_type': 'application',
        'cancel_url': 'admin_panel:admin_applications'
    })

@superuser_required
def admin_research_papers(request):
    papers = ResearchPaper.objects.select_related('posted_by').all().order_by('-created_at')
    return render(request, 'admin_panel/research_papers.html', {'papers': papers})

@superuser_required
def admin_edit_research_paper(request, paper_id):
    paper = get_object_or_404(ResearchPaper, id=paper_id)
    
    if request.method == 'POST':
        paper.title = request.POST.get('title')
        paper.author_name = request.POST.get('author_name')
        paper.field = request.POST.get('field')
        paper.abstract = request.POST.get('abstract')
        paper.save()
        
        messages.success(request, f"Research paper '{paper.title}' updated successfully!")
        return redirect('admin_panel:admin_research_papers')
    
    return render(request, 'admin_panel/edit_research_paper.html', {'paper': paper})

@superuser_required
def admin_delete_research_paper(request, paper_id):
    paper = get_object_or_404(ResearchPaper, id=paper_id)
    
    if request.method == 'POST':
        paper_title = paper.title
        paper.delete()
        messages.success(request, f"Research paper '{paper_title}' deleted successfully!")
        return redirect('admin_panel:admin_research_papers')
    
    return render(request, 'admin_panel/delete_confirm.html', {
        'object': paper,
        'object_type': 'research paper',
        'cancel_url': 'admin_panel:admin_research_papers'
    })

@superuser_required
def admin_internships(request):
    internships = Internship.objects.select_related('posted_by').all().order_by('-created_at')
    return render(request, 'admin_panel/internships.html', {'internships': internships})

@superuser_required
def admin_edit_internship(request, internship_id):
    internship = get_object_or_404(Internship, id=internship_id)
    
    if request.method == 'POST':
        internship.title = request.POST.get('title')
        internship.company = request.POST.get('company')
        internship.description = request.POST.get('description')
        internship.location = request.POST.get('location')
        internship.duration = request.POST.get('duration')
        internship.requirements = request.POST.get('requirements')
        internship.save()
        
        messages.success(request, f"Internship '{internship.title}' updated successfully!")
        return redirect('admin_panel:admin_internships')
    
    return render(request, 'admin_panel/edit_internship.html', {'internship': internship})

@superuser_required
def admin_delete_internship(request, internship_id):
    internship = get_object_or_404(Internship, id=internship_id)
    
    if request.method == 'POST':
        internship_title = internship.title
        internship.delete()
        messages.success(request, f"Internship '{internship_title}' deleted successfully!")
        return redirect('admin_panel:admin_internships')
    
    return render(request, 'admin_panel/delete_confirm.html', {
        'object': internship,
        'object_type': 'internship',
        'cancel_url': 'admin_panel:admin_internships'
    })

@superuser_required
def quick_update_status(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            data = json.loads(request.body)
            application_id = data.get('application_id')
            new_status = data.get('status')
            
            application = get_object_or_404(Application, id=application_id)
            application.status = new_status
            application.save()
            
            return JsonResponse({
                'success': True,
                'new_status': new_status,
                'status_display': application.get_status_display()
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})

@superuser_required
def quick_toggle_user_status(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_active = not user.is_active
    user.save()
    
    messages.success(request, f"User {user.username} {'activated' if user.is_active else 'deactivated'}!")
    return redirect('admin_panel:admin_users')
