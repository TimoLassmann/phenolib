# phenolib

Phenolib is a small library to compute semantic similarity between HPO terms.

All resources needed for computation are under `resources` - including a version of HPO from Feb 2024.

Two main methods are provided:
* `main_preprocess` - should be used when updating the version of HPO. This computes all prerequisites for the
semantic similarity metrics, as currently the library does not support having them computed on the fly; 
it would also be a lot slower; Make sure to adjust the file paths appropriately before re-running this.
* `main_modelslist` - assumes the need to find the most similar HPOs given a list of HPO terms that have models.
The models file used in the script is exemplified in `resources/example_models.list`.
Several options are provided by the 2 methods included in the script:
  * the semantic similarity to be used - currently 'resnik' and 'lin'
  * the use of information content or specificity as base metrics for computing the similarity measures
  * a threshold value to make things quicker.