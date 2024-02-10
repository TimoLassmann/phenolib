from onto.pathbuilder import PathBuilder
from semsim.semsim import SemSim


class SemResnik(SemSim):

    def compute(self, term1, term2, useIC=True):
        sPaths = self.ontoPathsMap[term1]
        dPaths = self.ontoPathsMap[term2]
        pathBuilder = PathBuilder(term1, term2)
        pathBuilder.build(sPaths, dPaths)
        paths = pathBuilder.getAllPaths()

        lcs = None
        shortestPath = 100000
        for ancestor in paths:
            pathSize = len(paths[ancestor])
            if pathSize < shortestPath:
                shortestPath = pathSize
                lcs = ancestor

        sim = 0.0
        if lcs:
            if lcs in self.icData:
                sim = self.icData[lcs]

            if not useIC:
                if lcs in self.specData:
                    sim = self.specData[lcs]
        return sim
