from threading import Thread

from django.contrib import messages
from django.shortcuts import HttpResponse, get_object_or_404, redirect
from django.template import loader
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.list import ListView

from account.models import User
from contest.models import Contest
from contest.ratings import calculate_rating_changes, clear_previous_ratings
from utils.email import send_mail_with_bcc
from ..base_views import BaseBackstageMixin


class ContestSendInvitationMail(BaseBackstageMixin, TemplateView):
    template_name = 'backstage/contest/invitation.jinja2'

    def post(self, request):
        head = request.POST['head']
        msg = request.POST['msg']
        if not head or not msg:
            messages.add_message(request, messages.ERROR, 'Message cannot be empty.')
        else:
            recipient_list = list(filter(lambda x: x, [u.email for u in User.objects.filter(is_active=True,
                                                                                            email_subscription=True).all()]))
            Thread(target=send_mail_with_bcc, args=(head, msg,),
                   kwargs=(dict(recipient_list=recipient_list,
                                fail_silently=True))).start()
            messages.add_message(request, messages.SUCCESS, "Email sending task added successfully.")
        return redirect(reverse('backstage:contest_send_invitation'))


class ContestList(BaseBackstageMixin, ListView):
    template_name = 'backstage/contest/contest.jinja2'
    queryset = Contest.objects.all()
    paginate_by = 100
    context_object_name = 'contest_list'


class ContestApplyRatingChanges(BaseBackstageMixin, View):
    def post(self, request, cid):
        try:
            contest = get_object_or_404(Contest, pk=cid)
            calculate_rating_changes(contest)
            messages.success(request, 'Ratings successfully updated.')
        except Exception as e:
            messages.error(request, str(e))
        return HttpResponse()


class ContestWithdrawRatingChanges(BaseBackstageMixin, View):
    def post(self, request, cid):
        contest = get_object_or_404(Contest, pk=cid)
        clear_previous_ratings(contest)
        return HttpResponse()
