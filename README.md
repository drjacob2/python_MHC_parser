# python_MHC_parser
this is a parser to read in MHC files from ANHIG / IMGTHLA and parse it to certain format requirements. 

## Background 
This project uses the HLA files located [here](https://github.com/ANHIG/IMGTHLA). This project is aimed at taking the alignment files, combining the subsets of the gen and nuc files for a given allele, provding a clean output file of the combined data, and providing a count.   

## file information 
-merge_file_B.txt - merged version of B_gen and B_nuc ran 09/06

-merge_file_C.txt - merged version of C_gen and C_nuc ran 09/06

-merged_file_DMA.txt - merged version of DMA_gen and DMA_nuc ran 09/06

-merged_files_A.txt - merged version of A_gen and A_nuc ran 09/06

-mergefiles.py - final version as of 09/06 to read in nuc and gen files and merge

-HLAtest.py - takes the alginments/gen file from the IMGTHLA database and uses pandas to count the unique values 

Jupyter notebooks are versions of importing gen file for cleaning and counting unique columns. 
