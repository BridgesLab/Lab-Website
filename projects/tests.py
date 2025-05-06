"""
This package contains the unit tests for the :mod:`projects` app.

It contains view and model tests for each model, grouped together.
Contains the one model tests:

* :class:`~papers.tests.ProjectModelTests` 

The API tests:

* :class:`~PublicationResourceTests`

And the view tests:

* :class:`~papers.tests.ProjectViewTests` 
"""

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User

from projects.models import Project, Funding, FundingAgency

MODELS = [Project, Funding]

class ProjectModelTests(TestCase):
    '''This class tests various aspects of the :class:`~papers.models.Publication` model.'''
    
    fixtures = ['test_project', ]

    def setUp(self):
        '''Instantiate the test client.  Creates a test user.'''
        self.client = Client()
        self.test_user = User.objects.create_user('testuser', 'blah@blah.com', 'testpassword')
        self.test_user.is_superuser = True
        self.test_user.is_active = True
        self.test_user.save()
        self.assertEqual(self.test_user.is_superuser, True)
        login = self.client.login(username='testuser', password='testpassword')
        self.failUnless(login, 'Could not log in')
    
    def tearDown(self):
        '''Depopulate created model instances from test database.'''
        for model in MODELS:
            for obj in model.objects.all():
                obj.delete()
                
    def test_create_new_project_minimum(self):
        '''This test creates a :class:`~projects.models.Project` with the required information only.'''
        test_project = Project(title='Test Project.')
        test_project.save()
        self.assertEqual(test_project.pk, 2)
        
    def test_create_new_project_all(self):
        '''This test creates a `:class:~projects.models.Project` with the required information only.'''
        test_project = Project(title='Test Project') #add more fields
        test_project.save()        
        
    def test_project_unicode(self):
        '''This tests the unicode representation of a :class:`~projects.models.Project`.'''
        test_project = Project.objects.get(title_slug='fixture-project')
        self.assertEqual(test_project.__unicode__(), "Fixture Project")
        
    def test_project_title_slug(self):
        '''This tests the title_slug field of a :class:`~projects.models.Project`.'''
        test_project = Project(title='Test Project.')
        test_project.save()
        self.assertEqual(test_project.title_slug, "test-project")  
        
    def test_project_absolute_url(self):
        '''This tests the title_slug field of a :class:`~projects.models.Project`.'''
        test_project = Project(title='Test Project')
        test_project.save()
        self.assertEqual(test_project.get_absolute_url(), "/projects/test-project") 
                                  
class ProjectResourceTests(TestCase):  
    '''This class tests varios aspects of the :class:`~projects.api.ProjectResource` API model.'''

    fixtures = ['test_project', ]

    def setUp(self):
        '''Instantiate the test client.  Creates a test user.'''
        self.client = Client()
        self.test_user = User.objects.create_user('testuser', 'blah@blah.com', 'testpassword')
        self.test_user.is_superuser = True
        self.test_user.is_active = True
        self.test_user.save()
        self.assertEqual(self.test_user.is_superuser, True)
        login = self.client.login(username='testuser', password='testpassword')
        self.failUnless(login, 'Could not log in')
    
    def tearDown(self):
        '''Depopulate created model instances from test database.'''
        for model in MODELS:
            for obj in model.objects.all():
                obj.delete()
                
    def api_project_list_test(self):
        '''This tests that the API correctly renders a list of :class:`~projects.models.Project` objects.'''
        response = self.client.get('/api/v1/projects/?format=json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json; charset=utf-8')
        
    def api_project_detail_test(self):
        '''This tests that the API correctly renders a particular :class:`~projects.models.Project` objects.'''
        response = self.client.get('/api/v1/projects/1/?format=json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json; charset=utf-8')     
       
