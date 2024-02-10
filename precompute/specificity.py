import math


class Specificity:
    ontoReader = None
    specData = {}

    def __init__(self, ontoReader):
        self.specData = {}
        self.ontoReader = ontoReader
        self.indexSpecificity()

    def indexSpecificity(self):
        leaves = {}
        for term in self.ontoReader.subClasses:
            if not self.ontoReader.subClasses[term]:
                leaves[term] = 0

        for term in self.ontoReader.terms:
            noLeaves = 0
            subsumers = 1
            if term in self.ontoReader.allSuperClasses:
                subsumers = len(self.ontoReader.allSuperClasses[term]) + 1

            for subclsURI in self.ontoReader.allSubClasses[term]:
                if subclsURI in leaves:
                    noLeaves += 1

            num = ((float(noLeaves)) / (float(subsumers))) + 1.0
            self.specData[term] = -math.log2(num / (len(leaves) + 1))

    def serialize(self, outFile):
        lines = []
        for term in self.specData:
            lines.append(term + '\t' + str(round(self.specData[term], 5)))

        with open(outFile, 'w') as fh:
            fh.write('\n'.join(lines))
