"""
This package contains the unit tests for the :mod:`papers` app.

It contains view and model tests for each model, grouped together.
Contains the two model tests:

* :class:`~papers.tests.PublicationModelTests` 
* :class:`~papers.tests.AuthorDetailsModelTests` 

The API tests:

* :class:`~PublicationResourceTests`

And the view tests:

* :class:`~papers.tests.PublicationViewTests` 
"""
import json
from datetime import date

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from papers.models import Publication, AuthorDetails, Person, Commentary
from papers.serializers import PublicationSerializer, PublicationListSerializer
from papers.filters import PublicationFilter

MODELS = [Publication, AuthorDetails, Commentary]

class PublicationModelTests(TestCase):
    '''This class tests various aspects of the :class:`~papers.models.Publication` model.'''
    
    fixtures = ['test_publication.json', 'test_publication_personnel.json']

    def setUp(self):
        '''Instantiate the test client.  Creates a test user.'''
        self.client = Client()
        self.test_user = User.objects.create_user('testuser', 'blah@blah.com', 'testpassword')
        self.test_user.is_superuser = True
        self.test_user.is_active = True
        self.test_user.save()
        self.assertEqual(self.test_user.is_superuser, True)
        login = self.client.login(username='testuser', password='testpassword')
        self.assertTrue(login, 'Could not log in')
                
    def test_create_new_paper_minimum(self):
        '''This test creates a :class:`~papers.models.Publication` with the required information only.'''
        test_publication = Publication(title='Test Publication.', laboratory_paper=True, interesting_paper=False, preprint=False)
        test_publication.save()
        self.assertEqual(test_publication.pk, 3)
        
    #def test_create_new_paper_all(self):
    #    '''This test creates a `::class:Publication` with the required information only.'''
    #    test_publication = Publication(title='Test Publication') #add more fields
    #    test_publication.save()        
        
    def test_paper_string(self):
        '''This tests the string representation of a :class:`~papers.models.Publication`.'''
        test_publication = Publication.objects.get(title_slug='14-3-3-proteins-a-number-of-functions-for-a-numbered-protein', laboratory_paper=True, interesting_paper=False, preprint=False)
        self.assertEqual(str(test_publication), "14-3-3 proteins: a number of functions for a numbered protein.")
        
    def test_paper_title_slug(self):
        '''This tests the title_slug field of a :class:`~papers.models.Publication`.'''
        test_publication = Publication(title='Test Publication.', laboratory_paper=True, interesting_paper=False, preprint=False)
        test_publication.save()
        self.assertEqual(test_publication.title_slug, "test-publication")  
        
    def test_paper_absolute_url(self):
        '''This tests the title_slug field of a :class:`~papers.models.Publication`.'''
        test_publication = Publication(title='Test Publication', laboratory_paper=True, interesting_paper=False, preprint=False)
        test_publication.save()
        self.assertEqual(test_publication.get_absolute_url(), "/papers/test-publication/") 
     
    def test_paper_doi_link(self):
        '''This tests the title_slug field of a :class:`~papers.models.Publication`.'''
        test_publication = Publication.objects.get(title="14-3-3 proteins: a number of functions for a numbered protein.", laboratory_paper=True, interesting_paper=False, preprint=False)
        self.assertEqual(test_publication.doi_link(), "http://dx.doi.org/10.1126/stke.2962005re10") 
        
    def test_full_pmcid(self):
        '''This tests that a correct full PMCID can be generated for a :class:`~papers.models.Publication`.'''
        test_publication = Publication(title="Test Publication", pmcid = "12345", laboratory_paper=True, interesting_paper=False, preprint=False)
        test_publication.save()
        self.assertEqual(test_publication.full_pmcid(), 'PMC12345')                         
                    
