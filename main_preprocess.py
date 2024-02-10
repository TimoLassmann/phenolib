from os.path import join

from onto.ontoreader import OntoReader
from onto.pathscreator import PathsCreator
from precompute.informationcontent import InformationContent
from precompute.specificity import Specificity

DEFAULT_HPO_FILE = 'hp.obo'
DEFAULT_PATHS_FILE = 'hp_paths.list'
DEFAULT_IC_FILE = 'hp_ic.list'
DEFAULT_SPEC_FILE = 'hp_spec.list'


class PreprocessAll:
    ontoReader = None

    def __init__(self, ontoFile='resources/' + DEFAULT_HPO_FILE):
        self.ontoReader = OntoReader(ontoFile)

    def createOntoPaths(self, hpoPathsFile):
        print(' - Creating paths data in [{}] ...'.format(hpoPathsFile))
        pathsCreator = PathsCreator(self.ontoReader)
        pathsCreator.serialize(hpoPathsFile)

    def createICData(self, icDataFile):
        print(' - Creating IC data in [{}] ...'.format(icDataFile))
        informationContent = InformationContent(self.ontoReader)
        informationContent.serialize((icDataFile))

    def createSpecData(self, specDataFile):
        print(' - Creating specificity data in [{}] ...'.format(specDataFile))
        specificity = Specificity(self.ontoReader)
        specificity.serialize((specDataFile))

    def createAllWithDefaults(self):
        print(' - Creating preprocessed data with default files ...')
        self.createOntoPaths(join('resources', DEFAULT_PATHS_FILE))
        self.createICData(join('resources', DEFAULT_IC_FILE))
        self.createSpecData(join('resources', DEFAULT_SPEC_FILE))


def main():
    preprocessAll = PreprocessAll()
    preprocessAll.createAllWithDefaults()


if __name__ == '__main__':
    main()
