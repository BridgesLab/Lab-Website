"""
This file contains the unit tests for the :mod:`communication` app.

Since this app has no models there is model and view tests:

* :class:`~communication.tests.CommunicationModelTests`
* :class:`~communication.tests.CommunicationViewTests` 

"""
import urllib.error
from unittest.mock import patch, Mock

from django.urls import reverse

from lab_website.tests import BasicTests

from communication.models import LabAddress, LabLocation, Post
from communication.sitemap import PostsSitemap
from communication.views import generate_twitter_timeline

from personnel.models import Address, Person
from papers.models import Publication
from projects.models import Project

class CommunicationModelTests(BasicTests):
    '''This class tests the views associated with models in the :mod:`communication` app.'''
    
    fixtures = ['test_address',]
    
    def test_create_new_lab_address(self):
        '''This test creates a :class:`~communication.models.LabAddress` with the required information.'''
 
        test_address = LabAddress(type='Primary', address=Address.objects.get(pk=1)) #repeat for all required fields
        test_address.save()
        self.assertEqual(test_address.pk, 1) #presumes no models loaded in fixture data     
        
    def test_lab_address_string(self):
        '''This tests the string representation of a :class:`~communication.models.LabAddress`.'''
 
        test_address = LabAddress(type='Primary', address=Address.objects.get(pk=1)) #repeat for all required fields
        test_address.save()
        self.assertEqual(test_address.pk, 1) #presumes no models loaded in fixture data  
        self.assertEqual(str(test_address), Address.objects.get(pk=1).__str__())
        
    def test_create_new_lab_location(self):
        '''This test creates a :class:`~communication.models.LabLocation` with the required information only.'''
 
        test_location = LabLocation(name = 'Memphis', 
            type='City', 
            priority=1) #repeat for all required fields
        test_location.save()
        self.assertEqual(test_location.pk, 1) #presumes no models loaded in fixture data         

    def test_create_new_lab_location_all(self):
        '''This test creates a :class:`~communication.models.LabLocation` with all fields included.'''
 
        test_location = LabLocation(name = 'Memphis', 
            type='City', 
            priority=1,
            address=Address.objects.get(pk=1),
            url = 'www.cityofmemphis.org',
            description = 'some description about the place',
            lattitude = 35.149534,
            longitude = -90.04898,) #repeat for all required fields
        test_location.save()
        self.assertEqual(test_location.pk, 1) #presumes no models loaded in fixture data
        
    def test_lab_location_string(self):
        '''This test creates a :class:`~communication.models.LabLocation` with the required information only.'''
 
        test_location = LabLocation(name = 'Memphis', 
            type='City', 
            priority=1) #repeat for all required fields
        test_location.save()
        self.assertEqual(test_location.pk, 1)
        self.assertEqual(str(test_location), 'Memphis') 

class CommunicationViewTests(BasicTests):
    '''This class tests the views associated with the :mod:`communication` app.'''
    
    
    def test_feed_details_view(self):
        """This tests the feed-details view, ensuring that templates are loaded correctly.  

        This view uses a user with superuser permissions so does not test the permission levels for this view."""
        
        test_response = self.client.get('/feeds', follow=True)
        self.assertEqual(test_response.status_code, 200)       
        self.assertTemplateUsed(test_response, 'feed_details.html')
        self.assertTemplateUsed(test_response, 'base.html') 
        self.assertTrue('google_calendar_id' in test_response.context)          
        
    def test_lab_rules_view(self):
        '''This tests the lab-rules view.
        
        The tests ensure that the correct template is used.
        It also tests whether the correct context is passed (if included).
        his view uses a user with superuser permissions so does not test the permission levels for this view.'''
        
        test_response = self.client.get('/lab-rules', follow=True)
        self.assertEqual(test_response.status_code, 200)       
        self.assertTemplateUsed(test_response, 'lab_rules.html')
        self.assertTemplateUsed(test_response, 'base.html') 
        self.assertTrue('lab_rules' in test_response.context)    
        self.assertTrue('lab_rules_source' in test_response.context)    

    def test_lab_rules_view(self):
        '''This tests the data-resource-sharing view.
        
        The tests ensure that the correct template is used.
        It also tests whether the correct context is passed (if included).
        his view uses a user with superuser permissions so does not test the permission levels for this view.'''
        
        test_response = self.client.get('/data-resource-sharing', follow=True)
        self.assertEqual(test_response.status_code, 200)       
        self.assertTemplateUsed(test_response, 'data_sharing_policy.html')
        self.assertTemplateUsed(test_response, 'base.html') 
        self.assertTrue('data_sharing_policy' in test_response.context)    
        self.assertTrue('data_sharing_policy_source' in test_response.context)
        
    def test_twitter_view(self):
        '''This tests the twitter view.
        
        Currently it just ensures that the template is loading correctly.
        '''
        test_response = self.client.get('/twitter', follow=True)
        self.assertEqual(test_response.status_code, 200)       
        self.assertTemplateUsed(test_response, 'twitter_timeline.html')
        self.assertTemplateUsed(test_response, 'base.html') 
        self.assertTrue('timeline' in test_response.context)         
        
        
    def test_calendar_view(self):
        '''This tests the google-calendar view.
        
        Currently it just ensures that the template is loading correctly.
        '''
        test_response = self.client.get('/calendar', follow=True)
        self.assertEqual(test_response.status_code, 200)       
        self.assertTemplateUsed(test_response, 'calendar.html')
        self.assertTemplateUsed(test_response, 'base.html') 
        self.assertTrue('google_calendar_id' in test_response.context)                    
                                