class ProjectViewTests(TestCase):
    '''This class tests the views for :class:`~project.models.Project` objects.'''

    fixtures = ['test_project',]

    def setUp(self):
        """Instantiate the test client.  Creates a test user."""
        self.client = Client()
        self.test_user = User.objects.create_user('testuser', 'blah@blah.com', 'testpassword')
        self.test_user.is_superuser = True
        self.test_user.is_active = True
        self.test_user.save()
        self.assertEqual(self.test_user.is_superuser, True)
        login = self.client.login(username='testuser', password='testpassword')
        self.failUnless(login, 'Could not log in')

    def tearDown(self):
        """Depopulate created model instances from test database."""
        for model in MODELS:
            for obj in model.objects.all():
                obj.delete()

    def test_project_view(self):
        """This tests the project-details view, ensuring that templates are loaded correctly.  

        This view uses a user with superuser permissions so does not test the permission levels for this view."""
        
        test_response = self.client.get('/projects/fixture-project')
        self.assertEqual(test_response.status_code, 200)
        self.assertTrue('project' in test_response.context)        
        self.assertTemplateUsed(test_response, 'project_detail.html')
        self.assertTemplateUsed(test_response, 'base.html') 
        self.assertTemplateUsed(test_response, 'disqus_snippet.html')                         
        self.assertEqual(test_response.context['project'].pk, 1)
        self.assertEqual(test_response.context['project'].title, u'Fixture Project')
        
    def test_project_list(self):
        """This tests the project-list view ensuring that templates are loaded correctly.
        
        This view uses a user with superuser permissions so does not test the permission levels for this view."""
        
        test_response = self.client.get('/projects/')
        self.assertEqual(test_response.status_code, 200)
        self.assertTrue('project_list' in test_response.context)        
        self.assertTemplateUsed(test_response, 'project_list.html')
        self.assertTemplateUsed(test_response, 'base.html') 
        self.assertEqual(test_response.context['project_list'][0].pk, 1)
        self.assertEqual(test_response.context['project_list'][0].title, u'Fixture Project')  
        
    def test_project_view_create(self):
        """This tests the project-new view, ensuring that templates are loaded correctly.  

        This view uses a user with superuser permissions so does not test the permission levels for this view."""
        
        test_response = self.client.get('/projects/new')
        self.assertEqual(test_response.status_code, 200)
        self.assertTemplateUsed(test_response, 'base.html')
        self.assertTemplateUsed(test_response, 'project_form.html')          

    def test_project_view_edit(self):
        """This tests the project-edit view, ensuring that templates are loaded correctly.  

        This view uses a user with superuser permissions so does not test the permission levels for this view."""
        
        test_response = self.client.get('/projects/fixture-project/edit')
        self.assertEqual(test_response.status_code, 200)
        self.assertTrue('project' in test_response.context)        
        self.assertTemplateUsed(test_response, 'base.html')
        self.assertTemplateUsed(test_response, 'project_form.html')       
        self.assertEqual(test_response.context['project'].pk, 1)
        self.assertEqual(test_response.context['project'].title, u'Fixture Project')

        #verifies that a non-existent object returns a 404 error presuming there is no object with pk=2.
        null_response = self.client.get('/projects/not-a-real-paper/edit')
        self.assertEqual(null_response.status_code, 404)   

    def test_project_view_delete(self):
        """This tests the project-delete view, ensuring that templates are loaded correctly.  

        This view uses a user with superuser permissions so does not test the permission levels for this view."""
        
        test_response = self.client.get('/projects/fixture-project/delete')
        self.assertEqual(test_response.status_code, 200)
        self.assertTrue('project' in test_response.context)        
        self.assertTemplateUsed(test_response, 'confirm_delete.html')
        self.assertEqual(test_response.context['project'].pk, 1)
        self.assertEqual(test_response.context['project'].title, u'Fixture Project')

        #verifies that a non-existent object returns a 404 error.
        null_response = self.client.get('/projects/not-a-real-paper/delete')
        self.assertEqual(null_response.status_code, 404)           

class FundingModelTests(TestCase):
    '''This class tests various aspects of the :class:`~projects.models.Funding` model.'''
    
    fixtures = ['test_funding', 'test_funding_agency']

    def setUp(self):
        '''Instantiate the test client.  Creates a test user.'''
        self.client = Client()
        self.test_user = User.objects.create_user('testuser', 'blah@blah.com', 'testpassword')
        self.test_user.is_superuser = True
        self.test_user.is_active = True
        self.test_user.save()
        self.assertEqual(self.test_user.is_superuser, True)
        login = self.client.login(username='testuser', password='testpassword')
        self.failUnless(login, 'Could not log in')
    
    def tearDown(self):
        '''Depopulate created model instances from test database.'''
        for model in MODELS:
            for obj in model.objects.all():
                obj.delete()
                
    def test_create_new_funding_minimum(self):
        '''This test creates a :class:`~projects.models.Funding` with the required information only.'''
        test_funding = Funding(title='Test Funding.', active=True)
        test_funding.save()
        self.assertEqual(test_funding.pk, 2)
        
    def test_create_new_funding_agency(self):
        '''This test creates a :class:`~projects.models.FundingAgency` with the required information only.'''
        test_funding_agency = FundingAgency(name='Test Agency')
        test_funding_agency.save()
        self.assertEqual(test_funding_agency.pk, 2)    
        
    def test_create_new_funding_all(self):
        '''This test creates a `:class:~projects.models.Funding` with the required information only.'''
        test_funding = Funding(title='Test Funding', active=True) #add more fields
        test_funding.save()        
        
    def test_funding_unicode(self):
        '''This tests the unicode representation of a :class:`~projects.models.Funding`.'''
        test_funding = Funding.objects.get(title_slug='fixture-funding')
        self.assertEqual(test_funding.__unicode__(), "Fixture Funding")
        
    def test_funding_title_slug(self):
        '''This tests the title_slug field of a :class:`~projects.models.Funding`.'''
        test_funding = Funding(title='Test Funding.', active=True)
        test_funding.save()
        self.assertEqual(test_funding.title_slug, "test-funding")  
        
    def test_funding_absolute_url(self):
        '''This tests the title_slug field of a :class:`~projects.models.Funding`.'''
        test_funding = Funding(title='Test Funding', active=True)
        test_funding.save()
        self.assertEqual(test_funding.get_absolute_url(), "/funding/test-funding") 
        
