from django.shortcuts import HttpResponse
from django.views import generic
from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import GroupForm


def hello(request):
    return HttpResponse('Hello main page\n')

def group(request):
    return HttpResponse('Hello group page\n')
    
    
    
class GroupView(View):
    form_class = GroupForm
    template_name = 'group.html'
    
    
    #blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})