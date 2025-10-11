
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Internship, InternshipApplication
from .forms import InternshipPostForm, InternshipApplicationForm

# Applicant: See all their internship applications
@login_required
def my_internship_applications(request):
    applications = InternshipApplication.objects.filter(applicant=request.user).select_related('internship').order_by('-applied_at')
    return render(request, 'internship/my_applications.html', {'applications': applications})

# Post owner: See all applications for their internships
@login_required
def my_post_internship_applications(request):
    applications = InternshipApplication.objects.filter(internship__posted_by=request.user).select_related('internship', 'applicant').order_by('-applied_at')
    return render(request, 'internship/my_post_applications.html', {'applications': applications})

def internship_list(request):
    internships = Internship.objects.all().order_by('-created_at')
    applied_internships = []
    # if request.user.is_authenticated:
    #     applied_internships = Application.objects.filter(applicant=request.user, internship__isnull=False).values_list('internship_id', flat=True)
    return render(request, 'internship/internships.html', {'internships': internships, 'applied_internships': applied_internships})

@login_required
def internship_post_create(request):
    if request.method == 'POST':
        form = InternshipPostForm(request.POST, request.FILES)
        if form.is_valid():
            internship = form.save(commit=False)
            internship.posted_by = request.user
            internship.save()
            messages.success(request, "Internship posted successfully.")
            return redirect('internship_list')
    else:
        form = InternshipPostForm()
    return render(request, 'internship/internship_post_form.html', {'form': form})


@login_required
def internship_apply(request, internship_id):
    internship = get_object_or_404(Internship, id=internship_id)
    if InternshipApplication.objects.filter(internship=internship, applicant=request.user).exists():
        messages.error(request, "You have already applied for this internship.")
        return redirect('internship_list')
    if request.method == 'POST':
        form = InternshipApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.internship = internship
            application.applicant = request.user
            application.status = 'pending'
            application.save()
            messages.success(request, "Application submitted successfully.")
            return redirect('internship_list')
    else:
        form = InternshipApplicationForm()
    return render(request, 'internship/internship_apply_form.html', {'form': form, 'internship': internship})

@login_required
def internship_delete(request, internship_id):
    internship = get_object_or_404(Internship, id=internship_id, posted_by=request.user)
    internship.delete()
    messages.success(request, "Internship deleted successfully.")
    return redirect('internship_list')


@login_required
def internship_application_manage(request, application_id):
    from .models import InternshipApplication
    application = get_object_or_404(InternshipApplication, id=application_id, internship__posted_by=request.user)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action in ['accept', 'reject']:
            application.status = 'accepted' if action == 'accept' else 'rejected'
            application.save()
            messages.success(request, f"Application {application.status} successfully.")
        else:
            messages.error(request, "Invalid action.")
        return redirect('internship_list')
    return render(request, 'internship/application_manage.html', {'application': application})