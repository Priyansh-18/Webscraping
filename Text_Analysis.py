from bs4 import BeautifulSoup
import requests
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
import pandas as pd


def analyse_text(input_file, stop_word_file, positive_word_file, nagative_word_file):
    
    # web scraping process
    
    excel = pd.read_excel(input_file)
    analyzed_data = pd.DataFrame()
    
    for index, row in excel.iterrows():
        urliD = row['URL_ID']
        url = row['URL']
        get_data = requests.get(url)
        html_reader = BeautifulSoup(get_data.text, "html.parser")
        title = html_reader.title
    
        footer = html_reader.find_all(class_="tdm-descr")
        for i in footer:
            i.extract()

        para = html_reader.find_all("p")

        remove_links = [p for p in para if not p.find('a')]


        with open(f'{urliD}.txt', 'w', encoding='utf-8') as file:
            file.write(f"Title :{title.string}")
            for i in remove_links:
                file.write(i.text)
    
    
    # analysis of text files starts here
    
    for index, row in excel.iterrows():
        url_id = row['URL_ID']
        url = row['URL']

        with open(f'{url_id}.txt', 'r', encoding='utf-8') as file:
            text = file.read()
        
        words = word_tokenize(text)
        word_count = len(words)
        Personal_Pronouns_words =  'i','we','my','ours','us'

        with open(stop_word_file, 'r', encoding='utf-8') as file:
            data = file.read()
        stop = [word for word in data if word.lower() not in Personal_Pronouns_words]

        filtered_words = [word for word in words if word.lower() not in stop]
        filtered_score = len(filtered_words)
        filtered_score



        with open(positive_word_file, 'r', encoding='utf-8') as file:
            positive = file.read()

        positive_words = [word for word in filtered_words if word.lower() in positive]
        positive_score = len(positive_words)
        positive_score



        with open(nagative_word_file, 'r') as file:
            negative = file.read()

        negative_words = [word for word in filtered_words if word.lower() in negative]
        negative_score = len(negative_words)
        negative_score
        
        
        punctuations = '?','!',',','.'
        cleand_words = [word for word in filtered_words if word.lower() not in punctuations]
        cleaned_word_count = len(cleand_words)



        Polarity_Score = (positive_score-negative_score)/ ((positive_score + negative_score) + 0.000001)
        Polarity_Score = round(Polarity_Score, 3)
        
        
        Subjectivity_Score = (positive_score + negative_score)/ ((filtered_score) + 0.000001)
        Subjectivity_Score = round(Subjectivity_Score, 3)


        sentences = sent_tokenize(text)
        sentence_score = len(sentences)


        Average_Sentence_Length = filtered_score / sentence_score
        Average_Sentence_Length = round(Average_Sentence_Length, 3)


        complex_words = [word for word in filtered_words if len(word) > 2]
        complex_words_score = len(complex_words)
        complex_words_score


        Percentage_Complex_words = complex_words_score/filtered_score
        Percentage_Complex_words = round(Percentage_Complex_words, 3)


        Fog_Index = 0.4 * (Average_Sentence_Length + Percentage_Complex_words)
        Fog_Index = round(Fog_Index, 3)


        Average_Words_Per_Sentence = filtered_score / sentence_score
        Average_Words_Per_Sentence = round(Average_Words_Per_Sentence, 3)


        temp = 0
        def syllable_score(word):
            word = word.lower()
            count = 0
            vowels = 'aeiouy'
            for i in range(0, len(word)):
                if word[i] in vowels:
                    count += 1
            if word.endswith('es' or 'ed'):
                count -= 1

            return count

        for i in filtered_words:
            temp += syllable_score(i)


        syllables_per_word = temp / filtered_score
        syllables_per_word = round(syllables_per_word, 3)



        Personal_Pronouns_score = 0

        for i in filtered_words:
            if i in Personal_Pronouns_words:
                Personal_Pronouns_score += 1
        Personal_Pronouns_score


        total_character  = 0
        for i in filtered_words:
            for j in i:
                total_character += 1
        total_character



        Average_Word_Length = total_character/filtered_score
        Average_Word_Length = round(Average_Word_Length, 3)
    
        analysis = {'URL_ID':url_id,
                    'URL':url,
                    'POSITIVE SCORE':positive_score,
                    'NEGATIVE SCORE':negative_score,
                    'POLARITY SCORE':Polarity_Score,
                    'SUBJECTIVITY SCORE':Subjectivity_Score,
                    'AVG SENTENCE LENGTH':Average_Sentence_Length,
                    'PERCENTAGE OF COMPLEX WORDS':Percentage_Complex_words,
                    'FOG INDEX':Fog_Index,
                    'AVG NUMBER OF WORDS PER SENTENCE':Average_Words_Per_Sentence,
                    'COMPLEX WORD COUNT':complex_words_score,
                    'WORD COUNT':cleaned_word_count,
                    'SYLLABLE PER WORD':syllables_per_word,
                    'PERSONAL PRONOUNS':Personal_Pronouns_score,
                    'AVG WORD LENGTH':Average_Word_Length
                   }
        analyzed_data = analyzed_data.append(analysis, ignore_index=True)
    
    analyzed_data.to_excel('Analyzed_Data.xlsx', index=False)
    return analyzed_data
    
    


input_file = 'Input.xlsx'
stop_word_file = 'StopWords\StopWords_All.txt'
positive_word_file = 'positive-words.txt'
nagative_word_file = 'negative-words.txt'

analyse_text(input_file, stop_word_file, positive_word_file, nagative_word_file)




