from django.contrib.syndication.feeds import Feed
from django.utils.feedgenerator import Atom1Feed
from forum.models import Post
from django.conf import settings

class RssFeed(Feed):
    title = _("Forum")
    link = "/forum/" 
    description = _("Forum")
    def items(self):
        return Post.objects.filter(state=settings.STATE_PUBLISHED).order_by('-pub_date')[:5]

class AtomFeed(RssFeed):
    feed_type = Atom1Feed
