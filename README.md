<img src="publication_header.png" width="400">

This repository contains the complete workflow for reproducing the findings in "Predictive modeling of Pseudomonas syringae virulence on bean using gradient boosted decision trees" (doi: 10.1371/journal.ppat.1010716).

## Installation requirements

1. fsm-lite: https://github.com/nvalimak/fsm-lite
2. Python3 libraries:

`$ pip3 install pandas`<br>
`$ pip3 install numpy`<br>
`$ pip3 install rpy2`<br>
`$ pip3 install xgboost`<br>
`$ pip3 install sklearn`<br>

## Running the workflow

The Nextflow script is available under the "Scripts" folder, alongside other Python and R scripts required for successfully running the workflow. The workflow was designed for PBS HPC systems. SLURM users may need to adjust the workflow cluster options.

`$ nextflow run predict_plant_health_phenotypes.nf -profile <your_HPC_profile>`<br>

## Model prediction

This script uses Scikit-learn to predict virulence/plant weight phenotypes based on whole-genome data from bacterial genomes.
