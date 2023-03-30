from django.urls import path
from groups.views import GroupViewSet, ParticipantViewSet, ShuffleViewSet

urlpatterns = [
    path('group/', GroupViewSet.as_view({
        'post': 'create'
    })),
    path('groups/', GroupViewSet.as_view({
        'get': 'list',
    })),
    path('group/<int:group_id>/', GroupViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy',
    })),

    path('group/<int:group_id>/participant/', ParticipantViewSet.as_view({
        'post': 'create'
    })),
    path('group/<int:group_id>/participant/<int:participant_id>/', ParticipantViewSet.as_view({
        'delete': 'destroy',
    })),

    path('group/<int:group_id>/toss/', ShuffleViewSet.as_view({
        'post': 'toss',
    })),
]
