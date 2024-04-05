import sys
import re

#this keeps track of k-mers which have identical sample distributions
kmer_dict = {}
samp_kmer = {}
k_num = 0
k_max = 0

infile = open(sys.argv[1], 'r')

for l in infile:
	l = l.rstrip()
	l = re.sub(':[0-9]+', '', l)
	[kmer, samp] = re.split(' \| ', l)
	
	if str(samp) not in kmer_dict:
		k_max += 1
		kmer_dict.update({str(samp) : [k_max, kmer]})
		k_num = k_max
	else:
		k_num = kmer_dict[str(samp)][0]
		kmer_dict[str(samp)].append(kmer)
	
		
	for s in re.split(' ', samp):
		if s not in samp_kmer:
			samp_kmer.update({s : {k_num : 1}})
		else:
			samp_kmer[s].update({k_num : 1})

infile.close()

kmer_out = open('./kmer_map.txt', 'w')

#print out mapping table of k-mer patterns
k_list = []

for k,v in kmer_dict.items():
	k_num = v.pop(0)
	print('pat_' + str(k_num), v, sep='\t', file=kmer_out)
	
	k_list.append(k_num)
	
table_out = open('./samp_kmer_table.txt', 'w')
				 


print('samp_id', '\tpat_'.join(map(str, range(1,k_max+1))), sep='\tpat_', file=table_out)

for samp in samp_kmer:
	pres = []
	for kmer in k_list:
		if kmer in samp_kmer[samp]:
			pres.append('1')
		else:
			pres.append('0')
	
	print(samp, '\t'.join(pres), sep='\t', file=table_out)

table_out.close()
kmer_out.close()

print('./samp_kmer_table.txt', './kmer_map.txt', sep='\n')
