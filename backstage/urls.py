from django.conf.urls import url

from .base_views import index
from .problem.views import ProblemCreate, ProblemUpdate, ProblemList, testdata
from .group.views import GroupList, GroupUpdate, GroupCreate, GroupManage, group_member_delete
from .contest.views import ContestList, ContestCreate, ContestUpdate, ContestManage
from .server.views import ServerCreate, ServerUpdate, ServerList, server_delete

urlpatterns = [
    url(r'^$', index, name='index'),

    url(r'^problem/$', ProblemList.as_view(), name='problem'),
    url(r'^problem/create/$', ProblemCreate.as_view(), name='problem_create'),
    url(r'^problem/edit/(?P<pk>\d+)/', ProblemUpdate.as_view(), name='problem_edit'),
    url(r'^problem/testdata/(?P<pk>\d+)/', testdata, name='problem_testdata'),

    url(r'^group/$', GroupList.as_view(), name='group'),
    url(r'^group/create/$', GroupCreate.as_view(), name='group_create'),
    url(r'^group/edit/(?P<pk>\d+)/', GroupUpdate.as_view(), name='group_edit'),
    url(r'^group/manage/(?P<pk>\d+)/', GroupManage.as_view(), name='group_manage'),
    url(r'^group/delete/(?P<membership_pk>\d+)/', group_member_delete, name='group_delete'),

    url(r'^contest/$', ContestList.as_view(), name='contest'),
    url(r'^contest/create/$', ContestCreate.as_view(), name='contest_create'),
    url(r'^contest/edit/(?P<pk>\d+)/', ContestUpdate.as_view(), name='contest_edit'),
    url(r'^contest/manage/(?P<pk>\d+)/', ContestManage.as_view(), name='contest_manage'),

    url(r'^server/$', ServerList.as_view(), name='server'),
    url(r'^server/create/', ServerCreate.as_view(), name='server_create'),
    url(r'^server/edit/(?P<pk>\d+)/', ServerUpdate.as_view(), name='server_edit'),
    url(r'^server/delete/(?P<pk>\d+)/', server_delete, name='server_delete'),
]