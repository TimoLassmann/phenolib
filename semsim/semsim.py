class SemSim:
    ontoPathsMap = {}
    icData = {}
    specData = {}

    def __init__(self, ontoPathsMap, icData, specData):
        self.ontoPathsMap = ontoPathsMap
        self.icData = icData
        self.specData = specData

    def compute(self, term1, term2, useIC = True):
        raise NotImplementedError('Not implemented')