from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from accounts.decorators import employer_required
from .forms import JobForm, ApplicationForm
from .models import Job, Application, Category
from accounts.models import EmployerProfile
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q

@login_required
@employer_required
def employer_dashboard(request):
    profile = request.user.employer_profile
    jobs = profile.jobs.all()
    return render(request, 'jobs/employer/dashboard.html', {'jobs': jobs, 'profile': profile})

@login_required
@employer_required
def create_job(request):
    profile = request.user.employer_profile
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.company = profile
            job.save()
            messages.success(request, "Job posted successfully.")
            return redirect('jobs:employer_dashboard')
    else:
        form = JobForm()
    return render(request, 'jobs/employer/create_job.html', {'form': form})

@login_required
@employer_required
def edit_job(request, pk):
    job = get_object_or_404(Job, pk=pk, company=request.user.employer_profile)
    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, "Job updated.")
            return redirect('jobs:employer_dashboard')
    else:
        form = JobForm(instance=job)
    return render(request, 'jobs/employer/edit_job.html', {'form': form, 'job': job})

@login_required
@employer_required
def view_applications(request, job_pk):
    job = get_object_or_404(Job, pk=job_pk, company=request.user.employer_profile)
    applications = job.applications.select_related('applicant')
    return render(request, 'jobs/employer/applications.html', {'job': job, 'applications': applications})

@login_required
@employer_required
def change_application_status(request, app_pk):
    app = get_object_or_404(Application, pk=app_pk, job__company=request.user.employer_profile)
    new_status = request.POST.get('status')
    if new_status in dict(Application.STATUS_CHOICES).keys():
        app.status = new_status
        app.save()
        messages.success(request, "Status updated.")
    return redirect('jobs:view_applications', job_pk=app.job.pk)

def job_list(request):
    q = request.GET.get('q','')
    location = request.GET.get('location','')
    category = request.GET.get('category','')
    company = request.GET.get('company','')

    jobs = Job.objects.filter(is_active=True)
    if q:
        jobs = jobs.filter(Q(title__icontains=q) | Q(description__icontains=q))
    if location:
        jobs = jobs.filter(location__icontains=location)
    if category:
        jobs = jobs.filter(category__id=category)
    if company:
        jobs = jobs.filter(company__id=company)

    paginator = Paginator(jobs, 10)
    page = request.GET.get('page')
    jobs_page = paginator.get_page(page)
    categories = Category.objects.all()
    companies = EmployerProfile.objects.all()
    return render(request, 'jobs/job_list.html', {'jobs': jobs_page, 'categories': categories, 'companies': companies, 'q': q})

def job_detail(request, pk, slug=None):
    job = get_object_or_404(Job, pk=pk, is_active=True)
    return render(request, 'jobs/job_detail.html', {'job': job})

@login_required
def apply_job(request, pk):
    job = get_object_or_404(Job, pk=pk, is_active=True)
    # only jobseekers allowed
    if not request.user.is_jobseeker():
        messages.error(request, "Only job seekers can apply.")
        return redirect('jobs:detail', pk=job.id, slug=job.slug)

    # prevent duplicate
    if job.applications.filter(applicant=request.user).exists():
        messages.warning(request, "You've already applied to this job.")
        return redirect('jobs:detail', pk=job.id, slug=job.slug)

    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            app = form.save(commit=False)
            app.job = job
            app.applicant = request.user
            app.save()
            messages.success(request, "Application submitted.")
            return redirect('jobs:my_applications')
    else:
        form = ApplicationForm()
    return render(request, 'jobs/apply.html', {'form': form, 'job': job})

@login_required
def my_applications(request):
    apps = request.user.applications.select_related('job').all()
    return render(request, 'jobs/my_applications.html', {'applications': apps})
