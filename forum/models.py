from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from published_manager.managers import PublishedManager

class Category(models.Model):
    """
    A forum's category 

    >>> # Create a category
    >>> c = Category.objects.create(name='a')
    >>> c.save()
    """
    name = models.CharField(maxlength=255, verbose_name=_("Category Name"))
    order = models.PositiveIntegerField(default=0, verbose_name=_("Ordering"))
    pub_date = models.DateTimeField(auto_now_add = True, verbose_name=_("Date Published"))

    def __str__(self):
        return _(self.name)

    class Meta:
        ordering = ['order', 'pub_date']
        get_latest_by = "pub_date"
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    class Admin:
        date_hierarchy = 'pub_date'
        ordering = ['order', 'pub_date']
        search_fields = ['name']
        list_display = ['name']

class Forum(models.Model):
    """
    A forum

    >>> # Create a category
    >>> c = Category.objects.create(name='a')
    >>> c.save()
    >>> # Create a forum
    >>> f = Forum.objects.create(category=c, name='a', slug='a', description='a')
    >>> f.save()
    """
    category = models.ForeignKey(Category, verbose_name=_("Category"))
    name = models.CharField(maxlength=255, verbose_name=_("Forum Name"))
    slug = models.SlugField(prepopulate_from=('name',), unique=True, verbose_name=_("Slug Field"))
    description = models.CharField(maxlength=255, verbose_name=_("Forum Description"))
    order = models.PositiveIntegerField(default=0, verbose_name=_("Ordering"))
    pub_date = models.DateTimeField(auto_now_add = True, verbose_name=_("Date Published"))

    def get_absolute_url(self):
        return "/forum/%s/" % self.slug

    def __str__(self):
        return _(self.name)

    class Meta:
        ordering = ['order', 'pub_date']
        get_latest_by = "pub_date"
        verbose_name = _("Forum")
        verbose_name_plural = _("Forums")

    class Admin:
        date_hierarchy = 'pub_date'
        list_display = ('name', 'description')
        ordering = ['order', 'pub_date']
        search_fields = ['name', 'description']
        fields = ( 
            (None, {
                'fields': ('name', 'category', 'description', 'order')
            }),
            (_('Advanced settings'), {
                'classes': 'collapse',
                'fields' : ('slug', 'pub_date')
            }),
        )

class Topic(models.Model):
    """
    A topic 

    >>> # Create a category
    >>> c = Category.objects.create(name='a')
    >>> c.save()
    >>> # Create a forum
    >>> f = Forum.objects.create(category=c, name='a', slug='b', description='a')
    >>> f.save()
    >>> # Create a user
    >>> from django.contrib.auth.models import User
    >>> u = User.objects.create(username='b', password='b')
    >>> u.save()
    >>> # Create a topic 
    >>> t = Topic.objects.create(forum=f, name='a', user=u, ip_address='127.0.0.1', slug='a')
    >>> t.save()
    """
    forum = models.ForeignKey(Forum, verbose_name=_("Forum"))
    name = models.CharField(maxlength=255, verbose_name=_("Topic Name"))
    user = models.ForeignKey(User, verbose_name=_("Author"))
    sticky = models.BooleanField(blank=True, default=False, verbose_name=_("Sticky?"), help_text=_("Makes your topic stick to the top of the forum topic list."))
    locked = models.BooleanField(blank=True, default=False, verbose_name=_("Locked?"), help_text=_("Makes your topic locked so that no new posts can be added."))
    pub_date = models.DateTimeField(auto_now_add = True, verbose_name=_("Date Published"))
    ip_address = models.IPAddressField(verbose_name=_("Author's IP Address"))
    state = models.CharField(maxlength=1, choices=settings.STATE_CHOICES, default=settings.STATE_DEFAULT, verbose_name=_("State of object"))
    slug = models.SlugField(prepopulate_from=('name',), unique=True, verbose_name=_("Slug Field"))
    objects = models.Manager()
    published_objects = PublishedManager()

    def get_absolute_url(self):
        return "/forum/topic/%d/" % self.id

    def __str__(self):
        return _(self.name)

    class Meta:
        ordering = ['sticky', 'pub_date']
        get_latest_by = "pub_date"
        verbose_name = _("Topic")
        verbose_name_plural = _("Topics")

    class Admin:
        date_hierarchy = 'pub_date'
        list_display = ('name', 'user', 'forum')
        ordering = ['sticky', 'pub_date']
        search_fields = ['name']
        fields = ( 
            (None, {
                'fields': ('name', 'user', 'forum', 'state', 'ip_address')
            }),
            (_('Options'), {
                'fields': ('sticky', 'locked')
            }),
            (_('Advanced settings'), {
                'classes': 'collapse',
                'fields': ('slug', 'pub_date')
            }),
        )

class Post(models.Model):
    """
    A post 

    >>> # Create a category
    >>> c = Category.objects.create(name='a')
    >>> c.save()
    >>> # Create a forum
    >>> f = Forum.objects.create(category=c, name='a', slug='c', description='a')
    >>> f.save()
    >>> # Create a user
    >>> from django.contrib.auth.models import User
    >>> u = User.objects.create(username='c', password='c')
    >>> u.save()
    >>> # Create a topic 
    >>> t = Topic.objects.create(forum=f, name='a', user=u, ip_address='127.0.0.1', slug='b')
    >>> t.save()
    >>> # Create a post 
    >>> p = Post.objects.create(topic=t, title='a', text='a', user=u, ip_address='127.0.0.1')
    >>> p.save()
    """
    topic = models.ForeignKey(Topic, verbose_name=_("Topic"))
    title = models.CharField(maxlength=255, verbose_name=_("Post Title"))
    text = models.TextField(verbose_name=_("Post Content"))
    user = models.ForeignKey(User, verbose_name=_("Author"))
    pub_date = models.DateTimeField(auto_now_add = True, verbose_name=_("Date Published"))
    mod_date = models.DateTimeField(auto_now = True, verbose_name=_("Date Modified"))
    ip_address = models.IPAddressField(verbose_name=_("Author's IP Address"))
    state = models.CharField(maxlength=1, choices=settings.STATE_CHOICES, default=settings.STATE_DEFAULT, verbose_name=_("State of object"))
    objects = models.Manager()
    published_objects = PublishedManager()

    def get_absolute_url(self):
        return "/forum/topic/%d/#post_%d" % (self.topic.id, self.id)

    def __str__(self):
        return _(self.text)

    class Meta:
        ordering = ['pub_date']
        get_latest_by = "pub_date"
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")

    class Admin:
        date_hierarchy = 'pub_date'
        list_display = ('title', 'text', 'user', 'topic')
        ordering = ['pub_date']
        search_fields = ['title', 'text']
        fields = ( 
            (None, {
                'fields': ('title', 'text', 'user', 'topic', 'state', 'ip_address')
            }),
            (_('Advanced settings'), {
                'classes': 'collapse',
                'fields' : ('pub_date', 'mod_date')
            }),
        )
