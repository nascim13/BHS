import sys
import re

# Initialize dictionaries to track k-mers and their sample distributions
kmer_dict = {}  # Maps sample distributions to a unique identifier and associated k-mers
samp_kmer = {}  # Maps samples to their k-mers
k_num = 0  # Current identifier for a unique k-mer pattern
k_max = 0  # Maximum identifier assigned, ensuring each pattern has a unique identifier

# Open input file for reading; filename is provided as a command line argument
infile = open(sys.argv[1], 'r')

# Process each line in the input file
for l in infile:
    l = l.rstrip()  # Remove trailing whitespace/newlines
    l = re.sub(':[0-9]+', '', l)  # Remove colon followed by numbers (e.g., counts)
    [kmer, samp] = re.split(' \| ', l)  # Split each line into k-mer and sample information
    
    # Check if this sample distribution is new
    if str(samp) not in kmer_dict:
        k_max += 1  # Assign a new unique identifier
        kmer_dict.update({str(samp): [k_max, kmer]})
        k_num = k_max
    else:
        # If not new, retrieve its identifier and add the k-mer to the existing list
        k_num = kmer_dict[str(samp)][0]
        kmer_dict[str(samp)].append(kmer)
    
    # Update the samp_kmer dictionary with samples and their k-mer identifiers
    for s in re.split(' ', samp):
        if s not in samp_kmer:
            samp_kmer.update({s: {k_num: 1}})
        else:
            samp_kmer[s].update({k_num: 1})

infile.close()  # Close the input file

# Open output file for writing the k-mer pattern mapping
kmer_out = open('./kmer_map.txt', 'w')

# List to keep track of all unique k-mer pattern identifiers
k_list = []

# Print out the mapping table of k-mer patterns to the kmer_out file
for k, v in kmer_dict.items():
    k_num = v.pop(0)  # Extract and remove the identifier from the list
    print('pat_' + str(k_num), v, sep='\t', file=kmer_out)
    k_list.append(k_num)

# Open another output file for writing the sample to k-mer pattern presence table
table_out = open('./samp_kmer_table.txt', 'w')

# Print the header row with pattern identifiers
print('samp_id', '\tpat_'.join(map(str, range(1, k_max+1))), sep='\tpat_', file=table_out)

# For each sample, determine the presence (1) or absence (0) of each k-mer pattern
for samp in samp_kmer:
    pres = []  # List to hold presence or absence indicators
    for kmer in k_list:
        if kmer in samp_kmer[samp]:
            pres.append('1')
        else:
            pres.append('0')
    
    # Print the sample and its k-mer pattern presence/absence to the table_out file
    print(samp, '\t'.join(pres), sep='\t', file=table_out)

# Close both output files
table_out.close()
kmer_out.close()

# Print the names of the output files generated
print('./samp_kmer_table.txt', './kmer_map.txt', sep='\n')
