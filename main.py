import os
import json
import requests
from bs4 import BeautifulSoup



def build_data_keys(table):
    data_dict = {}
    primary_headings = table.find_all('tr')[0]
    for primary_heading in primary_headings.find_all('th'):
        column_name = ''.join(primary_heading.text)
        data_dict[column_name] = {}
        if column_name == "警戒值":
            secondary_headings = table.find_all('tr')[1]
            for secondary_heading in secondary_headings.find_all('th'):
                subcolumn_name = ''.join(secondary_heading.text)
                data_dict[column_name][subcolumn_name] = {}
    return(data_dict)

def fill_data_dict(data_dict, table):
    array_json_objects = []
    data = table.find_all('tr')[2:]
    if len(table.find_all('tr')) > 3:
        primary_columns = list(data_dict.keys())
        secondary_columns = list(data_dict[primary_columns[5]].keys())
        for data_row in data:
            data_counter = 0 
            secondary_counter = 0
            while data_counter <= 8:
                
                if data_counter == 8:
                    data_item = data_row.find_all('td')[data_counter].text
                else: 
                    data_item = ''.join(data_row.find_all('td')[data_counter].contents)
                
                if data_counter >= 5 and data_counter <8:
                    data_dict[primary_columns[5]][secondary_columns[secondary_counter]] = data_item
                    secondary_counter = secondary_counter + 1
                else:
                    if data_counter == 8:
                        data_dict[primary_columns[6]] = data_item
                    else:
                        data_dict[primary_columns[data_counter]] = data_item
                data_counter = data_counter + 1
            json_object = json.dumps(data_dict) 
            array_json_objects.append(json_object)
        return(array_json_objects)

def write_data_2_json_file(array_json_objects, area_dict):
    if not os.path.isdir('data'):
        os.makedirs('data')
    with open(os.path.join('data',area_dict['AreaCode']+'_'+area_dict['Code']+'_water_level.json'), 'w', encoding='utf-8') as f:
        json.dump(array_json_objects, f, ensure_ascii=False, indent=4)

def main():
    url_post = "https://fhy.wra.gov.tw/fhy/Monitor/WaterInfo"
    url_get = "https://fhy.wra.gov.tw/fhy/api/Basinsapi/GetAll"
    all_locations_json = requests.get(url_get).json()

    for area_dict in all_locations_json:
        html_content = requests.post(url_post, data={"basin": area_dict['Code']}).text
        soup = BeautifulSoup(html_content, "lxml")
        table = soup.find("table")

        data_dict = build_data_keys(table)
        array_json_objects = fill_data_dict(data_dict, table)
        if bool(array_json_objects):
            write_data_2_json_file(array_json_objects, area_dict)

    


if __name__ == '__main__':

    main()