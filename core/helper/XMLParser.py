from __future__ import print_function
import pandas as pd
import csv
import os
from core.config.paths import output_path
import sys



class XMLParser:

    dict_list = []
    counter = 1
    total_element = int()
    output_file_counter = 1

    def __init__(self, each_item):
        self.each_item = each_item

    @staticmethod
    def to_string(s):
        try:
            return str(s).strip()
        except:
            # Change the encoding type if needed
            return s.encode('utf-8').strip()

    def travel_element_xml(self, row_dict, element, tag):
        for child in element:
            if len(child) == 0:
                key = str(tag + '__' + child.tag)
                value = child.text if child.text is not None else ''
                if key not in row_dict.keys():
                    row_dict[self.to_string(key)] = self.to_string(value)
                else:
                    row_dict[self.to_string(key)] = row_dict[self.to_string(key)] + ' || ' + self.to_string(value)
            else:
                self.travel_element_xml(row_dict, child, tag + '__' + child.tag)
        return row_dict

    def parse_from_root(self):
        row_dict = {}
        row_dict = self.travel_element_xml(row_dict, self.each_item, self.each_item.tag)
        # sys.stdout.write('{}{} %'.format('\r >>>  Progress: ',
        #                                  (int((XMLParser.counter / int(XMLParser.total_element)) * 100))))

        print(">>>  Progress:  {} %   ".format(int((XMLParser.counter/XMLParser.total_element)*100)), end='\r')
        sys.stdout.flush()
        XMLParser.counter += 1
        XMLParser.dict_list.append(row_dict)

    def start(self):
        self.parse_from_root()

    @classmethod
    def output_csv(cls):
        output_file = "{}{}.csv".format('output_', cls.output_file_counter)
        main_df = pd.DataFrame(cls.dict_list)
        # main_df = main_df.rename(columns={col: col.rsplit('##',1)[-1] for col in main_df.columns})
        main_df.to_csv(os.path.join(output_path, output_file), index=False, quoting=csv.QUOTE_ALL, encoding='utf-8')
        # reset the class variables
        cls.output_file_counter += 1
        cls.dict_list = []
        cls.counter = 1
