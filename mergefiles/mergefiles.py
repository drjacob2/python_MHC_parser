'''
mergefiles
take in a nuc file and gen file and merge 
Author: Danielle Jacobs
Date: 09/06/2020
Note: when running please update sections that say ###### ~ UPDATE
'''
import re

'''
------------------------------------------------------------
name: parsetodic
input: text file from https://github.com/ANHIG/IMGTHLA/tree/Latest/alignments nuc or gen files
output: list of allele names from file and list of allele sequences 
------------------------------------------------------------
'''
def parsetodic(text):
    alleles = {}  # create a dictionary called alleles
    nameList = []  # creates an empty list nameList
    with open(text, "r") as fp:  # open A_gen.txt and read at beginning position
        line = fp.readline()  # read line by line the file
        while(line):
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
        for k, v in alleles.items():  # for key value in alleles.items()
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

'''
------------------------------------------------------------
name: count_switch
    This counts the number of times we see a "|" in the code
    this pipe symbol indicates and intron/exon boundry
    in the nuc file it indicates where an intron would be
    in teh gen file it indicates that we are switching to a intron/exon
input: dictionary in the form recieved from parsetodic
output: count of |
------------------------------------------------------------
'''
def count_switch(dict):
    for k, v in dict.items():
        count = v.count('|')
    return count

'''
------------------------------------------------------------
name: nuc_file_split
    # split the alleles in the nuc file by the pipe (|) symbol
    # sequence is a list of the new seperated intron/exon values
    # add the sequence values to a dictionary defined 
    # where key = allele and value is the list of intron/exon values 
input: nuc file dictionary (obtained from parse to dic)
output: list of allele names from file and list of allele sequences 
------------------------------------------------------------
'''
def nuc_file_split(dict):
    d_seq_nuc = {}
    for k, v in dict.items():
        sequence = re.split('\|',v)
        count=0
        for i in sequence:
            k_count = k + ' exon-' + str(count)
            d_seq_nuc.update({k_count:i})
            count+=1
    return d_seq_nuc

'''
------------------------------------------------------------
name: gen_file_split
    # split the alleles in the gen file by the pipe (|) symbol
    # sequence is a list of the new seperated intron/exon values
    # add the sequence values to a dictionary defined 
    # where key = allele and value is the list of intron/exon values 
input: gen file dictionary (obtained from parse to dic)
output: list of allele names from file and list of allele sequences 
------------------------------------------------------------
'''
def gen_file_split(dict):
    d_seq_gen = {}
    for k, v in dict.items():
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
    return d_seq_gen

'''
------------------------------------------------------------
name: count_sequence_size
    count the length of each exon or intron. 
    I recommend using this on gen file becuase the gen file contains 
    the most information (both exon and intron)
input: gen file dictionary from gen_file_split and boundry= number of | found
output: returns a list of the exon/intron length  
------------------------------------------------------------
'''
def count_sequence_size(dict, boundary):
    l = []
    for v in dict.values():
        l.append(len(v))
    l = l[:(boundary+1)]
    return l


'''
------------------------------------------------------------
name: main()
    count the length of each exon or intron. 
    I recommend using this on gen file becuase the gen file contains 
    the most information (both exon and intron)
output: returns a text file 
------------------------------------------------------------
'''
def main():
    ## variables: 
    nameList_nuc = []
    alleles_nuc = {}  # create a dictionary called alleles_nuc
    nameList_gen = []
    alleles_gen = {} 
    d = {} 
    d_seq_gen= {}

    ## Read in Nuc and Gen files 
    ###### ~ UPDATE 
    nuc_text = input("Enter a nuc file path or hit enter to accept default:") or "/Users/drjacobs/Documents/python_MHC_parser/mergefiles/C_nuc.txt"
    # nuc file parsing
    nameList_nuc, alleles_nuc = parsetodic(nuc_text)
    # gen file parsing    
    # ###### ~ UPDATE 
    gen_text = input("Enter a gen file path or hit enter to accept default:") or "/Users/drjacobs/Documents/python_MHC_parser/mergefiles/C_gen.txt" 
    nameList_gen, alleles_gen = parsetodic(gen_text)

    # count number of exon/intron switches in each file 

    value_bar_gen = count_switch(alleles_gen)
    # return a dictionary that has alleles_gen split between 
    d_seq_gen = gen_file_split(alleles_gen)
    list_gen_values = count_sequence_size(d_seq_gen, value_bar_gen) # list of the lenght of gen entron and exon info. ex: [336, 88, 2145, 285, 629, 279, 211, 129, 402, 5, 504]
    #list_nuc_values = count_sequence_size(d_seq_nuc, value_bar_nuc)

    list_intronsize = [] # list of the intron size information 
    location_intron = [] # list of intron location. This is based on where the exon is located. 
    for i in list_gen_values:
        if list_gen_values.index(i) % 2 == 0:
            list_intronsize.append(i)
        else: 
            location_intron.append(i)
    
    # create list of intron inserts values 
    a= [] # a will hold all of the intron values 
    for i in list_intronsize:
        a.append(i*'*')
    # update nuc file with empty intron info 
    for k, v in alleles_nuc.items():
        j=0
        newstr = a[0] + "|"
        for i in range(len(v)):  # len(dictionary value)
            c = v[i]  # get the base value at position i
            if c == "|":  # check if it is |
                    j+=1
                    newstr += "|" + a[j] + "|"
            else:
                newstr += c  # else add value to new string
        newstr += "|" + a[-1] 
        alleles_nuc[k] = newstr  # reset dictionary here
    
    # combine files
    for key in alleles_nuc.keys():
        if key in alleles_gen:
            d.update(alleles_gen)
        else: 
            d[key] = alleles_nuc[key]
    # formatted print 
    for n in nameList_nuc:
        print("{},{}".format(n, d[n]), "\n")
    # print to text file: 
    filename = input("Enter a text filename to save to:") or "merge_file.txt"
    fo = open(filename, "w")
    for k, v in d.items():
        fo.write(str(k) + ' '+ str(v) + '\n')
    fo.close()

if __name__ == "__main__":
    main()