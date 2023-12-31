<img src="publication_header.png" width="400">

This repository contains the machine learning model, scripts, and data for predicting Pseudomonas syringae virulence in beans using gradient boosted decision trees.

## Installation requirements

1. fsm-lite: https://github.com/nvalimak/fsm-lite
2. Python3 libraries:

`$ pip3 install pandas`<br>
`$ pip3 install numpy`<br>
`$ pip3 install rpy2`<br>
`$ pip3 install xgboost`<br>
`$ pip3 install sklearn`<br>

## Model training

This script uses Scikit-learn to train gradient boosted models to predict virulence/plant weight phenotypes based on whole-genome data from bacterial genomes.

`$ python3 stratified_rf_regressor_xgboost.py`<br>

## Model prediction

This script uses Scikit-learn to predict virulence/plant weight phenotypes based on whole-genome data from bacterial genomes.

`$ python3 predict_with_rg_regressor_xgboost.py`<br>

## Input files

* cluster_phenotypes_kmers.rds: input table for model training in RDS format containing phenotype/plant weight values and presence and absence of kmers for the 318 isolates used in the study. Format:

> Sample_ID, Phenotype_value, kmer_pattern_1, ..., kmer_pattern_2053163

* model7.model: final gradient boosted model for predicting virulence/plant weight phenotypes.
