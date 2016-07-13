from django.conf.urls import url
from views import *
from django.contrib.auth.decorators import login_required
from postbox import api


urlpatterns=[

    url(r'^$', login_required(Newsfeed.as_view()), name='news'),
    url(r'^(?P<uname>[A-Za-z]*)/(?P<pid>[0-9]+)/comments/$', login_required(CommentList1.as_view()),name='comment_list1'),

    url(r'^(?P<uname>[A-Za-z]*)/profile/$', login_required(Profile.as_view()), name='user'),

    url(r'^(?P<uname>[A-Za-z]*)/(?P<cid>[0-9]+)/$', login_required(PostList.as_view()), name='post_list'),
    url(r'^(?P<uname>[A-Za-z]*)/(?P<cid>[0-9]+)/(?P<pid>[0-9]+)/comments/$', login_required(CommentList.as_view()), name='comment_list'),

    url(r'^(?P<uname>[A-Za-z]*)/create_category/$',login_required(CreateCat.as_view()),name='cform'),
    url(r'^(?P<uname>[A-Za-z]*)/(?P<cid>[0-9]+)/edit_cat/$', login_required(edit_cat.as_view()),name='cform_edit'),
    url(r'^(?P<uname>[A-Za-z]*)/(?P<cid>[0-9]+)/delete_cat/$', 'postbox.views.delete_cat', name='delete_cat'),

    url(r'^(?P<uname>[A-Za-z]*)/create_post/$', login_required(Create_post.as_view()),name='pform'),
    url(r'^(?P<uname>[A-Za-z]*)/(?P<pid>[0-9]+)/edit_post/$',login_required(Edit_post.as_view()),name='pform_edit' ),
    url(r'^(?P<uname>[A-Za-z]*)/(?P<pid>[0-9]+)/delete_post/$','postbox.views.delete_post', name='delete_post'),

    url(r'^(?P<uname>[A-Za-z]*)/(?P<cid>[0-9]+)/(?P<pid>[0-9]+)/(?P<cmid>[0-9]+)/edit_comment/$', login_required(EditComment.as_view()),name='cform_edit'),
    url(r'^(?P<uname>[A-Za-z]*)/(?P<cid>[0-9]+)/(?P<pid>[0-9]+)/(?P<cmid>[0-9]+)/delete_comment/$', 'postbox.views.delete_comment', name='delete_comment'),

    url(r'^(?P<uname>[A-Za-z]*)/(?P<pid>[0-9]+)/(?P<cmid>[0-9]+)/edit_comment/$',login_required(EditComment1.as_view()),name='cform_edit1'),
    url(r'^(?P<uname>[A-Za-z]*)/(?P<pid>[0-9]+)/(?P<cmid>[0-9]+)/delete_comment/$','postbox.views.delete_comment1', name='delete_comment1'),

    url(r'^api/user/$',api.user_list),
    url(r'^api/user/(?P<pk>[0-9]+)/categories/$', api.category_detail),
    url(r'^api/user/([0-9]+)/categories/(?P<pk>[0-9]+)/posts/$', api.post_detail),
    url(r'^api/user/([0-9]+)/categories/([0-9]+)/posts/(?P<pk>[0-9]+)/comments/$', api.comment_detail),

    url(r'^api/user/([0-9]+)/categories/(?P<pk>[0-9]+)/$', api.category_detail_view),
    url(r'^api/user/([0-9]+)/categories/([0-9]+)/posts/(?P<pk>[0-9]+)/$', api.post_detail_view),
    url(r'^api/user/([0-9]+)/categories/([0-9]+)/posts/([0-9]+)/comments/(?P<pk>[0-9]+)/$', api.comment_detail_view),

    # url(r'^api/categories/(?P<pk>[0-9]+)/items/$', category_detail),

]