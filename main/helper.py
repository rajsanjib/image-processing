def filter_text(text):
    for i, lin in enumerate(text):
        text[i] = text[i].strip().rstrip().lstrip()
    nT = []
    # Arrange a string with \n to multiple strings
    for i, lin in enumerate(text):
        b = lin.find('\n')
        while( b != -1):
            take = lin[:b]
            nT.append(take)
            lin = lin[b+1:]
            b = lin.find('\n')
        nT.append(lin)
    # Remove empty strings
    nT = list(filter(None, nT))
    # If properly processed
    data = {
        'Fathers Name' : nT[0],
        'Name' : nT[1],
        'DOB' : nT[2],
        'pan-id' : nT[4]}
    return data
