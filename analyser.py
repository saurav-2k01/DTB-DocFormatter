from langdetect import detect
import re
from doc_reader import DocReader
from doc_writer import DocWriter

class Analyser(object):
    def __init__(self, data):
        self.data = data

    def get_language(self):
        """ get_language function is used for getting the language of the data"""
        lang = {}
        try:
            for item in self.data:
                try:
                    language = detect(item.strip())
                    if language not in lang.keys():
                        lang[language] = 1
                    else:
                        lang[language] += 1
                except:
                    continue
        except TypeError as T:
            print("Type error occurred.")
            return -1
        index = list(lang.values()).index(max(lang.values()))
        language = list(lang.keys())[index]
        if language.lower() == "hi".lower():
            language = "Hindi"
        elif language.lower() == "en".lower():
            language = "English"
        else:
            pass
        return language


    def check_pattern(self):
        """ check_pattern function is used for analysing pattern of data and scoring them.
            it return a tuple of count of pattern matched, total number of items in data and
            score as total number of pattern matched divided by total number of items in the data.
            as (items_matched, items_count, score)
        """
        items_count = len(self.data)
        ques_pattern = r".+\?$|.+"
        opt_pattern = r"\(\w\).+"
        ans_pattern = r"Answer.*:?.+"
        items_matched = 0
        try:
            for items in self.data:
                particle_matched = 0
                particles = items.strip().split("\n")
                particles_count = len(particles)
                if re.match(ques_pattern, particles[0]):
                    particle_matched += 1
                else:
                    continue
                particle_matched += len(re.findall(opt_pattern, items))
                if re.match(ans_pattern, particles[-1]):
                    particle_matched += 1
                else:
                    continue
                particle_score = particle_matched / particles_count
                items_matched += particle_score

            score = items_matched / items_count
            return items_matched, items_count, score
        except:
            print("Something went wrong while analysing pattern.")
            return -1

