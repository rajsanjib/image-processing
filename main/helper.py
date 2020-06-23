def filter_text(text):
    if(len(text) > 0):
        # Clean texts
        for i, lin in enumerate(text):
            text[i] = text[i].strip().rstrip().lstrip()
        nT = []
        # Arrange a string with \n into multiple strings
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

        data = {
        'Fathers Name': '',
        'Name': '',
        'DOB': '',
        'pan-id': ''
        }

        # Filter personal account stuffs
        cut = ['Personal', 'Account', 'Pendent']
        for i, n in enumerate(nT):
          for c in cut:
            if c in n:
              nT.pop(i)

        # If properly processed
        # Find text with length 10, after second index and does not contain / Its probably pan-id
        for i, text in enumerate(nT):
            if (len(text) == 10) and (i > 1) and '/' not in text and not text.isdigit():
                data['pan-id'] = text
                break
        # Similar for date too
        for i, text in enumerate(nT):
            if (len(text) == 10) and (i > 1) and text.strip('/').isdigit():
                data['DOB'] = text
                break
        try:
            data['Fathers Name'] = nT[1]
            data['Name'] = nT[0]
        except:
            pass
        return data

    return False
