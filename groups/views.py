from random import randint, shuffle

from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import Group, Participant
from .serializers import GroupSerializer, GroupShortSerializer, ParticipantSerializer


class GroupViewSet(viewsets.ViewSet):

    def create(self, request):
        serializer = GroupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        group = serializer.save()
        return Response(group.id, status=201)

    def list(self, request):
        groups = Group.objects.all()
        return Response(GroupShortSerializer(groups, many=True).data)

    def retrieve(self, request, group_id):
        group = get_object_or_404(Group, id=group_id)
        return Response(GroupSerializer(group).data)

    def update(self, request, group_id):
        serializer = GroupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        group = get_object_or_404(Group, id=group_id)
        group = serializer.update(group, serializer.validated_data)
        return Response(GroupSerializer(group).data, status=204)

    def destroy(self, request, group_id):
        group = get_object_or_404(Group, id=group_id)
        deleted_group_id = group.id
        group.delete()
        return Response(deleted_group_id, status=204)

# [
#     {
#        "id": 1,
#        "name": "string",
#        "description": "string"
#      }
# ]

# {
#    "name": "string",
#    "description": "string"
#  }

# {
#    "name": "string",
#    "wish": "string"
#  }


class ParticipantViewSet(viewsets.ViewSet):

    def create(self, request, group_id):
        serializer = ParticipantSerializer(data=request.data, context={'group_id': group_id})
        serializer.is_valid(raise_exception=True)
        participant = serializer.save()
        return Response(participant.id, status=201)

    def destroy(self, request, group_id, participant_id):
        participant = get_object_or_404(Participant, id=participant_id, group_id=group_id)
        deleted_participant_id = participant.id
        participant.delete()
        return Response(deleted_participant_id, status=204)


class ShuffleViewSet(viewsets.ViewSet):

    def toss(self, request, group_id):

        participants = Participant.objects.filter(group_id=group_id)
        initial = [participant for participant in participants]
        if len(initial) < 3:
            raise ValidationError('Group must have 3 or more participants for toss')
        shuffle(initial)
        rotation = randint(1, len(initial) - 1)
        rotated = initial[rotation:] + initial[:rotation]

        for part, rec in zip(initial, rotated):
            part.recipient = rec
            part.save()
        data = ParticipantSerializer(participants, many=True).data
        return Response(data, status=204)
