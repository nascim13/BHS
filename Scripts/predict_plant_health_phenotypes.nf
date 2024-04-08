#!/usr/bin/env nextflow

nextflow.enable.dsl=2

params.path_to_genomes = '<path_to_the_holding_the_fasta_genome_assemblies>'
params.outDir = '<output_file_path>'
params.scripts_folder = '<path_to_your_Scripts_folder>'
params.input_for_predictions = '<path_to_input_file_for_predictions.txt'

// This block generates an input list for FSM-lite containing the pathogen genomes of interest
process create_input_list {
    publishDir params.outDir, mode: 'copy'

    output:
    path "input_list.txt"

    script:
    """
    ls ${params.path_to_genomes}/*.fasta > input_list.txt
    """
}

// This block splits the genome sequences into unique kmers (length = 31) and records their distributions
process run_fsm_lite {
    publishDir params.outDir, mode: 'copy'
	
    clusterOptions = '-l select=1:ncpus=1:mem=100gb,walltime=12:00:00'

    input:
    path(list_file)

    output:
    path "fsm_kmers.txt"

    script:
    """
    fsm-lite -l ${list_file} -m 31 -M 31 -v -t fsm_kmers.tmp > fsm_kmers.txt
    """
}

// This block removes redudancy and parses the FSM-lite output into a table format 
process parse_kmers {
    publishDir "${params.outDir}", mode: 'copy'

    clusterOptions = '-l select=1:ncpus=1:mem=100gb,walltime=01:00:00'

    input:
    path(kmers)

    output:
    path "samp_kmer_table.txt"

    script:
    """
    python3 ${params.scripts_folder}/kmer_table_make.py ${kmers}
    """
}

// This block merges phenotype and genotype data and saves them into RDS for faster loading
process merge_datasets {
     publishDir params.outDir, mode: 'copy'

     clusterOptions = '-l select=1:ncpus=1:mem=100gb,walltime=48:00:00'

     input:
     path(kmer_table)

     output:
     path "feature_labels_table.rds"

     script:
     """
     Rscript /${params.scripts_folder}/merge_phenotype_kmers.R ${kmer_table}
     """
}

// This block trains a gradient boosting model using kmer patterns as features and plant weight phenotypes as labels
process train_model {
     publishDir params.outDir, mode: 'copy'
     clusterOptions = '-l select=1:ncpus=1:mem=100gb,walltime=48:00:00'

     input:
     path(merged_table)

     output:
     path "stratified_results.txt"

     script:
     """
     python3 ${params.scripts_folder}/stratified_rf_regressor_xgboost.py ${merged_table}
     """
}

// This block predicts plant weight phenotypes from new genomes
process make_predictions {
     publishDir params.outDir, mode: 'copy'
     clusterOptions = '-l select=1:ncpus=1:mem=100gb,walltime=12:00:00'

     input:
     path(models)

     output:
     path "plant_weight_predictions.txt"

     script:
     """
     python3 /srv/scratch/cking/ralmeida/PhD/Scripts/predict_plant_health_phenotypes.py ${params.input_for_predictions}
     """
}

// This block runs the workflow
workflow {
    list_file_results = create_input_list()
    fsm_kmers_results = run_fsm_lite(list_file_results)
    kmers_table_results = parse_kmers(fsm_kmers_results)
    merged_table_results = merge_datasets(kmers_table_results)
    trained_model_results = train_model(merged_table_results)
    prediction_results = make_predictions(trained_model_results)
}
