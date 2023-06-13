import csv
import re
import time
import psutil

def load_dictionary(file_path):
    dictionary = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) == 2:
                english_word = row[0]
                french_word = row[1]
                dictionary[english_word] = french_word
    return dictionary

def load_find_words(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        find_words = [word.strip() for word in file.readlines()]
    return find_words

def translate_text(input_text, dictionary):
    translated_text = input_text
    frequency = {}
    for word in dictionary.keys():
        pattern = r'\b' + re.escape(word) + r'\b'
        occurrences = re.findall(pattern, input_text)
        if occurrences:
            french_word = dictionary[word]
            translated_text = re.sub(pattern, french_word, translated_text)
            frequency[word] = len(occurrences)
    return translated_text, frequency

def save_output(file_path, translated_text):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(translated_text)

def save_frequency(file_path, frequency):
    with open(file_path, 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['English word', 'French word', 'Frequency'])
        for word, count in frequency.items():
            writer.writerow([word, dictionary[word], count])

def get_elapsed_time(start_time):
    elapsed_time = time.time() - start_time
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    return minutes, seconds

def get_memory_usage():
    process = psutil.Process()
    memory_usage = process.memory_info().rss / 1024 / 1024 # in MB
    return memory_usage



input_file = 't8.shakespeare.txt'
find_words_file = 'find_words.txt'
dictionary_file = 'french_dictionary.csv'
output_file = 't8.shakespeare.translated.txt'
frequency_file = 'frequency.csv'
performance_file = 'performance.txt'


dictionary = load_dictionary(dictionary_file)
find_words = load_find_words(find_words_file)


with open(input_file, 'r', encoding='utf-8') as file:
    input_text = file.read()


start_time = time.time()
translated_text, frequency = translate_text(input_text, dictionary)
minutes, seconds = get_elapsed_time(start_time)
memory_used = get_memory_usage()


save_output(output_file, translated_text)


save_frequency(frequency_file, frequency)


performance_text = f"Time to process: {minutes} minutes {seconds} seconds\nMemory used: {memory_used:.2f} MB"
with open(performance_file, 'w') as file:
    file.write(performance_text)
