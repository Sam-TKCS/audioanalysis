from configparser import SafeConfigParser
import myspsolution as mysp
import os
from decimal import Decimal
import pprint
import sys

# path to the file's directory
def run_overview(file_title):
    file_location = os.getcwd()
    print("Running analysis on " + file_location+"/"+file_title)
    total = mysp.mysptotal(file_title, file_location)
    print(total)
    #index = total.index
    if total is False:
        return False
        
    return {
        'syllables_count': total.iloc[0][0],
        'pauses_count': total.iloc[1][0],
        'articulation_rate': total.iloc[3][0],
        'speaking_duration': total.iloc[4][0],
        'original_duration': total.iloc[5][0]
    }

def run_pronunciation_posteriori_probability_score_percentage(file_title):
    file_location = os.getcwd()
    print(f"Running Pronunciation posteriori probability score percentage on {file_location}/{file_title}")
    return mysp.mysppron(file_title, file_location)


def main():

    print("Name of file to analyze: ", sys.argv[1])


    overview = run_overview(sys.argv[1])
    score = run_pronunciation_posteriori_probability_score_percentage(sys.argv[1])
    rounded_score = round(score)
    
    words_per_minute = (Decimal(overview['syllables_count'])/Decimal(overview['original_duration']))*60/Decimal(1.66)
    articulation_rate = Decimal(overview['syllables_count'])/Decimal(overview['speaking_duration'])
    overview['pronunciation_articulation_score'] = Decimal(rounded_score).quantize(Decimal('.01'))
    overview['rate_of_speech_score'] = 100 - abs(round(words_per_minute) - 132)
    overview['rate_of_speech'] = words_per_minute.quantize(Decimal('.01'))
    overview['articulation_rate'] = articulation_rate.quantize(Decimal('.01'))
    # metrics['pause_score'] = (Decimal(metrics['pauses_count']) /  Decimal(metrics['original_duration'])).quantize(Decimal('.01'))
    
    pp = pprint.PrettyPrinter(indent=4)
    
    pp.pprint(overview)

main()