class Noun:
    def __init__(self,stem,gender,irregular=False):
        self.stem = stem
        self.gender = gender
        self.irregular = irregular

        self.short_vowels = ['a','e','i','o','u','y']
        self.long_vowels = ['ā','ē','ī','ō','ū','ӯ']
        self.all_vowels = self.short_vowels + self.long_vowels
        self.stops = ['p','b','t','d','c','g','k']
        self.dentals = ['t','d']
        self.velars = ['c','g','k']

    def shorten_vowel(self,vowel):
        return self.short_vowels[self.long_vowels.index(vowel)]

    def lengthen_vowel(self,vowel):
        return self.long_vowels[self.short_vowels.index(vowel)]

    def vowel_weakening(self):
        if len(self.stem) < 2:
            return self.stem
        elif self.stem[-2] not in self.short_vowels:
            return self.stem
        else:
            if self.stem[-1] == 'r':
                return self.stem[:-2] + "e" + self.stem[-1]
            else:
                return self.stem[:-2] + "i" + self.stem[-1]

    def add_s(self):
        pass

    def add_m(self):
        if self.stem[-1] == "o":
            return self.stem[:-1] + "um"
        elif self.stem[-1] in self.short_vowels:
            return self.stem + 'm'
        elif self.stem[-1] in self.long_vowels:
            short_vowel = self.shorten_vowel(self.stem[-1])
            return  self.stem[:-1] + short_vowel + 'm'
        else:
            new_stem = self.vowel_weakening()
            return new_stem + 'em'

    def add_i(self):
        if self.stem[-1] == 'a':
            return self.stem + 'e'
        elif self.stem[-1] == 'o':
            return self.stem[:-1] + "ī"
        elif self.stem[-1] in self.short_vowels:
            return self.stem + "ī"
        elif self.stem[-1] in self.long_vowels:
            if self.stem[-1] == "ē":
                if self.stem[-2] in self.all_vowels:
                    return self.stem + "ī"
                else:
                    short_vowel = self.shorten_vowel(self.stem[-1])
                    return self.stem[:-1] + short_vowel + "ī"
            else:
                short_vowel = self.shorten_vowel(self.stem[-1])
                return self.stem[:-1] + short_vowel + "ī"
        else:
            new_stem = self.vowel_weakening()
            return new_stem + "ī"

    def add_nts(self):
        pass

    def add_ns(self):
        pass

    def add_sum(self):
        pass

    def add_e(self):
        pass

    def add_is(self):
        pass

    def add_es(self):
        pass

    def add_um(self):
        pass

    def add_ibus(self):
        pass

first = Noun('puella','feminine')
second = Noun('pino','feminine')
third = Noun('mīlet','feminine')
third_alt = Noun("cinis","feminine")
fourth = Noun('manu','feminine')
fifth = Noun('rē','feminine')
fifth_alt = Noun("diē","feminine")

words = [first,second,third,third_alt,fourth,fifth,fifth_alt]
[print(word.add_i()) for word in words]
