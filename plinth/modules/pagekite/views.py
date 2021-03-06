#
# This file is part of Plinth.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from gettext import gettext as _
from django.core.urlresolvers import reverse, reverse_lazy
from django.http.response import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.utils.decorators import method_decorator
from django.views.generic import View, TemplateView
from django.views.generic.edit import FormView

from plinth import package
from .util import get_pagekite_config, get_pagekite_services, \
    get_kite_details, prepare_service_for_display
from .forms import ConfigurationForm, StandardServiceForm, \
    AddCustomServiceForm, DeleteCustomServiceForm


required_packages = ('pagekite', 'augeas-tools', 'python-augeas')
subsubmenu = [{'url': reverse_lazy('pagekite:index'),
               'text': _('About PageKite')},
              {'url': reverse_lazy('pagekite:configure'),
               'text': _('Configure PageKite')},
              {'url': reverse_lazy('pagekite:standard-services'),
               'text': _('Standard Services')},
              {'url': reverse_lazy('pagekite:custom-services'),
               'text': _('Custom Services')}]


def index(request):
    """Serve introduction page"""
    return TemplateResponse(request, 'pagekite_introduction.html',
                            {'title': _('Public Visibility (PageKite)'),
                             'subsubmenu': subsubmenu})


class ContextMixin(object):
    """Mixin to add 'subsubmenu' and 'title' to the context.

    Also adds the requirement of all necessary packages to be installed
    """
    def get_context_data(self, **kwargs):
        """Use self.title and the module-level subsubmenu"""
        context = super(ContextMixin, self).get_context_data(**kwargs)
        context['title'] = getattr(self, 'title', '')
        context['subsubmenu'] = subsubmenu
        return context

    @method_decorator(package.required(required_packages))
    def dispatch(self, *args, **kwargs):
        return super(ContextMixin, self).dispatch(*args, **kwargs)


class DeleteServiceView(ContextMixin, View):
    def post(self, request):
        form = DeleteCustomServiceForm(request.POST)
        if form.is_valid():
            form.delete(request)
        return HttpResponseRedirect(reverse('pagekite:custom-services'))


class CustomServiceView(ContextMixin, TemplateView):
    template_name = 'pagekite_custom_services.html'

    def get_context_data(self, *args, **kwargs):
        context = super(CustomServiceView, self).get_context_data(*args,
                                                                  **kwargs)
        unused, custom_services = get_pagekite_services()
        for service in custom_services:
            service['form'] = AddCustomServiceForm(initial=service)
        context['custom_services'] = [prepare_service_for_display(service)
                                      for service in custom_services]
        context.update(get_kite_details())
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = AddCustomServiceForm(prefix="custom")
        context['form'] = form
        return self.render_to_response(context)

    def post(self, request):
        form = AddCustomServiceForm(request.POST, prefix="custom")
        if form.is_valid():
            form.save(request)
            form = AddCustomServiceForm(prefix="custom")

        context = self.get_context_data()
        context['form'] = form

        return self.render_to_response(context)


class StandardServiceView(ContextMixin, FormView):
    template_name = 'pagekite_standard_services.html'
    title = 'PageKite Standard Services'
    form_class = StandardServiceForm
    success_url = reverse_lazy('pagekite:standard-services')

    def get_initial(self):
        return get_pagekite_services()[0]

    def form_valid(self, form):
        form.save(self.request)
        return super(StandardServiceView, self).form_valid(form)


class ConfigurationView(ContextMixin, FormView):
    template_name = 'pagekite_configure.html'
    form_class = ConfigurationForm
    prefix = 'pagekite'
    success_url = reverse_lazy('pagekite:configure')

    def get_initial(self):
        return get_pagekite_config()

    def form_valid(self, form):
        form.save(self.request)
        return super(ConfigurationView, self).form_valid(form)