class AuthorDetailsModelTests(TestCase):
    '''This class tests varios aspects of the :class:`~papers.models.AuthorDetails` model.'''

    fixtures = ['test_publication', 'test_publication_personnel']

    def setUp(self):
        '''Instantiate the test client.  Creates a test user.'''
        self.client = Client()
        self.test_user = User.objects.create_user('testuser', 'blah@blah.com', 'testpassword')
        self.test_user.is_superuser = True
        self.test_user.is_active = True
        self.test_user.save()
        self.assertEqual(self.test_user.is_superuser, True)
        login = self.client.login(username='testuser', password='testpassword')
        self.assertTrue(login, 'Could not log in')
    
    def test_create_new_authordetail_minimum(self):
        '''This test creates a :class:`~papers.models.AuthorDetails` with the required information only.'''
        test_authordetail = AuthorDetails(author=Person.objects.get(pk=1), 
            order = 1, corresponding_author=True, equal_contributors=False)
        test_authordetail.save()
        
    def test_create_new_authordetail_all(self):
        '''This test creates a :class:`~papers.models.AuthorDetails` with the required information only.'''
        test_authordetail = AuthorDetails(author=Person.objects.get(pk=1), 
            order = 1,
            corresponding_author = True,
            equal_contributors = True)
        test_authordetail.save()             
            
    def test_authordetail_string(self):
        '''This tests that the string representaton of an :class:`~papers.models.AuthorDetails` object is correct.'''
        test_authordetail = AuthorDetails(author=Person.objects.get(pk=1), 
            order = 1, corresponding_author=True, equal_contributors=False)
        test_authordetail.save() 
        self.assertEqual(str(test_authordetail), '1 - None -  Dave Bridges')
        
class CommentaryModelTests(TestCase):
    '''This class tests various aspects of the :class:`~papers.models.Commentary` model.'''
    
    fixtures = ['test_publication', 'test_personnel','test_publication_personnel.json']

    def setUp(self):
        '''Instantiate the test client.  Creates a test user.'''
        self.client = Client()
        self.test_user = User.objects.create_user('testuser', 'blah@blah.com', 'testpassword')
        self.test_user.is_superuser = True
        self.test_user.is_active = True
        self.test_user.save()
        self.assertEqual(self.test_user.is_superuser, True)
        login = self.client.login(username='testuser', password='testpassword')
        self.assertTrue(login, 'Could not log in')
                
    def test_create_new_commentary_minimum(self):
        '''This test creates a :class:`~papers.models.Commentary` with the required information only.'''
        test_commentary = Commentary(paper=Publication.objects.get(pk=1),
            comments = "Some comments")
        test_commentary.save()
        self.assertEqual(test_commentary.pk, 1) 
        
    def test_create_new_commentary_all(self):
        '''This test creates a :class:`~papers.models.Commentary` with all fields entered.'''
        test_commentary = Commentary(paper=Publication.objects.get(pk=1),
            comments = "Some comments",
            author = Person.objects.get(pk=1),
            citation = "some citation")
        test_commentary.save()
        self.assertEqual(test_commentary.pk, 1) 
        
    def test_commentary_string(self):
        '''This test creates a :class:`~papers.models.Commentary` and then verifies the string representation is correct.'''
        test_commentary = Commentary(paper=Publication.objects.get(pk=1),
            comments = "Some comments")
        test_commentary.save()
        self.assertEqual(str(test_commentary), "Journal club summary on 14-3-3 proteins: a number of functions for a numbered protein.")

