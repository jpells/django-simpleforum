from django.conf.urls.defaults import *
from forum.models import Category
from forum.feeds import RssFeed, AtomFeed
        
category_dict = { 
    'queryset': Category.objects.all(),
}

feeds = { 
    'rss': RssFeed,
    'atom': AtomFeed,
}

urlpatterns = patterns('django.views.generic.list_detail',
    (r'^$', 'object_list', category_dict),
)

urlpatterns += patterns('',
    (r'^rss/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds, 'url': 'rss'}),
    (r'^atom/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds, 'url': 'atom'}),
)

urlpatterns += patterns('forum.views',
    (r'^topics/$', 'topic_list'),
    (r'^posts/$', 'post_list'),
    (r'^topic/(?P<topic_id>\d+)/$', 'post_list'),
    (r'^topic/(?P<topic_id>\d+)/create/$', 'post_form'),
    (r'^(?P<slug>[-\w]+)/$', 'topic_list'),
    (r'^(?P<slug>[-\w]+)/create/$', 'topic_form'),
)
