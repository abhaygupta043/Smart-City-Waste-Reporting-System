from django.contrib import admin
from .models import Report, User
admin.site.site_header = "CleanTrack Admin Portal"
admin.site.site_title = " CleanTrack Logging"
admin.site.index_title = "Welcome to the CleanTrack Management System"




# Register User so you can see points in the Admin Panel
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'reward_points', 'is_staff')

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('location', 'user', 'status', 'created_at')
    list_filter = ('status',)
    actions = ['approve_reports', 'reject_reports']

    def approve_reports(self, request, queryset):
        count = 0
        for report in queryset:
            # Check for 'Pending' or any status that isn't already 'Approved'
            if report.status != 'Approved':
                report.status = 'Approved'
                report.save()

                # Access the related user and increment points
                user = report.user
                user.reward_points += 10
                user.save()
                count += 1
        
        self.message_user(request, f"Successfully approved {count} reports and awarded points!")

    def reject_reports(self, request, queryset):
        queryset.update(status='Rejected')
        self.message_user(request, "Selected reports have been rejected.")