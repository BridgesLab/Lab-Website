"""
This file contains the basic unit tests, which are imported into other apps.


"""

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User

from papers.models import Publication
from personnel.models import Person
from projects.models import Project
from lab_website.templatetags.shuffle import shuffle

MODELS = [Publication, Person, Project]

class BasicTests(TestCase):
    '''This class covers the setup and tear down for all unit tests'''

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
                
class HomeViewTests(BasicTests):
    '''This class tests the views associated with the :mod:`communication` app.'''
    
    fixtures = ['test_address','test_labaddress']
    
    def test_feed_details_view(self):
        """This tests the feed-details view, ensuring that templates are loaded correctly.  

        This view uses a user with superuser permissions so does not test the permission levels for this view."""

        test_response = self.client.get('/')
        self.assertEqual(test_response.status_code, 200)       
        self.assertTemplateUsed(test_response, 'index.html')
        self.assertTemplateUsed(test_response, 'base.html') 
        self.assertTemplateUsed(test_response, 'facebook_api_sdk_script.html') 
        self.assertTemplateUsed(test_response, 'job_posting_snippet.html') 
        self.assertTemplateUsed(test_response, 'analytics_tracking.html') 
         #check that context processors are being passed                       
        self.assertTrue('lab_name' in test_response.context)
        self.assertTrue('twitter' in test_response.context)
        self.assertTrue('google_plus' in test_response.context)
        self.assertTrue('facebook' in test_response.context)
        self.assertTrue('disqus_forum' in test_response.context)        
        self.assertTrue('fb_app_id' in test_response.context)
        self.assertTrue('fb_admins' in test_response.context)
        self.assertTrue('analytics_tracking' in test_response.context)        
        self.assertTrue('analytics_root' in test_response.context)


class PhotoViewTests(BasicTests):
    """Tests for the PhotoView."""

    fixtures = ['test_address', 'test_labaddress']

    def test_photo_view_returns_200(self):
        """Photo view returns a 200 response."""
        response = self.client.get('/lab-photos/')
        self.assertEqual(response.status_code, 200)

    def test_photo_view_uses_correct_template(self):
        """Photo view renders the lab_photos template."""
        response = self.client.get('/lab-photos/')
        self.assertTemplateUsed(response, 'lab_photos.html')

    def test_photo_view_context_has_photo_data(self):
        """Photo view context always contains photo_data key."""
        response = self.client.get('/lab-photos/')
        self.assertIn('photo_data', response.context)

    def test_photo_view_context_has_lab_name(self):
        """Photo view context contains lab_name."""
        response = self.client.get('/lab-photos/')
        self.assertIn('lab_name', response.context)

    def test_photo_data_is_dict_with_data_key(self):
        """photo_data in context is always a dict with a 'data' list (even on API failure)."""
        response = self.client.get('/lab-photos/')
        self.assertIn('data', response.context['photo_data'])
        self.assertIsInstance(response.context['photo_data']['data'], list)


class ShuffleFilterTests(TestCase):
    """Tests for the shuffle template filter."""

    def test_shuffle_returns_list(self):
        """shuffle filter returns a list."""
        result = shuffle([1, 2, 3, 4, 5])
        self.assertIsInstance(result, list)

    def test_shuffle_preserves_length(self):
        """shuffle filter returns a list of the same length."""
        original = [1, 2, 3, 4, 5]
        result = shuffle(original)
        self.assertEqual(len(result), len(original))

    def test_shuffle_preserves_elements(self):
        """shuffle filter returns all original elements."""
        original = [1, 2, 3, 4, 5]
        result = shuffle(original)
        self.assertEqual(sorted(result), sorted(original))

    def test_shuffle_does_not_mutate_input(self):
        """shuffle filter does not modify the original list."""
        original = [1, 2, 3, 4, 5]
        original_copy = original[:]
        shuffle(original)
        self.assertEqual(original, original_copy)

    def test_shuffle_works_with_empty_list(self):
        """shuffle filter handles an empty list."""
        result = shuffle([])
        self.assertEqual(result, [])

    def test_shuffle_works_with_queryset(self):
        """shuffle filter works with a Django queryset (converts to list)."""
        result = shuffle(Publication.objects.all())
        self.assertIsInstance(result, list)

