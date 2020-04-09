from cltk.tokenize.latin.sentence import SentenceTokenizer
from cltk.stem.latin.j_v import JVReplacer
from cltk.lemmatize.latin.backoff import BackoffLatinLemmatizer
from cltk.tag import ner
from unidecode import unidecode

class TextFile:
    """

    TextFile process a .txt file using the cltk language
    processing tools to return a sentence stripped of 
    numbers and most punctuation. The period remains for
    its use in abbreviations which the sentence tokenizer
    can recognize.

    ...

    Attributes
    ----------
    file_name : str
        the name of the file

    Methods
    -------
    get_work()
        Returns a .txt file as a string
    sentence_tokenizer()
        Returns a list of sentences from a string

    """
    def __init__(self,file_name):
        self.file_name = file_name

    def get_work(self):
        """ Return the contents of a .txt file as a string """

        contents = ''

        with open(f"./{self.file_name}", "r") as myfile:
            for myline in myfile:
                contents += myline

        return contents

    def sentence_tokenizer(self):
        """ Return a list of sentences from a string """

        sent_tokenizer = SentenceTokenizer(strict=True)

        return sent_tokenizer.tokenize(self.get_work())

class Sentence:
    """

    Sentence processess a text string. using unidecode,
    cltk's j_v standardization and some basic replacement
    tools it removes non-alphabetical characters

    ...

    Attributes
    ----------
    sentence : str
        a string of text, presumably a sentence

    Methods
    -------
    remove_final_punctuation()
        Returns the string with the very last character
        removed

    remove_newlines()
        Returns the string without newlines

    remove_non_alpha()
        Returns the string stripped of numerals and most
        punctuation (excepting periods), as well as
        editorial characters such as brackets and daggers.

    remove_macrons()
        Using the unidecode package, returns a string where
        long marks over vowels are removed

    replace_j_and_v()
        Using cltk's tools, returns a string where 'j' and
        'v' are replaced by 'i' and 'u' respectively

    tokenize()
        Returns a list of 'words' that may still include
        periods; additional processing is still necessary
        to identify enclitics, remove names, and final
        periods

    """

    def __init__(self,sentence):
        self.sentence = sentence

    def __repr__(self):
        return self.sentence

    def remove_final_punctuation(self):
        self.sentence =  self.sentence[:-1]
        return self.sentence

    def remove_newlines(self):
        self.sentence = " ".join(self.sentence.splitlines())
        return self.sentence

    def remove_non_alpha(self):
        """ Return a string only consisting of words """

        translation_table = dict.fromkeys(map(ord, ",0123456789(){}[]*<>-+'†"), None)
        self.sentence = self.sentence.translate(translation_table)
        return self.sentence

    def remove_macrons(self):
        """ Return a string without macrons """
        self.sentence = unidecode(self.sentence)
        return self.sentence

    def replace_j_and_v(self):
        """ Return a string where 'j' and 'v' have been replaced """
        j = JVReplacer()
        self.sentence = j.replace(self.sentence)
        return self.sentence

    def tokenize(self):
        """ Return a list of 'words' """

        return self.sentence.split(' ')

class Word:
    """

    Word processess a word, splitting 'que' from the end if
    'que' is a conjunction and recognizes proper nouns,
    using cltk's named entity recognition

    After that initial processing, using cltk's backoff
    lemmatizer, it will return a tuple of the original
    word and its lemma

    Attributes
    ----------
    word : str
        a word, perhaps abbreviated or with enclitics

    Methods
    -------
    identify_proper_noun()
        returns True or False if the word is a proper noun

    identify_enclitic_que()
        returns True or False if the enclitic 'que' is
        present


    """

    def __init__(self,word):
        self.word = word

    def __repr__(self):
        return self.word

    def identify_proper_noun(self):
        """ Return True if a proper noun; very flawed """

        result = ner.tag_ner('latin', input_text=self.word, output_type=list)

        if len(result) > 0:
            if len(result[0]) > 1:
                return True
            else:
                return False

    def identify_enclitic_que(self):
        """ Return True if there's an enclitic 'que' """

        que_adverbs = [
                'atque','denique','itaque','namque','neque',
                'quoque','undique'
                ]
        que_inflected = [
                'plerique','plerumque','plerisque','quaeque',
                'quaque','quasque','quemque','quique','quisque',
                'quodque','quorumque','uterque','utramque','utraque',
                'utrisque','utriusque','utrumque'
                ]
        cumque_inflected = ['quascumque','quibuscumque',
                'quodcumque','quaecumque'
                ]
        
        que_words = que_adverbs + que_inflected + cumque_inflected

        if len(self.word) > 3:
            if self.word[-3:] == 'que':
                if self.word.lower() not in que_words:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

def compile_lemmata(filename):
    """ Given a .txt file, returns a list of lemmata ignoring names """

    unique_word_forms = ['que',]

    # compile list of unique word forms

    text = TextFile(filename)
    sentences = text.sentence_tokenizer()
    for sentence in sentences:
        sentence = Sentence(sentence)
        sentence.remove_final_punctuation()
        sentence.remove_newlines()
        sentence.remove_non_alpha()
        sentence.remove_macrons()
        sentence.replace_j_and_v()
        words = sentence.tokenize()
        for word in words:
            if word not in unique_word_forms:
                unique_word_forms.append(word)

    # remove proper nouns and enclitic 'que'

    for word in unique_word_forms:
        word_form = Word(word)
        if word_form.identify_proper_noun():
            unique_word_forms.remove(word)
        elif word_form.identify_enclitic_que():
            unique_word_forms.remove(word)
            real_word = word[:-3]
            if real_word not in unique_word_forms:
                unique_word_forms.append(real_word)

    # lowercase everything

    unique_word_forms = [word.lower() for word in unique_word_forms]

    # lemmatize unique_word_forms

    lemmatizer = BackoffLatinLemmatizer()

    lemma_pair = lemmatizer.lemmatize(unique_word_forms)

    # make list of unique lemmata

    unique_lemmata = []

    [unique_lemmata.append(pair[1]) for pair in lemma_pair if pair[1] not in unique_lemmata]

    return unique_lemmata

filename = 'allAPReadings.txt'
word_list = compile_lemmata(filename)
print(word_list)
