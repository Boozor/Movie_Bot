# -*- coding: utf-8 -*-

import ujson

dictionary = {}

def create_dict(arr):
    global dictionary
    for i in '#'.join(arr).split('BREAK'):
        a = [a for a in i.split('#') if a != '']
        if len(a) > 3:
            name = a[0].replace("'", "")
            if name not in dictionary:
                dictionary[name] = {}
                dictionary[name]['review'] = []
                dictionary[name]['review'].append((a[1], a[2], a[3]))
            else:
                dictionary[name]['review'].append((a[1], a[2], a[3]))

    with open('amazon2.json', 'w') as w:
        ujson.dump(dictionary, w)


def amazon_parser(filename='amazon_movies.txt'):

    with open(filename, 'rb') as f:
        count = 0
        arr = []

        for line in f:
            count += 1
            if count < 80000000:
                if line != b"\n":
                    if str(line).split(':')[0][2::] == 'product/productId':
                        arr.append(str(line).replace('\\n', '').split(': ')[1])
                    if str(line).split(':')[0][2::] == 'review/text':
                        arr.append(str(line).replace('\\n', '').split('review/text: ')[1])
                    if str(line).split(':')[0][2::] == 'review/helpfulness':
                        arr.append(str(line).replace('\\n', '').split(': ')[1])
                    if str(line).split(':')[0][2::] == 'review/score':
                        arr.append(str(line).replace('\\n', '').split(': ')[1])

                elif line == b"\n" or len(line) < 3:
                    arr.append('BREAK')
                    if count % 1000 == 0:
                        print(count)
                        create_dict(arr)
            else:
                break

    return arr


if __name__ == '__main__':
    # Transform crawled data into a normal format
    results = ujson.load(open('amazon_crawled_data.json'))

    lookup_dictionary = {}
    for l in results:
        lookup_dictionary[l['event_url'].split('/')[-1]] = l['event_title'][0].split(': ')[2]

    with open('lookup_dictionary.json', 'w') as w:
        ujson.dump(lookup_dictionary, w)

    print('Start with amazon')

    # Transform amazon keys
    amazon = ujson.load(open('amazon.json'))
    print(len(amazon.keys()))

    nice_amazon = {}

    for k in amazon:
        if k in lookup_dictionary:
            nice_amazon[lookup_dictionary[k]] = amazon[k]
        else:
            print(k)

    with open('clean_amazon.json', 'w') as w:
        ujson.dump(nice_amazon, w)

    nice_amazon2 = ujson.load(open('clean_amazon.json'))
    print(len(nice_amazon2.keys()))

    for k in nice_amazon2:
        print(k)
