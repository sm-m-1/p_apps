from html.parser import HTMLParser
import requests
import re
from collections import Counter

def get_web_page_text(url):
    """
    This function takes a url and returns a list of all the real words that
    appear in the given url. Real words meaning the text from the given url
    after ignoring HTML tags, spaces, new line '\n' character etc.
    :param url: a url
    :return: a list of words
    """
    response = requests.get(url)
    parser = CustomHTMLParser()
    parser.feed(response.text)
    words = parser.get_real_words()
    return words


class TextAnalyzer():
    def __init__(self, word_list):
        self.words = word_list
        self.words_count = Counter(self.words)

    def get_most_common(self, n):
        return self.words_count.most_common(n)



class CustomHTMLParser(HTMLParser):

    bad_tags = {"style", "script"}

    def __init__(self):
        self.phrase_list = []
        self.real_words = []
        self.valid_start_tag = True
        super().__init__()

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
        if self.valid_start_tag and len(data) > 0:
            self.phrase_list.append(data.rstrip())

    def get_real_words(self):
        """
        A function that calls extract words and gets real words from a url.
        :return: a list
        """
        return self.extract_words(self.phrase_list)

    def extract_words(self, list):
        """
        This function takes a list and returns a list of all the real words that
        appear in the given list. Real words means ignoring special characters
        such as new line '\n' character, '[*]' etc.
        :return: a list of words
        """
        words = []
        for text in list:
            sentence_list = re.findall("[a-z0-9']+", text.lower())
            for word in sentence_list:
                words.append(word)
        return words
