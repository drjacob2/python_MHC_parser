alleles = {}  # create a dictionary called alleles
nameList = []  # creates an empty list nameList
with open("DMA_nuc.txt", "r") as fp:  # open A_gen.txt and read at beginning position
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
# pdr: I would suggest that using the nameList list
# to process here
for k, v in alleles.items():  # for key value in alleles.items()
    #print(k, "and", v)
    #print(len(v))
    newstr = "" 
    for i in range(len(v)):  # len(value) 
        c = v[i] # get the base value at position i
        if c == "-": # check if it is -
            newstr += first[i] # if it is - then add the first allele has in the same position to new string 
        else:
            newstr += c # else add value to new string 
    alleles[k] = newstr # reset dictionary here
for k, v in alleles.items():
    print("key:", k, "value:", v, "\n")
for n in nameList:
    print(n)
for n in nameList:
    print("{},{}".format(n, alleles[n]), "\n")

