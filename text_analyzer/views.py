from django.shortcuts import render
from django.urls import reverse
from django.views import generic
from text_analyzer import utils

# Create your views here.
from text_analyzer.forms import TextAnalyzerForm


class TextAnalyzerFormView(generic.FormView):
    form_class = TextAnalyzerForm
    template_name = "text_analyzer_form.html"

    def form_valid(self, form):
        # this method is called when valid form data as been posted.
        valid = super().form_valid(form)
        user_url = form.cleaned_data.get('user_url')
        user_essay = form.cleaned_data.get('user_essay')
        self.request.session['user_url'] = user_url
        self.request.session['user_essay'] = user_essay
        x = 5
        return valid

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.method == 'GET':
            user_url = self.request.session.get('user_url')
            user_essay = self.request.session.get('user_essay')
            context['user_essay'] = user_essay
            context['user_url'] = user_url
            if user_url:
                url_analysis = {
                    'basic_analysis': [],
                    'word_frequency': [],
                    'total_words': 0,
                    'syllable_counter': [],
                    'unfiltered_word_frequency': [],
                    'url': "",
                }
                response = utils.get_web_page_text(url=user_url)
                analyzer = utils.TextAnalyzer(response)

                url_analysis['basic_analysis'].append(('Total words', analyzer.words_in_text))
                url_analysis['basic_analysis'].append(('Unique words', analyzer.unique_words_in_text))
                url_analysis['basic_analysis'].append(('Text lexical density', analyzer.text_lexical_density))
                url_analysis['basic_analysis'].append(('Total sentences', analyzer.sentences_in_text))
                url_analysis['basic_analysis'].append(('Avg sentence size', analyzer.avg_sentence_size))

                url_analysis['word_frequency'] = analyzer.get_filtered_text_word_frequency()
                url_analysis['syllable_counter'] = analyzer.syllable_counter
                url_analysis['total_words'] = analyzer.words_in_text

                url_analysis['unfiltered_word_frequency'] = analyzer.get_text_word_frequency()
                url_analysis['url'] = user_url
                context['user_url_data'] = url_analysis

            if user_essay:
                user_input_analysis = {
                    'basic_analysis': [],
                    'word_frequency': [],
                    'total_words': 0,
                    'syllable_counter': [],
                    'unfiltered_word_frequency': [],
                }
                analyzer = utils.TextAnalyzer([user_essay])

                user_input_analysis['basic_analysis'].append(('Total words', analyzer.words_in_text))
                user_input_analysis['basic_analysis'].append(('Unique words', analyzer.unique_words_in_text))
                user_input_analysis['basic_analysis'].append(('Text lexical density', analyzer.text_lexical_density))
                user_input_analysis['basic_analysis'].append(('Total sentences', analyzer.sentences_in_text))
                user_input_analysis['basic_analysis'].append(('Avg sentence size', analyzer.avg_sentence_size))

                user_input_analysis['word_frequency'] = analyzer.get_filtered_text_word_frequency()
                user_input_analysis['syllable_counter'] = analyzer.syllable_counter
                user_input_analysis['total_words'] = analyzer.words_in_text

                user_input_analysis['unfiltered_word_frequency'] = analyzer.get_text_word_frequency()
                context['user_input_data'] = user_input_analysis
            # reset the session values after displaying the results to user.
            self.request.session['user_url'] = {}
            self.request.session['user_essay'] = {}
        return context

    def get_success_url(self):
        return reverse('text_analyzer_form')


# Not using the form below because of the limit of GET request parameter length size.
# The upper example of using Post request to process the form is needed for accepting
# a form with very large textarea size.

# class TextAnalyzerView(generic.TemplateView):
#     template_name = 'text_analyzer.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # user_url = self.request.GET.get('user_url')
#         # user_essay = self.request.GET.get('user_essay')
#         user_url = self.request.session.get('user_url')
#         user_essay = self.request.session.get('user_essay')
#         context['user_essay'] = user_essay
#         context['user_url'] = user_url
#         if user_url:
#             url_analysis = {
#                 'basic_analysis': [],
#                 'word_frequency': [],
#                 'total_words': 0,
#                 'syllable_counter': [],
#                 'unfiltered_word_frequency': [],
#             }
#             response = utils.get_web_page_text(url=user_url)
#             analyzer = utils.TextAnalyzer(response)
#
#             url_analysis['basic_analysis'].append(('Total words', analyzer.words_in_text))
#             url_analysis['basic_analysis'].append(('Unique words', analyzer.unique_words_in_text))
#             url_analysis['basic_analysis'].append(('Text lexical density', analyzer.text_lexical_density))
#             url_analysis['basic_analysis'].append(('Total sentences', analyzer.sentences_in_text))
#             url_analysis['basic_analysis'].append(('Avg sentence size', analyzer.avg_sentence_size))
#
#             url_analysis['word_frequency'] = analyzer.get_filtered_text_word_frequency()
#             url_analysis['syllable_counter'] = analyzer.syllable_counter
#             url_analysis['total_words'] = analyzer.words_in_text
#
#             url_analysis['unfiltered_word_frequency'] = analyzer.get_text_word_frequency()
#             context['user_url_data'] = url_analysis
#
#         if user_essay:
#             user_input_analysis = {
#                 'basic_analysis': [],
#                 'word_frequency': [],
#                 'total_words': 0,
#                 'syllable_counter': [],
#                 'unfiltered_word_frequency': [],
#             }
#             analyzer = utils.TextAnalyzer([user_essay])
#
#             user_input_analysis['basic_analysis'].append(('Total words', analyzer.words_in_text))
#             user_input_analysis['basic_analysis'].append(('Unique words', analyzer.unique_words_in_text))
#             user_input_analysis['basic_analysis'].append(('Text lexical density', analyzer.text_lexical_density))
#             user_input_analysis['basic_analysis'].append(('Total sentences', analyzer.sentences_in_text))
#             user_input_analysis['basic_analysis'].append(('Avg sentence size', analyzer.avg_sentence_size))
#
#             user_input_analysis['word_frequency'] = analyzer.get_filtered_text_word_frequency()
#             user_input_analysis['syllable_counter'] = analyzer.syllable_counter
#             user_input_analysis['total_words'] = analyzer.words_in_text
#
#             user_input_analysis['unfiltered_word_frequency'] = analyzer.get_text_word_frequency()
#             context['user_input_data'] = user_input_analysis
#
#
#         return context
