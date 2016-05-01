from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.views.generic import View, TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from .models import Deploy
from .exceptions import DeployAlreadyInProgress
from .const import ENVIRONMENTS


class CaptainDeploy(View):
    urlname = 'captain_deploy'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(CaptainDeploy, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Initiates a new deploy by actual awesome_deploy
        """
        env = request.POST.get('env')
        code_branch = request.POST.get('code_branch')
        user = request.POST.get('deploy_user')

        deploy = Deploy.objects.create(
            env=env,
            code_branch=code_branch,
            user=user,
        )
        try:
            deploy.deploy()
        except DeployAlreadyInProgress:
            return HttpResponseBadRequest('There is already a deploy in progress')

        return HttpResponseRedirect(reverse(CaptainStatusPage.urlname))

    def get(self, request, *args, **kwargs):
        """
        Returns a JSON representation of the current deploy status
        """
        env = request.GET.get('env')
        context = {'deploys': []}

        deploys = Deploy.current_deploys_for_env(env)
        context['deploys'][env] = map(lambda d: d.as_json(), deploys)
        return JsonResponse(context)


class BasePageView(TemplateView):
    urlname = None  # name of the view used in urls
    page_title = None  # what shows up in the <title>
    template_name = ''

    @property
    def page_name(self):
        """
        This is what is visible to the user.
        page_title is what shows up in <title> tags.
        """
        return self.page_title

    @property
    def page_url(self):
        raise NotImplementedError()

    @property
    def parent_pages(self):
        """
        Specify parent pages as a list of
        [{
            'title': <name>,
            'url: <url>,
        }]
        """
        return []

    @property
    def main_context(self):
        """
        The shared context for rendering this page.
        """
        return {
            'current_page': {
                'page_name': self.page_name,
                'title': self.page_title,
                'url': self.page_url,
                'parents': self.parent_pages,
                'urlname': self.urlname,
            },
        }

    @property
    def page_context(self):
        """
        The Context for the settings page
        """
        return {}

    def get_context_data(self, **kwargs):
        context = super(BasePageView, self).get_context_data(**kwargs)
        context.update(self.main_context)
        context.update(self.page_context)
        return context

    def render_to_response(self, context, **response_kwargs):
        """
        Returns a response with a template rendered with the given context.
        """
        return render(self.request, self.template_name, context)


class MonitorPage(BasePageView):
    urlname = 'monitor_page'
    page_title = 'Captain Monitor'
    template_name = 'captain/monitor.html'

    def page_url(self):
        return reverse(self.urlname)


class CaptainStatusPage(BasePageView):
    urlname = 'captain_status_page'
    page_title = 'Captain'
    template_name = 'captain/status.html'

    # @method_decorator(require_superuser)
    def dispatch(self, *args, **kwargs):
        return super(CaptainStatusPage, self).dispatch(*args, **kwargs)

    def page_url(self):
        return reverse(self.urlname)

    def get_context_data(self, **kwargs):
        context = super(CaptainStatusPage, self).get_context_data(**kwargs)
        context.update({
            'hide_filters': True,
            # TODO make this dynamic so india can only deploy india
            'environments': ENVIRONMENTS,
            'deploys': Deploy.current_deploys(),
            'previous_deploys': Deploy.previous_deploys(),
        })
        return context
