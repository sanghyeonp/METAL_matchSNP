"""
Sanghyeon Park
2021.12.07

If there is any problem or suggestion, please contact. Thanks!
T: 010-8767-7043
E: sh.austin.park@gmail.com
"""

import code
import argparse
import pathlib
import os
import csv
from tqdm import tqdm


def parse_args():
	parser = argparse.ArgumentParser(description="Matching information for SNPs in meta-analysis")
	
	parser.add_argument('--file', '-f', type=pathlib.Path, required=True, help='Specify the file generated using METAL tool.')
	parser.add_argument('--sumstat', '-s', type=pathlib.Path, required=True, nargs='*', help='Specify the summary statistics used to for meta-analysis.')
	parser.add_argument('--delimiter', '-d', nargs='+', choices=['WHITESPACE', 'TAB', 'COMMA', 'SEMI-COLON', 'COLON'], default=None, help='Specify the delimiter for each summary statistics. If all summary statistics are tab separated, then it is not necessary to specify this argument. But if any one summary statistics are not tab separated, specify the delimiter for all summary statistics (default: None).')
	parser.add_argument('--snp', nargs='+', required=False, default=None, help='Specify the column name indicating rsID for each of summary statistics. It is not necessary to specify if all the summary statistics have rsID column name as SNP. It is case-insensitive(default: None).')
	parser.add_argument('--chr', nargs='+', required=False, default=None, help='Specify the column name indicating CHROMOSOME for each of summary statistics. It is not necessary to specify if all the summary statistics have CHROMOSOME column name as CHR. It is case-insensitive(default: None).')
	parser.add_argument('--pos', nargs='+', required=False, default=None, help='Specify the column name indicating POSITION for each of summary statistics. It is not necessary to specify if all the summary statistics have POSITION column name as POS. It is case-insensitive(default: None).')
	parser.add_argument('--dir', type=str, required=False, default=None, help="Specify the directory path where the output file will be saved. If not specified, it will be saved in the same directory as where the meta file is located (default=None).")
	parser.add_argument('--out', '-o', type=str, required=False, default=None, help="Specify the name of the output file. If the output file name is not defined, then it will be saved in the format 'step3.Meta.Final.<Meta file name>.txt'. The output file will be saved as a text file with tab separator (default: None).")

	args = parser.parse_args()
	return args


def main(meta, sumstats, delimiter, snp, chr, pos, dir, out):
	## Process meta analysis file
	meta = str(meta)
	meta_snp2info = {}
	with open(meta, 'r') as f:
		r = csv.reader(f, delimiter='\t')
		meta_header = r.__next__()
		for row in tqdm(r, leave=False, desc='Processing Meta File'):
			assert row[0] not in meta_snp2info, "ALERT! [{}] is duplicated SNP.".format(row[0])
			meta_snp2info[row[0]] = row

	## Process summary statistics files
	sumstats = [str(s) for s in sumstats]
	if delimiter is None:
		delimiter = ['\t' for _ in range(len(sumstats))]
	else:
		delim = {'WHITESPACE':' ', 'TAB':'\t', 'COMMA':',', 'SEMI-COLON':';', 'COLON':':'}
		delimiter = [delim[i] for i in delimiter]
	if chr is None:
		chr = ['CHR' for _ in range(len(sumstats))]
	if pos is None:
		pos = ['POS' for _ in range(len(sumstats))]
	if snp is None:
		snp = ['SNP' for _ in range(len(sumstats))]
	sumstat_snp2info = {}
	for i, sumstat in enumerate(tqdm(sumstats, leave=False, desc='Processing SumStat')):
		with open(sumstat, 'r') as f:
			r = csv.reader(f, delimiter=delimiter[i])
			header = r.__next__()
			idx_chr = header.index(chr[i])
			idx_pos = header.index(pos[i])
			idx_snp = header.index(snp[i])
			for row in r:
				 if row[idx_snp] not in sumstat_snp2info:
				 	sumstat_snp2info[row[idx_snp]] = (row[idx_chr], row[idx_pos])
				 else:	# Checking if previously identified chromosome and position are identical
				 	pre_chr, pre_pos = sumstat_snp2info[row[idx_snp]]
				 	assert pre_chr==row[idx_chr], "ALERT! Chromosome coding for SNP: [{}] is different in summary statistics [{}] => [{}] and [{}] => [{}]. ".format(row[idx_snp], sumstats[0], pre_chr, sumstat, row[idx_chr])
				 	assert pre_pos==row[idx_pos], "ALERT! Position coding for SNP: [{}] is different in summary statistics [{}] => [{}] and [{}] => [{}]. ".format(row[idx_snp], sumstats[0], pre_pos, sumstat, row[idx_pos])

	## Match information and save into a file
	if dir is None:
		dir = os.path.split(meta)[0]
	if out is None:
		out = 'step3.Meta.Final.' + ''.join(os.path.split(meta)[-1].split(sep='.')[:-1])
	matched = []
	for snp, meta_info in meta_snp2info.items():
		matched.append([int(i) for i in sumstat_snp2info[snp]] + meta_info)
	with open(os.path.join(dir, out + '.txt'), 'wt', newline='') as f:
		w = csv.writer(f, delimiter='\t')
		w.writerow(['CHR', 'POS'] + meta_header)
		for row in sorted(matched):
			w.writerow(row)


if __name__ == '__main__':
	args = parse_args()
	main(meta=args.file, sumstats=args.sumstat, delimiter=args.delimiter, chr=args.chr, pos=args.pos, snp=args.snp, dir=args.dir, out=args.out)
