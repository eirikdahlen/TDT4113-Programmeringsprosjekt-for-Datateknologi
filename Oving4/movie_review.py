import os
import re
from operator import itemgetter
import math
from time import time

class Reader:

    def __init__(self, pos_path_and_reviews, neg_path_and_reviews, reader_type):
        # Tuppel på formen: (path til pos/neg reviews, listen over pos/neg reviews(filnavn)
        self.pos_path_and_reviews = pos_path_and_reviews
        self.neg_path_and_reviews = neg_path_and_reviews
        # Finner antall positive og negative reviews
        self.number_of_pos_reviews = len(self.pos_path_and_reviews[1])
        self.number_of_neg_reviews = len(self.neg_path_and_reviews[1])
        self.stop_words = self.get_stop_words()
        self.n = 3
        if reader_type == "training_data":
            self.pos_word_count = self.get_word_count(self.pos_path_and_reviews)
            self.neg_word_count = self.get_word_count(self.neg_path_and_reviews)
            self.top_pos_words = self.get_most_used_words("pos")
            self.top_neg_words = self.get_most_used_words("neg")
            self.pos_informative_words = self.most_informative_words("pos")
            self.neg_informative_words = self.most_informative_words("neg")


    def read_from_file(self, filepath):
        file = open(filepath, encoding='utf-8')
        r = file.read()
        review = re.sub("[.,#+()-:?!&<´>/;\"'^*]", '', r.lower()).split()
        for i in range(len(review) - self.n + 1):
            if self.n == 2:
                review.append(review[i] + "_" + review[i+1])
            elif self.n == 3:
                review.append(review[i] + "_" + review[i+1])
                review.append(review[i] + "_" + review[i + 1] + "_" + review[i+2])
        #Fjerner duplikater
        review = set(review)
        #Fjerner stoppord
        self.remove_stop_words(review)
        file.close()
        return review

    def get_word_count(self, review_type):
        word_counter = {}
        # Går gjennom hver fil i oppgitte review-typen (pos eller neg)
        for file in review_type[1]:
            # Leser av og samler alle ordene (maks 1 forekomst) i et set
            review = self.read_from_file(review_type[0] + file)
            # Går gjennom settet med ord og plusser på 1 forekomst for hvert ord
            for word in review:
                if word in word_counter:
                    word_counter[word] += 1
                else:
                    word_counter[word] = 1
        return word_counter

    def get_most_used_words(self, type):
        if type == "pos":
            word_counter = self.pos_word_count
        elif type == "neg":
            word_counter = self.neg_word_count
        return self.sort_dict(word_counter, 25)

    def sort_dict(self, dicti, end):
        # Sorterer etter value i dict, gir liste med tupler
        most_common_words = sorted(dicti.items(), key=itemgetter(1))
        most_common_words.reverse()
        most_common_words = most_common_words[:end]
        # Lager dict på formen {word: count, ...}
        # Vil ha dict fremfor liste med tupler, i tilfelle senere søk
        return dict(most_common_words)

    def most_informative_words(self, type):
        # Sjekker om jeg skal finne informasjonsverdien til ord fra positive eller negative anmeldelser
        if type == "pos":
            this = self.pos_word_count
            other = self.neg_word_count
        elif type == "neg":
            this = self.neg_word_count
            other = self.pos_word_count

        most_informative_words = {}
        for word in this:
            this_word_count = this[word]
            if word in other:
                other_word_count = other[word]
            else:
                other_word_count = 0
            # Pruner ordet, dvs. fjerner ordet dersom det ikke inngår i minst 3 % av reviewsene
            if self.valid_prune_value(this_word_count):
                informativ_value = this_word_count/ (this_word_count + other_word_count)
                most_informative_words[word] = informativ_value
        # Sorterer dict og har kuttet ned listen
        return self.sort_dict(most_informative_words, len(most_informative_words)//8)

    def valid_prune_value(self, this_word_count):
        return this_word_count/(self.number_of_pos_reviews + self.number_of_neg_reviews) > 0.03

    def get_popularity(self, word, top_words, number_of_reviews):
        return top_words[word] / number_of_reviews

    def remove_stop_words(self, words):
        for stop_word in self.stop_words:
            if stop_word in words:
                words.remove(stop_word)
        return words

    def get_stop_words(self):
        file = open("d\data\stop_words.txt", 'r')
        r = file.read()
        words = r.split()
        file.close()
        return words

class Clasification():
    def __init__(self, training_data, test_data):
        self.training_data = training_data
        self.test_data = test_data

    def read_from_file(self, filepath):
        return self.training_data.read_from_file(filepath)

    def is_positive_review(self, review):
        #print(review)
        pos_value = 0
        neg_value = 0
        for word in review:
            if word in self.training_data.pos_informative_words:
                informative_value = self.training_data.pos_informative_words[word]
                pos_value += math.log(informative_value)
            else:
            #if word not in self.training_data.pos_informative_words:
                # Straffer positive dersom det ikke inneholder ordet
                pos_value += math.log(0.03)
            if word in self.training_data.neg_informative_words:
                informative_value = self.training_data.neg_informative_words[word]
                neg_value += math.log(informative_value)
            else:
            #if word not in self.training_data.neg_informative_words:
                # Straffer negative dersom det ikke inneholder ordet
                neg_value += math.log(0.03)
        return pos_value > neg_value

#TESTFUNKSJON
def subset_testdata(training_data):
    print("---------------------------------DEL 1------------------------------------")
    pos_path = training_data.pos_path_and_reviews[0]  # Pathen til positive reviews
    neg_path = training_data.neg_path_and_reviews[0]  # Pathen til negative reviews
    pos_reviews = training_data.pos_path_and_reviews[1]  # Liste over alle de positive filnavnene
    neg_reviews = training_data.neg_path_and_reviews[1]  # Liste over alle de negative filnavnene
    # DEL 1 - Lag funksjonalitet for å lese et dokument i trenings-settet fra fil
    pos_first_review = pos_reviews[0]
    neg_first_review = neg_reviews[0]
    pos_review = training_data.read_from_file(pos_path + pos_first_review)
    neg_review = training_data.read_from_file(neg_path + neg_first_review)
    print("Liste med ord fra første postive review:")
    print(pos_review)
    print("Liste med ord fra første negative review:")
    print(neg_review)

    print("------------------------------DEL 2/DEL 3------------------------------------")
    # DEL 2 - Utvid koden til å lese alle filene i trenings-settet. Analyser representasjonen
    # så du finner de 25 mest populære ordene for hhv. positive og negative anmeldelser.
    # Popularitet = antall pos/neg anmeldelser med <ord> / antall pos/neg anmeldelser totalt
    # Utvid systemet til å fjerne alle stopp-ord
    top_pos = training_data.top_pos_words
    top_neg = training_data.top_neg_words
    top_pos_sort = sorted(top_pos.items(), key=itemgetter(1))
    top_neg_sort = sorted(top_neg.items(), key=itemgetter(1))
    top_pos_sort.reverse()
    top_neg_sort.reverse()
    print(top_pos_sort)
    print(top_neg_sort)
    word = "movie"
    print(word + " har popularitet " + str(training_data.get_popularity(word, training_data.top_pos_words,
                                                                          training_data.number_of_pos_reviews)) + " i positive reviewer")
    print(word + " har popularitet " + str(training_data.get_popularity(word, training_data.top_neg_words,
                                                                          training_data.number_of_neg_reviews)) + " i negative reviewer")

    print("---------------------------------DEL 4/ DEL 5/ DEL 6------------------------------------")
    # Utvid systemet til å finne informasjonsverdien av ord.
    # Skriv ut de 25 mest informative ordene for positive og negative anmeldelser
    # Prun vekk ord som ikke forekommer i minst 4 % av alle anmeldelsene
    # Implementer n-grams

    top_pos_inf = training_data.pos_informative_words
    top_neg_inf = training_data.neg_informative_words
    top_pos_sort_inf = sorted(top_pos_inf.items(), key=itemgetter(1))
    top_neg_sort_inf = sorted(top_neg_inf.items(), key=itemgetter(1))
    top_pos_sort_inf.reverse()
    top_neg_sort_inf.reverse()
    print("Mest informative ord for positive review:")
    print(top_pos_sort_inf)
    print("Mest informative ord for negative reviews:")
    print(top_neg_sort_inf)

    print("-----------------------------DEL 7------------------------------------------")

def alle_test(training_data, test_data):
    c = Clasification(training_data, test_data)

    pos_reviews = 0
    for file in test_data.pos_path_and_reviews[1]:
        review = test_data.read_from_file(test_data.pos_path_and_reviews[0] + file)
        if c.is_positive_review(review):
            pos_reviews += 1

    neg_reviews = 0
    for file in test_data.neg_path_and_reviews[1]:
        review = test_data.read_from_file(test_data.neg_path_and_reviews[0] + file)
        if not c.is_positive_review(review):
            neg_reviews += 1

    print("Antall positive reviews: " + str(test_data.number_of_pos_reviews) + " --> " + str(pos_reviews) + " ble analysert til positive")
    print("Antall negative reviews: " + str(test_data.number_of_neg_reviews) + " --> " + str(neg_reviews) + " ble analysert til negative")
    print("Riktig: " + str((pos_reviews + neg_reviews) / (test_data.number_of_pos_reviews + test_data.number_of_neg_reviews)*100) + "%")


def main():
    start = time()
    training_data = Reader(("d\data\\alle\\train\\pos\\", os.listdir("d\data\\alle\\train\\pos\\")),
                           ("d\data\\alle\\train\\neg\\", os.listdir("d\data\\alle\\train\\neg\\")), "training_data")

    subset_testdata(training_data)

    test_data = Reader(("d\data\\alle\\test\\pos\\", os.listdir("d\data\\alle\\test\\pos\\")),
                       ("d\data\\alle\\test\\neg\\", os.listdir("d\data\\alle\\test\\neg\\")), "test_data")

    alle_test(training_data,test_data)
    slutt = time()
    print("Brukte " + str(slutt-start) + " sekunder")
main()
