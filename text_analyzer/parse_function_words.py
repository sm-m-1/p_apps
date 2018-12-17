import re

def generate_list_of_function_words(old_file, new_file):
    '''\
    Read a list of words from a file line by line only extracting words.
    The the new word set in a new file.
    '''
    size = 0
    new_words = []
    with open(old_file, 'r') as read_file:
        for line in read_file:
            sentence = line.rstrip()
            words = re.findall("[a-z']+", sentence)
            for word in words:
                new_words.append(word)

    print("len: ", len(new_words))
    with open(new_file, 'w', encoding='utf-8') as write_file:
        variable_name = "FUNCTION_WORDS = {\n"
        write_file.write(variable_name)
        for word in new_words:
            write_file.write("  " + '"{}",\n'.format(word))

        write_file.write("}\n")

if __name__ == '__main__':
    generate_list_of_function_words("function_words.txt", "corpus.py")