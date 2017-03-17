from django.db import models
from django.utils import timezone

from account.models import User
from problem.models import Problem
from group.models import Group


class ContestManager(models.Manager):

    def get_status_list(self):
        cmp = dict(Running=-1, Pending=0, Ended=1)
        contest_list = super(ContestManager, self).get_queryset().all()
        now = timezone.now()
        for contest in contest_list:
            if contest.start_time <= now <= contest.end_time:
                contest.status = 'Running'
            elif now <= contest.start_time:
                contest.status = 'Pending'
            else:
                contest.status = 'Ended'
        contest_list = sorted(contest_list, key=lambda c: cmp[c.status])
        return contest_list


class Contest(models.Model):
    title = models.CharField(max_length=48)
    description = models.TextField()
    created_by = models.ForeignKey(User)

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    create_time = models.DateTimeField(auto_now_add=True)

    groups = models.ManyToManyField(Group)
    problems = models.ManyToManyField(Problem, through='ContestProblem')

    visible = models.BooleanField(default=False)

    objects = ContestManager()

    class Meta:
        ordering = ['-start_time']


class ContestProblem(models.Model):
    problem = models.ForeignKey(Problem)
    contest = models.ForeignKey(Contest)
    identifier = models.CharField(max_length=12)
    total_submit_number = models.IntegerField(default=0)
    total_accept_number = models.IntegerField(default=0)

    class Meta:
        unique_together = ('problem', 'contest')


class ContestClarification(models.Model):
    contest = models.ForeignKey(Contest)
    question = models.TextField()
    answer = models.TextField(blank=True)
    username = models.CharField(max_length=30)