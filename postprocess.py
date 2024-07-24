from difflib import SequenceMatcher
import pandas as pd
from datetime import datetime
import json


def similar(a,words): #to account for the errors in detection of text by easyocr
    mx=0
    index=None
    for i,word in enumerate(words):
        if SequenceMatcher(None,a,word).ratio()>mx:
            mx=SequenceMatcher(None,a,word).ratio()
            index=i
    return mx,index

def extract_information(data_string):
    # Split the data string into a list of words based on "|"
    updated_data_string = data_string.replace(".", "")
    words = [word.strip() for word in updated_data_string.split("|") if len(word.strip()) > 2]
    print(words)
    # Initialize the dictionary to store the extracted information
    extracted_info = {
        "ID": "",
        "Name": "",
        "Father's Name": "",
        "DOB": "",
        "ID Type": "PAN"
    }

    try:

        #matching thw words that are present , but maybe not accurately , so using sequencematcher...
        _,id_number_index = similar("Permanent Account Number",words)
        extracted_info["ID"] = words[id_number_index+1]

        _,name_index = similar("Name",words)
        extracted_info["Name"] = words[name_index+1]

        mx,fathers_name_index = similar("Father's Name",words)
        if(mx>0.5):
            extracted_info["Father's Name"] = words[fathers_name_index+1]
        else:
            extracted_info["Father's Name"] = words[fathers_name_index+2]
        
        _,dob_index = similar("Date of Birth",words)
        extracted_info["DOB"] = words[dob_index+1]

        if dob_index is not None:
            extracted_info["DOB"] = datetime.strptime(words[dob_index+1], "%d/%m/%Y")
        else:
            print("Error: Date of birth not found.")
    except ValueError:
        print("Error: Some required information is missing or incorrectly formatted.")

    return extracted_info
