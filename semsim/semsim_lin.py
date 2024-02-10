from onto.pathbuilder import PathBuilder
from semsim.semsim import SemSim


class SemLin(SemSim):

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
            ic1 = 0.0
            ic2 = 0.0
            icLCS = 0.0

            if term1 in self.icData:
                ic1 = self.icData[term1]
            if term2 in self.icData:
                ic2 = self.icData[term2]
            if lcs in self.icData:
                icLCS = self.icData[lcs]

            if not useIC:
                if term1 in self.specData:
                    ic1 = self.specData[term1]
                if term2 in self.specData:
                    ic2 = self.specData[term2]
                if lcs in self.specData:
                    icLCS = self.specData[lcs]

            if (ic1 != 0.0) or (ic2 != 0.0):
                sim = (2 * icLCS) / (ic1 + ic2)
        return sim
