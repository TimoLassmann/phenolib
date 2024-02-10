class OntoPath:
    terms = []

    def __init__(self, newTerms=None):
        self.terms = []
        if newTerms:
            self.terms.extend(newTerms)

    def getTerms(self):
        return self.terms

    def setTerms(self, newTerms):
        self.terms = newTerms

    def toString(self):
        s = ''
        for term in self.terms:
            s += term + '-'
        return s[0: len(s) - 1]
