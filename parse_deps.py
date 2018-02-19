def parse(prefix):
    amrdata = __import__("amrdata_en")
    data = amrdata.AMRDataset(prefix, False)
    alltokens = []
    alldependencies = []
    allrelations = []
    allalignments = []
    for i_s, sentence in enumerate(data.getAllSents()):
        print ("Sentence", i_s + 1)
        input()

