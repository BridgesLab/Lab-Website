'''This package sets up the admin interface for the :mod:`papers` app.'''

from django.contrib import admin

from papers.models import Publication, AuthorDetails, AuthorContributions, JournalClubArticle, Commentary

class PublicationAdmin(admin.ModelAdmin):
    '''The :class:`~papers.models.Publication` model admin is the default.'''
    pass
admin.site.register(Publication, PublicationAdmin)

class AuthorDetailsAdmin(admin.ModelAdmin):
    '''The :class:`~papers.models.AuthorDetails` model admin is the default.'''
    pass
admin.site.register(AuthorDetails, AuthorDetailsAdmin)

class AuthorContributionsAdmin(admin.ModelAdmin):
    pass
admin.site.register(AuthorContributions, AuthorContributionsAdmin)

class JournalClubArticleAdmin(admin.ModelAdmin):
	pass
admin.site.register(JournalClubArticle,JournalClubArticleAdmin)

class CommentaryAdmin(admin.ModelAdmin):
	pass
admin.site.register(Commentary,CommentaryAdmin)