#!/usr/bin/python -tt

from crawler import crawl_web, compute_ranks
from search import lucky_search, lookup_best

wc = crawl_web('localhost', 200)
ranks = compute_ranks(wc, 50)

print 'Enter 0 to exit.'
while True:
    user_input = raw_input("Enter: keyword any_number_for_lucky_search [e.g. php]: ")
    if user_input:
        input = user_input.split()
        word = input[0]
        option = 1 if len(input) == 1 else 2
        if word == '0':
            break
        if option == 1:
            results = lookup_best(word, wc, ranks)
            if results:
                for result in results[:25]:
                    print result, '\t'*4, ranks[result]
            else:
                print 'No results!'
        else:
            print lucky_search(word, wc, ranks) or 'Not lucky! -_-'
    print

print '\nThanks for using me!'