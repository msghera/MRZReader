MRZ_TYPE = ['I', '1', 'T',  '!', 't']

ALPHA ={
   "0": "O",
   "1": "I",
   "2": "Z",
   "4": "A",
   "5": "S",
   "6": "G",
   "8": "B"
}

NUM = {
   "B": "8",
   "C": "0",
   "D": "0",
   "G": "6",
   "I": "1",
   "O": "0",
   "Q": "0",
   "S": "5",
   "Z": "2"
}

def convert_to(given_text, given_dict):
    given_text = list(given_text)
    for i in range(len(given_text)):
        if given_text[i] in given_dict:
            given_text[i] = given_dict[given_text[i]]

    return ''.join(given_text)

if __name__ == '__main__':
    print(convert_to('8Sd', ALPHA))
    print(convert_to('8Sd', NUM))