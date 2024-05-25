import datetime
import shutil
import json,os

def today_formatted():
    return datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
# schema = json.loads(open("schema.json").read())
# validator = Draft7Validator(schema,format_checker=jsonschema.FormatChecker())

class OutputJSON:
    filename = None
    file = None
    def __init__(self, script_name):
        self.filename = script_name + "_" + today_formatted() + ".json"
        self.file = open("C:/Users/addiction computers/Desktop/swaping project/gec_common/json_file" + "/" + self.filename, encoding="utf8", mode="w")
        self.list = []  
        
    def writeNoticeToJSONFile(self, dictionary):
        self.list.append(dictionary)
        
    def copyFinalJSONToServer(self, list_name):
        json.dump(self.list,self.file,indent = 6,sort_keys = True)
        self.close()
#         final_full_filename = application_properties.GENERATED_JSON_ROOT_DIR + "/" + directory_name + "/" + self.filename
#         shutil.move(application_properties.TMP_DIR + "/" + self.filename, final_full_filename)
#         json_single_File = final_full_filename
        
        
    def close(self):
        self.file.write("\n")
        self.file.close()
