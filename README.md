# python_MHC_parser
this is a parser to read in MHC files from ANHIG / IMGTHLA and parse it to certain format requirements. 

## Background 
This project uses the HLA files located [here](https://github.com/ANHIG/IMGTHLA). This project is aimed at taking the alignment files, combining the subsets of the gen and nuc files for a given allele, provding a clean output file of the combined data, and providing a count.   



## file information 
-merge_file_B.txt - merged version of B_gen and B_nuc ran 09/06

-merge_file_C.txt - merged version of C_gen and C_nuc ran 09/06

-merged_file_DMA.txt - merged version of DMA_gen and DMA_nuc ran 09/06

-merged_files_A.txt - merged version of A_gen and A_nuc ran 09/06

-**mergefiles.py** - final version as of 09/06 to read in nuc and gen files and merge

-HLAtest.py - takes the alginments/gen file from the IMGTHLA database and uses pandas to count the unique values 

-DataQ&A.pptx - an attempted walk through of the gen and nuc data sets and how they need to be combined 

Jupyter notebooks are versions of importing gen file for cleaning and counting unique columns. 

#### Running mergefiles.py
any where that you see a comment `###### ~ UPDATE`, please update that line prior to running. As seen in the following lines: 
```python
            ###### ~ UPDATE 
            if("C*" in line):
            # Remove the whitespaces from the
            # beginning and end from name
                name = line[0:16].strip()
                if name not in nameList:
                    nameList.append(name)
                # we are stripping out the beginning / end whitespace
                value = line[19:].strip()
                # let's get rid of internal whitespace and compress sequence
                value = value.replace(" ", "")
                # we want to be able to distinguish
                # between intron/exon, but need the
                # full value - we will do this after
                # the entire allele value is captured
                if name in alleles:
                # we're appending to the existing
                    alleles[name] += value
                else:
                    alleles[name] = value
            line = fp.readline()
        # replace bars with first allele values
        ###### ~ UPDATE 
        first = alleles["C*01:02:01:01"]
```

```python
    ## Read in Nuc and Gen files 
    ###### ~ UPDATE 
    nuc_text = input("Enter a nuc file path or hit enter to accept default:") or \
    "/Users/drjacobs/Documents/python_MHC_parser/mergefiles/C_nuc.txt"
    # nuc file parsing
    nameList_nuc, alleles_nuc = parsetodic(nuc_text)
    # gen file parsing    
    # ###### ~ UPDATE 
    gen_text = input("Enter a gen file path or hit enter to accept default:") or \
    "/Users/drjacobs/Documents/python_MHC_parser/mergefiles/C_gen.txt" 
    nameList_gen, alleles_gen = parsetodic(gen_text)
```

