from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.views.generic.list_detail import object_list
from django.views.generic.create_update import create_object
from django import newforms as forms
from forum.models import Topic, Post, Forum
from common.views.views import sorted_paginated_authored_archived_list
from django.conf import settings

def topic_list(request, slug=None, username=None, sort_field=None, paginate_by=10):
    base_url = '/forum/topics/'
    template_name = None
    extra_context = dict()
    filter = dict()
    if slug != None:
        base_url = "/forum/" + slug + "/"
        template_name = 'forum/forum_topic_list.html'
        forum = Forum.objects.get(slug=slug)
        sort_field = '-sticky'
        extra_context = dict(forum=forum)
        filter = dict(forum__slug=slug, state=settings.STATE_PUBLISHED)
    return sorted_paginated_authored_archived_list(request, Topic, base_url, username=username, sort_field=sort_field, paginate_by=paginate_by, filter=filter, extra_context=extra_context, template_name=template_name)

def topic_form(request, slug):
    forum = Forum.objects.get(slug=slug)
    return create_object(request, Topic, login_required='true', extra_context={'forum': forum, 'STATE_DEFAULT': settings.STATE_DEFAULT})

def post_list(request, topic_id=None, username=None, sort_field=None, paginate_by=10):
    base_url = '/forum/posts/'
    template_name = None
    extra_context = dict()
    filter = dict()
    if topic_id:
        base_url = '/forum/topic/'+topic_id+'/'
        template_name = 'forum/topic_post_list.html'
        topic = Topic.objects.get(id=topic_id)
        sort_field = 'pub_date'
        extra_context = dict(topic=topic)
        filter = dict(topic__id=topic_id, state=settings.STATE_PUBLISHED)
    return sorted_paginated_authored_archived_list(request, Post, base_url, username=username, sort_field=sort_field, paginate_by=paginate_by, filter=filter, extra_context=extra_context, template_name=template_name)

def post_form(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    if topic.locked:
        return HttpResponseRedirect("/forum/topic/%d" % topic.id)
    if int(topic.state) != settings.STATE_PUBLISHED:
        return HttpResponseRedirect("/forum/topic/%d" % topic.id)
    return create_object(request, Post, login_required='true', extra_context={'topic': topic, 'STATE_DEFAULT': settings.STATE_DEFAULT})
