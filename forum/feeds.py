from django.contrib.syndication.feeds import Feed
from django.utils.feedgenerator import Atom1Feed
from forum.models import Post
from django.conf import settings
from django.utils.translation import ugettext as _

class RssFeed(Feed):
    title = _("Forum")
    link = "/forum/" 
    description = _("Forum")
    def items(self):
        return Post.published_objects.all().order_by('-pub_date')[:5]

class AtomFeed(RssFeed):
    feed_type = Atom1Feed
