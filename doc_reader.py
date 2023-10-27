import csv
import pandas as pd
from docxlatex import Document as doctex
from docx import Document
from docx.opc.exceptions import PackageNotFoundError
from pylatexenc.latex2text import LatexNodes2Text
import re

""" Document reader """

class DocReader(object):
    def __init__(self, filename):
        self.filename = filename
        self.pattern = {
            "question": r"Question\s*.\s*(.*)",
            "option": r"\(\w\)\s*(.*)",
            "answer": r"Answer\s*:\s*\w",
            "exam_tag": r"Exam\sTag\s*:(.*)",
            "solution": r"Solution\s*:(.*)",
            "ques_pattern": r"\.+\?$|.+",
            "opt_pattern": r"\(\w\).+",
            "ans_pattern": r"Answer.*:?.+",
            "exception": r"[0-9]+\.+"
        }
        self.data = ""


    def latex2txt(self, latx):
        latx = fr"""{latx}"""
        txt = LatexNodes2Text().latex_to_text(latx)
        return txt


    def read_file(self, latex_flag=False):
        try:
            if latex_flag:
                doc = doctex(self.filename)
                data = doc.get_text()
                data = self.latex2txt(data)
                print("Document has been read successfully.")
                return data
            else:
                doc = Document(self.filename)
                data = [item.text for item in doc.paragraphs]
                data = "\n".join(data)
                print("Document has been read successfully.")
                return data
        except PackageNotFoundError as E:
            print("Something went wrong while reading file.")
            return -1


    def map_data(self, data):
        try:
            pattern = r"(Answer.*:?.+)"
            mapped_data = list(enumerate([i.strip() for i in re.split(pattern, data)]))
            print("Data has been mapped successfully.")
            return mapped_data
        except:
            print("Something went wrong while mapping data.")
            return -1


    def make_blocks(self, mapped_data: list):
        blocks = []
        try:
            for i in mapped_data:
                index, text = i
                if len(text) > 0:
                    if index % 2 == 0:
                        full_text = text + "\n" + mapped_data[index + 1][1]
                        blocks.append(full_text)
                    else:
                        pass
                else:
                    continue
            print("Making block accomplished.")
            return blocks
        except:
            print("Something went wrong while making blocks.")
            return -1


    def get_file_format(self):
        """ get_file_format function is used for returning extension of the file."""
        extension = self.filename.split(".")[-1]
        return extension


    def qoa_seperator(self, data):
        pattern = self.pattern
        if data[0] != -1:
            count = 1
            sep_qoa_list = []
            for i in data:
                if len(i) > 0:
                    sep_data = {"sr.no.": "", "question": "", "option": [], "answer": "", "solution": "",
                                "exam_tag": ""}
                    answer = re.findall(pattern["ans_pattern"], i)  # [0].split(":")[-1]
                    exam_tag = re.findall(pattern["exam_tag"], i)
                    sep_data["exam_tag"] = exam_tag
                    sep_data["answer"] = answer
                    # print(sep_data)
                    option = re.findall(pattern["opt_pattern"], i)
                    sep_data["option"] = option
                    question = re.sub(pattern["opt_pattern"], "", (re.sub(pattern["ans_pattern"], "", i))).strip()
                    if re.match(pattern["ques_pattern"], question):
                        if re.match(pattern["exception"], question):
                            question = re.split(pattern["exception"], question)[-1]
                            sep_data["question"] = question
                        else:
                            sep_data["question"] = question
                    else:
                        pass
                    sep_data["sr.no."] = count
                    count += 1
                    sep_qoa_list.append(sep_data)
                else:
                    pass
            print("Question, Option & Answer has been separated successfully.")
            return sep_qoa_list
        else:
            print("Something went wrong while separating Question, Option & Answer.")
            return -1


    def make_dict(self, data):
        final_data = []
        try:
            for dict_ in data:
                temp = {}
                for key, value in dict_.items():
                    if key == "sr.no.":
                        temp["sr.no."] = value
                    elif key == "question":
                        temp["question"] = value
                    elif key == "option":
                        v = [re.sub("\(\w\)", "", i).strip() for i in value]
                        if len(dict_[key]) == 5:
                            temp['optionA'], temp['optionB'], temp['optionC'], temp['optionD'], temp['optionE'] = v
                        else:
                            temp['optionA'], temp['optionB'], temp['optionC'], temp['optionD'] = v
                    elif key == "answer":
                        temp['answer'] = value[0].split(":")[-1].strip()
                    elif key == "solution":
                        temp["solution"] = ""
                    elif key == "exam_tag":
                        temp["exam_tag"] = ""
                final_data.append(temp)
            print("Making dictionary accomplished.")
            return final_data
        except:
            print("Something went wrong while making dictionary.")
            return -1

    def remove_key(self, listdict_: list[dict], *keys):
        for key in keys:
            try:
                for dict_ in listdict_:
                    del dict_[key]
                print(f"Given keys [{key}] removed successfully.")
            except (KeyError, TypeError)as E:
                print("key error occurred ", E)
                return -1


"""dr = DocReader("SET-1(29-01-2017) 1 TO 75 QUESTION.docx")
data = dr.read_file(latex_flag=True)
data = dr.map_data(data)
data = dr.make_blocks(data)
data = dr.qoa_seperator(data)
data = dr.make_dict(data)
for i in data:
    del i["sr.no"]
    del i ["exam_tag"]
csv = dr.to_csv("abc", data)
excel = dr.csv2excel("abc.csv")
"""