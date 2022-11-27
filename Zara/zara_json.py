
import requests
import time
import json
import os

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'}


link_header = "https://www.zara.com/eg/en/category/"
link_footer = "/products?ajax=true"
brand = "Zara"
links_file_name = "links.json"

links_file_path = os.getcwd() + "/" + links_file_name

with open(links_file_path,encoding='UTF-8') as sections_file:    
    sections = json.load(sections_file)[brand] 

men_responses = list()
women_responses = list()

for section in sections:
    for category in sections[section]:
        # print(sections)
        if requests.get(link_header + sections[section][category] + link_footer , headers=headers,timeout=None).status_code == 200:
            print('Get "{} {}" Items IDs Status Code'.format(section,category), 200)
            json_text = requests.get(link_header + sections[section][category] + link_footer,headers=headers).json()
            json_object = json.dumps(json_text)
                
            if section == "Men":
                men_responses.append(json.loads(json_object))
            elif section == "Women":
                women_responses.append(json.loads(json_object))
        else:
            print("errr")
            
with open("Zara/zara_men_content.json", "w") as outfile1:
    json.dump(men_responses,outfile1)
with open("Zara/zara_women_content.json", "w") as outfile2:
    json.dump(women_responses,outfile2)    

