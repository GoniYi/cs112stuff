from dataclasses import dataclass
import csv
import math
import re

@dataclass
class Song:
    id: int
    title: str
    year: int
    artist: str
    genre: str
    lyrics: list

"""
Place your answers to the Design check questions here:

1. {the: 2, dog: 1, bit: 1, man: 1}
   tf represents how often a word appears in a certain document while
   idf shows how the more unqiue the word is (the less it is repeated) the more
   weight it holds
   1
   ln(4/3)
   3ln(4/3)
2. We can give it a song that has a genre that we are certain of
   We can also consider sampled songs to see if it skews the data
   If the corpus is empty, return empty set or dictionary
"""
bad_characters = re.compile(r"[^\w]")

def clean_word(word: str) -> str:
    """input: string
    output: string
    description: using the bad characters regular expression, this function 
    strips out invalidcharacters"""
    word = word.strip().lower()
    return bad_characters.sub("", word)

def clean_lyrics(lyrics: str) -> list:
    """input: string representing the lyrics for a song
    output: a list with each of the words for a song
    description: this function parses through all of the lyrics for a song 
    and makes surethey contain valid characters"""
    lyrics = lyrics.replace("\n", " ")
    return [clean_word(word) for word in lyrics.split(" ")]

def create_corpus(filename: str) -> list:
    """input: a filename
    output: a list of Songs
    description: this function is responsible for creating the collection of 
    songs, including some data cleaning"""
    with open(filename, encoding="utf8") as f:
        corpus = []
        iden = 0
        for s in csv.reader(f):
            if s[4] != "Not Available": #if genre is NA
                new_song = Song(iden, s[1], s[2], s[3], s[4], 
                                                            clean_lyrics(s[5]))
                corpus.append(new_song)
                iden += 1
        return corpus #makes a new song with lyrics we can determine genre from

def compute_idf(corpus: list) -> dict:
    #DONE
    """input: a list of Songs
    output: a dictionary from words to inverse document frequencies (as floats)
    description: this function is responsible for calculating inverse document
      frequencies of every word in the corpus
    """
    lyrics = {}
    idf = {}
    for song in corpus:
        for word in song.lyrics:
            if word not in lyrics:
                lyrics[word] = set()
            lyrics[word].add(song.id)
    # #actual idf stuff
    for word in lyrics:
        idf[word] = math.log(len(corpus)/len(lyrics[word]))
    return idf 

def compute_tf(song_lyrics: list) -> dict:
    #DONE
    """input: list representing the song lyrics
    output: dictionary containing the term frequency for that set of lyrics
    description: this function calculates the term frequency for a set of lyrics
    """
    tf = {}
    for lyric in song_lyrics:
        if lyric not in tf:
            tf[lyric] = 1
        else:
            tf[lyric] += 1
    return tf

def compute_tf_idf(song_lyrics: list, corpus_idf: dict) -> dict:
    """input: a list representing the song lyrics and an inverse document 
    frequency dictionary
    output: a dictionary with tf-idf weights for the song (words to weights)
    description: this function calculates the tf-idf weights for a song
    """
    #DONE
    tf_idf = {}
    tf_dict = compute_tf(song_lyrics)
    for lyric in tf_dict:
        if lyric in corpus_idf:
            tf_idf[lyric] = tf_dict[lyric] * corpus_idf[lyric]
        elif lyric not in corpus_idf:
            tf_idf[lyric] = 0
    return tf_idf

def compute_corpus_tf_idf(corpus: list, corpus_idf: dict) -> dict:
    #DONE
    """input: a list of songs and an idf dictionary
    output: a dictionary from song ids to tf-idf dictionaries
    description: calculates tf-idf weights for an entire corpus
    """
    corpus_tf_idf = {}
    for song in corpus:
        corpus_tf_idf[song.id] = compute_tf_idf(song.lyrics, corpus_idf)
    return corpus_tf_idf

def cosine_similarity(l1: dict, l2: dict) -> float:
    """input: dictionary containing the term frequency - inverse document
    frequency weights (tf-idf) for a song, dictionary containing the term 
    frequency - inverse document frequency weights (tf-idf) for a song
    output: float representing the similarity between the values of the two 
    dictionaries description: this function finds the similarity score between 
    two dictionaries by representing them as vectors and comparing their 
    proximity.
    """
    magnitude1 = math.sqrt(sum(w * w for w in l1.values()))
    magnitude2 = math.sqrt(sum(w * w for w in l2.values()))
    dot = sum(l1[w] * l2.get(w, 0) for w in l1)
    return dot / (magnitude1 * magnitude2)

