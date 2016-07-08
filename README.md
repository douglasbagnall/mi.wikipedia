# A corpus of Māori text from Wikpedia

This corpus is derived from http://mi.wikpedia.org which is the Māori
wikipedia and is a readily available source of modern written Māori by
many authors on many topics. The language and information is probably
of variable quality.

The text is by various authors, as listed at http://mi.wikpedia.org,
and is [CC-BY-SA licensed](https://creativecommons.org/licenses/by-sa/3.0/).

The associated bits of software are GPLv3 licensed.

## Steps to reproduce

1. Get a wikipedia dump file:

```
    wget https://dumps.wikimedia.org/miwiki/latest/miwiki-latest-pages-articles.xml.bz2
    # This one is actually from 2016-06-01
    # wget https://dumps.wikimedia.org/miwiki/20160601/miwiki-20160601-pages-articles-multistream.xml.bz2
    bunzip2 miwiki-latest-pages-articles.xml.bz2
```

2. Clone and run https://github.com/attardi/wikiextractor

Don't bother with the `setup.py` stuff, just run it in place:

    ~/src/wikiextractor/WikiExtractor.py --min_text_length 500 -xns 0  -o - \
    miwiki-latest-pages-articles.xml > mi-wp-min-500.txt

This creates a file `mi-wp-min-500.txt` containing all the articles
that contain more than 500 characters of text. The articles are
separated by `</doc><doc ...>` pseudo-xml tags. There are many
articles shorter than 500 characters, but the majority of them appear
to be automatically generated stubs, with very repetitive language.

3. Clean up the corpus a bit.

A few articles are mostly in English. You can find them by searching
for `the` (there are false positives, but no long stretch of English
can evade this search). Or maybe you can just apply the patch:

    patch mi-wp-min-500.txt < mi-wp-min-500-remove-english.patch

4. Remove article boundary markers

Remove the `<doc>` tags:

    grep -vP '</?doc.*>' mi-wp-min-500.txt > mi-wp-min-500-text-only.txt


##  Nga kōrero a Reweti Kohere Mā

This one is quite simple, though it contains a number of English phrases.

```
wget http://nzetc.victoria.ac.nz//tm/scholarly/tei-TeoNgak.html
./extract-nzetc-text TeoNgak.xml > nga-kōrero-a-reweti-kohere-mā.txt
```

## Te Ngutu Kura spelling dictionary

This is a dictionary compiled by
[Karaitiana Taiuru](http://www.taiuru.maori.nz/) and made available
under the
[CC-BY license](https://creativecommons.org/licenses/by/3.0/). It is
essentially just a word list, designed for spell-checking software. As
such it is not much help in finding the natural frequencies of various
n-grams, but it does ensure exposure to a range of words.

```
wget http://www.taiuru.maori.nz/tnk/aspell/mi_NZ.dic
```

## count-ngrams and notes

The `count-ngrams` script calculates some very simple statistics about
the n-grams that occur in the corpus, while the `notes` directory
contains examples of its output. Use `count-ngrams --help`.
