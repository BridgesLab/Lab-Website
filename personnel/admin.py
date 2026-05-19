'''This package sets up the admin interface for the :mod:`personnel` app.'''

from django.contrib import admin
from personnel.models import Role, JobType, Degree, Award, Organization, Address, Person, JobPosting
class AddressAdmin(admin.ModelAdmin):    passadmin.site.register(Address, AddressAdmin)class RoleAdmin(admin.ModelAdmin):    passadmin.site.register(Role, RoleAdmin)class JobTypeAdmin(admin.ModelAdmin):    passadmin.site.register(JobType, JobTypeAdmin)class DegreeAdmin(admin.ModelAdmin):    passadmin.site.register(Degree, DegreeAdmin)class AwardAdmin(admin.ModelAdmin):    passadmin.site.register(Award, AwardAdmin)class OrganizationAdmin(admin.ModelAdmin):    passadmin.site.register(Organization, OrganizationAdmin)class PersonAdmin(admin.ModelAdmin):    passadmin.site.register(Person, PersonAdmin)

class JobPostingAdmin(admin.ModelAdmin):
    pass
admin.site.register(JobPosting, JobPostingAdmin)

from django.contrib import admin
from personnel.models import Person

# Proxy model for current lab members
class CurrentLabMember(Person):
    class Meta:
        proxy = True
        verbose_name = "Current Lab Member"
        verbose_name_plural = "Current Lab Members"

# Custom admin for the proxy model
@admin.register(CurrentLabMember)
class CurrentLabMemberAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(current_lab_member=True)

    # Customize the admin list view
    list_display = ['full_name', 'email', 'current_lab_member', 'lab_roles_display']
    list_filter = ['gender', 'lab_roles']
    search_fields = ['first_name', 'last_name', 'email']
    readonly_fields = ['name_slug', 'created', 'updated']

    # Custom method to display lab roles
    def lab_roles_display(self, obj):
        return ", ".join([str(role) for role in obj.lab_roles.all()]) if obj.lab_roles.exists() else "None"
    lab_roles_display.short_description = "Lab Roles"

