from django.conf.urls.defaults import *
from django.conf import settings
from explainthis.questions.models import Question, Answer
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

question_vote_dict = {
    'model': Question,
    'template_object_name': 'question',
    'allow_xmlhttprequest': True,
    'template_name':"questions/vote.html"
}

answer_vote_dict = {
    'model': Answer,
    'template_object_name': 'answer',
    'allow_xmlhttprequest': True,
    'template_name':"answers/vote.html"
}

urlpatterns = patterns('',
    # Example:
    # (r'^instamedia/', include('instamedia.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^accounts/', include('django_rpx_plus.urls')),
    url(r"^accounts/(?P<user_slug>.*)", 'explainthis.questions.views.user_profile', name="user_profile"),
    (r"^logout", 'django.contrib.auth.views.logout'),
    
    (r'^admin/', include(admin.site.urls)),
    (r'^comments/', include('django.contrib.comments.urls')),
    url(r'^comments/(?P<comment_type_post>.*)/post/(?P<question_id>.*)/(?P<answer_id>.*)', 'explainthis.questions.views.post_comment',name="comment_post_answer"),
    url(r'^comments/(?P<comment_type_post>.*)/post/(?P<question_id>.*)', 'explainthis.questions.views.post_comment',name="comment_post"),
    url(r'^$', 'explainthis.questions.views.index', name="home"),
    url(r'^question/ask$', 'explainthis.questions.views.ask', name="ask_question"),
    (r'^question/(?P<object_id>\d+)/(?P<direction>up|down|clear)vote$', 'explainthis.questions.views.vote', question_vote_dict, "vote_question"),
    (r'^answer/(?P<object_id>\d+)/(?P<direction>up|down|clear)vote$', 'explainthis.questions.views.vote', answer_vote_dict, "vote_answer"),
    url(r'^subsite/create$', 'explainthis.questions.views.create_subsite', name="create_subsite"),
    url(r'^question/(?P<question_id>.*)/answer$', 'explainthis.questions.views.answer', name="answer_question"),
    url(r"^(?P<widget_type>(site|json|iframe))/(?P<site_slug>.*)/question/ask$", 'explainthis.questions.views.ask', name="site_question_ask"),
    url(r"^(?P<widget_type>(site|json|iframe))/(?P<site_slug>[^/]*)$", 'explainthis.questions.views.site', name="site_view"),
    url(r"^(?P<widget_type>(site|json|iframe))/(?P<site_slug>.*)/question/(?P<question_slug>.*)", 'explainthis.questions.views.question', name="question_view"),
    url(r"^site/(?P<site_slug>.*)/admin", 'explainthis.questions.views.admin_site', name="site_admin"),
    
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
    
)