class FundingViewTests(TestCase):
    '''This class tests the views for :class:`~project.models.Funding` objects.'''

    fixtures = ['test_funding',]

    def setUp(self):
        """Instantiate the test client.  Creates a test user."""
        self.client = Client()
        self.test_user = User.objects.create_user('testuser', 'blah@blah.com', 'testpassword')
        self.test_user.is_superuser = True
        self.test_user.is_active = True
        self.test_user.save()
        self.assertEqual(self.test_user.is_superuser, True)
        login = self.client.login(username='testuser', password='testpassword')
        self.failUnless(login, 'Could not log in')

    def tearDown(self):
        """Depopulate created model instances from test database."""
        for model in MODELS:
            for obj in model.objects.all():
                obj.delete()

    def test_funding_view(self):
        """This tests the funding-details view, ensuring that templates are loaded correctly.  

        This view uses a user with superuser permissions so does not test the permission levels for this view."""
        
        test_response = self.client.get('/funding/fixture-funding')
        self.assertEqual(test_response.status_code, 200)
        self.assertTrue('funding' in test_response.context)        
        self.assertTemplateUsed(test_response, 'funding_detail.html')
        self.assertTemplateUsed(test_response, 'base.html') 
        self.assertTemplateUsed(test_response, 'disqus_snippet.html')                         
        self.assertEqual(test_response.context['funding'].pk, 1)
        self.assertEqual(test_response.context['funding'].title, u'Fixture Funding')
        
    def test_funding_list(self):
        """This tests the funding-list view ensuring that templates are loaded correctly.
        
        This view uses a user with superuser permissions so does not test the permission levels for this view."""
        
        test_response = self.client.get('/funding/')
        self.assertEqual(test_response.status_code, 200)
        self.assertTrue('funding_list' in test_response.context)        
        self.assertTemplateUsed(test_response, 'funding_list.html')
        self.assertTemplateUsed(test_response, 'base.html') 
        self.assertEqual(test_response.context['funding_list'][0].pk, 1)
        self.assertEqual(test_response.context['funding_list'][0].title, u'Fixture Funding')  
        
    def test_funding_view_create(self):
        """This tests the funding-new view, ensuring that templates are loaded correctly.  

        This view uses a user with superuser permissions so does not test the permission levels for this view."""
        
        test_response = self.client.get('/funding/new')
        self.assertEqual(test_response.status_code, 200)
        self.assertTemplateUsed(test_response, 'base.html')
        self.assertTemplateUsed(test_response, 'funding_form.html')          

    def test_publication_view_edit(self):
        """This tests the funding-edit view, ensuring that templates are loaded correctly.  

        This view uses a user with superuser permissions so does not test the permission levels for this view."""
        
        test_response = self.client.get('/funding/fixture-funding/edit')
        self.assertEqual(test_response.status_code, 200)
        self.assertTrue('funding' in test_response.context)        
        self.assertTemplateUsed(test_response, 'base.html')
        self.assertTemplateUsed(test_response, 'funding_form.html')       
        self.assertEqual(test_response.context['funding'].pk, 1)
        self.assertEqual(test_response.context['funding'].title, u'Fixture Funding')

        #verifies that a non-existent object returns a 404 error presuming there is no object with pk=2.
        null_response = self.client.get('/funding/not-a-real-funding/edit/')
        self.assertEqual(null_response.status_code, 404)   

    def test_funding_view_delete(self):
        """This tests the funding-delete view, ensuring that templates are loaded correctly.  

        This view uses a user with superuser permissions so does not test the permission levels for this view."""
        
        test_response = self.client.get('/funding/fixture-funding/delete')
        self.assertEqual(test_response.status_code, 200)
        self.assertTrue('funding' in test_response.context)        
        self.assertTemplateUsed(test_response, 'confirm_delete.html')
        self.assertEqual(test_response.context['funding'].pk, 1)
        self.assertEqual(test_response.context['funding'].title, u'Fixture Funding')

        #verifies that a non-existent object returns a 404 error.
        null_response = self.client.get('/funding/not-a-real-funding/delete/')
        self.assertEqual(null_response.status_code, 404)                   