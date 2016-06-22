#!/usr/bin/python -tt

import urllib2, time
from urlparse import urlparse,urljoin
from webcorpus import WebCorpus
from bs4 import BeautifulSoup

def get_html_doc(url):
    try:
        return urllib2.urlopen(url).read()
    except:
        return {'error': -1}

def no_hash(href):
    return href and href[0] != '#'

def get_all_links(page, soup):
    out_links = set([])
    links = set( soup('a', href=no_hash) ) # or soup.find_all('a')
    for link in links:
        out_link = link.get('href').strip()
        out_link = '%20'.join( out_link.split() )
        out_link = urljoin(page, out_link)
        out_link = out_link.split('#')[0]
        out_links.add(out_link)
    return list( out_links )

def add_to_index(index, keyword, url):
    if len(keyword) <= 2:
        return
    if keyword in index:
        if url not in index[keyword]:
            index[keyword].append(url)
    else:
        index[keyword] = [url]

def split_string(source, splitlist):
    output = []
    atsplit = True
    for char in source:
        if char in splitlist:
            atsplit = True
        else:
            if atsplit:
                output.append(char)
                atsplit = False
            else:
                output[-1] = output[-1] + char
    return output # don't forget to return!

slist = [' ', '.', ',', ';', "'", '"', '-', '_', '+', '=', '(', ')',
'[', ']', '{', '}', ':', '/', '\\', '|', '<', '>', '*', '&', '%', '$',
'@', '#', '!', '~', '`', '?']
def add_page_to_index(index, url, content):
    content = content.lower()
    for keyword in split_string(content, slist):
        add_to_index(index, keyword, url)

def crawl_web(seed_page, max_pages):
    scheme = urlparse(seed_page)[0]
    if scheme not in ['http', 'https']:
        seed_page = 'http://' + seed_page
    tocrawl = set( [seed_page] )
    crawled = set()
    index = {}
    graph = {}
    starting = True
    while tocrawl:
        page = tocrawl.pop()
        if page not in crawled and len(crawled) < max_pages:
            if not starting:
                if page.find('localhost') or page.find('127.0.0.1'):
                    # Don't sleep if you have a super computer and/or you
                    # love your fan's sound
                    time.sleep(2)
                    # print 'waiting 2 secs...'
                else:
                    time.sleep(5) # secs
                    # print 'waiting 5 secs...'
            starting = False
            html_doc = get_html_doc(page)
            if type(html_doc) == dict:
                print "Can't crawl %s" % page
                continue
            print 'Crawling %s' % page
            soup = BeautifulSoup(html_doc, 'lxml')
            outlinks = get_all_links(page, soup)
            for outlink in outlinks:
                print '\t %s' % outlink
            add_page_to_index(index, page, soup.get_text())
            graph[page] = outlinks
            tocrawl.update(outlinks)
            crawled.add(page)
            if tocrawl:
                print
    return WebCorpus(index, graph)

def compute_ranks(webcorpus, numloops):
    d = 0.8 # damping factor

    graph = webcorpus.graph
    ranks = {}
    npages = len(graph)
    for page in graph:
        ranks[page] = 1.0 / npages # don't forget the .

    for i in range(0, numloops):
        newranks = {}
        for page in graph:
            newrank = (1 - d) / npages
            for node in graph:
                if page in graph[node]:
                    newrank += d * (ranks[node] / len(graph[node]))
            newranks[page] = newrank
        ranks = newranks
    return ranks
