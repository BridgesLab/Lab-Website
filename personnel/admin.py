'''This package sets up the admin interface for the :mod:`personnel` app.'''

from django.contrib import admin
from personnel.models import Role, JobType, Degree, Award, Organization, Address, Person, JobPosting
class AddressAdmin(admin.ModelAdmin):    passadmin.site.register(Address, AddressAdmin)class RoleAdmin(admin.ModelAdmin):    passadmin.site.register(Role, RoleAdmin)class JobTypeAdmin(admin.ModelAdmin):    passadmin.site.register(JobType, JobTypeAdmin)class DegreeAdmin(admin.ModelAdmin):    passadmin.site.register(Degree, DegreeAdmin)class AwardAdmin(admin.ModelAdmin):    passadmin.site.register(Award, AwardAdmin)class OrganizationAdmin(admin.ModelAdmin):    passadmin.site.register(Organization, OrganizationAdmin)class PersonAdmin(admin.ModelAdmin):    passadmin.site.register(Person, PersonAdmin)

class JobPostingAdmin(admin.ModelAdmin):
    pass
admin.site.register(JobPosting, JobPostingAdmin)
