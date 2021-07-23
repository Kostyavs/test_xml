import re


def my_text_gen(text):
    for string in text:
        yield string


def xml_to_dict2(text_gen):
    dictionary = {}
    value_list = []
    for string in text_gen:
        key = re.search(r'<([^/][\s\S]*?)>', string)
        key = key.group(1)
        if re.search(r'</' + key + '>', string):
            value = re.search(r'<' + key + '>([\s\S]*?)</' + key + '>', string)
            value = value.group(1)
            if key in dictionary:
                if type(dictionary[key]) == str:
                    dictionary[key] = [dictionary[key], value]
                else:
                    dictionary[key].append(value)
            else:
                dictionary[key] = value
        else:
            for string2 in text_gen:
                if re.search(r'</' + key + '>', string2):
                    new_gen = my_text_gen(value_list)
                    value_list = []
                    dictionary[key] = xml_to_dict2(new_gen)
                    break
                else:
                    value_list.append(string2)
    return dictionary


if __name__ == '__main__':
    text = open('file.xml').readlines()
    text_gen = my_text_gen(text)
    result = xml_to_dict2(text_gen)
    print('result: ', result)
