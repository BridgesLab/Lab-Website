'''This package contains views for the root app.

So far this includes the home page.'''

import json
import urllib.request
import urllib.error
import time
import re
from datetime import datetime

from django.conf import settings
from django.views.generic.base import TemplateView
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from personnel.models import JobPosting
from papers.models import Publication, Commentary, JournalClubArticle
from communication.models import Post, LabAddress

class IndexView(TemplateView):
    '''This view redirects to the home page.'''
    
    template_name = "index.html"   
    
    def get_context_data(self, **kwargs):
        '''This function provides the context which is passed to this view.
        
        This will query facebook's pages API for information regarding the group.
        From facebook there will be separate queries for posts, photos, milestones and general information.
        The Twitter API will be used to request facebook 
        There will also be an internal query for lab publications.'''
        
        context = super(IndexView, self).get_context_data(**kwargs)
        
        def facebook_request(request_url):
            '''This function takes a request url and token and returns deserialized data.'''
            request = urllib.request.Request(request_url)
            try:
                response = urllib.request.urlopen(request)
            except urllib.error.URLError as e:
                if e.code == 404:
                    data = "Facebook API is not Available."
                else:
                    #this is for a non-404 URLError.
                    data = "Facebook API is not Available."
            except ValueError:
                data = "Facebook API is not Available."        
            else:
                #successful connection
                json_data = response.read()
                data = json.loads(json_data)
                return data
        
        def urlify_text(text):
            '''Convert URLs in text to clickable links.'''
            if not text:
                return text
                
            # URL regex pattern
            url_pattern = re.compile(
                r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
            )
            
            def replace_url(match):
                url = match.group(0)
                return format_html('<a href="{}" target="_blank" rel="noopener noreferrer">{}</a>', url, url)
            
            return mark_safe(url_pattern.sub(replace_url, text))
        
        def process_facebook_posts(posts_data):
            '''Process Facebook posts to extract text, date, and urlify links, limiting to 5 most recent.'''
            processed_posts = []
            
            if isinstance(posts_data, str):  # Error case
                return processed_posts
                
            if 'data' in posts_data:
                # Sort posts by created_time (newest first) and take top 5
                sorted_posts = sorted(
                    posts_data['data'],
                    key=lambda x: x.get('created_time', ''),
                    reverse=True
                )[:5]
                
                for post in sorted_posts:
                    processed_post = {
                        'id': post.get('id', ''),
                        'message': urlify_text(post.get('message', '')),
                        'created_time': format_facebook_date(post.get('created_time', '')),
                        'created_time_raw': post.get('created_time', ''),
                        'full_picture': post.get('full_picture', ''),
                        'status_type': post.get('status_type', ''),
                        'permalink_url': post.get('permalink_url', ''),
                        'shared_link': ''
                    }
                    # Check for shared links in attachments
                    if 'attachments' in post and 'data' in post['attachments']:
                        for attachment in post['attachments']['data']:
                            if 'url' in attachment and attachment.get('type') == 'share':
                                processed_post['shared_link'] = attachment['url']
                    
                    processed_posts.append(processed_post)
            
            return processed_posts
        
        def format_facebook_date(date_string):
            '''Parse Facebook date string to a datetime object.'''
            if not date_string:
                return None
            try:
                # Facebook returns dates in ISO format like "2024-01-15T10:30:00+0000"
                return datetime.fromisoformat(date_string.replace('Z', '+00:00'))
            except (ValueError, AttributeError):
                return date_string
        
        # Updated URLs to get more post data including created_time, attachments, and permalink
        general_request_url = 'https://graph.facebook.com/v23.0/' + settings.FACEBOOK_ID + '?fields=id,description,about,name,photos{webp_images},picture.height(961)&access_token='+ settings.FACEBOOK_ACCESS_TOKEN
        
        # Updated posts URL to include attachments for shared links
        posts_request_url = 'https://graph.facebook.com/v23.0/' + settings.FACEBOOK_ID + '/posts?fields=id,status_type,message,full_picture,created_time,permalink_url,attachments{url,type}&limit=20&access_token='+ settings.FACEBOOK_ACCESS_TOKEN
        
        # Keep existing photo URL for backward compatibility
        photo_request_url = 'https://graph.facebook.com/v23.0/' + settings.FACEBOOK_ID + '/posts?fields=id,status_type,message,full_picture&access_token='+ settings.FACEBOOK_ACCESS_TOKEN
        
        # Context data
        context['recent_papers'] = Publication.objects.filter(laboratory_paper=True)[:5]
        context['recent_posts'] = Post.objects.all()[:10]
        context['recent_comments'] = Commentary.objects.all()[:5]
        context['journal_article_list'] = JournalClubArticle.objects.all()[:5]
        context['general_data'] = facebook_request(general_request_url)
        context['photo_data'] = facebook_request(photo_request_url)
        context['news'] = process_facebook_posts(facebook_request(posts_request_url))
        context['postings'] = JobPosting.objects.filter(active=True)
        context['twitter'] = settings.TWITTER_NAME
        context['google_plus'] = settings.GOOGLE_PLUS_ID
        context['facebook'] = settings.FACEBOOK_NAME
        context['lab_name'] = settings.LAB_NAME
        context['disqus_forum'] = settings.DISQUS_SHORTNAME
        context['fb_app_id'] = settings.FACEBOOK_APP_ID
        context['fb_admins'] = settings.FACEBOOK_ID
        context['analytics_tracking'] = settings.ANALYTICS_TRACKING
        context['analytics_root'] = settings.ANALYTICS_ROOT
        context['address'] = LabAddress.objects.filter(type="Primary")[0]

        return context                 

class PhotoView(TemplateView):
    '''This view shows images pulled from the facebook API, moved off the main page'''

    template_name = "lab_photos.html"

    def get_context_data(self, **kwargs):
        '''This function provides the context which is passed to this view.

        This will query facebook's pages API for photos.'''

        context = super(PhotoView, self).get_context_data(**kwargs)

        def facebook_request(request_url):
            '''This function takes a request url and token and returns deserialized data.'''
            request = urllib.request.Request(request_url)
            try:
                response = response = urllib.request.urlopen(request)
            except urllib.error.URLError as e:
                if e.code == 404:
                    data = "Facebook API is not Available."
                else:
                    # this is for a non-404 URLError.
                    data = "Facebook API is not Available."
            except ValueError:
                data = "Facebook API is not Available."
            else:
                # successful connection
                json_data = response.read()
                data = json.loads(json_data)
            return data

        general_request_url = (
            'https://graph.facebook.com/v13.0/' + settings.FACEBOOK_ID +
            '?fields=id,description,about,name,photos{webp_images},picture.height(961)&access_token=' +
            settings.FACEBOOK_ACCESS_TOKEN
        )
        photo_request_url = (
            'https://graph.facebook.com/v20.0/' + settings.FACEBOOK_ID +
            '/posts?fields=id,status_type,message,full_picture&access_token=' +
            settings.FACEBOOK_ACCESS_TOKEN
        )

        context['general_data'] = facebook_request(general_request_url)
        context['photo_data'] = facebook_request(photo_request_url)
        context['lab_name'] = settings.LAB_NAME

        return context
