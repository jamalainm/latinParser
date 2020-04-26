from cltk.stem.latin.syllabifier import Syllabifier

class Stem:
    """
    
    Stem as of 2020.04.22 revolves around nominals and considers
    the changes that happen to a nominal stem when various
    inflections are added to it. I hope that this will eventually
    be extensible to more (all?) stem types.

    ...

    Attributes
    ----------
    stem : str
        the stem to be processed; this is not just the genitive
        minus the ending or the infinitive minus the "re" but
        is informed by historical linguistics and so beware
        the input. For example, the stem of "puer" is:
        "puero" and the stem of "capere" is "capi" and the
        stem of "mīles" is "mīlet".
        
        As may be apparent from the above paragraph, this
        class assumes the use of unicode characters and
        that vowels long by nature will be marked with
        macrons.

    short_vowels : list
        a list of short vowels

    long_vowels : a list of long vowels

    diphthongs : list
        not yet implemented; not sure how to deal with digraphs

    stops : list
        a list of consonants representing stops

    dentals : list
        a list of dental stops

    velars : list
        a list of velar stops

    Methods
    -------
    shorten_vowel(vowel)
        given a long vowel, returns the equivalent short
        vowel

    lenthen_vowel(vowel)
        given a short vowel, returns the equivalent long
        vowel

    rhotacism()
        used when adding a vowel to the stem to determine
        whether an [s] should evolve into an [r]

    vowel_weakening(rhotacized)
        given a stem that has been checked for rhotacism
        will weaken preceding short vowels; has not been
        checked against diphthongs yet (2020.04.22)

    add_s()
        adds [s] to the stem withe all the linguistic
        repercussions entailed

    add_m()
        adds [m] to the stem; assumes this is word final
        and so shortens preceding vowel; may need to adjust
        in future (2020.04.22)

    add_ei()
        This usually is simplified to [ī] in Classical Latin
        when it doesn't just combine to make a diphthong

    add_ns()
        The [n] is usually lost leading to compensatory
        lengthening of preceding short vowels.

    add_sum()
        the [s] experiences rhotacism and evolves into [r]

    add_e()
        Takes into account rhotacism and vowel lenition
        before addint the [e]

    add_is()
        For 3rd and 4th declension genitives; accounts for
        consonant and vowel stems.

    add_eis()
        primarily seen in 1st and 2nd declension dative/ablative
        plurals; eventually overwhelms the stem vowel as [īs]

    add_ibus()
        adds this sound to the stem, checking for final sounds,
        whether they are long/short vowels, or consonants, and
        adjusting the stem accordingly

    """
    def __init__(self,stem):
        self.stem = stem

        self.short_vowels = ['a','e','i','o','u','y']
        self.long_vowels = ['ā','ē','ī','ō','ū','ӯ']
        self.all_vowels = self.short_vowels + self.long_vowels
        self.stops = ['p','b','t','d','c','g','k']
        self.dentals = ['t','d']
        self.velars = ['c','g','k']

    def shorten_vowel(self,vowel):
        """ Return the shortened value of the given long vowel """
        return self.short_vowels[self.long_vowels.index(vowel)]

    def lengthen_vowel(self,vowel):
        """ Return the lengthened value of the given short vowel """
        return self.long_vowels[self.short_vowels.index(vowel)]

    def vowel_weakening(self,rhotacized):
        """
        Does not recognize diphthongs; assumes vowel is ante-
        penultimate; reduces short vowel in open syllable to
        [i] unless is is preceded by [r]

        ...

        Parameters
        ----------
        rhotacized = str
            assumes a check will have been run to determine
            whether a stem-final [s] must evolve into [r]

        """
        if len(rhotacized) < 2:
            return rhotacized
        elif rhotacized[-3] == 'i':
            return rhotacized
        elif rhotacized[-2] not in self.short_vowels:
            return rhotacized
        else:
            if rhotacized[-1] == 'r':
                return rhotacized[:-2] + "e" + rhotacized[-1]
            else:
                return rhotacized[:-2] + "i" + rhotacized[-1]

    def rhotacism(self):
        """
        Changes stem final [s] to [r]
        """
        if self.stem[-1] == 's' and self.stem[-2] in self.all_vowels:
            return self.stem[:-1] + "r"
        else:
            return self.stem

    def add_s(self):
        """
        Adds [s] to the stem and accounts for the various
        irregularities among nouns, not pronouns, as of
        2020.04.22.
        """
        if self.stem[-1] in self.dentals:
            return self.stem[:-1] + "s"
        elif self.stem[-1] == 'r':
            if self.stem[-2] in self.long_vowels:
                return self.stem[:-2] + self.shorten_vowel(self.stem[-2]) + 'r'
            else:
                return self.stem
        elif self.stem[-1] == 'n':
            if self.stem[-2] == 'e':
                return self.stem
            elif self.stem[-2] in self.short_vowels:
                return self.stem[:-2] + self.lengthen_vowel(self.stem[-2])
            else:
                return self.stem[:-1]
        elif self.stem[-1] in self.velars:
            return self.stem[:-1] + 'x'
        elif self.stem[-1] == "e":
            return self.stem[:-1] + "ēs"
        elif self.stem[-1] == 's':
            return self.stem
        elif self.stem[-1] != 'o':
            return self.stem + "s"
        else:
            if self.stem[-2] != 'r':
                return self.stem[:-1] + 'us'
            elif self.stem[-3] not in self.all_vowels:
                return self.stem[:-2] + 'er'
            else:
                syllabifier = Syllabifier()
                syllables = syllabifier.syllabify(self.stem)
                if len(syllables) != 3:
                    if self.stem == 'uiro':
                        return 'uir'
                    else:
                        return self.stem[:-1] + 'us'
                else:
                    if syllables[-2][-1] in self.short_vowels:
                        return self.stem[:-1]


    def add_m(self):
        """ Assumes this is a word final [m] and adds to stem """
        if self.stem[-1] == "o":
            return self.stem[:-1] + "um"
        elif self.stem[-1] == 'i':
            return self.stem[:-1] + 'em'
        elif self.stem[-1] in self.short_vowels and self.stem != 'i':
            return self.stem + 'm'
        elif self.stem[-1] in self.long_vowels:
            short_vowel = self.shorten_vowel(self.stem[-1])
            return  self.stem[:-1] + short_vowel + 'm'
        else:
            new_stem = self.rhotacism()
            new_stem = self.vowel_weakening(new_stem)
            return new_stem + 'em'

    def add_ei(self):
        """ 
        the [ei] is Old Latin which in Classical Latin is
        most often represented as [ī] when not combined. Some
        pragmatic and not strictly historically linguistic
        rules have been imposed below.
        """
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
            new_stem = self.rhotacism()
            new_stem = self.vowel_weakening(new_stem)
            return new_stem + "ī"

    def add_ns(self):
        """ lose the [n] and see compensatory lengthening """
        if self.stem[-1] in self.short_vowels:
            long_vowel = self.lengthen_vowel(self.stem[-1])
            return self.stem[:-1] + long_vowel + "s"
        elif self.stem[-1] in self.long_vowels:
            return self.stem + "s"
        else:
            new_stem = self.rhotacism()
            new_stem = self.vowel_weakening(new_stem)
            return new_stem + "ēs"

    def add_sum(self):
        """ rhotacism of [s] """
        if self.stem in self.short_vowels:
            long_vowel = self.lengthen_vowel(self.stem[-1])
            return self.stem[:-1] + long_vowel + "rum"
        else:
            return self.stem + "rum"

    def add_e(self):
        """ check for rhotacism and vowel lenition, then add [e] """
        new_stem = self.rhotacism()
        new_stem = self.vowel_weakening(new_stem)
        return new_stem + "e"

    def add_is(self):
        """ check for rhotacism and lenition; assimilate and add [e] """
        if self.stem[-1] == 'u':
            return self.stem[:-1] + 'ūs'
        elif self.stem[-1] in self.short_vowels:
            return self.stem[:-1] + 'is'
        else:
            new_stem = self.rhotacism()
            new_stem = self.vowel_weakening(new_stem)
            return new_stem + "is"

    def add_eis(self):
        """ gobble up final vowel of stem and add [īs] """
        return self.stem[:-1] + 'īs'

    def add_es(self):
        pass

    def add_um(self):
        pass

    def add_ibus(self):
        """ 
        Checks if final sound of stem is a vowel; if long
        only adds [bus], if short, replaces with [ibus] even
        in the 4th declension; if consonant then does 
        rhotacism check and lenition check.
        """
        if self.stem[-1] in self.long_vowels:
            return self.stem + "bus"
        elif self.stem[-1] == 'a':
            return self.stem[:-1] + "ābus"
        elif self.stem[-1] in self.short_vowels:
            return self.stem[:-1] + "ibus"
        else:
            new_stem = self.rhotacism()
            new_stem = self.vowel_weakening(new_stem)
            return new_stem + "ibus"

