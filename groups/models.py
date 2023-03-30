from django.db import models


class Group(models.Model):
    name = models.CharField(verbose_name=' название группы', max_length=500)
    description = models.CharField(verbose_name='описание группы', max_length=500, blank=True)


class Participant(models.Model):
    name = models.CharField(verbose_name='имя участника', max_length=500)
    wish = models.CharField(verbose_name='пожелание', max_length=500)
    recipient = models.ForeignKey("self", verbose_name='подопечный', null=True, on_delete=models.SET_NULL)
    group = models.ForeignKey(Group,
                              verbose_name='группа',
                              null=True,
                              on_delete=models.SET_NULL,
                              related_name='participants')
