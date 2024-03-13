import argparse
import os
import sys

from onto.ontopathsloader import OntoPathsLoader
from onto.ontoreader import OntoReader
from semsim.semsim_lin import SemLin
from semsim.semsin_resnik import SemResnik

current_dir = os.path.dirname(os.path.abspath(__file__))

DEFAULT_HPO_FILE = current_dir + "/resources/hp.obo"
DEFAULT_PATHS_FILE = current_dir + "/resources/hp_paths.list"
DEFAULT_IC_FILE = current_dir + "/resources/hp_ic.list"
DEFAULT_SPEC_FILE = current_dir + "/resources/hp_spec.list"


class ModelsList:
    modelsData = []
    ontoReader = None

    semSims = {}
    ontoPathsMap = {}
    icData = {}
    specData = {}

    def __init__(
        self,
        modelsFile,
        hpoFile=DEFAULT_HPO_FILE,
        ontoPathsFile=DEFAULT_PATHS_FILE,
        hpICFile=DEFAULT_IC_FILE,
        hpSpecFile=DEFAULT_SPEC_FILE,
    ):
        self.ontoReader = OntoReader(hpoFile)

        self.loadPrerequisites(ontoPathsFile, hpICFile, hpSpecFile)

        self.modelsData = []
        self.readModelsFile(modelsFile)

    def loadPrerequisites(self, ontoPathsFile, hpICFile, hpSpecFile):
        self.ontoPathsMap = OntoPathsLoader(ontoPathsFile).getOntoPathsMap()
        self.icData = self.loadData(hpICFile)
        self.specData = self.loadData(hpSpecFile)

        self.semSims = {
            "resnik": SemResnik(self.ontoPathsMap, self.icData, self.specData),
            "lin": SemLin(self.ontoPathsMap, self.icData, self.specData),
        }

    def loadData(self, dataFile):
        with open(dataFile, "r") as fh:
            lines = fh.readlines()
        data = {}
        for line in lines:
            line = line.strip()
            if line:
                segs = line.split("\t")
                data[segs[0].strip()] = float(segs[1].strip())
        return data

    def readModelsFile(self, modelsFile):
        with open(modelsFile, "r") as fh:
            lines = fh.readlines()

        for line in lines:
            line = line.strip()
            segs = line.split("=")
            hpoId = segs[0]
            flag = segs[1]

            consolidatedHPOId = self.ontoReader.consolidate(hpoId)
            if not consolidatedHPOId:
                print("Term {} from the models file does not exist.".format(hpoId))
                continue

            if flag.lower() == 'y':
                self.modelsData.append(consolidatedHPOId)


    def getBestModelForTerm(self, term: str, semsim: str, useIC=True, threshold=0.0):
        if term in self.modelsData:
            return term, -1.0
        max = None
        maxVal = 0.0
        for entry in self.modelsData:
            semVal = self.semSims[semsim].compute(term, entry, useIC)
            if semVal >= threshold:
                if semVal > maxVal:
                    maxVal = semVal
                    max = entry

        if max:
            #print("Best model for term {} is: {} ({})".format(term, max, maxVal))
            return max, maxVal

        return None, None

    def getBestModelsForList(
        self, termList: [str], semsim: str, useIC=True, threshold=0.0
    ):
        result = {}
        for term in termList:
            max, maxVal = self.getBestModelForTerm(term, semsim, useIC, threshold)
            if max:
                result[term] = (max, maxVal)
        return result


def read_hpo_terms(file_path):
    with open(file_path, "r") as file:
        # Assuming all HPO terms are on a single line, separated by spaces
        line = file.readline().strip()
        # Split the line into HPO terms
        hpo_terms = line.split()
    return hpo_terms


# Call the function and get the list of HPO terms


def check_input_and_output_writability(input_file_path, output_file_path):
    # Check if the input file exists and is a file
    if os.path.exists(input_file_path) and os.path.isfile(input_file_path):
        print(f"Input file '{input_file_path}' exists.")
    else:
        print(f"Input file '{input_file_path}' does not exist or is not a file.")
        return False  # Early return if input file check fails

    # Check if the output file can be written
    output_dir = os.path.dirname(output_file_path) or "."
    if os.path.exists(output_file_path):
        # Check if the existing file is writable
        if os.access(output_file_path, os.W_OK):
            print(f"Output file '{output_file_path}' exists and is writable.")
            return True
        else:
            print(f"Output file '{output_file_path}' exists but is not writable.")
            return False
    else:
        # If the file does not exist, check if the directory is writable
        if os.path.exists(output_dir) and os.access(output_dir, os.W_OK):
            print(
                f"Output directory '{output_dir}' exists and is writable. File can be created."
            )
            return True
        else:
            print(
                f"Output directory '{output_dir}' does not exist or is not writable. File cannot be created."
            )
            return False


def main():
    parser = argparse.ArgumentParser(
        description="Script to compare the HPO ontology with presence of IMPPROVE models."
    )
    parser.add_argument(
        "--input",
        type=str,
        help="File containing patient specific HPO terms",
        required=True,
    )

    parser.add_argument(
        "--out",
        type=str,
        help="Output list of HPO terms having a model available.",
        required=True,
    )
    # parser.add_argument(
    #     "--hpo",
    #     type=str,
    #     help="Path to the HPO ontology file (hp.obo) .",
    #     required=True,
    # )
    parser.add_argument(
        "--modelmap",
        type=str,
        help="Path to model list.",
        required=True,
    )

    args = parser.parse_args()
    input_name = args.input
    outfile_name = args.out
    # hpo_file = args.hpo
    modelsListFile = args.modelmap

    if check_input_and_output_writability(input_name, outfile_name):
        print("Input and output parameters are ok. ")
    else:
        print(f"Either input {input_name} or output {outfile_name} is not accessible")
        sys.exit(1)

    hpo_terms = read_hpo_terms(input_name)
    print(hpo_terms)
    # modelsListFile = current_dir + "/resources/example_models.list"
    modelsList = ModelsList(modelsListFile)
    with open(outfile_name, 'w') as file:        
        for hpo in hpo_terms:
            try:
                max, maxVal = modelsList.getBestModelForTerm(hpo, 'lin')
                if max:
                    file.write("{},{}\n".format(max, maxVal))
                
            except Exception:
                file.write("{}\n".format(hpo))
                
            # max, maxVal = modelsList.getBestModelForTerm(hpo, 'lin')

            # if max:
            #     file.write("{},{}\n".format(max, maxVal))
                


if __name__ == "__main__":
    main()
