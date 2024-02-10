from onto.ontopath import OntoPath
from onto.term2termpath import Term2TermPath


class PathBuilder:
    allPaths = {}

    curie1 = None

    curie2 = None

    def __init__(self, curie1, curie2):
        self.curie1 = curie1
        self.curie2 = curie2
        self.allPaths = {}

    def getAllPaths(self):
        return self.allPaths

    def reversePath(self, path):
        lst = []
        lst.extend(path)
        lst.reverse()
        return lst

    def do_hash(self, path):
        sHash = ''
        if not path:
            return sHash

        for s in path:
            sHash += s + '-'

        return sHash[0: len(sHash) - 1]

    def build(self, sPaths: [OntoPath], dPaths: [OntoPath]):
        for path in sPaths:
            index1 = path.getTerms().index(self.curie1)
            index2 = -1
            if self.curie2 in path.getTerms():
                index2 = path.getTerms().index(self.curie2)

            if index1 == index2:
                currentBranch = []
                currentBranch.append(self.curie1)

                newPath = Term2TermPath(self.curie1, currentBranch, [])
                noPaths = []
                noPaths.append(newPath)
                self.allPaths[self.curie1] = noPaths
            else:
                subPath = path.getTerms()[0: index1 + 1]
                self.processNonRootBasedAncestor(subPath, dPaths)

    def processNonRootBasedAncestor(self, sSubPath, dPaths):
        for path in dPaths:
            index = path.getTerms().index(self.curie2)
            subPath = path.getTerms()[0: index + 1]
            ancestorIndexInSubPath = -1
            ancestor = None
            for uri in sSubPath:
                if uri in subPath:
                    idx = subPath.index(uri)
                    if idx > ancestorIndexInSubPath:
                        ancestorIndexInSubPath = idx
                        ancestor = uri
            if ancestorIndexInSubPath != -1:
                rightBranch = subPath[ancestorIndexInSubPath: index + 1]
                idx = sSubPath.index(ancestor)
                leftBranch = self.reversePath(sSubPath[idx + 1: len(sSubPath)])
                existingPaths = []
                if ancestor in self.allPaths:
                    existingPaths = self.allPaths[ancestor]
                found = False
                for existingPath in existingPaths:
                    if existingPath.hasBranches(self.do_hash(leftBranch), self.do_hash(rightBranch)):
                        found = True
                        break
                if not found:
                    newPath = Term2TermPath(ancestor, leftBranch, rightBranch)
                    existingPaths.append(newPath)
                    self.allPaths[ancestor] = existingPaths
