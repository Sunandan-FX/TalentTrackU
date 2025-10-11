from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ResearchPaper, Application
from .forms import ResearchPaperPostForm

def research_paper_list(request):
    papers = ResearchPaper.objects.all().order_by('-created_at')
    applications = None
    if request.user.is_authenticated:
        applications = Application.objects.filter(applicant=request.user)
    return render(request, 'research_paper/research_papers.html', {'papers': papers, 'applications': applications})

@login_required
def research_paper_post_create(request):
    if request.user.user_profile.role not in ['student','alumni', 'company']:
        messages.error(request, "You don't have permission to post research papers.")
        return redirect('research_paper_list')
    if request.method == 'POST':
        form = ResearchPaperPostForm(request.POST, request.FILES)
        if form.is_valid():
            paper = form.save(commit=False)
            paper.posted_by = request.user
            paper.save()
            messages.success(request, "Research paper posted successfully.")
            return redirect('research_paper_list')
    else:
        form = ResearchPaperPostForm()
    return render(request, 'research_paper/research_paper_post_form.html', {'form': form})

@login_required
def research_paper_apply(request, paper_id):
    if request.user.user_profile.role != 'student':
        messages.error(request, "Only students can apply for research papers.")
        return redirect('research_paper_list')
    paper = get_object_or_404(ResearchPaper, id=paper_id)
    if Application.objects.filter(paper=paper, applicant=request.user).exists():
        messages.error(request, "You have already applied for this paper.")
        return redirect('research_paper_list')
    Application.objects.create(paper=paper, applicant=request.user)
    messages.success(request, "Application submitted successfully.")
    return redirect('research_paper_list')

@login_required
def research_paper_delete(request, paper_id):
    paper = get_object_or_404(ResearchPaper, id=paper_id, posted_by=request.user)
    if request.user.user_profile.role not in ['alumni', 'company']:
        messages.error(request, "You don't have permission to delete this paper.")
        return redirect('research_paper_list')
    paper.delete()
    messages.success(request, "Research paper deleted successfully.")
    return redirect('research_paper_list')