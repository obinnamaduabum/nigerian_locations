import lxml.html as lh
from urllib.request import Request, urlopen
import json
import re
import json


class WebScrapper:
    count=0

    def create_json_file(self, filename):
        obj = {
                "data_arr": [

                ]
            }
        json_object = json.dumps(obj, indent = 4)
        with open(filename, "w") as outfile:
            outfile.write(json_object)

    def append_to_json(self, new_data, filename):
    
        with open(filename,'r+') as file:
            # First we load existing data into a dict.
            file_data = json.load(file)
            # Join new_data with file_data inside emp_details
            file_data["data_arr"].append(new_data)
            # Sets file's current position at offset.
            file.seek(0)
            # convert back to json.
            json.dump(file_data, file, indent = 4)

    def makeApiCall(self, state_name):

        print('triggered api call ...')


        if state_name != 'FCT - Abuja':
            state_under_score = state_name.replace(' ', '_')
            url = f'https://en.wikipedia.org/wiki/List_of_villages_in_{state_under_score}_State'
            print(url)
        else:
            url = 'https://en.wikipedia.org/wiki/List_of_villages_in_the_Federal_Capital_Territory,_Nigeria'

        # Set user agent to mozilla to fix 403 forbidden error 
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html_bytes = urlopen(req).read()
        html = html_bytes.decode("utf-8")
        # print(html)

        #Store the contents of the website under doc
        doc = lh.fromstring(html)
        # print(doc)
        #Parse data that are stored between <tr>..</tr> of HTML
        tr_elements = doc.xpath('//tr')
        # print(tr_elements)
        return tr_elements
    
    def getJson(self, tr_elements, state):
        main_list = []
        for row in range(1, len(tr_elements)):

            table_tr = tr_elements[row]

            inner_list = []

            children_length = len(table_tr)
            
            if children_length > 2:
                for column in table_tr.iterchildren():
                    data = column.text_content()
                    # if data[0] != None and data[1] != None and data[2] != None:
                    print(data)
                    inner_list.append(data)
                
                    x = inner_list[0] 
                # if re.search("\\W", inner_list[0]):
                #     x = 's' + inner_list[0]

                if state == 'Zamfara':
                    if(len(inner_list) > 3):

                        if inner_list[1] != 'LGA':
                            dict = {
                                'state': state,
                                'LGA': inner_list[1],
                                'District/Area': self.removeWord('(Rural)', inner_list[2]),
                                'Postal code': 'N/A',
                                'villages': self.split_string_to_array(inner_list[3])
                            }

                            self.append_to_json(dict, "states-lga-and-areas.json")
                            main_list.append(dict)
                else:
                    if(len(inner_list) > 3):

                        if x != 'LGA':
                            dict = {
                                'state': state,
                                'LGA': x,
                                'District/Area': self.removeWord('(Rural)', inner_list[1]),
                                'Postal code': inner_list[2],
                                'villages': self.split_string_to_array(inner_list[3])
                            }

                            self.append_to_json(dict, "states-lga-and-areas.json")
                            main_list.append(dict)

        return main_list

    def doWork(self, list_of_states):

        for state in list_of_states:
            print(state)
            response = self.makeApiCall(state)
            self.getJson(response, state)

    def readjson(self):
        f = open('nigerian-states.json')
        data = json.load(f)
        list = []
        for i in data:
            list.append(i)
        f.close()
        return list

    def split_string_to_array(self, actual_input_string):
        input_string = actual_input_string.strip('\n')
        if ';' in input_string:
            list = input_string.split(';')
            stripped_list = []
            for item in list:
                if ',' in item:
                    list_with_comma = item.split(',')
                    for item_without_comma in list_with_comma:
                        stripped_item = item_without_comma.strip()
                        stripped_list.append(stripped_item)
                else:
                    stripped_item = item.strip()
                    stripped_list.append(stripped_item)
            return stripped_list   

        return input_string.strip()

    def removeWord(self, word, input_string):
        stripped = input_string.replace(word, '')
        return stripped

    def remove_back_slash(self, input_list):

        new_list = []
        for input_string in input_list:
            list = input_string.split('/')
            if len(list) > 0:
                new_list.append(list[0])
            new_list.append(input_string)

        return new_list

webScrapper = WebScrapper()
list_of_states = webScrapper.readjson()
webScrapper.create_json_file("states-lga-and-areas.json")
webScrapper.doWork(list_of_states)