from onto.ontopath import OntoPath


class OntoPathsLoader:
    ontoPathsMap = {}

    def __init__(self, ontoPathsFile):
        self.ontoPathsMap = {}
        with open(ontoPathsFile, 'r') as fh:
            lines = fh.readlines()
        for line in lines:
            line = line.strip()
            self.loadPath(line)

    def loadPath(self, line):
        terms = line.split('-')
        for term in terms:
            lst = []
            if term in self.ontoPathsMap:
                lst = self.ontoPathsMap[term]
            lst.append(OntoPath(terms))
            self.ontoPathsMap[term] = lst

    def getOntoPathsMap(self):
        return self.ontoPathsMap
