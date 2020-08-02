import json
import logging
from Similar import *
from datetime import date

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("MRZParser")

class MRZParser():

    def __init__(self, text):

        self.__data = {
            'Response' : None
        }

        self.__text = text.split('\n')
        self.__text = list(filter(
            lambda x: '<' in x, self.__text) 
        )
        self.__text = [line.replace(' ', '') for line in self.__text]

        # print(self.__text)

        if len(self.__text) != 3:
            raise ValueError('MRZ line should be exactly 3.')

        ## first line 
        log.info('Processing first line of MRZ.')
        line = list(filter(
            lambda x: len(x) > 0, self.__text[0].split('<')) 
        )


        if len(line) < 3:
            if len(line[0]) > 2:
                line.insert(1, line[0][2:])
                line[0] = line[0][0]
            
            if len(line) < 3 and len(line[1]) > 9:
                line.insert(2, line[1][13:])
                line[1] = line[1][:12]

            else :
                raise ValueError('Less sections in line 1 then expected.')
        
        # print(line)

        if len(line[0]) != 1 or line[0][0] not in MRZ_TYPE:
            raise ValueError('MRZ type {} is not supported.'.format(line[0]))
        else:
            self.__data['MRZ Type'] = 'ID Card' 

        if len(line[1]) <3:
            self.__data['Issued Country'] = None 
            self.__data['NID No.'] = None 
        else:
            self.__data['Issued Country'] = convert_to(line[1][:3], ALPHA)
            if len(line[1]) <12:
                self.__data['NID No.'] = None 
            else:
                self.__data['NID No.'] = convert_to(line[1][3:] + line[2][0], NUM)


        ## second line 
        log.info('Processing second line of MRZ.')
        line = list(filter(
            lambda x: len(x) > 0, self.__text[1].split('<')) 
        )[0]

        if len(line) != 18:
            raise ValueError('Unexpected length {} is found \
                for the second line MRZ is found.'.format(len(line)))
        else:
            self.__data['Date of Birth'] = self.__convert_date(line[:6], 'Birth')
            if convert_to(line[7], ALPHA) == 'M':
                self.__data['Gender'] = 'Male'
            elif convert_to(line[7], ALPHA) == 'F':
                self.__data['Gender'] = 'Female'
            else:
                self.__data['Gender'] = None
            self.__data['Date of Card Expiration'] = self.__convert_date(line[8:14], 'Exp.')
            self.__data['Nationality'] = convert_to(line[15:], ALPHA)
        ## third line
        log.info('Processing third line of MRZ.') 
        line = list(filter(
            lambda x: len(x) > 0 and x.isalpha(), self.__text[2].split('<')) 
        )

        if (len(line)) > 1:
            self.__data['Last Name'] = line[0]
            self.__data['First Name'] = ' '.join(line[1:])
        elif (len(line)) == 1:
            self.__data['Last Name'] = line[0]
            self.__data['First Name'] = None
        else:
            self.__data['Last Name'] = None
            self.__data['First Name'] = None

        self.__data['Response'] = 200 

        log.info('Processing MRZ completed successfully.\n\n') 
         


    def __repr__(self):
        if self.__data['Response'] is None :
            raise Exception('Uncaught exception occured')

        return json.dumps(self.__data, indent=4) 


    def __convert_date(self, some_date, date_type='Birth'):

        if not some_date.isnumeric():
            return None

        date_type = '19' if date_type[0] == 'B' else '20'

        some_date = convert_to(some_date[:6], NUM)
        some_date = date.fromisoformat('{}{}-{}-{}'.format(date_type, some_date[:2], some_date[2:4], some_date[4:6]))
        return some_date.strftime("%d %B, %Y")



if __name__ == '__main__':
    MRZParser()