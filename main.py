import Music as msc
import pandas as pd
import numpy as np
from sklearn import preprocessing
import chart_studio.plotly as plt
import plotly.express as plx
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

EXPORT_GRAFIC_ANALISIS = True

layoutPie = {
        "title": "Quantidade de Exemplos por Genero Musical",
        "grid": {"rows": 1, "columns": 1},
        "annotations": [
            {
                "font": {
                    "size": 20
                },
                "showarrow": False,
                "text": "Genero Musical"

            }
        ]
    }

def load_stop_words():
    list = []
    with open('stopwords','r') as file:
        for word in file.readlines():
            list.append(word)

    return list

def routine():



    file = pd.read_csv("Data/SpotifyFeatures.csv")
    file_frame = pd.DataFrame(file)
    with open("Results/describe.txt",'w') as desc_file:
        desc_file.write(str(file_frame.describe(include='all')))

    artist_list = file_frame['artist_name'].tolist()
    title_list = file_frame['track_name'].tolist()

    # print(len(file_frame.keys()))

    music_by_genre = dict()

    genres = file_frame['genre'].values
    genres = set(genres.flatten())
    #print(len(genres),genres)

    valueCounts = file_frame['genre'].value_counts().to_dict()
    valueCountsHtml = ""
    genresPieList = []
    for key, value in valueCounts.items():
        genresPieList.append(key)
        valueCountsHtml += "<li>" + key + " " + str(value) + " exemplos na base"

    trace_Pie = go.Pie(
        labels= genresPieList,
        values= [valueCounts[x] for x in genresPieList],
        domain={"column": 0},
        textinfo="label+percent+value",
        hole=.4
    )

    genres_Pie = [trace_Pie]

    fig2 = dict(data=genres_Pie, layout=layoutPie)
    genres_Pie_plot = plot(fig2,
                 config={"displayModeBar": True},
                 show_link=False,
                 include_plotlyjs=False,
                 output_type='div'
                 )

    #file_frame.cov().to_latex("Results/covariance.tex")
    #file_frame.corr().to_csv("Results/correlation.csv")
    #file_frame.corr().to_latex("Results/correlation.tex")
    #file_frame.corr(method='spearman').to_csv("Results/correlation_spearman.csv")
    #file_frame.corr(method='spearman').to_latex("Results/correlation_spearman.tex")

    # print("Missing Values:")
    # for key in file_frame.keys():
    #     print(key,':',sum(file_frame[key].isnull()))
    #
    # print("Outliers:")
    # for key in file_frame.keys():
    #     if file_frame[key].dtype != 'object':
    #         std_dev = file_frame[key].std()
    #         print(key, ':', (np.sum(np.abs(file_frame[key]) > 3.0*std_dev)))

    normalized_frame = file_frame.copy()
    for key in normalized_frame.keys():
        if normalized_frame[key].dtype != 'object':
            # normalized_frame[key] = (normalized_frame[key] - normalized_frame[key].min())/(normalized_frame[key].max() - normalized_frame[key].min())
            normalized_frame[key] = (normalized_frame[key] - normalized_frame[key].mean())/normalized_frame[key].std()

    with open("Results/describe_post_transform.txt",'w') as file:
        file.write(str(normalized_frame.describe(include='all')))

    baseName = ''''"Spotify Tracks DB - Music database (232k tracks) key, mode and time signature are cleaned"'''
    baseLink = '''"https://www.kaggle.com/zaheenhamidani/ultimate-spotify-tracks-db/"'''
    genresString = ''
    for genre in genres:
        genresString += "<li>"+genre+"</li>\n"

    head = '''<html>
        <head>
          <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
          <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css">
          <style>body{ margin:0 100; background:whitesmoke; }</style>
        </head>
        <body>'''

    capa = '''
        <div>
            <h5>Potificia Universidade Católica do Paraná</h5>
            <h5>Escola Politécnica</h5>
            <h5>Ciência de Dados</h5>
            <h5> Prof. Dr. Julio Cesar Nievola</h5>
            <br />
            <br />
            <h2> Relatório de Projeto </h2>
            <br />
            <br />
            <br /> 
            <h5> Guilherme Gustavo Henschel </h5>
        </div> 
    '''

    databaseDescription = '''
        <div>
            <h1>Descrição Da Base</h1>
            <br/>
            <p><b>Nome:</b>'''+ baseName + '''
            <p><a href=''' + baseLink + ''' > Link para Base </a>
            <p><b>Conteudo da Base:</b> <i>Dados de 232 mil (232725) músicas contidas no Spotify, afim de verificar dados diversos em relação ao genero musical</i>
            <p>Base de dados Forneceida por Zaheen Hamidani (<a href="https://www.kaggle.com/zaheenhamidani">https://www.kaggle.com/zaheenhamidani</a>) utilizando codigo fornecido por Tomi Gelo(<a href="https://www.kaggle.com/tomigelo">https://www.kaggle.com/tomigelo</a>) disponivel em (<a href="https://github.com/tgel0/spotify-data">https://github.com/tgel0/spotify-data</a>)
            <br />
            <h2>Descrição dos Atributos</h2>
            <p><b>Atributos:</b>
            <p> '<i>Atributo</i>' - <i>tipo de dado</i> [<i>min. value</i> - <i>max. value</i>]
            <ul>
                <li>'genre' - Nominal
                    <ol>
                    ''' + genresString + '''
                    </ol>
                </li>
                <li>'artist_name' - Nominal</li>
                <li>'track_name' - Nominal</li>
                <li>'track_id' - Nominal (unique)</li>
                <li>'popularity' - Real [0.0 - 100.000]
                <li>'acousticness' - Real [0.0 - 0.996000]</li>
                <li>'danceability' - Real [0.056900 - 0.989000]</li>
                <li>'duration_ms' - Real [1.538700e+04 - 5.552917e+06]</li>
                <li>'energy' - Real [0.000020 - 0.999000]</li>
                <li>'instrumentalness' - Real [0.0 - 0.999000]</li>
                <li>'key' - Nominal</li>
                <li>'liveness' - Real [0.009670 - 1.0]</li>
                <li>'loudness' - Real [-52.457000 - 3.744000]</li>
                <li>'mode' - Nominal
                    <ul>
                        <li>Major</li>
                        <li>Minor</li>
                    </ul>
                </li>
                <li>'speechiness' - Real [0.022200 - 0.967000]</li>
                <li>•'tempo' - Real [30.379000  - 242.903000 ]</li>
                <li>'time_signature' - Nominal </li>
                <li>'valence' - Real [0.0 - 1.0]</li>
            </ul>
            <br/>
            <i>Não foram encontradas Publicações originais que utilizaram essa base</i>
            <br/>
            <h3>Exemplos Para classificação</h3>
            ''' + genres_Pie_plot + '''
            <br />
        </div>
    '''

    scatterMatrix = plx.scatter_matrix(file_frame,
                                       dimensions=['popularity','acousticness','danceability','duration_ms'],color='genre')

    scatterMatrix2 = plx.scatter_matrix(file_frame,
                                        dimensions=['popularity','instrumentalness','liveness','loudness'], color='genre')

    scatterMatrix3 = plx.scatter_matrix(file_frame,
                                        dimensions=['popularity','speechiness','energy' ,'tempo','valence'], color='genre')

    scatterMatrixPlot = plot(scatterMatrix,
                           config={"displayModeBar": True},
                           show_link=False,
                           include_plotlyjs=False,
                           output_type='div'
                           ) + plot(scatterMatrix2,
                           config={"displayModeBar": True},
                           show_link=False,
                           include_plotlyjs=False,
                           output_type='div'
                           ) + plot(scatterMatrix3,
                           config={"displayModeBar": True},
                           show_link=False,
                           include_plotlyjs=False,
                           output_type='div'
                           )

    box1 = plx.box(file_frame, y='popularity',color='genre')
    box2 = plx.box(file_frame, y='duration_ms', color='genre')

    boxPlot = plot(box1,
                    config={"displayModeBar": True},
                    show_link=False,
                    include_plotlyjs=False,
                    output_type='div'
                    ) + plot(box2,
                    config={"displayModeBar": True},
                    show_link=False,
                    include_plotlyjs=False,
                    output_type='div'
                    )

    paralallelCoord = plx.parallel_coordinates(file_frame,color='popularity',color_continuous_scale=plx.colors.diverging.Geyser)
    paralallelCat = plx.parallel_categories(file_frame, dimensions=['genre','key','mode','time_signature'] ,color='popularity',color_continuous_scale=plx.colors.diverging.Geyser)

    paralallelPlot = plot(paralallelCoord,
                    config={"displayModeBar": True},
                    show_link=False,
                    include_plotlyjs=False,
                    output_type='div'
                    ) + plot(paralallelCat,
                    config={"displayModeBar": True},
                    show_link=False,
                    include_plotlyjs=False,
                    output_type='div'
                    )

    scatterEnergy = plx.scatter(file_frame,x='energy',y='loudness',color='genre')
    scatterEnergy2 = plx.scatter(file_frame, x='energy', y='acousticness', color='genre')
    scatterPlot = plot(scatterEnergy,
                    config={"displayModeBar": True},
                    show_link=False,
                    include_plotlyjs=False,
                    output_type='div'
                    ) + plot(scatterEnergy2,
                    config={"displayModeBar": True},
                    show_link=False,
                    include_plotlyjs=False,
                    output_type='div'
                    )

    estatiscalDescription = '''
        <div>
            <h1>Estatisticas</h1>
            <h3>Dataframe</h3>
            ''' + str(file_frame.describe(include="all").to_html()) + '''
            <h2>Graficos Estatisticos</h2>
            <h4>Scatter Matrix</h4>
            ''' + scatterMatrixPlot + '''
            <br/>
            <h4>Bar Plot</h4>
            ''' + boxPlot + '''
            <br />
            <h4>Parallel Coordinates</h4>
            ''' + paralallelPlot + '''
            <br />
            <h2>Correlações</h2>
            <p><b>Correlações Notáveis:</b>
            <p><i>Nota: Consideravel notável qualquer correlação com valor absoluto maior que 0.70</i>
            <ul>
                <li> <b>energy & loudness:</b> 0.81609 (pearson)</li>
                <li> <b>energy & acousticness:</b> -0.72558 (pearson)</li>
            </ul>
            <h4>Covariancias</h4>
            ''' + str(file_frame.cov().to_html()) + '''
            <h4>Correlações por Pearson</h4>
            ''' + str(file_frame.corr().to_html()) + '''
            <h4>Correlações por Spearman</h4>
            ''' + str(file_frame.corr(method='spearman').to_html()) + '''
            <h4>Scatter Plot</h4>
            ''' + scatterPlot + '''
        </div>
        <a href="Report2.html" >Proxima Pagina</a>
    '''

    normalized_frame = file_frame.copy()
    for key in normalized_frame.keys():
        if normalized_frame[key].dtype != 'object':
            normalized_frame[key] = (normalized_frame[key] - normalized_frame[key].min())/(normalized_frame[key].max() - normalized_frame[key].min())
            #normalized_frame[key] = (normalized_frame[key] - normalized_frame[key].mean()) / normalized_frame[key].std()

    paralallelCoord = plx.parallel_coordinates(normalized_frame, color='popularity',
                                               color_continuous_scale=plx.colors.diverging.Geyser)

    paralallelPlot = plot(paralallelCoord,
                          config={"displayModeBar": True},
                          show_link=False,
                          include_plotlyjs=False,
                          output_type='div'
                          )

    outliers = ""

    for key in normalized_frame.keys():
        if normalized_frame[key].dtype == "float64":
            n_outlier = sum(np.array(np.abs(normalized_frame[key] - normalized_frame[key].mean()) > 3*normalized_frame[key].std()))
            p_outliers = n_outlier/normalized_frame[key].count()
            outliers +="<li><b>" +str(key) + ":</b>  " + str(n_outlier) + "<i>( "+ str(p_outliers) +"% )</i></li>\n"


    boxPlot = ""

    for key in normalized_frame.keys():
        if normalized_frame[key].dtype == "float64":
            box = plx.box(normalized_frame, y=key, color='genre')
            boxPlot += plot(box,
                   config={"displayModeBar": True},
                   show_link=False,
                   include_plotlyjs=False,
                   output_type='div')

    baseTransform = '''
        <div>
            <h2>Normalização da Base</h2>
            <h4>Dataframe</h4>
            ''' + str(normalized_frame.describe().to_html()) + ''''
            <h4>Coordenadas Paralelas</h4>
             ''' + paralallelPlot + '''
            <h4>Outliers</h4>
            <p><i>Foi utilizado 3 desvios padrões para determinar o numero de outliers de cada variavel</i>
            <ul>
            ''' + outliers + '''
            </ul>
            <h4>Box plot</h4>
            ''' + boxPlot + '''
        </div>
    '''



    bottom = '''</body>
    </html>
    '''



    with open("Results/Report.html", 'w') as htmlReport:
        htmlReport.writelines([head,capa,databaseDescription,estatiscalDescription,bottom])

    with open("Results/Report2.html", 'w') as htmlReport:
        htmlReport.writelines([head, baseTransform, bottom])

    lyrics = []

    for index, row in file_frame.iterrows():
        artist = row['artist_name']
        title = row['track_name']
        test1 = msc.Music(artist, title)
        for word in load_stop_words():
            test1.remove_word_from_lyric(word)

        if test1.lyrics.lyric_as_is != "" and test1.lyrics.lyric_as_is != 'NotFound' and EXPORT_GRAFIC_ANALISIS:
            gw = msc.GraphicalWriter(test1)
            gw.create_grafical_representation()

        lyrics.append(test1.lyrics.lyric_as_is)

    file_frame['lyrics'] = pd.Series(lyrics)
    file_frame.to_csv("Data/WithLyrics.csv")

    with open("Results/describe2.txt", 'w') as desc_file:
        desc_file.write(str(file_frame.describe(include='all')))

    file_frame.describe(include='all').to_latex("Results/new_file.tex")

    from wordcloud import WordCloud, STOPWORDS

    comment_words = ' '
    stopwords = set(STOPWORDS)

    # iterate through the csv file
    for val in file_frame['lyrics'].CONTENT:

        # typecaste each val to string
        val = str(val)

        # split the value
        tokens = val.split()

        # Converts each token into lowercase
        for i in range(len(tokens)):
            tokens[i] = tokens[i].lower()

        for words in tokens:
            comment_words = comment_words + words + ' '

    wordcloud = WordCloud(width=800, height=800,
                          background_color='white',
                          stopwords=stopwords,
                          min_font_size=10).generate(comment_words)

    wordcloud.to_file("Results/WordCloud.jpeg")

    lyrcs_report = '''
        
    '''

    with open("Results/Report3.html", 'w') as htmlReport:
        htmlReport.writelines([head,lyrcs_report , bottom])

if __name__ == '__main__':
    routine()