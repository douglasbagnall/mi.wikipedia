# Library functions for manipulating Māori text corpora.
# Copyright Douglas Bagnall <douglas@halo.gen.nz> GPLv3
import re
import unicodedata
import sys

DIPHTHONGS = {
    'ae': 'æ',
    'ai': 'ȧ',
    'ao': 'å',
    'au': 'ä',
    'oi': 'ȯ',
    'oe': 'œ',
    'ou': 'ö',
    'ei': 'ė',
    'eu': 'ë'
}

def debug(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def possible_n_grams(n, state='v'):
    """Estimate the number of possible n-grams, very roughly."""
    # let's assume there are two states, vowel and consonant.
    # vowels = 10     # a e i o u ā ē ī ō ū
    # consonants = 10 # h k m n ng p r t w wh
    if n <= 0:
        return 1

    total = 0
    if state == 'v':
        total += 10 * possible_n_grams(n - 1, 'c')
    total += 10 * possible_n_grams(n - 1, 'v')
    return total


def generate_n_grams(n, prefix, diphthongs, macrons):
    """Estimate the number of possible n-grams, very roughly."""
    # let's assume there are two states, vowel and consonant.
    if n <= 0:
        return [prefix]

    chars = 'aeiou'
    if diphthongs:
        chars += ''.join(DIPHTHONGS.values())

    if macrons:
        chars += 'āēīōū'

    if prefix == '' or prefix[-1] in chars:
        chars += 'fhkmnŋprtw'

    ngrams = []
    for c in chars:
        ngrams.extend(generate_n_grams(n - 1, prefix + c, diphthongs, macrons))
    return ngrams


has_bad_letter = re.compile('[^aeiouāēīōūfhkmnŋprtw ]').search
has_bad_cluster = re.compile(r'[fhkmnŋprtw](?:[fhkmnŋprtw]|\b)').search

def has_english(text):
    if has_bad_letter(text) or has_bad_cluster(text):
        return True
    return False

def remove_english(text):
    words = text.split()
    good_words = []
    for word in words:
        if has_english(word):
            continue
        good_words.append(word)
    return ' '.join(good_words)


def normalise_text(text, diphthongs, macrons):
    text = unicodedata.normalize('NFC', text)
    text = text.lower()
    text = re.sub(r'[^\wāēōūī]+', ' ', text)
    text = re.sub(r'ng', 'ŋ', text)
    text = re.sub(r'wh', 'f', text)
    text = remove_english(text)
    if not macrons:
        text = demacronise(text)
    if diphthongs:
        for k, v in DIPHTHONGS.items():
            text = re.sub(k, v, text)
    return text


def denormalise_text(text):
    text = re.sub(r'ŋ', 'ng', text)
    text = re.sub(r'f', 'wh', text)
    for k, v in DIPHTHONGS.items():
        text = re.sub(v, k, text)
    return text


def demacronise(text):
    return (text
            .replace('ā', 'aa')
            .replace('ē', 'ee')
            .replace('ī', 'ii')
            .replace('ō', 'oo')
            .replace('ū', 'uu'))


def load_raw_text(filenames):
    raw = []
    for fn in filenames:
        f = open(fn)
        raw.append(f.read())
        f.close()
    return '\n\n'.join(raw)


def load_text(filenames, diphthongs=False, macrons=False):
    text = load_raw_text(filenames)
    return normalise_text(text, diphthongs, macrons)
