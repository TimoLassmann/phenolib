import math


class InformationContent:
    ontoReader = None
    icData = {}

    def __init__(self, ontoReader):
        self.icData = {}
        self.ontoReader = ontoReader
        self.indexIC()

    def indexIC(self):
        for term in self.ontoReader.terms:
            count = 0
            if term in self.icData:
                count = self.icData[term]
            count += 1
            self.icData[term] = count

            if term in self.ontoReader.allSuperClasses:
                for superCls in self.ontoReader.allSuperClasses[term]:
                    count = 0
                    if superCls in self.icData:
                        count = self.icData[superCls]
                    count += 1
                    self.icData[superCls] = count

    def serialize(self, outFile):
        lines = []
        for term in self.icData:
            ic = round(-math.log2(self.icData[term] / len(self.ontoReader.terms)), 5)
            lines.append(term + '\t' + str(ic))

        with open(outFile, 'w') as fh:
            fh.write('\n'.join(lines))