#         
#     def test_wikipedia_view(self):
#         '''This tests the google-calendar view.
#         
#         Currently it just ensures that the template is loading correctly.
#         '''
#         test_response = self.client.get('/wikipedia', follow=True)
#         self.assertEqual(test_response.status_code, 200)       
#         self.assertTemplateUsed(test_response, 'wikipedia_edits.html')
#         self.assertTemplateUsed(test_response, 'base.html') 
#         self.assertTemplateUsed(test_response, 'jquery_script.html') 
#         self.assertTrue('pages' in test_response.context)                                 
                                
    def test_news_view(self):
        '''This tests the lab-news view.
        
        Currently it just ensures that the template is loading correctly.
        '''
        test_response = self.client.get('/news', follow=True)
        self.assertEqual(test_response.status_code, 200)       
        self.assertTemplateUsed(test_response, 'lab_news.html')
        self.assertTemplateUsed(test_response, 'base.html') 
        #self.assertTrue('statuses' in test_response.context) 
        self.assertTrue('links' in test_response.context)           
        #self.assertTrue('milestones' in test_response.context) 
        
    def test_contact_page(self):
        '''This tests the contact-page view.
        
        Currently it just ensures that the template is loading correctly.
        '''
        test_response = self.client.get('/contact/', follow=True)
        self.assertEqual(test_response.status_code, 200)       
        self.assertTemplateUsed(test_response, 'contact.html')
        self.assertTemplateUsed(test_response, 'base.html') 
        
    def test_location_page(self):
        '''This tests the location view.
        
        Currently it ensures that the template is loading, and that that the location_list context is passed.
        ''' 
        test_response = self.client.get('/location', follow=True)
        self.assertEqual(test_response.status_code, 200)       
        self.assertTemplateUsed(test_response, 'location.html')
        self.assertTemplateUsed(test_response, 'base.html') 
        self.assertTrue('lablocation_list' in test_response.context)  
        
class PostModelTests(BasicTests):
    '''This class tests various aspects of the :class:`~papers.models.Post` model.'''
    
    fixtures = ['test_publication','test_publication_personnel', 'test_project', 'test_personnel']   
                
    def test_create_new_post_minimum(self):
        '''This test creates a :class:`~papers.models.Post` with the required information only.'''
        
        test_post = Post(post_title="Test Post",
        author = Person.objects.get(pk=1),
        markdown_url = 'https://raw.githubusercontent.com/BridgesLab/Lab-Website/master/LICENSE.md')
        test_post.save()
        self.assertEqual(test_post.pk, 1) 
        
    def test_create_new_post_all(self):
        '''This test creates a :class:`~papers.models.Post` with all fields entered.'''
        
        test_post = Post(post_title="Test Post",
            author = Person.objects.get(pk=1),
            markdown_url = 'https://raw.githubusercontent.com/BridgesLab/Lab-Website/master/LICENSE.md',
            paper = Publication.objects.get(pk=1),
            project = Project.objects.get(pk=1))
        test_post.save()
        self.assertEqual(test_post.pk, 1) 
        
    def test_post_string(self):
        '''This test creates a :class:`~papers.models.Post` and then verifies the string representation is correct.'''
        
        test_post = Post(post_title="Test Post",
            author = Person.objects.get(pk=1),
            markdown_url = 'https://raw.githubusercontent.com/BridgesLab/Lab-Website/master/LICENSE.md')
        test_post.save()
        self.assertEqual(str(test_post), "Test Post")  
        
    def test_post_slugify(self):
        '''This test creates a :class:`~papers.models.Post` and then verifies the slug representation is correct.'''
        
        test_post = Post(post_title="Test Post",
            author = Person.objects.get(pk=1),
            markdown_url = 'https://raw.githubusercontent.com/BridgesLab/Lab-Website/master/LICENSE.md')
        test_post.save()   
        self.assertEqual(test_post.post_slug, "test-post")  

    def test_get_absolute_url(self):
        """Test the get_absolute_url method"""
        test_post = Post(post_title="Test Post",
            author = Person.objects.get(pk=1),
            markdown_url = 'https://raw.githubusercontent.com/BridgesLab/Lab-Website/master/LICENSE.md')
        test_post.save() 
        expected_url = reverse('post-details', args=[test_post.post_slug])
        self.assertEqual(test_post.get_absolute_url(), expected_url) 
      
