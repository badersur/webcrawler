#!/usr/bin/python -tt

def lookup_best(keyword, webcorpus, ranks):
    """ returns sorted [] of urls. """
    if keyword in webcorpus.index:
        urls = webcorpus.index[keyword]
        # both correct
        # return sorted(urls, key=lambda rank: ranks[rank])
        return sorted(urls, key=ranks.__getitem__, reverse=True)
    return None

def lucky_search(keyword, webcorpus, ranks):
    """ returns a url with the highest rank. """
    best = lookup_best(keyword, webcorpus, ranks)
    return best[0] if best else None