class Noun(Stem):
    """
    Inherits from the Stem class, and can apply the
    sound change rules. Additionally behaves differently
    according to the stem ending, producing the appropriate
    paradigm based onthe Noun classification into declension

    ...

    Attributes
    ----------
    stem : str
        this is the classical / Old Latin stem of the word;
        Note that it expects unicode characters, [u] for [v]
        and macrons to mark vowels that are long by nature

    gender : str
        As of 2020.04.22 this doesn't have any impact on the
        script. Eventually want to see neuter nouns treated
        differently.

    Methods
    -------
    each of these methods calls the affixing properties of
    the Stem class in order to represent the various cases
    for the basic declensions. Woud like to eventually add
    support for determiners, pronouns, and adjectives.

    """
    def __init__(self,stem,gender,irregular=False):
        super().__init__(stem)
        self.gender = gender

    def nom_sg(self):
        """ return the nominative singular form of a noun """
        if self.stem[-1] == 'a':
            return self.stem
        else:
            return super(Noun, self).add_s()

    def gen_sg(self):
        """ return the genitive signular form of a noun """
        if self.stem[-1] in ['a','o','ē']:
            return super(Noun, self).add_ei()
        else:
            return super(Noun, self).add_is()

    def dat_sg(self):
        """ return the dative singular form of a noun """
        return super(Noun, self).add_ei()

    def acc_sg(self):
        """ return the accusative singular form of a noun """
        return super(Noun, self).add_m()

    def abl_sg(self):
        """ return the ablative signular form of a noun """
        if self.stem[-1] in ['a','i','o','u']:
            return self.stem[:-1] + super(Noun, self).lengthen_vowel(self.stem[-1])
        elif self.stem[-1] not in self.all_vowels:
            return super(Noun, self).add_e()
        elif self.stem[-1] == 'ē':
            return self.stem

    def voc_sg(self):
        """ return the vocative singular form of a noun """
        if self.stem[-1] != 'o':
            return self.nom_sg()
        elif self.stem[-2] == 'i':
            return self.stem[:-2] + 'ī'
        else:
            nom = super(Noun, self).add_s()
            if nom[-1] == 'r':
                return nom
            else:
                return self.stem[:-1] + 'e'

first = Noun('fīlia','feminine')
second = Noun('libro','masculine')
third = Noun('mīlet','masculine')
fourth = Noun("manu",'masculine')
fifth = Noun('spē','feminine')
sixth = Noun('cīvi','masculine')
seventh = Noun('fīlio','masculine')
eighth = Noun('asino','masculine')
ninth = Noun('rēg','masculine')
tenth = Noun('prīncep','masculine')
eleventh = Noun('homon','masculine')
twelfth = Noun('sermōn','masculine')
thirteenth = Noun('sacerdōt','masculine')
fourteenth = Noun('labōr','masculine')
fifteenth = Noun('flāmen','masculine')
sixteenth = Noun('hiem','feminine')

words = [first,second,third,fourth,fifth,sixth,seventh,eighth,ninth,tenth,eleventh,twelfth,thirteenth,fourteenth,fifteenth,sixteenth]
[print(word.nom_sg(), word.gen_sg(), word.dat_sg(), word.acc_sg(), word.abl_sg()) for word in words]
