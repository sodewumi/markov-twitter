import sys
from random import choice

class LowerCaseMixin(object):
    """A Mixin that converts any string to lowercase"""

    def lower_case(self, markov_text):
        return markov_text.lower()

class RemovePunctuationMixin(object):
    """A mixin that removes punctuation from a string"""

    def rm_punctuation(self, markov_text):
        string_wo_punctuation = ""
        for ltr in markov_text:
            if ltr.isalpha() or ltr == " ":
                string_wo_punctuation += ltr
        return string_wo_punctuation

class SimpleMarkovGenerator(object):
    def __init__(self, length):
        self.length = length


    def read_files(self, filenames):
        """Given a list of files, make chains from them."""
        file_list = []
        for filename in filenames:
            open_file = open(filename)
            open_file = open_file.read().split()
            file_list.extend(open_file)
        
        # print file_list
        return self.make_chains(file_list)



    def make_chains(self, corpus_path):
        """Takes input text as string; stores chains."""

        key = []
        n_grams = {}

        for i in range(len(corpus_path)-self.length):

            for t in range(self.length):
                key.append(corpus_path[i+t])

            key = tuple(key)

            nxt_word = corpus_path[i + self.length]

            n_grams.setdefault(key, []).append(nxt_word)

            key = []

        return self.make_text(n_grams)
        

    def make_text(self, chains):
        """Takes dictionary of markov chains; returns random text."""

        # choose a random bi-gram then find the value of said bi-gram. 
        # Afterward choose a random value from the generated list
        random_n_gram = choice(chains.keys())
        random_word = choice(chains[random_n_gram])
        generated_txt = random_word

        # the last word from the previous bi-gram key along with the randomly
        # choosen word is saved for the next iteration of the while loop
        next_tuple = random_n_gram[1:] + tuple([random_word])
        n_gram_value = chains.get(next_tuple)

        while n_gram_value:
            # the random word is put in the first element of the nxt word tuple,
            # and the second element is the newly choosen random word.
            new_random_word = choice(n_gram_value)
            generated_txt = generated_txt +" "+ new_random_word
            next_tuple = next_tuple[1:] + tuple([new_random_word])

            # if the bi-gram from the previous while loop has a value, return it
            # If there is not a value, return None and close the loop
            n_gram_value = chains.get(next_tuple)


        return generated_txt

class Twitter(SimpleMarkovGenerator):

    def __init__(self, length):
        super(Twitter, self).__init__(length)
    
    def read(self, filenames):
        return self.read_files(filenames)

    def make_text(self, chains):
        """Takes dictionary of markov chains; returns random text."""

        # choose a random bi-gram then find the value of said bi-gram. 
        # Afterward choose a random value from the generated list
        random_n_gram = choice(chains.keys())
        random_word = choice(chains[random_n_gram])
        generated_txt = random_word

        # the last word from the previous bi-gram key along with the randomly
        # choosen word is saved for the next iteration of the while loop
        next_tuple = random_n_gram[1:] + tuple([random_word])
        n_gram_value = chains.get(next_tuple)

        while n_gram_value and len(generated_txt) < 141:
            # the random word is put in the first element of the nxt word tuple,
            # and the second element is the newly choosen random word.
            new_random_word = choice(n_gram_value)
            if len(generated_txt +" "+ new_random_word) < 141:
                generated_txt = generated_txt +" "+ new_random_word
                next_tuple = next_tuple[1:] + tuple([new_random_word])
            else:
                break

            # if the bi-gram from the previous while loop has a value, return it
            # If there is not a value, return None and close the loop
            n_gram_value = chains.get(next_tuple)

        return generated_txt





if __name__ == "__main__":

    # we should get list of filenames from sys.argv
    # we should make an instance of the class
    # we should call the read_files method with the list of filenames
    # we should call the make_text method 5x

    n_gram_length = int(raw_input("How long do you want you n_gram to be > "))

    punctuation = raw_input("Do you want to check for punctuation? Yes or No > ")

    twitter = raw_input("do you want a twitter bot?")

    if twitter == "yes":
        mwp = Twitter(n_gram_length)
        mwp.read(sys.argv[1:])
    elif twitter == "no":  
        smg = SimpleMarkovGenerator(n_gram_length)
        smg.read_files(sys.argv[1:])