from onto.HP import ROOT
from onto.ontopath import OntoPath


class PathsCreator:
    ontoReader = None
    maxDepth = 0
    visited = []
    ontoPaths = []

    def __init__(self, ontoReader):
        self.ontoReader = ontoReader
        self.maxDepth = 0
        self.visited = []
        self.ontoPaths = []
        self.subclasses = {}
        self.createPath(ROOT, [])

    def createPath(self, uri, currentPath):
        subCls = self.ontoReader.subClasses[uri]
        currentPath.append(uri)

        if uri in self.visited:
            ontoPath = OntoPath(currentPath)
            self.ontoPaths.append(ontoPath)
            if len(currentPath) > self.maxDepth:
                self.maxDepth = len(currentPath)
            currentPath.remove(uri)
            return
        self.visited.append(uri)

        if len(subCls) != 0:
            for child in subCls:
                self.createPath(child, currentPath)
        else:
            ontoPath = OntoPath(currentPath)
            self.ontoPaths.append(ontoPath)
            if len(currentPath) > self.maxDepth:
                self.maxDepth = len(currentPath)
        currentPath.remove(uri)

    def serialize(self, outFile):
        lines = []
        for ontoPath in self.ontoPaths:
            lines.append(ontoPath.toString())

        with open(outFile, 'w') as fh:
            fh.write('\n'.join(lines))
