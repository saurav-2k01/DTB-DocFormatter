import pandas as pd
import csv
from docx import Document
import xlsxwriter
import re

""" Doc-Format changer """

class DocWriter(object):
    def __init__(self, data:list):
        self.data = data

    def to_csv(self, filename: str,encoding: str='utf-8'):
        if ".csv" not in filename:
            filename = filename+".csv"
        else:
            pass
        fields = ["test_id", "question", "optionA", "optionB", "optionC", "optionD", "optionE", "answer", "solution",
                  "manual_update"]
        with open(filename, 'w', newline='', encoding=encoding, errors='ignore') as file:
            try:
                writer = csv.DictWriter(file, fieldnames=fields)
                writer.writeheader()
                writer.writerows(self.data)
                print(f"Data has been successfully saved in {filename}")
                return 1
            except:
                print("Something went wrong while converting writing csv file.")
                return -1


    def csv2excel(self, csv_file, excelfilename):
        if ".csv" not in csv_file:
            csv_file = csv_file+".csv"
        else:
            pass
        try:
            df = pd.DataFrame(self.data)
            writer = pd.ExcelWriter(excelfilename, engine="xlsxwriter")
            df.to_excel(writer, sheet_name="sheet1")
            writer.close()
        except:
            print("Something went wrong while converting csv file to excel file.")
            return -1

    def write2doc(self, filename):
        try:
            data = self.data
            doc = Document()
            item_count = len(data)
            count = 1
            for item in data:
                doc.add_paragraph(f"""Question: {count}
Level: Low
Tag: 
Answer: {item['answer']}
Hindi:
Q: {item['question']}
(a) {item['optionA']}
(b) {item['optionB']}
(c) {item['optionC']}
(d) {item['optionD']}
(e) 
Solution:\n\n""")
                count += 1
                progress = round((count / item_count) * 100)
                yield progress
            doc.save(filename)
            print("File has been written successfully")
        except:
            print("Some error occurred.")
            return -1