class PublicationResourceTests(TestCase):  
    '''This class tests varios aspects of the :class:`~papers.api.PublicationResource` API model.'''

    fixtures = ['test_publication', 'test_publication_personnel']

    def setUp(self):
        '''Instantiate the test client.  Creates a test user.'''
        self.client = Client()
        self.test_user = User.objects.create_user('testuser', 'blah@blah.com', 'testpassword')
        self.test_user.is_superuser = True
        self.test_user.is_active = True
        self.test_user.save()
        self.assertEqual(self.test_user.is_superuser, True)
        login = self.client.login(username='testuser', password='testpassword')
        self.assertTrue(login, 'Could not log in')
                
    def api_publication_list_test(self):
        '''This tests that the API correctly renders a list of :class:`~papers.models.Publication` objects.'''
        response = self.client.get('/api/v1/publications/?format=json', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json; charset=utf-8')
        
    def api_publication_detail_test(self):
        '''This tests that the API correctly renders a particular :class:`~papers.models.Publication` objects.'''
        response = self.client.get('/api/v1/publications/1/?format=json', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json; charset=utf-8')  
        print(response)    
       
class PublicationViewTests(TestCase):
    '''This class tests the views for :class:`~papers.models.Publication` objects.'''

    fixtures = ['test_publication', 'test_publication_personnel']

    def setUp(self):
        """Instantiate the test client.  Creates a test user."""
        self.client = Client()
        self.test_user = User.objects.create_user('testuser', 'blah@blah.com', 'testpassword')
        self.test_user.is_superuser = True
        self.test_user.is_active = True
        self.test_user.save()
        self.assertEqual(self.test_user.is_superuser, True)
        login = self.client.login(username='testuser', password='testpassword')
        self.assertTrue(login, 'Could not log in')

    def test_publication_view(self):
        """This tests the paper-details view, ensuring that templates are loaded correctly.  

        This view uses a user with superuser permissions so does not test the permission levels for this view."""
        
        test_response = self.client.get('/papers/14-3-3-proteins-a-number-of-functions-for-a-numbered-protein/', follow=True)
        self.assertEqual(test_response.status_code, 200)
        self.assertTrue('publication' in test_response.context)        
        self.assertTemplateUsed(test_response, 'paper-detail.html')
        self.assertTemplateUsed(test_response, 'base.html') 
        self.assertTemplateUsed(test_response, 'disqus_snippet.html') 
        self.assertTemplateUsed(test_response, 'altmetric_snippet.html')                        
        self.assertEqual(test_response.context['publication'].pk, 1)
        self.assertEqual(test_response.context['publication'].title, '14-3-3 proteins: a number of functions for a numbered protein.')
        
    def test_lab_papers_list(self):
        """This tests the laboratory-papers view ensuring that templates are loaded correctly.
        
        This view uses a user with superuser permissions so does not test the permission levels for this view."""
        
        test_response = self.client.get('/papers/', follow=True)
        self.assertEqual(test_response.status_code, 200)
        self.assertTrue('publication_list' in test_response.context)        
        self.assertTemplateUsed(test_response, 'paper-list.html')
        self.assertTemplateUsed(test_response, 'base.html')
        self.assertTemplateUsed(test_response, 'facebook_api_sdk_script.html') 
        self.assertTemplateUsed(test_response, 'analytics_tracking.html')   
        self.assertTemplateUsed(test_response, 'paper-detail-snippet.html')
        self.assertEqual(test_response.context['publication_list'][0].pk, 1)
        self.assertEqual(test_response.context['publication_list'][0].title, '14-3-3 proteins: a number of functions for a numbered protein.')  
        
    def test_interesting_papers_list(self):
        """This tests the interesting-papers view ensuring that templates are loaded correctly.
        
        This view uses a user with superuser permissions so does not test the permission levels for this view."""
        
        test_response = self.client.get('/papers/interesting', follow=True)
        self.assertEqual(test_response.status_code, 200)
        self.assertTrue('publication_list' in test_response.context)       
        self.assertTemplateUsed(test_response, 'paper-list.html')
        self.assertTemplateUsed(test_response, 'base.html')
        self.assertTemplateUsed(test_response, 'paper-detail-snippet.html')                                
        self.assertEqual(test_response.context['publication_list'][0].pk, 2)
        self.assertEqual(test_response.context['publication_list'][0].title, "THE RELATION OF ADENOSINE-3', 5'-PHOSPHATE AND PHOSPHORYLASE TO THE ACTIONS OF CATECHOLAMINES AND OTHER HORMONES.")           

    def test_publication_view_create(self):
        """This tests the paper-new view, ensuring that templates are loaded correctly.  

        This view uses a user with superuser permissions so does not test the permission levels for this view."""
        
        test_response = self.client.get('/papers/new/', follow=True)
        self.assertEqual(test_response.status_code, 200)
        self.assertTemplateUsed(test_response, 'publication_form.html')         

    def test_publication_view_edit(self):
        """This tests the paper-edit view, ensuring that templates are loaded correctly.  

        This view uses a user with superuser permissions so does not test the permission levels for this view."""
        
        test_response = self.client.get('/papers/14-3-3-proteins-a-number-of-functions-for-a-numbered-protein/edit/', follow=True)
        self.assertEqual(test_response.status_code, 200)
        self.assertTrue('publication' in test_response.context)        
        self.assertTemplateUsed(test_response, 'publication_form.html')       
        self.assertEqual(test_response.context['publication'].pk, 1)
        self.assertEqual(test_response.context['publication'].title, '14-3-3 proteins: a number of functions for a numbered protein.')

        #verifies that a non-existent object returns a 404 error presuming there is no object with pk=2.
        null_response = self.client.get('/papers/not-a-real-paper/edit/', follow=True)
        self.assertEqual(null_response.status_code, 404)   

    def test_publication_view_delete(self):
        """This tests the paper-delete view, ensuring that templates are loaded correctly.  

        This view uses a user with superuser permissions so does not test the permission levels for this view."""
        
        test_response = self.client.get('/papers/14-3-3-proteins-a-number-of-functions-for-a-numbered-protein/delete/', follow=True)
        self.assertEqual(test_response.status_code, 200)
        self.assertTrue('publication' in test_response.context)        
        self.assertTemplateUsed(test_response, 'confirm_delete.html')
        self.assertEqual(test_response.context['publication'].pk, 1)
        self.assertEqual(test_response.context['publication'].title, '14-3-3 proteins: a number of functions for a numbered protein.')

        #verifies that a non-existent object returns a 404 error.
        null_response = self.client.get('/papers/not-a-real-paper/delete/', follow=True)
        self.assertEqual(null_response.status_code, 404)  
        
class CommentaryViewTests(TestCase):
    '''This class tests the views for :class:`~papers.models.Commentary` objects.'''

    fixtures = ['test_publication', 'test_personnel', 'test_commentary','test_publication_personnel']

    def setUp(self):
        """Instantiate the test client.  Creates a test user."""
        self.client = Client()
        self.test_user = User.objects.create_user('testuser', 'blah@blah.com', 'testpassword')
        self.test_user.is_superuser = True
        self.test_user.is_active = True
        self.test_user.save()
        self.assertEqual(self.test_user.is_superuser, True)
        login = self.client.login(username='testuser', password='testpassword')
        self.assertTrue(login, 'Could not log in')

    def test_commentary_view(self):
        """This tests the commentary-detail view, ensuring that templates are loaded correctly.  

        This view uses a user with superuser permissions so does not test the permission levels for this view."""
        test_response = self.client.get('/papers/commentary/1', follow=True)
        self.assertEqual(test_response.status_code, 200)
        self.assertTrue('commentary' in test_response.context)        
        self.assertTemplateUsed(test_response, 'commentary-detail.html')
        self.assertTemplateUsed(test_response, 'base.html') 
        self.assertTemplateUsed(test_response, 'disqus_snippet.html') 
        self.assertTemplateUsed(test_response, 'analytics_tracking.html')                        
        self.assertEqual(test_response.context['commentary'].pk, 1)
        self.assertEqual(test_response.context['commentary'].paper.__str__(), '14-3-3 proteins: a number of functions for a numbered protein.')  
        self.assertEqual(test_response.context['commentary'].comments, "some comments for this fixture")
        
        #verifies that a non-existent object returns a 404 error.
        null_response = self.client.get('/papers/commentary/9999', follow=True)
        self.assertEqual(null_response.status_code, 404) 
                 
    def test_commentary_view_create(self):
        """This tests the commentary-new view, ensuring that templates are loaded correctly.  

        This view uses a user with superuser permissions so does not test the permission levels for this view."""
        
        test_response = self.client.get('/papers/commentary/new', follow=True)
        self.assertEqual(test_response.status_code, 200)
        self.assertTemplateUsed(test_response, 'commentary-form.html')                             
        
    def test_commentary_view_edit(self):
        """This tests the commentary-edit view, ensuring that templates are loaded correctly.  

        This view uses a user with superuser permissions so does not test the permission levels for this view."""
        
        test_response = self.client.get('/papers/commentary/1/edit', follow=True)
        self.assertEqual(test_response.status_code, 200)
        self.assertTrue('commentary' in test_response.context)        
        self.assertTemplateUsed(test_response, 'commentary-form.html')                            
        self.assertEqual(test_response.context['commentary'].pk, 1)
        self.assertEqual(test_response.context['commentary'].paper.__str__(), '14-3-3 proteins: a number of functions for a numbered protein.')  
        self.assertEqual(test_response.context['commentary'].comments, "some comments for this fixture") 
        
        #verifies that a non-existent object returns a 404 error.
        null_response = self.client.get('/papers/commentary/9999/edit', follow=True)
        self.assertEqual(null_response.status_code, 404) 
        
    def test_commentary_view_delete(self):
        """This tests the commentary-delete view, ensuring that templates are loaded correctly.  

        This view uses a user with superuser permissions so does not test the permission levels for this view."""
        
        test_response = self.client.get('/papers/commentary/1/delete', follow=True)
        self.assertEqual(test_response.status_code, 200)
        self.assertTrue('object' in test_response.context)        
        self.assertTemplateUsed(test_response, 'base.html')
        self.assertTemplateUsed(test_response, 'confirm_delete.html')  
        
    def test_commentary_view_list(self):
        """This tests the commentary-list view, ensuring that templates are loaded correctly.  

        This view uses a user with superuser permissions so does not test the permission levels for this view."""
        
        test_response = self.client.get('/papers/commentaries', follow=True)
        self.assertEqual(test_response.status_code, 200)
        self.assertTrue('commentary_list' in test_response.context)        
        self.assertTemplateUsed(test_response, 'base.html')
        self.assertTemplateUsed(test_response, 'commentary-list.html')                                  
        self.assertTemplateUsed(test_response, 'analytics_tracking.html')  
        self.assertEqual(test_response.context['commentary_list'][0].pk, 1)
        self.assertEqual(test_response.context['commentary_list'][0].paper.__str__(), '14-3-3 proteins: a number of functions for a numbered protein.')  
        self.assertEqual(test_response.context['commentary_list'][0].comments, "some comments for this fixture") 

    def test_jc_view_list(self):
        """This tests the jc-list view, ensuring that templates are loaded correctly.  

        This view uses a user with superuser permissions so does not test the permission levels for this view."""
        
        test_response = self.client.get('/journal-club', follow=True)
        self.assertEqual(test_response.status_code, 200)
        self.assertTrue('journal_club_list' in test_response.context)        
        self.assertTemplateUsed(test_response, 'base.html')
        self.assertTemplateUsed(test_response, 'jc-list.html')                                  
        self.assertTemplateUsed(test_response, 'analytics_tracking.html')    

class PublicationSerializerTest(TestCase):
    """Test cases for Publication serializers."""

    fixtures = ['test_publication', 'test_publication_personnel']
    
    def setUp(self):
        """Set up test data."""
        self.publication = Publication.objects.create(
            title='Test Publication',
            abstract='This is a test abstract.',
            journal='Test Journal',
            year=2023,
            volume=10,
            issue=2,
            pages='123-456',
            type='journal-article',
            doi='10.1234/test.doi',
            pmid='12345678',
            preprint=False,
            laboratory_paper=True,
            interesting_paper=False,
        )
    
    def test_publication_serializer_fields(self):
        """Test PublicationSerializer includes all expected fields."""
        serializer = PublicationSerializer(self.publication)
        data = serializer.data
        
        expected_fields = [
            'id', 'title', 'title_slug', 'abstract', 'journal', 'year',
            'volume', 'issue', 'pages', 'type', 'doi', 'pmid', 'pmcid',
            'mendeley_id', 'mendeley_url', 'laboratory_paper',
            'interesting_paper', 'date_added', 'date_last_modified'
        ]
        
        for field in expected_fields:
            self.assertIn(field, data)
    
    def test_publication_list_serializer_excludes_abstract(self):
        """Test PublicationListSerializer excludes abstract field."""
        serializer = PublicationListSerializer(self.publication)
        data = serializer.data
        
        self.assertNotIn('abstract', data)
        self.assertIn('title', data)
        self.assertIn('journal', data)
    
    def test_serializer_read_only_fields(self):
        """Test that read-only fields cannot be modified."""
        serializer = PublicationSerializer(self.publication)
        
        # These fields should be read-only
        read_only_fields = ['id', 'title_slug', 'date_added', 'date_last_modified', 'absolute_url']
        
        for field in read_only_fields:
            self.assertIn(field, serializer.fields)
            self.assertTrue(serializer.fields[field].read_only)
    
    def test_serializer_validation(self):
        """Test serializer validation."""
        valid_data = {
            'title': 'New Publication',
            'journal': 'New Journal',
            'year': 2024,
            'type': 'journal-article',
            'preprint': 'False',
            'laboratory_paper':'True',
            'interesting_paper':'False',

        }
        
        serializer = PublicationSerializer(data=valid_data)
        self.assertTrue(serializer.is_valid())
    
    def test_serializer_invalid_year(self):
        """Test serializer with invalid year."""
        invalid_data = {
            'title': 'Invalid Publication',
            'year': 'not-a-year',
            'type': 'journal-article',
        }
        
        serializer = PublicationSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('year', serializer.errors)  

class PublicationViewSetTest(APITestCase):
    """Test cases for Publication API views."""

    fixtures = ['test_publication', 'test_publication_personnel']
    
    def setUp(self):
        """Set up test data."""
        self.publication1 = Publication.objects.create(
            title='First Publication',
            abstract='First abstract.',
            journal='Journal A',
            year=2023,
            type='journal-article',
            preprint=False,
            laboratory_paper=True,
            interesting_paper=False,
        )
        
        self.publication2 = Publication.objects.create(
            title='Second Publication',
            abstract='Second abstract.',
            journal='Journal B',
            year=2022,
            type='book-section',
            preprint=False,
            laboratory_paper=False,
            interesting_paper=True,
        )
    
    def test_list_publications(self):
        """Test listing all publications."""
        url = reverse('api-publication-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 4)
    
    def test_list_publications_json_format(self):
        """Test listing publications with JSON format."""
        url = reverse('api-publication-list')
        response = self.client.get(url, {'format': 'json'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['Content-Type'], 'application/json')
    
    def test_list_publications_xml_format(self):
        """Test listing publications with XML format."""
        url = reverse('api-publication-list')
        response = self.client.get(url, {'format': 'xml'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['Content-Type'], 'application/xml; charset=utf-8')
    
    def test_retrieve_single_publication(self):
        """Test retrieving a single publication."""
        url = reverse('api-publication-detail', kwargs={'pk': self.publication1.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'First Publication')
        self.assertIn('abstract', response.data)  # Full serializer includes abstract
    
    def test_filter_by_year(self):
        """Test filtering publications by year."""
        url = reverse('api-publication-list')
        response = self.client.get(url, {'year': 2023})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['year'], 2023)
    
    def test_filter_by_type(self):
        """Test filtering publications by type."""
        url = reverse('api-publication-list')
        response = self.client.get(url, {'type': 'journal-article'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3)
        self.assertEqual(response.data['results'][0]['type'], 'journal-article')
    
    def test_filter_by_laboratory_paper(self):
        """Test filtering publications by laboratory_paper flag."""
        url = reverse('api-publication-list')
        response = self.client.get(url, {'laboratory_paper': True})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        self.assertTrue(response.data['results'][0]['laboratory_paper'])
    
    def test_search_publications(self):
        """Test searching publications."""
        url = reverse('api-publication-list')
        response = self.client.get(url, {'search': 'First'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3)
        self.assertEqual(response.data['results'][0]['title'], 'First Publication')
    
    def test_get_publication_set(self):
        """Test retrieving multiple publications by IDs."""
        url = reverse('api-publication-get-set', kwargs={'ids': f'{self.publication1.pk},{self.publication2.pk}'})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(len(response.data['results']), 2)
    
    def test_get_publication_set_invalid_ids(self):
        """Test retrieving publications with invalid IDs."""
        url = '/api/v2/publications/set/invalid,ids/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Invalid ID format', response.data['error'])
    
    def test_laboratory_papers_endpoint(self):
        """Test laboratory papers endpoint."""
        url = reverse('api-publication-laboratory-papers')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        self.assertTrue(response.data['results'][0]['laboratory_paper'])
    
    def test_interesting_papers_endpoint(self):
        """Test interesting papers endpoint."""
        url = reverse('api-publication-interesting-papers')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        self.assertTrue(response.data['results'][0]['interesting_paper'])
    
    def test_ordering_by_year(self):
        """Test ordering publications by year."""
        url = reverse('api-publication-list')
        response = self.client.get(url, {'ordering': 'year'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        self.assertEqual(results[0]['year'], 1960)  # Earlier year first
        self.assertEqual(results[1]['year'], 2005)
    
    def test_pagination(self):
        """Test pagination works correctly."""
        # Create more publications to test pagination
        for i in range(25):
            Publication.objects.create(
                title=f'Publication {i}',
                year=2023,
                type='journal-article',
                preprint=False,
                laboratory_paper=False,
                interesting_paper=True,
            )
        
        url = reverse('api-publication-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 20)  # Page size
        self.assertIsNotNone(response.data['next'])  # Has next page  

class PublicationFilterTest(TestCase):
    """Test cases for Publication filters."""

    fixtures = ['test_publication', 'test_publication_personnel']
    
    def setUp(self):
        """Set up test data."""
        self.publication1 = Publication.objects.create(
            title='First Publication',
            journal='Nature',
            year=2023,
            type='journal-article',
            laboratory_paper=True,
            preprint=False,
            interesting_paper=False,
        )
        
        self.publication2 = Publication.objects.create(
            title='Second Publication',
            journal='Science',
            year=2022,
            type='book-section',
            laboratory_paper=False,
            preprint=False,
            interesting_paper=False,
        )
    
    def test_year_filter(self):
        """Test filtering by exact year."""
        filter_set = PublicationFilter(data={'year': 2023})
        queryset = filter_set.qs
        
        self.assertEqual(queryset.count(), 1)
        self.assertEqual(queryset.first().year, 2023)
    
    def test_year_range_filter(self):
        """Test filtering by year range."""
        filter_set = PublicationFilter(data={'year_after': 2022, 'year_before': 2023})
        queryset = filter_set.qs
        
        self.assertEqual(queryset.count(), 2)
    
    def test_type_filter(self):
        """Test filtering by publication type."""
        filter_set = PublicationFilter(data={'type': 'journal-article'})
        queryset = filter_set.qs
        
        self.assertEqual(queryset.count(), 3)
        self.assertEqual(queryset.first().type, 'journal-article')
    
    def test_laboratory_paper_filter(self):
        """Test filtering by laboratory_paper flag."""
        filter_set = PublicationFilter(data={'laboratory_paper': True})
        queryset = filter_set.qs
        
        self.assertEqual(queryset.count(), 2)
        self.assertTrue(queryset.first().laboratory_paper)
    
    def test_journal_filter(self):
        """Test filtering by journal name."""
        filter_set = PublicationFilter(data={'journal': 'Nature'})
        queryset = filter_set.qs
        
        self.assertEqual(queryset.count(), 1)
        self.assertEqual(queryset.first().journal, 'Nature')                     