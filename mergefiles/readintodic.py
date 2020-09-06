import re

'''
name: parsetodic
input: text file from https://github.com/ANHIG/IMGTHLA/tree/Latest/alignments nuc or gen files
output: list of allele names from file and list of allele sequences 
'''

def parsetodic(text):
    alleles = {}  # create a dictionary called alleles
    nameList = []  # creates an empty list nameList
    with open(text, "r") as fp:  # open A_gen.txt and read at beginning position
        line = fp.readline()  # read line by line the file
        while(line):
            if("DMA*" in line):
            # Remove the whitespaces from the
            # beginning and end from name
                name = line[0:16].strip()
    # We will use the nameList to process the
    # alleles list in order LATER
    # add new allele names to list
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
            #value = value.replace("|","")
                if name in alleles:
                # we're appending to the existing
                    alleles[name] += value
                else:
                    alleles[name] = value
            line = fp.readline()
        # replace bars with first allele values
        first = alleles["DMA*01:01:01:01"]
        for k, v in alleles.items():  # for key value in alleles.items()
            #print(k, "and", v)
            # print(len(v))
            newstr = ""
            for i in range(len(v)):  # len(value)
                c = v[i]  # get the base value at position i
                if c == "-":  # check if it is -
                    # if it is - then add the first allele has in the same position to new string
                    newstr += first[i]
                else:
                    newstr += c  # else add value to new string
                alleles[k] = newstr  # reset dictionary here
            #for k, v in alleles.items():
             #   print("key:", k, "value:", v, "\n")
            #for n in nameList:
            #    print(n)
            #for n in nameList:
             #   print("{},{}".format(n, alleles[n]), "\n")
    return nameList, alleles

def count_switch(dict):
    # add more features to the 
    for k, v in dict.items():
        #print(type(v))
        count = v.count('|')
        #print(count)
    return count


def main():
    nameList_nuc = []
    alleles_nuc = {}  # create a dictionary called alleles_nuc
    nameList_gen = []
    alleles_gen = {} 
    d = {} 

    nuc_text = "DMA_nuc.txt"
    # nuc file parsing
    nameList_nuc, alleles_nuc = parsetodic(nuc_text)
    # print(nameList_nuc)
    # print(alleles_nuc)

    # gen file parsing 
    gen_text = "DMA_gen.txt" 
    nameList_gen, alleles_gen = parsetodic(gen_text)
    # print(nameList_gen)
    # print(alleles_gen)

    # add more features to the dictionaries 
    # 1. count number of exon/intron switches in each file 
    value_bar_nuc = count_switch(alleles_nuc)
    value_bar_gen = count_switch(alleles_gen)
    # print(value_bar_nuc, 'and', value_bar_gen)
    
    for k, v in alleles_nuc.items():
        #regex = re.compile('\|')
        # print(k, 'and', v)
        sequence = re.split('\|',v)
        print(k, "\n", sequence)
        d[k]=sequence
        print('i am printing the dictionary \n\n', d)
    #print(alleles_nuc)
    #print('---------------------------', d)

    '''
    make each allele dictionary into a dictionary where each key is exon# and each value is the correspondig value 
    
    make new dictionary 
    read keys from nuc and gen.
    if keys match 
    read 
    '''



if __name__ == "__main__":
    main()
