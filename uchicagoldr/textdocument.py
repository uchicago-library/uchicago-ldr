from uchicagoldr.item import Item
from re import escape, split


class TextDocument(Item):
    """
    A sublass of the item class, meant to potentially aid with text analysis
    """
    unique_terms = []
    terms = []
    term_counts = []

    def __init__(self, path, root):
        Item.__init__(self, path, root)

    def find_terms(self):
        with open(self.filepath, 'r', errors='replace') as f:
            fileString = f.read()
        fileString = fileString.lower()
        regexPattern = '|'.join(map(escape, [" ", "\n", ".", ",", ";", "'",
                                             "-", "\t", "?", "!", '(', ')',
                                             '[', ']', '\\']))
        splitString = split(regexPattern, fileString)
        return splitString

    def set_terms(self, newTerms):
        self.terms = newTerms

    def get_terms(self):
        return self.terms

    def find_unique_terms(self):
        assert(self.terms)
        uniqueTerms = set(self.terms)
        return uniqueTerms

    def set_unique_terms(self, newUnique):
        self.unique_terms = newUnique

    def get_unique_terms(self):
        return self.unique_terms

    def find_term_counts(self):
        assert(self.terms)
        counts = []
        uniques = self.find_unique_terms()
        for term in uniques:
            counts.append((term, self.terms.count(term)))
        return counts

    def set_term_counts(self, newCounts):
        self.term_counts = newCounts

    def get_term_counts(self):
        return self.term_counts
