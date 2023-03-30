from django.shortcuts import get_object_or_404

from rest_framework import serializers

from .models import Group, Participant


class ParticipantShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = ['id', 'name', 'wish']


class ParticipantSerializer(serializers.ModelSerializer):
    recipient = ParticipantShortSerializer(required=False)

    class Meta:
        model = Participant
        fields = ['id', 'name', 'wish', 'recipient']

    def create(self, validated_data):
        group_id = self.context['group_id']
        group = get_object_or_404(Group, id=group_id)
        print(validated_data)
        participant = Participant.objects.create(group=group, **validated_data)
        return participant


class GroupShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name', 'description']


class GroupSerializer(serializers.ModelSerializer):
    participants = ParticipantSerializer(many=True)

    class Meta:
        model = Group
        fields = ['id', 'name', 'description', 'participants']

    def create(self, validated_data):
        group = Group.objects.create(**validated_data)
        return group