def nearest_neighbor(
    song_lyrics: str, corpus: list, corpus_tf_idf: dict, corpus_idf: dict
) -> Song:
    #DONE
    """input: a string representing the lyrics for a song, a list of songs,
    tf-idf weights for every song in the corpus, and idf weights for every 
    word in the corpus
    output: a Song object
    description: this function produces the song in the corpus that is most 
    similar to the lyrics it is given
    """
    most_similar_song = 0 #songid
    songtf_idf = compute_tf_idf(clean_lyrics(song_lyrics), corpus_idf)
    cos_sim_num = 0.0
    for id in corpus_tf_idf:
        if cosine_similarity(corpus_tf_idf[id], songtf_idf) > cos_sim_num:
            cos_sim_num = cosine_similarity(corpus_tf_idf[id], songtf_idf)
            most_similar_song = id
    for song in corpus: 
        if song.id == most_similar_song:
            return song

def main(filename: str, lyrics: str):
    corpus = create_corpus(filename)
    corpus_idf = compute_idf(corpus)
    corpus_tf_idf = compute_corpus_tf_idf(corpus, corpus_idf)
    print(nearest_neighbor(lyrics, corpus, corpus_tf_idf, corpus_idf).genre)

main("small_songdata.csv", " ".join(clean_lyrics("""You good, T-Minus?
Niggas been countin' me out
I'm countin' my bullets, I'm loadin' my clips
I'm writin' down names, I'm makin' a list
I'm checkin' it twice and I'm gettin' 'em hit
The real ones been dyin', the fake ones is lit
The game is off balance, I'm back on my shit
The Bentley is dirty, my sneakers is dirty
But that's how I like it, you all on my dick
I'm all in my bag, this hard as it get
I do not snort powder, I might take a sip
I might hit the blunt, but I'm liable to trip
I ain't poppin' no pill, but you do as you wish
I roll with some fiends, I love 'em to death
I got a few mil' but not all of them rich
What good is the bread if my niggas is broke?
What good is first class if my niggas can't sit?
That's my next mission, that's why I can't quit
Just like LeBron, get my niggas more chips
Just put the Rollie right back on my wrist
This watch came from Drizzy, he gave me a gift
Back when the rap game was prayin' I'd diss
They act like two legends cannot coexist
But I'd never beef with a nigga for nothin'
If I smoke a rapper, it's gon' be legit
It won't be for clout, it won't be for fame
It won't be 'cause my shit ain't sellin' the same
It won't be to sell you my latest lil' sneakers
It won't be 'cause some nigga slid in my lane
Everything grows, it's destined to change
I love you lil' niggas, I'm glad that you came
I hope that you scrape every dollar you can
I hope you know money won't erase the pain
To the OGs, I'm thankin' you now
Was watchin' you when you was pavin' the ground
I copied your cadence, I mirrored your style
I studied the greats, I'm the greatest right now
Fuck if you feel me, you ain't got a choice
Now I ain't do no promo, still made all that noise
This shit gon' be different, I set my intentions
I promise to slap all that hate out your voice
Niggas been countin' me out
I'm countin' my bullets, I'm loadin' my clips
I'm writin' down names, I'm makin' a list
I'm checkin' it twice and I'm gettin' 'em hit
The real ones been dyin', the fake ones is lit
The game is off balance, I'm back on my shit
The Bentley is dirty, my sneakers is dirty
But that's how I like it, you all on my dick
I just poured somethin' in my cup
I've been wantin' somethin' I can feel
Promise I am never lettin' up
Money in your palm don't make you real
Foot is on they neck, I got 'em stuck
I'ma give 'em somethin' they can feel
If it ain't 'bout the squad, don't give a fuck
Pistol in your hand don't make you real
I'm dead in the middle of two generations
I'm little bro and big bro all at once
Just left the lab with young 21 Savage
I'm 'bout to go and meet Jigga for lunch
Had a long talk with the young nigga Kodak
Reminded me of young niggas from 'Ville
Straight out the projects, no fakin', just honest
I wish that he had more guidance, for real
Too many niggas in cycle of jail
Spending they birthdays inside of a cell
We coming from a long bloodline of trauma
We raised by our mamas, Lord we gotta heal
We hurting our sisters, the babies as well
We killing our brothers, they poisoned the well
Distorted self image, we set up to fail
I'ma make sure that the real gon' prevail, nigga
I just poured somethin' in my cup
I've been wantin' somethin' I can feel
Promise I am never lettin' up
Money in your palm don't make you real
Foot is on they neck, I got 'em stuck
I'ma give 'em somethin' they can feel
If it ain't 'bout the squad, don't give a fuck
Pistol in your hand don't make you real
Money in your palm don't make you real
Pistol in your hand don't make you real
Money in your palm don't make you real""")))