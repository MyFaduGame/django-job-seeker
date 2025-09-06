from django.contrib import admin
from .models import Job, Application, Category
import csv
from django.http import HttpResponse

class ApplicationInline(admin.TabularInline):
    model = Application
    extra = 0
    readonly_fields = ('applicant', 'resume', 'applied_at', 'status')
    can_delete = False

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'location', 'employment_type', 'is_active', 'posted_at')
    list_filter = ('is_active','employment_type','company')
    search_fields = ('title','description','company__company_name')
    inlines = [ApplicationInline]
    actions = ['deactivate_jobs','export_applicants_csv']

    def deactivate_jobs(self, request, queryset):
        count = queryset.update(is_active=False)
        self.message_user(request, f"{count} job(s) deactivated.")
    deactivate_jobs.short_description = "Deactivate selected jobs"

    def export_applicants_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=applicants.csv'
        writer = csv.writer(response)
        writer.writerow(['Job Title', 'Applicant Username', 'Applicant Email', 'Phone', 'Status', 'Applied At'])
        for job in queryset:
            for app in job.applications.select_related('applicant').all():
                writer.writerow([
                    job.title,
                    app.applicant.username,
                    app.applicant.email,
                    getattr(app.applicant, 'phone', ''),
                    app.status,
                    app.applied_at.isoformat()
                ])
        return response
    export_applicants_csv.short_description = "Export applicants for selected jobs to CSV"

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('job','applicant','status','applied_at')
    list_filter = ('status','applied_at')
    search_fields = ('applicant__username','job__title')

admin.site.register(Category)
