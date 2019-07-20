import Music as msc

def load_stop_words():
    list = []
    with open('stopwords','r') as file:
        for word in file.readlines():
            list.append(word)

    return list

list_of_music = [
    #("Dream Theater", "Glass Prison"),
    #("Dream Theater", "Pull Me Under"),
    #("Michael Jackson", "Bad"),
    #("Pink Floyd", "Time"),
    #("Pink Floyd", "Keep Talking"),
    #("Rick Astley", "Never Gonna Give You Up"),
    #("Foster The People", "Pumped Up Kicks"),
    #("Panic at The Disco", "Nine in The Afternoon"),
    #("Tom Jobim", "Chega de Saudade"),
    #("Tom Jobim", "Garota de Ipanema"),
    #("Blind Guardian","Mirror Mirror"),
    #("Zumbis do Espaco", "Satan Chegou"),
    #("Panic! at The Disco", "Hey Look Ma, I made It"),
    #("Pink Floyd", "High Hopes"), ("Panic! at The Disco", "High Hopes"),
    #("Imagine Dragons", "Natural"),
    #("twenty one pilots", "Chlorine"),
    #("The Black Keys","Lo Hi"),
    #("Iron Maiden","Blood Brothers"),
    #("Iron Maiden","The Trooper")
]

for (artist, title) in list_of_music:
    test1 = msc.Music(artist, title)
    for word in load_stop_words():
        test1.remove_word_from_lyric(word)
    gw = msc.GraphicalWriter(test1)
    gw.create_grafical_representation()
