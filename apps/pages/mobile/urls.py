from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from components.activities.models import ActivityBase

urlpatterns = patterns('',
    url(r'^$', 'pages.mobile.views.landing', name='mobile_landing'),
    url(r'^home/?$', 'pages.mobile.views.index', name='mobile_index'),
    url(r'^logout/?$', 'pages.mobile.views.logout', name='mobile_logout'),
    url(r'^setup/$', direct_to_template, {"template": 'mobile/setup.html'}, name='mobile_setup'),
    url(r'^smartgrid/?$', 'pages.mobile.views.smartgrid', name='mobile_smartgrid'),
    url(r'^smartgrid/(?P<category_slug>[\w\d\-]+)/?$', 'pages.mobile.views.sgactivities', name='mobile_activities'),
    url(r'^smartgrid/(?P<category_slug>[\w\d\-]+)/(?P<slug>[\w\d\-]+)/denied/?$', 'pages.mobile.views.taskdeny', name='mobile_task_deny'),
    url(r'^smartgrid/(?P<category_slug>[\w\d\-]+)/(?P<slug>[\w\d\-]+)/?$', 'pages.mobile.views.task', name='mobile_task'),
    url(r'^smartgrid/(?P<category_slug>[\w\d\-]+)/(?P<slug>[\w\d\-]+)/add/?$', 'pages.mobile.views.sgadd', name='mobile_task_add'),
    url(r'^events/(\w*)/?$', 'pages.mobile.views.events', name='mobile_events'), 
    url(r'^quests/popup/?$', 'pages.mobile.views.popup', name='mobile_quest_popup'),
    url(r'^quests/(\w*)/?$', 'pages.mobile.views.quests', name='mobile_quests'),
    url(r'^quests/(?P<ref>[-\w]+)/(?P<slug>[-\w]+)/?$', 'pages.mobile.views.quest_detail', name='mobile_quest_detail'),
    url(r'^scoreboard/?$', 'pages.mobile.views.scoreboard', name='mobile_scoreboard'), 
    url(r'^summary/?$', 'pages.mobile.views.summary', name='mobile_summary'),
    url(r'^help/?$', 'pages.mobile.views.help', name='mobile_help'),
    url(r'^help/(?P<category>\w+)/(?P<slug>[\w\d\-]+)/$', 'pages.mobile.views.helptopic', name='mobile_help_topic'),
    url(r'^profile/?$', 'pages.mobile.views.profile', name='mobile_profile'),
    url(r'^raffle/?$', 'pages.mobile.views.raffle', name='mobile_raffle'),
    url(r'^raffle/(?P<prize_slug>[\w\d\-]+)/?$', 'pages.mobile.views.raffle_item', name="mobile_raffle_item"),
    url(r'^power_and_energy/?$', 'pages.mobile.views.power_and_energy', name='mobile_power_and_energy'), 
    url(r'^news/?$', 'pages.mobile.templates.mobile.news.views.news' , name='mobile_news'),
)
