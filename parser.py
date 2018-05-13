#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess
import sys
import json

from datetime import datetime


def search_key(data, key, substr_flag = 0):
    
    if (data is None or len(data) == 0):
        return None
    
    for item in data:
        if (substr_flag == 0 and item == key or
            substr_flag == 1 and item[0:len(key)] == key or
            substr_flag == 2 and item[-len(key):] == key) :
            return data[item]
        if (type(data[item]) is dict):
            res = search_key(data[item], key)
            if (res is not None):
                return res
    return None

class Main:

    log_filename = ""
    parsed_arguments = []

    def __init__(self, logging = False):
        self.logging = logging
        if self.logging:
            self.log_path = os.path.dirname(os.path.abspath(__file__)) + '/logs'
            if not os.path.isdir(self.log_path):
                os.makedirs(self.log_path)
            self.log_filename = self.log_path + "/" + str(datetime.now().strftime("%Y-%m-%d.%H-%M-%S")) + ".txt"
            file_object  = open(self.log_filename, 'w')
            file_object.write("Start logging\n")
            file_object.close()

    def log(self, string, raw = False):
        if not self.logging:
            return None
        file_object  = open(self.log_filename, 'a')
        string = str(string)
        if not raw:
            string = string + "\n"
        file_object.write(string)
        file_object.close()


    def get_core_data(self, key):
        output = subprocess.check_output(["/usr/bin/sensors", "-j"])
        output = output.decode("utf-8")
        data = json.loads(output)
        self.log(data)
        max_cores = 50
        
        if (key[0:4] == 'Core'):
            return search_key(data, key)
        if (key == "max"):
            max_temp = 0
            max_key = None
            for core in range(0, max_cores):
                current_key = "Core " + str(core)
                current_data = search_key(data, current_key)
                if (current_data is not None):
                    current_temp = search_key(current_data, "input", 2)
                    if (current_temp is not None and current_temp > max_temp):
                        max_temp = current_temp
                        max_key = current_key
            return search_key(data, max_key)
        if (key == "discovery"):
            res = "{\n"
            res += "\t\"data\":[\n\n"
            is_first = True
            for core in range(0, max_cores):
                current_key = "Core " + str(core)
                current_data = search_key(data, current_key)
                if (current_data is not None):
                    if (is_first is False):
                        res += " },\n"
                    is_first = False
                    res += "\t{"
                    res += " \"{#CORENAME}\":\"" + current_key + "\""

            res += " }\n\n"
            res += "\t]\n"
            res += "}\n"

            
            self.log("Printing next JSON:")
            self.log(res)
            print(res)
            
        return None

    def read_argument(self):
        res = None
        if (len(self.parsed_arguments) > 0):
            res = self.parsed_arguments[0]
            self.parsed_arguments = self.parsed_arguments[1:]
        return res
    

    def main(self, arguments):
        self.parsed_arguments = arguments
        
        key = self.read_argument()
        if (key.isnumeric()):
            key = "Core " + key
        if (key == "Core"):
            number = self.read_argument()
            if (number.isnumeric):
                key = "Core " + number
            
        core_data = self.get_core_data(key)
        if (key == 'discovery'):
            return ''
        next_param = self.read_argument()
        value = None
        if (next_param is not None):
            value = search_key(core_data, next_param, 2)
        if (value is None):
            value = search_key(core_data, 'input', 2)
        if (value is None):
            self.log("Printing 0")
            print(0)
            return None
        self.log("Printing value = " + str(value))
        print(value)

if __name__ == '__main__':
    main = Main(False)
    main.log(sys.argv)
    if (len(sys.argv) > 1):
        main.main(sys.argv[1:])
    else:
        print("Usage:")
        print("\t" + sys.argv[0] + " KEY VALUE")
        print("\t\tKEY is one of (\d, max) where \d means Core number & max will look for a Core with max input temperature")
        print("\t\tVALUE is what to print (input, max, crit) allowed")
