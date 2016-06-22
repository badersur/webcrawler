#!/usr/bin/python -tt

class WebCorpus(object):
    """
    WebCorpus that encapsulates index and graph of the crawler!
    """

    def __init__(self, index, graph):
        self.index = index
        self.graph = graph

    def __str__(self):
        return "WebCorpus Object!"