class PostViewTests(BasicTests):
    '''These test the views associated with post objects.'''
    
    fixtures = ['test_post','test_publication','test_publication_personnel', 'test_project', 'test_personnel']   
    
    def test_post_details_view(self):
        """This tests the post-details view, ensuring that templates are loaded correctly.  

        This view uses a user with superuser permissions so does not test the permission levels for this view."""
        
        test_response = self.client.get('/posts/fixture-post', follow=True)
        self.assertEqual(test_response.status_code, 200)       
        self.assertTemplateUsed(test_response, 'post_detail.html')
        self.assertTemplateUsed(test_response, 'base.html') 
        self.assertTemplateUsed(test_response, 'analytics_tracking.html')
        self.assertTrue('post' in test_response.context)  
        
        test_response = self.client.get('/posts/not-a-fixture-post', follow=True) 
        self.assertEqual(test_response.status_code, 404)          
        
    def test_post_list(self):
        """This tests the post-list view, ensuring that templates are loaded correctly.  

        This view uses a user with superuser permissions so does not test the permission levels for this view."""
        
        test_response = self.client.get('/posts/', follow=True)
        self.assertEqual(test_response.status_code, 200)       
        self.assertTemplateUsed(test_response, 'post_list.html')
        self.assertTemplateUsed(test_response, 'base.html') 
        self.assertTemplateUsed(test_response, 'analytics_tracking.html')
        self.assertTrue('post_list' in test_response.context)
        
    def test_post_new(self):
        """This tests the post-new view, ensuring that templates are loaded correctly.  

        This view uses a user with superuser permissions so does not test the permission levels for this view."""
        
        test_response = self.client.get('/posts/new', follow=True)
        self.assertEqual(test_response.status_code, 200)       
        self.assertTemplateUsed(test_response, 'post_form.html')
        
    def test_post_edit(self):
        """This tests the post-edit view, ensuring that templates are loaded correctly.  

        This view uses a user with superuser permissions so does not test the permission levels for this view."""
        
        test_response = self.client.get('/posts/fixture-post/edit', follow=True)
        self.assertEqual(test_response.status_code, 200)       
        self.assertTemplateUsed(test_response, 'post_form.html')
        
        test_response = self.client.get('/posts/not-a-fixture-post/edit', follow=True) 
        self.assertEqual(test_response.status_code, 404)                      
                                                                               
    def test_post_delete(self):
        """This tests the post-edit view, ensuring that templates are loaded correctly.  

        This view uses a user with superuser permissions so does not test the permission levels for this view."""
        
        test_response = self.client.get('/posts/fixture-post/delete', follow=True)
        self.assertEqual(test_response.status_code, 200)       
        self.assertTemplateUsed(test_response, 'confirm_delete.html')
        self.assertTemplateUsed(test_response, 'base.html')                                                          

        test_response = self.client.get('/posts/not-a-fixture-post/delete', follow=True)
        self.assertEqual(test_response.status_code, 404)


class PostsFeedTests(BasicTests):
    """Tests for the PostsFeed RSS feed."""

    fixtures = ['test_post', 'test_publication', 'test_publication_personnel', 'test_project', 'test_personnel']

    def setUp(self):
        super().setUp()
        from datetime import date
        author = Person.objects.get(pk=1)
        self.modified_post = Post.objects.create(
            post_title='Modified Post',
            author=author,
            markdown_url='http://example.com/post.md',
            modified=date.today(),
        )

    def test_posts_feed_returns_200(self):
        """Posts feed URL returns a valid RSS response."""
        response = self.client.get('/feeds/posts/')
        self.assertEqual(response.status_code, 200)

    def test_posts_feed_is_xml(self):
        """Posts feed response is RSS/XML."""
        response = self.client.get('/feeds/posts/')
        self.assertIn('xml', response['Content-Type'])

    def test_posts_feed_contains_fixture_post(self):
        """Posts feed contains the fixture post title."""
        response = self.client.get('/feeds/posts/')
        self.assertContains(response, 'Fixture Post')

    def test_posts_feed_contains_author(self):
        """Posts feed contains the post author."""
        response = self.client.get('/feeds/posts/')
        post = Post.objects.get(post_slug='fixture-post')
        self.assertContains(response, str(post.author))

    def test_posts_feed_item_updateddate_when_modified_set(self):
        """Posts feed renders correctly when a post has a modified date."""
        response = self.client.get('/feeds/posts/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Modified Post')


