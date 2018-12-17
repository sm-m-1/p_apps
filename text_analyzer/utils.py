from html.parser import HTMLParser
import requests
import re
from collections import Counter
from .corpus import FUNCTION_WORDS

def get_web_page_text(url):
    """
    This function takes a url and returns the cleaned data of response.
    :param url: a url
    :return: a list of phrases
    """
    response = requests.get(url)
    parser = CustomHTMLParser()
    parser.feed(response.text)
    words = parser.get_cleaned_data()
    return words


class TextAnalyzer():
    def __init__(self, phrase_list):
        self.phrase_list = phrase_list
        self.real_words = []
        self.filtered_words = []
        self.word_count = 0
        self.sentence_count = 0
        self.word_counter = None
        self.word_counter_filtered = None
        self._process_data()

    def _process_data(self):
        """
        This function does some processing of data and sets
        the appropriate member variables.
        :return: none
        """
        self.real_words = self._extract_real_words(self.phrase_list)
        self.word_count = len(self.real_words)
        self.sentence_count = self._calculate_total_sentences()
        self.word_counter = Counter(self.real_words)
        self.filtered_words = self._extract_filtered_words(self.real_words)
        self.word_counter_filtered = Counter(self.filtered_words)

    def get_word_count(self):
        """

        :return: Counter
        """
        return self.word_count

    def get_word_counter_filtered(self):
        """

        :return: Counter
        """
        return self.word_counter_filtered

    def get_real_words(self):
        """
        Gets the list of real words in the response.
        :return: a list
        """
        return self.real_words

    def get_lexical_density(self):
        # Lexical Density.
        # What words are should be counted: http://www.analyzemywriting.com/lexical_density.html
        return len(self.filtered_words) / len(self.real_words)

    def _calculate_total_sentences(self):
        count = 0
        for p in self.phrase_list:
            count += p.count(".")
        return count

    def _extract_real_words(self, list):
        """
        This function takes a list of text and returns a list of all the real words that
        appear in the given list. Real words means ignoring special characters
        such as new line '\n' character, '[*]', etc.
        :param list: a list of str values. str can be sentences.
        :return: a list of words
        """
        words = []
        for text in list:
            sentence_list = re.findall("[a-z0-9']+", text.lower())
            for word in sentence_list:
                words.append(word)
        return words

    def _extract_filtered_words(self, list):
        """
        This function takes a list of words and discards words that are
        commonly occurring jargon words, function words, etc.
        :param list: a list of str values. Each str is a word
        :return: a list of words
        """
        return [w for w in self.real_words if w not in FUNCTION_WORDS]


class CustomHTMLParser(HTMLParser):

    bad_tags = {"style", "script"}

    def __init__(self):
        self.phrase_list = []
        self.valid_start_tag = True
        super().__init__()

    def get_cleaned_data(self):
        return self.phrase_list

    def handle_starttag(self, tag, attrs):
        if tag in self.bad_tags:
            self.valid_start_tag = False
        else:
            self.valid_start_tag = True

    def handle_endtag(self, tag):
        if tag in self.bad_tags:
            self.valid_start_tag = True

    def handle_data(self, data):
        # this check is needed to ignore the data between style and script tags
        cleaned_data = data.strip()
        if self.valid_start_tag and len(cleaned_data) > 0:
            self.phrase_list.append(cleaned_data)

