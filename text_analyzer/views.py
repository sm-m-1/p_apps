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
        if user_url:
            url_analysis = {
                'basic_analysis': [],
                'word_frequency': [],
                'total_words': 0,
                'syllable_counter': [],
                'unfiltered_word_frequency': [],
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


        return context
