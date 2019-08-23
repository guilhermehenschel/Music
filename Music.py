import re
import pylyrics3 as ply
from PIL import Image, ImageEnhance
import random
import numpy as np
import unidecode


def get_spaced_colors(n):
    max_value = 16581374  # 255**3
    interval = int(max_value / n)
    colors = [hex(I)[2:].zfill(6) for I in range(0, max_value, interval)]

    return [(int(i[:2], 16), int(i[2:4], 16), int(i[4:], 16)) for i in colors]

class Lyric:
    def __init__(self,lyric_str):
        self.lyric_as_is = str(lyric_str)
        self.lyric_as_list = re.split(r'\. |, |\* |\n |\t |! |\? |; |: |¡ |\( |\) | ', str(lyric_str))
        self.lyric_as_list = [x.lower() for x in self.lyric_as_list]
        self.lyric_as_list = list(filter(lambda a : a != '', self.lyric_as_list ))

    def lyrics_as_list(self):
        return self.lyric_as_list.copy()

    def remove_word_from_lyric(self,word):
        if word in self.lyric_as_list:
            self.lyric_as_list = list(filter(lambda a : a != word, self.lyric_as_list ))


class Music:
    def __init__(self,artist,music,lyric=None):
        self.music = unidecode.unidecode(music)
        self.artist = unidecode.unidecode(artist)
        if lyric is None:
            try:
                lyric = ply.get_song_lyrics(re.sub('[^A-Za-z0-9]+',' ', self.artist.replace('-','').replace('\'','')),re.sub('[^A-Za-z0-9]+',' ', self.music.replace('\'','')))
            except ValueError:
                #print("Couldn't Retrieve Lyrics for {%s} - {%s}" % (artist,music))
                lyric = "NotFound"
        if not lyric:
            #print("Couldn't Retrieve Lyrics for {%s} - {%s}" % (artist, music))
            lyric = "NotFound"
        self.lyrics = Lyric(lyric)

    def remove_word_from_lyric(self,word):
        self.lyrics.remove_word_from_lyric(word)

    def lyric_as_list(self):
        return self.lyrics.lyrics_as_list()


class ColorEncoder:
    def __init__(self, lyrics):
        set_of_words = set(lyrics)
        number_diferent_words = len(set_of_words)

        rgb = get_spaced_colors(number_diferent_words+2)

        rgb.remove((0,0,0))

        random.shuffle(rgb)

        self.word_color = dict()

        for i in range(0,len(lyrics)):
            word = lyrics[i]

            if word not in self.word_color:
                if i >= len(lyrics)-2:
                    color = rgb.pop()
                    self.word_color[word] = color
                else:
                    next_word = lyrics[i+1]
                    if next_word not in self.word_color:
                        color = rgb.pop()
                        self.word_color[word] = color
                    else:
                        next_color = self.word_color[next_word]
                        color = rgb.pop()
                        dist = np.linalg.norm(np.array(color) - np.array(next_color))
                        count = 0
                        while dist < 34.0 and count < number_diferent_words/2:
                            rgb.append(color)
                            color = rgb.pop()
                            dist = np.linalg.norm(np.array(color) - np.array(next_color))
                            count+=1

                        self.word_color[word] = color

    def color(self, word):
        return self.word_color[word]


class GraphicalWriter:
    def __init__(self,music):
        self.music = music
        self.color_encoder = None

    def create_grafical_representation(self):
        lyrics_list = self.music.lyric_as_list()
        if not self.color_encoder:
            self.color_encoder = ColorEncoder(lyrics_list)

        img_name = "Results/Images/%s_%s.jpeg" % (re.sub('[^A-Za-z0-9]+','', self.music.artist),re.sub('[^A-Za-z0-9]+','', self.music.music))
        img_name = img_name.replace('?','')
        im = Image.new('RGB',(len(lyrics_list), len(lyrics_list)),"black")

        pixels = im.load()

        for i in range(len(lyrics_list)):
            for j in range(len(lyrics_list)):
                if lyrics_list[i] == lyrics_list[j]:
                    pixels[i,j] = self.color_encoder.color(lyrics_list[i])

        resizingScale = 1
        if len(lyrics_list) < 1500:
            resizingScale = int(np.round(1500/len(lyrics_list)))

        im = im.resize((resizingScale*len(lyrics_list), resizingScale*len(lyrics_list)),resample=Image.BICUBIC)

        try:
            enh = ImageEnhance.Contrast(im)
            im = enh.enhance(1.3)
        except MemoryError:
            print(__name__, " [Memory Error]: ",self.music.artist,"-",self.music.music)

        try:
            enh = ImageEnhance.Sharpness(im)
            im = enh.enhance(1.3)
        except MemoryError:
            print(__name__, " [Memory Error]: ",self.music.artist,"-",self.music.music)

        im.save(img_name,"JPEG")





