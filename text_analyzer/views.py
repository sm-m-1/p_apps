from django.shortcuts import render
from django.views import generic
from text_analyzer import utils

# Create your views here.
class TextAnalyzerView(generic.TemplateView):
    template_name = 'text_analyzer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_essay = self.request.GET.get('user_essay')
        user_url = self.request.GET.get('user_url')
        context['user_essay'] = user_essay
        context['user_url'] = user_url
        return context
