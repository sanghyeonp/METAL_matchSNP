# METAL_SNPmatching

A script for matching the chromosome and the base position of SNPs that have been meta-analyzed using METAL tool.


Clone the repository.
```shell
git clone https://github.com/sanghyeonp/METAL_matchSNP.git
```

## The parser arguments are as below:

**--file, -f** : Specify the file (path) generated using METAL tool\
**--sumstat, -s** : Specify the summary statistics used to for meta-analysis\
* For example, if 3 summary statistics were used for meta-analysis, then specify their path with whitespace between them as follows => **-s ./sumstat1.txt ./sumstat2.tbl ./sumstat3.txt**

**--delimiter, -d** : Specify the delimiter for each summary statistics. If all summary statistics are tab separated, then it is not necessary to specify this argument. But if any one summary statistics are not tab separated, specify the delimiter for all summary statistics (default: None). The choices of delimiter is ['WHITESPACE', 'TAB', 'COMMA', 'SEMI-COLON', 'COLON'].
* For example, if 3 summary statistics were used for meta-analysis and second summary statistics is comma separated, then speicfy their separation as follow => **-d TAB COMMA TAB**

**--snp** : Specify the column name indicating rsID for each of summary statistics. It is not necessary to specify if all the summary statistics have rsID column named as SNP. It is case-sensitive(default: None).

**--chr** : Specify the column name indicating CHROMOSOME for each of summary statistics. It is not necessary to specify if all the summary statistics have CHROMOSOME column named as CHR. It is case-sensitive(default: None).

**--pos** : Specify the column name indicating POSITION for each of summary statistics. It is not necessary to specify if all the summary statistics have POSITION column named as POS. It is case-sensitive(default: None).

**--dir** : Specify the directory path where the output file will be saved. If not specified, it will be saved in the same directory as where the meta file is located (default=None).

**--out** : Specify the name of the output file. If the output file name is not defined, then it will be saved in the format 'step3.Meta.Final.\<Meta file name>\.txt'. The output file will be saved as a text file with tab separator (default: None).


## Run example

The final meta-analyzed summary statistic generated with the name **meta_final.txt**.

3 summary statistics (**sumstat1.txt, sumstat2.tbl, sumstat3.txt**) were used for meta-analysis using METAL tool and they are located at **./raw.**\
For each summary statistics,
* Separated by **tab, whitespace, and tab**
* SNP column named as **SNP, rsID, and MarkerID**
* Chromosome column named as **CHR, chr, and chromosome**
* Position column named as **pos, POS, and POSITION**

Lastly, let's say I want to save the output file to **./savehere** with the name **meta_final_matched**.

```shell
python matchSNP.py 
--file meta_final.txt 
--sumstat ./raw/sumstat1.txt ./raw/sumstat2.tbl ./raw/sumstat3.txt
--delimiter TAB WHITESPACE TAB  # Case-sensitive
--snp SNP rsID MarkerID # Case-sensitive
--chr CHR chr chromosome    # Case-sensitive 
--pos pos POS POSITION  # Case-sensitive 
--dir ./savehere
--out meta_final_matched
```

## Contact
If there are any problem or suggestion for further improvement, please feel free to contact.\
E: sh.austin.park@gmail.com\
T: (+82) 10-8767-7043