class PostsSitemapTests(BasicTests):
    """Tests for the PostsSitemap."""

    fixtures = ['test_post', 'test_publication', 'test_publication_personnel', 'test_project', 'test_personnel']

    def test_sitemap_items_returns_all_posts(self):
        """PostsSitemap.items() returns all Post objects."""
        sitemap = PostsSitemap()
        self.assertEqual(list(sitemap.items()), list(Post.objects.all()))

    def test_sitemap_lastmod_returns_modified_when_set(self):
        """PostsSitemap.lastmod() returns modified when it is not None."""
        from datetime import date
        post = Post.objects.get(post_slug='fixture-post')
        post.modified = date.today()
        sitemap = PostsSitemap()
        self.assertEqual(sitemap.lastmod(post), post.modified)

    def test_sitemap_lastmod_falls_back_to_created(self):
        """PostsSitemap.lastmod() falls back to created when modified is None."""
        sitemap = PostsSitemap()
        post = Post.objects.get(post_slug='fixture-post')
        post.modified = None
        self.assertEqual(sitemap.lastmod(post), post.created)


class TwitterTimelineTests(BasicTests):
    """Unit tests for generate_twitter_timeline covering all error/success branches."""

    @patch('communication.views.requests.get')
    def test_rate_limit_on_user_lookup(self, mock_get):
        """Returns error dict when user lookup returns 429."""
        resp = Mock(status_code=429)
        mock_get.return_value = resp
        result = generate_twitter_timeline(5)
        self.assertIn('error', result)

    @patch('communication.views.requests.get')
    def test_user_id_not_found(self, mock_get):
        """Returns error dict when API returns no user id."""
        resp = Mock(status_code=200)
        resp.raise_for_status = Mock()
        resp.json.return_value = {'data': {}}
        mock_get.return_value = resp
        result = generate_twitter_timeline(5)
        self.assertIn('error', result)

    @patch('communication.views.requests.get')
    def test_rate_limit_on_tweet_fetch(self, mock_get):
        """Returns error dict when tweet fetch returns 429."""
        user_resp = Mock(status_code=200)
        user_resp.raise_for_status = Mock()
        user_resp.json.return_value = {'data': {'id': '99'}}
        tweet_resp = Mock(status_code=429)
        mock_get.side_effect = [user_resp, tweet_resp]
        result = generate_twitter_timeline(5)
        self.assertIn('error', result)

    @patch('communication.views.requests.get')
    def test_request_exception(self, mock_get):
        """Returns error dict on RequestException."""
        from requests.exceptions import RequestException
        mock_get.side_effect = RequestException("network error")
        result = generate_twitter_timeline(5)
        self.assertIn('error', result)

    @patch('communication.views.requests.get')
    def test_successful_timeline(self, mock_get):
        """Returns tweet list on successful API calls."""
        user_resp = Mock(status_code=200)
        user_resp.raise_for_status = Mock()
        user_resp.json.return_value = {'data': {'id': '99'}}
        tweet_resp = Mock(status_code=200)
        tweet_resp.raise_for_status = Mock()
        tweet_resp.json.return_value = {'data': [{'text': 'hello'}]}
        mock_get.side_effect = [user_resp, tweet_resp]
        result = generate_twitter_timeline(5)
        self.assertEqual(result, [{'text': 'hello'}])

    @patch('communication.views.requests.get')
    def test_twitter_view_success_path(self, mock_get):
        """TwitterView sets timeline in context on successful API response."""
        user_resp = Mock(status_code=200)
        user_resp.raise_for_status = Mock()
        user_resp.json.return_value = {'data': {'id': '99'}}
        tweet_resp = Mock(status_code=200)
        tweet_resp.raise_for_status = Mock()
        tweet_resp.json.return_value = {'data': [{'text': 'test tweet'}]}
        mock_get.side_effect = [user_resp, tweet_resp]
        response = self.client.get('/twitter', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['timeline'], [{'text': 'test tweet'}])
        self.assertIsNone(response.context['twitter_error'])


