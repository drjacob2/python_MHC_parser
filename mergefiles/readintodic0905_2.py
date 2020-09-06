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
    return nameList, alleles

def count_switch(dict):
    # add more features to the 
    for k, v in dict.items():
        count = v.count('|')
    return count

def nuc_file_split(dict):
    # split the alleles in the nuc file by the pipe (|) symbol
    # sequence is a list of the new seperated intron/exon values
    # add the sequence values to a dictionary defined 
    # where key = allele and value is the list of intron/exon values 
    d_seq_nuc = {}
    for k, v in dict.items():
        sequence = re.split('\|',v)
        count=0
        for i in sequence:
            k_count = k + ' exon-' + str(count)
            d_seq_nuc.update({k_count:i})
            count+=1
        # print(d_seq_nuc)
    return d_seq_nuc

def gen_file_split(dict):
    # split the alleles in the gen file by the pipe (|) symbol
    # sequence is a list of the new seperated intron/exon values
    # add the sequence values to a dictionary defined 
    # where key = allele and value is the list of intron/exon values 
    d_seq_gen = {}
    for k, v in dict.items():
        # print(k, 'and', v, "\n")
        sequence = re.split('\|',v)
        count_intron=0
        count_exon=0
        count=0
        for i in sequence:
            if count % 2 ==0:
                k_count = k + ' intron-' + str(count_intron)
                d_seq_gen.update({k_count:i})
                count_intron+=1
            else:
                k_count = k + ' exon-' + str(count_exon)
                d_seq_gen.update({k_count:i})
                count_exon+=1
            count+=1
        for key, value in d_seq_gen.items():
            print(key, "and", value, "\n")
    return d_seq_gen

def count_introns(dict, length):
    l = []
    for v in dict.values():
        #print(len(v))
        l.append(len(v))
    l = l[:(length+1)]
    #print(l)
    return l

def union_collections(d1, d2):
    return { k: sorted(
                    list(
                        set(
                            d1.get(k, []) + d2.get(k, [])
                        )
                    )
                )
             for k in set(d1.keys() + d2.keys()) }

def main():
    nameList_nuc = []
    alleles_nuc = {}  # create a dictionary called alleles_nuc
    nameList_gen = []
    alleles_gen = {} 
    d = {} 
    d_seq_nuc = {} 
    d_seq_gen= {}
    l = []

    nuc_text = "DMA_nuc.txt"
    # nuc file parsing
    nameList_nuc, alleles_nuc = parsetodic(nuc_text)
    # print(nameList_nuc)
    # print(alleles_nuc)

    # gen file parsing 
    gen_text = "DMA_gen.txt" 
    nameList_gen, alleles_gen = parsetodic(gen_text)
    print(nameList_gen)
    print(alleles_gen)

    # add more features to the dictionaries 
    # 1. count number of exon/intron switches in each file 
    value_bar_nuc = count_switch(alleles_nuc)
    value_bar_gen = count_switch(alleles_gen)
    print(value_bar_nuc, 'and', value_bar_gen)
    

    # split the alleles in the gen file by the pipe (|) symbol
    # sequence is a list of the new seperated intron/exon values
    # add the sequence values to a dictionary defined 
    # where key = allele and value is the list of intron/exon values 
    d1 = {}
    for k, v in alleles_gen.items():
        print(k, 'and', v, "\n")
        sequence = re.split('\|',v)
        count_intron=0
        count_exon=0
        count=0
        for i in sequence:
            if count % 2 ==0:
                k_count = k + ' intron-' + str(count_intron)
                d1.update({k_count:i})
                count_intron+=1
            else:
                k_count = k + ' exon-' + str(count_exon)
                d1.update({k_count:i})
                count_exon+=1
            count+=1
        alleles_gen[k].update(d1)
        for key, value in alleles_gen.items():
            print(key, "and", value, "\n")


    d_seq_nuc = nuc_file_split(alleles_nuc)
    d_seq_gen = gen_file_split(alleles_gen)
    list_gen_values = count_introns(d_seq_gen, value_bar_gen)
    print(list_gen_values)
    list_intronsize = [] # list of the intron size information 
    location_intron = []
    for i in list_gen_values:
        if list_gen_values.index(i) % 2 == 0:
            #print(i)
            list_intronsize.append(i)
        else: 
            location_intron.append(i)
    print(list_intronsize)
    print(location_intron)

    for key in alleles_nuc.keys():
        if key in alleles_gen:
            d[key] = alleles_gen[key]
        else: 
            d[key] = alleles_nuc[key]
    
   # print(d)


if __name__ == "__main__":
    main()