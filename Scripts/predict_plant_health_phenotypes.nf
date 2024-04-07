#!/usr/bin/env nextflow

nextflow.enable.dsl=2

params.path_to_genomes = '<path_to_the_holding_the_fasta_genome_assemblies>'
params.outDir = '<output_file_path>'
params.scripts_folder = '<path_to_your_Scripts_folder>'

process create_input_list {
    publishDir params.outDir, mode: 'copy'

    output:
    path "input_list.txt"

    script:
    """
    ls ${params.path_to_genomes}/*.fasta > input_list.txt
    """
}

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

workflow {
    list_file_results = create_input_list()
    fsm_kmers_results = run_fsm_lite(list_file_results)
    kmers_table_results = parse_kmers(fsm_kmers_results)
    merged_table_results = merge_datasets(kmers_table_results)
    trained_model_results = train_model(merged_table_results)
}