class LabRulesViewTests(BasicTests):
    """Tests for LabRulesView covering all urlopen branches."""

    @patch('urllib.request.urlopen')
    def test_404_error(self, mock_urlopen):
        """Sets lab_rules to error message on 404."""
        mock_urlopen.side_effect = urllib.error.HTTPError('url', 404, 'Not Found', {}, None)
        response = self.client.get('/lab-rules/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['lab_rules'], 'Lab Rules File is not Available.')

    @patch('urllib.request.urlopen')
    def test_non_404_url_error(self, mock_urlopen):
        """Sets lab_rules to error message on non-404 URLError."""
        mock_urlopen.side_effect = urllib.error.HTTPError('url', 500, 'Error', {}, None)
        response = self.client.get('/lab-rules/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['lab_rules'], 'Lab Rules File is not Available.')

    @patch('urllib.request.urlopen')
    def test_value_error(self, mock_urlopen):
        """Sets lab_rules to error message on ValueError."""
        mock_urlopen.side_effect = ValueError("bad url")
        response = self.client.get('/lab-rules/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['lab_rules'], 'Lab Rules File is not Available.')

    @patch('urllib.request.urlopen')
    def test_successful_response(self, mock_urlopen):
        """Sets lab_rules to file content on success."""
        mock_resp = Mock()
        mock_resp.read.return_value = b'# Lab Rules Content'
        mock_urlopen.return_value = mock_resp
        response = self.client.get('/lab-rules/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['lab_rules'], b'# Lab Rules Content')


class PublicationPolicyViewTests(BasicTests):
    """Tests for PublicationPolicyView covering all urlopen branches."""

    @patch('urllib.request.urlopen')
    def test_404_error(self, mock_urlopen):
        mock_urlopen.side_effect = urllib.error.HTTPError('url', 404, 'Not Found', {}, None)
        response = self.client.get('/publication-policy/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['publication_policy'], 'Publication Policy File is not Available.')

    @patch('urllib.request.urlopen')
    def test_non_404_url_error(self, mock_urlopen):
        mock_urlopen.side_effect = urllib.error.HTTPError('url', 500, 'Error', {}, None)
        response = self.client.get('/publication-policy/', follow=True)
        self.assertEqual(response.status_code, 200)

    @patch('urllib.request.urlopen')
    def test_value_error(self, mock_urlopen):
        mock_urlopen.side_effect = ValueError("bad url")
        response = self.client.get('/publication-policy/', follow=True)
        self.assertEqual(response.status_code, 200)

    @patch('urllib.request.urlopen')
    def test_successful_response(self, mock_urlopen):
        mock_resp = Mock()
        mock_resp.read.return_value = b'# Publication Policy'
        mock_urlopen.return_value = mock_resp
        response = self.client.get('/publication-policy/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['publication_policy'], b'# Publication Policy')


class DataResourceSharingViewTests(BasicTests):
    """Tests for DataResourceSharingPolicyView covering all urlopen branches."""

    @patch('urllib.request.urlopen')
    def test_404_error(self, mock_urlopen):
        mock_urlopen.side_effect = urllib.error.HTTPError('url', 404, 'Not Found', {}, None)
        response = self.client.get('/data-resource-sharing/', follow=True)
        self.assertEqual(response.status_code, 200)

    @patch('urllib.request.urlopen')
    def test_non_404_url_error(self, mock_urlopen):
        mock_urlopen.side_effect = urllib.error.HTTPError('url', 500, 'Error', {}, None)
        response = self.client.get('/data-resource-sharing/', follow=True)
        self.assertEqual(response.status_code, 200)

    @patch('urllib.request.urlopen')
    def test_value_error(self, mock_urlopen):
        mock_urlopen.side_effect = ValueError("bad url")
        response = self.client.get('/data-resource-sharing/', follow=True)
        self.assertEqual(response.status_code, 200)


class PostDetailErrorTests(BasicTests):
    """Tests for PostDetail markdown fetch error handling."""

    fixtures = ['test_post', 'test_publication', 'test_publication_personnel', 'test_project', 'test_personnel']

    @patch('urllib.request.urlopen')
    def test_url_error_fallback(self, mock_urlopen):
        """PostDetail sets post_data to unavailable message on URLError."""
        mock_urlopen.side_effect = urllib.error.URLError("connection refused")
        response = self.client.get('/posts/fixture-post', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['post_data'], 'Post is not Available.')
        self.assertFalse(response.context['has_citations'])

    @patch('urllib.request.urlopen')
    def test_value_error_fallback(self, mock_urlopen):
        """PostDetail sets post_data to unavailable message on ValueError."""
        mock_urlopen.side_effect = ValueError("bad url")
        response = self.client.get('/posts/fixture-post', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['post_data'], 'Post is not Available.')