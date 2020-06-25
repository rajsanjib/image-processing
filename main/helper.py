import re

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

        # If properly processed
        # Find text with length 10, after second index and does not contain / Its probably pan-id
        for i, text in enumerate(nT):
            if (len(text) == 10) and '/' not in text and not text.isdigit() and not text.isalpha():
                data['pan-id'] = text
                nT.pop(i)
                break
        # Similar for date too
        pattern_date_time = '([0-9]{2}.[0-9]{2}.[0-9]{4})'
        for i, text in enumerate(nT):
          match = re.match(pattern_date_time, text)
          if match is not None:
              date = match.group()
              data['DOB'] = date
              nT.pop(i)
              break
        # Filter personal account stuffs
        cut = ['Personal', 'Account', 'Pendent', 'Government', 'Signature']
        for i, n in enumerate(nT):
          for c in cut:
            if c in n:
              nT.pop(i)
        try:
            data['Fathers Name'] = nT[1]
            data['Name'] = nT[0]
        except:
            pass
        return data

    return False
