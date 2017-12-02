'''This package contains views for the root app.

So far this includes the home page.'''

import json
import urllib, urllib2
import time
import datetime

from django.conf import settings
from django.views.generic.base import View, TemplateView

from personnel.models import JobPosting
from papers.models import Publication, Commentary
from communication.models import Post

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
            request = urllib2.Request(request_url)
            try:
                    response = urllib2.urlopen(request)
            except urllib2.URLError, e:
                    if e.code == 404:
                        data = "Facebook API is not Available."
                    else:
                        #this is for a non-404 URLError.
                        data = "Facebook API is not Available."
            except ValueError:
                    lab_rules = "Facebook API is not Available."        
            else:
                     #successful connection
                     json_data = response.read()
                     data = json.loads(json_data)
                     return data
         
        general_request_url = 'https://graph.facebook.com/v2.11/' + settings.FACEBOOK_ID + '?access_token=' + settings.FACEBOOK_ACCESS_TOKEN + '&fields=description,about,cover,photos{webp_images}'
        context['recent_papers'] =  Publication.objects.filter(laboratory_paper=True)[0:10]  
        context['recent_posts'] =  Post.objects.all()[0:5]  
        context['recent_comments'] =  Commentary.objects.all()[0:5]                 
        context['general_data'] = facebook_request(general_request_url)
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

        return context                            
