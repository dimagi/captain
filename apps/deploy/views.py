from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.views.generic import View, TemplateView

from .models import Deploy
from .exceptions import DeployAlreadyInProgress

ENVIRONMENTS = ['staging', 'production']


class ChiefDeploy(View):
    urlname = 'chief_deploy'

    def post(self, request, *args, **kwargs):
        """
        Initiates a new deploy by actual awesome_deploy
        """
        env = request.POST.get('env')

        deploy = Deploy.objects.create(env=env)
        try:
            deploy.deploy()
        except DeployAlreadyInProgress:
            return HttpResponseBadRequest('There is already a deploy in progress')

        return HttpResponse('Deploy has been triggered')

    def get(self, request, *args, **kwargs):
        """
        Returns a JSON representation of the current deploy status
        """
        deploy = Deploy.current_deploy()
        return JsonResponse(deploy.as_json())


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


class ChiefStatusPage(BasePageView):
    urlname = 'chief_status_page'
    page_title = 'HQ Chief'
    template_name = 'chief/status.html'

    # @method_decorator(require_superuser)
    def dispatch(self, *args, **kwargs):
        return super(ChiefStatusPage, self).dispatch(*args, **kwargs)

    def page_url(self):
        return reverse(self.urlname)

    def get_context_data(self, **kwargs):
        context = super(ChiefStatusPage, self).get_context_data(**kwargs)
        context.update({
            'hide_filters': True,
            # TODO make this dynamic so india can only deploy india
            'environments': ENVIRONMENTS,
            'deploys': Deploy.current_deploys()
        })
        return context
