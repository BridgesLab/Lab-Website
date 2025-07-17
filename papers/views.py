'''This app contains the views for the :mod`papers` app.

There are three views for this app, :class:`~papers.views.LaboratoryPaperList`, :class:`~papers.views.InterestingPaperList` and :class:`~papers.views.PaperDetailView`

'''
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.template import RequestContext
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q

from django.contrib.auth.mixins import PermissionRequiredMixin

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import PublicationSerializer, PublicationListSerializer
from .filters import PublicationFilter

from papers.models import Publication, Commentary, JournalClubArticle
from papers.context_processors import api_keys
from papers.forms import PublicationForm, PublicationEditForm

class LaboratoryPaperList(ListView):
    '''This class generates the view for laboratory-papers located at **/papers**.
    
    This is filtered based on whether the :class:`~papers.models.Publication` is marked as laboratory_paper = True.
    '''
    queryset = Publication.objects.filter(laboratory_paper=True)
    template_name = "paper-list.html"
    
    def get_context_data(self, **kwargs):
        '''This method adds to the context the paper-list-type  = interesting.'''
        context = super(LaboratoryPaperList, self).get_context_data(**kwargs)
        context['paper_list_type'] = "laboratory"
        return context           
    
class InterestingPaperList(ListView):
    '''This class generates the view for interesting-papers located at **/papers/interesting**.
    
    This is filtered based on whether the :class:`~papers.models.Publication` is marked as interesting_paper = True.
    '''
    queryset = Publication.objects.filter(interesting_paper=True)
    template_name = "paper-list.html"
    
    def get_context_data(self, **kwargs):
        '''This method adds to the context the paper-list-type  = interesting.'''
        context = super(InterestingPaperList, self).get_context_data(**kwargs)
        context['paper_list_type'] = "interesting"
        return context               

class PaperDetailView(DetailView):
    '''This class generates the view for paper-details located at **/papers/<title_slug>**.
    
    '''
    model = Publication
    slug_field = "title_slug"
    slug_url_kwarg = "title_slug"
    template_name = "paper-detail.html"
                
class PaperCreate(PermissionRequiredMixin, CreateView):
    '''This view is for creating a new :class:`~papers.models.Publication`.
    
    It requires the permissions to create a new paper and is found at the url **/paper/new**.'''
    
    permission_required = 'papers.create_publication'
    model = Publication
    form_class = PublicationForm
    template_name = 'publication_form.html'
    
class PaperUpdate(PermissionRequiredMixin, UpdateView):
    '''This view is for updating a :class:`~papers.models.Publication`.
    
    It requires the permissions to update a paper and is found at the url **/paper/<slug>/edit**.'''
    
    permission_required = 'papers.update_publication'
    model = Publication
    form_class = PublicationEditForm
    slug_field = "title_slug"
    slug_url_kwarg = "title_slug"
    template_name = 'publication_form.html' 
    
class PaperDelete(PermissionRequiredMixin, DeleteView):
    '''This view is for deleting a :class:`~papers.models.Publication`.
    
    It requires the permissions to delete a paper and is found at the url **/paper/<slug>/delete**.'''
    
    permission_required = 'papers.delete_publication'
    model = Publication
    slug_field = "title_slug"
    slug_url_kwarg = "title_slug"
    template_name = 'confirm_delete.html'
    template_object_name = 'object' 
    success_url = reverse_lazy('laboratory-papers')        
                   
    
class CommentaryList(ListView):
    '''This class generates the view for commentaries located at **/papers/commentary**.
    '''
    model = Commentary
    template_name = "commentary-list.html"

    def get_context_data(self, **kwargs):
        context = super(CommentaryList, self).get_context_data(**kwargs)
        context['journal_article_list'] = JournalClubArticle.objects.all()[:10]
        return context
        
class JournalClubList(ListView):
    '''This class generates the view for journal club articles located at **/papers/journal-club**.
    '''
    model = JournalClubArticle
    template_name = "jc-list.html"   
    context_object_name = 'journal_club_list'  

