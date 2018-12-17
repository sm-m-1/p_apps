import re
def generate_list_of_function_words(old_file, new_file):
    '''\
    Read a list of names from a file line by line into an output file.
    If a line begins with a particular name, insert a string of text
    after the name before appending the line to the output file.
    '''

    size = 0
    new_words = []
    with open(old_file, 'r') as read_file:
        for line in read_file:
            sentence = read_file.readline().rstrip()
            words = re.findall("[a-z']+", sentence)
            for word in words: new_words.append(word)

    with open(new_file, 'w', encoding='utf-8') as write_file:
        variable_name = "FUNCTION_WORDS = {\n"
        write_file.write(variable_name)
        for word in new_words:
            write_file.write("  " + '"{}",\n'.format(word))

        write_file.write("}\n")

if __name__ == '__main__':
    generate_list_of_function_words("function_words.txt", "function_words.py")