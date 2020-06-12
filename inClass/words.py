'''
1. translate to Graph problem
2. build Graph
3. do search
'''
import string
from util import Queue


class Graph:
    def __init__(self, words):
        self.nodes = {}
        self.build_graph(words)

    def build_graph(self, words):
        letters = list(string.ascii_lowercase)
        for i, w in enumerate(words):
            self.nodes[w] = []
            word_letters = list(w)
            # itterate through the word
            for j in range(len(word_letters)):
                # loop through all letters to try swapping
                for l in letters:
                    t = list(word_letters)
                    t[j] = l
                    w_new = ''.join(t)
                    # check to see if the word is a valid one
                    if w_new != w and w_new in word_set:
                        self.nodes[w].append(w_new)

    def find_word_path(self, starting, ending):

        paths = {starting: [starting]}
        q = Queue()
        q.enqueue((starting, None))
        n = None
        while q.size() > 0:
            n, t = q.dequeue()
            if n not in paths:
                paths[n] = paths[t] + [n]
                for x in self.nodes[n]:
                    q.enqueue((x, n))
            elif n == starting:
                for x in self.nodes[n]:
                    q.enqueue((x, n))
        if ending in paths:
            return paths[ending]
        else:
            return 'No Path Found'


if __name__ == '__main__':
    word_set = set()
    with open('words.txt', 'r') as f:
        for line in f:
            line = line.strip()
            word_set.add(line.lower())
    g = Graph(list(word_set))

    print(g.find_word_path('fast', 'slow'))
