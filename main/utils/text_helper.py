import re
import collections
import random

def filter_text(text):
    if(len(text) > 0):
        nT = clean(text)

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
        nT = remove_extra_text(nT)
        try:
            data['Name'] = try_name(nT)
            data['Fathers Name'] = try_name(nT.remove())
        except:
            pass
        return data

    return False


def filter_text_for_adhar(text):
    if len(text) > 0:
        nT = clean(text)

        data = {
        'Name': '',
        'DOB': '',
        'Gender': '',
        'adhar-id': ''
        }

        for i, text in enumerate(nT):
            if 'Female' in text:
                data['Gender'] = 'Female'
                nT.pop(i)
                break
            elif 'Male' in text:
                data['Gender'] = 'Male'
                nT.pop(i)
                break

        pattern_id_number = re.compile(r'(^[0-9]{4}$)')
        id = ''
        for i, text in enumerate(nT):
          match = re.search(pattern_id_number, text)
          if match is not None:
              find = match.group()
              id += find+' '
        data['adhar-id'] = id

        pattern_id_number = re.compile(r'([0-9]{4}.[0-9]{4}.[0-9]{4})')
        for i, text in enumerate(nT):
          match = re.search(pattern_id_number, text)
          if match is not None:
              id = match.group()
              data['adhar-id'] = id
              nT.pop(i)
              break
        # Similar for date too
        pattern_date_time = re.compile(r'([0-9]{2}.[0-9]{2}.[0-9]{4})')
        for i, text in enumerate(nT):
          match = re.search(pattern_date_time, text)
          if match is not None:
              date = match.group()
              data['DOB'] = date
              nT.pop(i)
              break
        nT = remove_extra_text(nT)
        if(len(nT) > 0):
            data['Name'] = try_name(nT)
        return data

def try_name(list):
    name = None
    if len(list) > 0:
        for text in list:
            if (re.fullmatch('[A-Za-z]{2,25}\s([A-Z][a-z]{2,25})?', text)) is not None:
                print(text)
                return text
            elif (re.fullmatch('[A-Za-z]{2,25}?', text)) is not None:
                name = text
        if name is not None:
            return name
        else:
            return random.choice(list)
    return None

def remove_extra_text(list):
    new = []
    print(list)
    if len(list) > 0:
        for text in list:
          if not set('[~!@#$%^&*()_+{}":;\']+$').intersection(text):
              if len([l for l in text if l.isupper()]) > 0:
                  if len(text) > 3:
                    if (collections.Counter(text)[' ']) < 2:
                      if not any(s in text for s in ['Name', 'DOB', 'MALE']):
                          if (re.fullmatch('[A-Z][A-Z|a-z]{2,25} ([A-Z][A-Z|a-z]{2,25})?', text.replace('.', ''))) is not None:
                            new.append(text)
        return new
    return None

def clean(text):
    # Clean texts
    if len(text) > 0:
        for i, lin in enumerate(text):
            text[i] = text[i].strip()
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
        return nT
    return None

def filter_address(text):
    text = text[text.find('Address:'):].replace('Address:', '')
    return text

# def remove_nonsense_words(text):
#     words = set(nltk.corpus.words.words())
#     " ".join(w for w in nltk.wordpunct_tokenize(text) if w.lower() in words or not w.isalpha())
