from django.conf.urls import url,include
from . import views

urlpatterns = [
    url(r'^$', views.main, name='home'),
    url(r'^good_new/$', views.good, name='good'),
    url(r'^category$', views.category, name='category'),
    url(r'^goods/$', views.goods, name='goods'),
    url(r'^image/(?P<nn>[0-9]+)/new/$', views.image_new, name='image_new'),
    url(r'^good/(?P<nn>[0-9]+)/edit/$', views.good_edit, name='good_edit'),
    url(r'^contacts/$', views.contacts, name='contacts'),
    url(r'^good/(?P<nn>[0-9]+)/delete/$', views.good_delete, name='good_delete'),
    #url(r'^get_turn$', views.get_turn, name='get_turn'),
    #url(r'^get.m3u8$', views.get_m3u8, name='get_m3u8'),
    #url(r'^video_feed$', views.video_feed, name='video_feed'),
    #url(r'^streams$', views.streams, name='streams'),
    #url(r'^get_cl$', views.get_cl, name='get_cl'),
    #url(r'^map$', views.map, name='map'),

    ]
