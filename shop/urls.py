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
    url(r'^image/(?P<nn>[0-9]+)/(?P<pk>[0-9]+)/delete/$', views.image_del, name='image_del'),
    url(r'^posts/$', views.posts, name='posts'),
    url(r'^post/(?P<nn>[0-9]+)/delete/$', views.post_delete, name='post_delete'),
    url(r'^theory/$', views.theory, name='theory'),
    url(r'^theory_new/$', views.theory_new, name='theory_new'),
    url(r'^theory/(?P<slug>[-\w]+)/edit/$', views.theory_edit, name='theory_edit'),
    url(r'^theory/(?P<slug>[-\w]+)/delete/$', views.theory_delete, name='theory_delete'),
    url(r'^theory/(?P<nn>[0-9]+)/adelete/$', views.theory_adelete, name='theory_adelete'),
    url(r'^category/(?P<nn>[0-9]+)/adelete/$', views.category_adelete, name='category_adelete'),
    url(r'^basket$', views.basket, name='basket'),
    #url(r'^get.m3u8$', views.get_m3u8, name='get_m3u8'),
    #url(r'^video_feed$', views.video_feed, name='video_feed'),
    #url(r'^streams$', views.streams, name='streams'),
    #url(r'^get_cl$', views.get_cl, name='get_cl'),
    #url(r'^map$', views.map, name='map'),

    ]
