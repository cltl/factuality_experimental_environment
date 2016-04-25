# Factuality: experimental setup

This repository contains various scripts (and some data) for running experiments on factuality classifiers.
The setup is designed for modules using NAF and evaluation data annotated with the CAT tool.
The current version supports experiments on the NewsReader MEANTIME corpus.


## Gold corpus

As mentioned above, the current code was used with the NewsReader MEANTIME corpus. The corpus can be downloaded from:

http://www.newsreader-project.eu/results/data/wikinews/

We used the corpora under intra_cross-doc_annotation/ to create as a gold (these corpora were also used to get the tokens and raw for the input NAF files).


## Scripts for creating NAF input. 

In order to make sure tokens correspond between system output and annotated data, we run our system on the tokens from the gold annotations.

Scripts:
 * create_naftoks_from_cat.py creates a NAF-file with a token layer based on the CAT tokens
 * generate_raw_from_tokens.py adds a NAF-raw layer to the NAF file based on the NAF tokens

Creating a NAF input corpus with token layer from a CAT corpus:

1. python create_naftoks_from_cat.py CATdir NAFdir
2. python generate_raw_from_tokens.py NAFindir NAFoutdir

NB: 
1. create_naftoks_from_cat.py keeps the original file names from CAT. generate_raw_from_tokens.py adds a .naf suffix
2. These input corpora can also be used for preparing data for other evaluation tasks (they just create a raw and token layer based on the gold).

## Factuality input

We ran the NewsReader pipeline version 3.0 from the token layer upto (and not including) the factuality module.
This corpus contains all layers and relevant information to run the factuality module for evaluation.

## Factuality evaluation

Scripts:
 * conversion_scripts/naf_to_cat_factuality.py takes a NAF file as input and creates a CAT file with EVENT_MENTION and factuality values.
 * scorer_based_on_CAT_EVENTI_2014/scorer_CAT_v4.py compares the output of two directories calculating the matching events and factuality values

1. Create CAT files from NAF output:

python naf_to_cat_factuality.py NAFdir CATdir

2: Run evaluation script (from the directory where list_class_att is located)

python scorer_CAT.py folder_gold/ folder_system/ list_class_att

NB: the names of the CATfiles created by naf_to_cat_factuality.py correspond to the NAF files minus the .naf suffix. If your files where generated with the scripts for preparing input data and you used the same filename for input and output while running the pipeline, your system names and gold names should be identical. If not: please make sure they are.

## Corpora

For convenience, we provide the NAF input files of the pipeline (NAFpipelineInput/) and the NAF input files for factuality modules (NAFfactualityInput/).
These files have been created following the procedures outlined above.

The corpora folder is structured as follows:

corpora/MEANTIME/language/NAFpipelineInput/
corpora/MEANTIME/language/NAFfactualityInput/

## Further information

For comments and questions, please contact:

antske.fokkens@vu.nl

 
