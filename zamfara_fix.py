import json

class ZamafaraFix:

    old_file_name = "states-lga-and-areas.json"
    new_file_name = "new-states-lga-and-areas.json"

    def append_to_json(self, new_data, filename):
    
        with open(filename,'r+') as file:
        
            file_data = json.load(file)
        
            file_data["data_arr"].append(new_data)
           
            file.seek(0)
           
            json.dump(file_data, file, indent = 4)

    def get_json_file(self, filename):
    
        f = open(filename,)
        # returns JSON object as
        # a dictionary
        data = json.load(f)
        zamfara = "Zamfara"
        list_of_lgas = []

        # current_area = ''
        for i in data['data_arr']:
            state_name = i['state']
            state_name_lower = str(str(state_name).lower)
            print(str(state_name))
            # break
            if state_name != zamfara:
                self.append_to_json(i, self.new_file_name)
            else:

                villages_list = []
                lga = i['LGA']
                state = i['state']
                area = i['District/Area']
                postal_code = i['Postal code'],
                village_string = i['villages']
                village = village_string.replace("\\", "")
                villages_list.append(village)
                # current_area = area

                #if current_lga != '' and any(x.LGA == current_lga for x in list_of_lgas):
                index = next((i for i, obj in enumerate(list_of_lgas) if obj['LGA'] == lga), -1)
                if index > -1:
                   # print('*****')
                   list_of_lgas[index]['villages'].append(village)
                else:
                    
                    dist = {
                        'state': state,
                        'LGA': lga,
                        'District/Area': 'N/A',
                        'Postal code': 'N/A',
                        'villages': villages_list
                    }
                    
                    list_of_lgas.append(dist)
                    

        length = len(list_of_lgas)
        print(length)
        for x in range(length):
           self.append_to_json(list_of_lgas[x], self.new_file_name)
        
        # Closing file
        f.close()

    def recreate_json_file(self, filename):
        obj = {
                "data_arr": [

                ]
            }
        json_object = json.dumps(obj, indent = 4)
        with open(filename, "w") as outfile:
            outfile.write(json_object)

    def perform_fix(self):
        pass

    def init(self):
        self.recreate_json_file(self.new_file_name)
        self.get_json_file(self.old_file_name)


myloader = ZamafaraFix()
myloader.init()