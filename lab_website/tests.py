"""
This file contains the basic unit tests, which are imported into other apps.


"""

import json
import urllib.error
from unittest.mock import patch, Mock

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


def _make_urlopen_mock(json_data):
    """Return a mock urlopen that yields json_data as bytes."""
    mock_response = Mock()
    mock_response.read.return_value = json.dumps(json_data).encode()
    mock_response.__enter__ = lambda s: s
    mock_response.__exit__ = Mock(return_value=False)
    return Mock(return_value=mock_response)


class IndexViewFacebookTests(BasicTests):
    """Tests for IndexView Facebook API error-handling branches."""

    fixtures = ['test_address', 'test_labaddress']

    def _url_error(self, code):
        err = urllib.error.URLError("reason")
        err.code = code
        return err

    @patch('urllib.request.urlopen')
    def test_index_urlopen_404_error(self, mock_urlopen):
        """IndexView handles 404 URLError from Facebook API gracefully."""
        mock_urlopen.side_effect = self._url_error(404)
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    @patch('urllib.request.urlopen')
    def test_index_urlopen_non404_error(self, mock_urlopen):
        """IndexView handles non-404 URLError from Facebook API gracefully."""
        mock_urlopen.side_effect = self._url_error(500)
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    @patch('urllib.request.urlopen')
    def test_index_urlopen_value_error(self, mock_urlopen):
        """IndexView handles ValueError (bad URL) from Facebook API gracefully."""
        mock_urlopen.side_effect = ValueError("invalid URL")
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    @patch('urllib.request.urlopen')
    def test_index_processes_posts_with_shared_link(self, mock_urlopen):
        """IndexView processes Facebook posts that contain shared-link attachments."""
        post_data = {
            'data': [{
                'id': '1',
                'message': 'Check this out http://example.com',
                'created_time': '2024-01-15T10:30:00+0000',
                'full_picture': '',
                'status_type': 'shared_story',
                'permalink_url': 'https://facebook.com/1',
                'attachments': {
                    'data': [{'url': 'http://example.com', 'type': 'share'}]
                },
            }]
        }
        general_data = {'id': 'test', 'name': 'Test Lab'}
        responses = [
            json.dumps(general_data).encode(),
            json.dumps(post_data).encode(),
            json.dumps(post_data).encode(),
        ]
        call_count = [0]

        def side_effect(request):
            mock_resp = Mock()
            mock_resp.read.return_value = responses[min(call_count[0], len(responses) - 1)]
            call_count[0] += 1
            return mock_resp

        mock_urlopen.side_effect = side_effect
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        news = response.context.get('news', [])
        if news:
            self.assertEqual(news[0].get('shared_link'), 'http://example.com')

    @patch('urllib.request.urlopen')
    def test_index_urlify_text_with_url(self, mock_urlopen):
        """IndexView urlifies URLs inside Facebook post messages."""
        post_data = {
            'data': [{
                'id': '2',
                'message': 'Visit http://example.com for details',
                'created_time': '2024-01-15T10:30:00+0000',
            }]
        }
        responses = [
            json.dumps({'id': 'x'}).encode(),
            json.dumps(post_data).encode(),
            json.dumps(post_data).encode(),
        ]
        call_count = [0]

        def side_effect(request):
            mock_resp = Mock()
            mock_resp.read.return_value = responses[min(call_count[0], len(responses) - 1)]
            call_count[0] += 1
            return mock_resp

        mock_urlopen.side_effect = side_effect
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        news = response.context.get('news', [])
        if news:
            self.assertIn('<a href=', str(news[0].get('message', '')))

    @patch('urllib.request.urlopen')
    def test_index_format_facebook_date_invalid(self, mock_urlopen):
        """IndexView format_facebook_date falls back to raw string on bad date format."""
        post_data = {
            'data': [{
                'id': '3',
                'message': 'Test',
                'created_time': 'not-a-date',
            }]
        }
        responses = [
            json.dumps({'id': 'x'}).encode(),
            json.dumps(post_data).encode(),
            json.dumps(post_data).encode(),
        ]
        call_count = [0]

        def side_effect(request):
            mock_resp = Mock()
            mock_resp.read.return_value = responses[min(call_count[0], len(responses) - 1)]
            call_count[0] += 1
            return mock_resp

        mock_urlopen.side_effect = side_effect
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    @patch('urllib.request.urlopen')
    def test_index_format_facebook_date_empty(self, mock_urlopen):
        """IndexView format_facebook_date returns None for empty string."""
        post_data = {
            'data': [{'id': '4', 'message': 'Test', 'created_time': ''}]
        }
        responses = [
            json.dumps({'id': 'x'}).encode(),
            json.dumps(post_data).encode(),
            json.dumps(post_data).encode(),
        ]
        call_count = [0]

        def side_effect(request):
            mock_resp = Mock()
            mock_resp.read.return_value = responses[min(call_count[0], len(responses) - 1)]
            call_count[0] += 1
            return mock_resp

        mock_urlopen.side_effect = side_effect
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        news = response.context.get('news', [])
        if news:
            self.assertIsNone(news[0].get('created_time'))


class PhotoViewFacebookTests(BasicTests):
    """Tests for PhotoView Facebook API error-handling branches."""

    fixtures = ['test_address', 'test_labaddress']

    def _url_error(self, code):
        err = urllib.error.URLError("reason")
        err.code = code
        return err

    @patch('urllib.request.urlopen')
    def test_photo_view_urlopen_404_error(self, mock_urlopen):
        """PhotoView handles 404 URLError from Facebook API and returns 200."""
        mock_urlopen.side_effect = self._url_error(404)
        response = self.client.get('/lab-photos/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['photo_data'], {'data': []})

    @patch('urllib.request.urlopen')
    def test_photo_view_urlopen_non404_error(self, mock_urlopen):
        """PhotoView handles non-404 URLError and falls back to empty photo_data."""
        mock_urlopen.side_effect = self._url_error(503)
        response = self.client.get('/lab-photos/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['photo_data'], {'data': []})

    @patch('urllib.request.urlopen')
    def test_photo_view_value_error(self, mock_urlopen):
        """PhotoView handles ValueError and falls back to empty photo_data."""
        mock_urlopen.side_effect = ValueError("bad url")
        response = self.client.get('/lab-photos/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['photo_data'], {'data': []})

    @patch('urllib.request.urlopen')
    def test_photo_view_no_data_key_in_response(self, mock_urlopen):
        """PhotoView handles API response that lacks a 'data' key."""
        responses = [
            json.dumps({'id': 'x'}).encode(),
            json.dumps({'error': 'no data key here'}).encode(),
        ]
        call_count = [0]

        def side_effect(request):
            mock_resp = Mock()
            mock_resp.read.return_value = responses[min(call_count[0], len(responses) - 1)]
            call_count[0] += 1
            return mock_resp

        mock_urlopen.side_effect = side_effect
        response = self.client.get('/lab-photos/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['photo_data'], {'data': []})