class CommentaryDetail(DetailView):
    '''This class generates the view for commentary-detail located at **/papers/commentary/<pk>**.
    '''
    model = Commentary
    template_name = "commentary-detail.html"
                
class CommentaryCreate(PermissionRequiredMixin, CreateView):
    '''This view is for creating a new :class:`~papers.models.Commentary`.
    
    It requires the permissions to create a new paper and is found at the url **/papers/commentary/new**.'''
    
    permission_required = 'papers.create_commentary'
    model = Commentary
    fields = "__all__"
    template_name = "commentary-form.html"

class CommentaryUpdate(PermissionRequiredMixin, UpdateView):
    '''This view is for updating a :class:`~papers.models.Commentary`.
    
    It requires the permissions to update a commentary and is found at the url **/paper/commentary/<pk>/edit**.'''
    
    permission_required = 'papers.update_commentary'
    model = Commentary
    fields = "__all__"
    template_name = 'commentary-form.html' 
    
class CommentaryDelete(PermissionRequiredMixin, DeleteView):
    '''This view is for deleting a :class:`~papers.models.Commentary`.
    
    It requires the permissions to delete a paper and is found at the url **/paper/commentary/<pk>/delete**.'''
    
    permission_required = 'papers.delete_commentary'
    model = Commentary
    template_name = 'confirm_delete.html'
    template_object_name = 'object'
    success_url = reverse_lazy('commentary-list') 

class PublicationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Publication model providing read-only API access.
    
    Provides endpoints for:
    - GET /api/v2/publications/ - List all publications
    - GET /api/v2/publications/{id}/ - Retrieve single publication
    - GET /api/v2/publications/set/{ids}/ - Retrieve multiple publications by IDs
    
    Supports filtering by:
    - year: Exact year match
    - type: Publication type (exact or contains)
    - laboratory_paper: Boolean filter
    - search: Full-text search across title, abstract, journal
    
    Supports ordering by:
    - year, title, journal, date_added, date_last_modified
    
    Default ordering: -date_added (newest first)
    """
    
    queryset = Publication.objects.all()
    serializer_class = PublicationSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = PublicationFilter
    search_fields = ['title', 'abstract', 'journal']
    ordering_fields = ['year', 'title', 'journal', 'date_added', 'date_last_modified']
    ordering = ['-date_added']
    
    def get_serializer_class(self):
        """
        Return appropriate serializer class based on action.
        
        Uses PublicationListSerializer for list view to optimize performance
        by excluding large text fields like abstract.
        """
        if self.action == 'list':
            return PublicationListSerializer
        return PublicationSerializer
    
    @action(detail=False, methods=['get'], url_path='set/(?P<ids>[^/]+)')
    def get_set(self, request, ids=None):
        """
        Retrieve multiple publications by their IDs.
        
        Args:
            ids: Comma-separated list of publication IDs
            
        Returns:
            List of publications matching the provided IDs
            
        Example:
            GET /api/v1/publications/set/1,3,5/
        """
        try:
            id_list = [int(id.strip()) for id in ids.split(',') if id.strip()]
        except ValueError:
            return Response(
                {'error': 'Invalid ID format. Use comma-separated integers.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        publications = self.get_queryset().filter(id__in=id_list)
        serializer = self.get_serializer(publications, many=True)
        
        return Response({
            'count': len(serializer.data),
            'results': serializer.data
        })
    
    @action(detail=False, methods=['get'])
    def laboratory_papers(self, request):
        """
        Retrieve all laboratory papers.
        
        Returns:
            List of publications where laboratory_paper=True
        """
        publications = self.get_queryset().filter(laboratory_paper=True)
        serializer = self.get_serializer(publications, many=True)
        
        return Response({
            'count': len(serializer.data),
            'results': serializer.data
        })
    
    @action(detail=False, methods=['get'])
    def interesting_papers(self, request):
        """
        Retrieve all interesting papers.
        
        Returns:
            List of publications where interesting_paper=True
        """
        publications = self.get_queryset().filter(interesting_paper=True)
        serializer = self.get_serializer(publications, many=True)
        
        return Response({
            'count': len(serializer.data),
            'results': serializer.data
        })
