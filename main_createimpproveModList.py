import argparse
import os

# from os.path import join, abspath

from onto.ontoreader import OntoReader

# from onto.pathscreator import PathsCreator
# from precompute.informationcontent import InformationContent
# from precompute.specificity import Specificity

DEFAULT_HPO_FILE = "hp.obo"
DEFAULT_PATHS_FILE = "hp_paths.list"
DEFAULT_IC_FILE = "hp_ic.list"
DEFAULT_SPEC_FILE = "hp_spec.list"


class PreprocessAll:
    ontoReader = None

    def __init__(self, ontoFile="resources/" + DEFAULT_HPO_FILE):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        ontoFile = current_dir + "/" + ontoFile
        self.ontoReader = OntoReader(ontoFile)

    def createIMPPROVE_LIST(self, model_path: str = "", out: str = ""):
        print(" - Creating preprocessed data with default files ...")
        with open(out, "w") as result_file:
            for term in self.ontoReader.terms:
                # print(f"{term}")
                numeric_part = term.split(":")[-1].lstrip("0")

                # Construct the expected file name
                file_name = f"{numeric_part}.jlso"
                # print(f"{term} -> {file_name}")
                file_exists = os.path.isfile(os.path.join(model_path, file_name))
                # Write the result to the file
                # print(f"{term}={'Y' if file_exists else 'N'}")
                result_file.write(f"{term}={'Y' if file_exists else 'N'}\n")


def main():
    parser = argparse.ArgumentParser(
        description="Script to compare the HPO ontology with presence of IMPPROVE models."
    )
    parser.add_argument(
        "--dir",
        type=str,
        help="Directory where the model files are supposed to be located",
        required=True,
    )

    parser.add_argument(
        "--out",
        type=str,
        help="Output file name.",
        required=True,
    )
    args = parser.parse_args()
    model_path = os.path.abspath(args.dir)
    outfile_name = args.out
    print(f"{model_path}")
    preprocessAll = PreprocessAll()
    preprocessAll.createIMPPROVE_LIST(model_path, outfile_name)


if __name__ == "__main__":
    main()
