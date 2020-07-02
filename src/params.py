class Params:
    # leagues we have in db
    leagues = [ 'premiere_league', 'la_liga', 'serie-a', 'bundesliga', 'championship','segunda_division', 'serie-b' ]

    # link were we get info
    link_leagues = {'premiere_league': 'https://footystats.org/england/premier-league/fixtures',
                    'la_liga': 'https://footystats.org/spain/la-liga/fixtures',
                    'serie-a': 'https://footystats.org/italy/serie-a/fixtures',
                    'bundesliga': 'https://footystats.org/germany/bundesliga/fixtures',
                    'championship': 'https://footystats.org/england/championship/fixtures',
                    'segunda_division': 'https://footystats.org/spain/segunda-division/fixtures',
                    'serie-b': 'https://footystats.org/italy/serie-b/fixtures'}

    # list unique of teams per league
    list_teams = {'premiere_league': [ 'Norwich City', 'Tottenham Hotspur', 'Watford',
                                       'Brighton & Hove Albion', 'West Ham United', 'AFC Bournemouth',
                                       'Newcastle United', 'Aston Villa', 'Everton', 'Liverpool', 'Arsenal',
                                       'Crystal Palace', 'Sheffield United', 'Southampton', 'Wolverhampton Wanderers',
                                       'Burnley', 'Chelsea', 'Manchester United', 'Leicester City', 'Manchester City' ],
                  'la_liga': [ 'FC Barcelona', 'Real Madrid', 'Atlético Madrid', 'Sevilla FC',
                               'Getafe CF', 'Villarreal', 'Real Sociedad', 'Valencia CF',
                               'Athletic Club Bilbao', 'Granada CF', 'CA Osasuna', 'Levante UD',
                               'Real Betis', 'Real Valladolid', 'Deportivo Alavés',
                               'Celta de Vigo', 'SD Eibar', 'RCD Mallorca', 'Leganés',
                               'RCD Espanyol' ],
                  'serie-a': [ 'Juventus', 'Lazio', 'Inter Milan', 'Atalanta', 'Roma', 'Napoli',
                               'AC Milan', 'Parma', 'Hellas Verona', 'Cagliari', 'Bologna',
                               'Sassuolo', 'Torino', 'Fiorentina', 'Udinese', 'Sampdoria',
                               'Genoa', 'Lecce', 'Brescia', 'SPAL' ],
                  'bundesliga': [ 'Bayern München', 'Borussia Dortmund', 'RB Leipzig',
                                  "Borussia M'gladbach", 'Bayer Leverkusen', 'Hoffenheim',
                                  'Wolfsburg', 'Freiburg', 'Eintracht Frankfurt', 'Hertha BSC',
                                  'Union Berlin', 'Schalke 04', 'Mainz 05', 'Köln', 'Augsburg',
                                  'Werder Bremen', 'Fortuna Düsseldorf', 'Paderborn' ],
                  'championship': [ 'Leeds United', 'West Bromwich Albion', 'Brentford',
                                    'Nottingham Forest', 'Fulham', 'Cardiff City', 'Preston North End',
                                    'Derby County', 'Blackburn Rovers', 'Swansea City', 'Millwall',
                                    'Bristol City', 'Sheffield Wednesday', 'Queens Park Rangers',
                                    'Reading', 'Birmingham City', 'Wigan Athletic',
                                    'Charlton Athletic', 'Middlesbrough', 'Stoke City', 'Hull City',
                                    'Huddersfield Town', 'Luton Town', 'Barnsley' ],
                  'segunda_division': [ 'Cádiz', 'Real Zaragoza', 'SD Huesca', 'Almería', 'Girona FC',
                                        'Elche CF', 'AD Alcorcón', 'Rayo Vallecano', 'CD Tenerife',
                                        'Sporting Gijón', 'Mirandés', 'SD Ponferradina', 'CF Fuenlabrada',
                                        'UD Las Palmas', 'Málaga CF', 'Deportivo La Coruña',
                                        'Albacete Balompié', 'CD Numancia', 'Real Oviedo', 'CD Lugo',
                                        'Extremadura UD', 'Racing Santander' ],
                  'serie-b': [ 'Benevento', 'Crotone', 'Cittadella', 'Spezia', 'Pordenone',
                               'Frosinone', 'Chievo', 'Salernitana', 'Pisa', 'Empoli',
                               'Virtus Entella', 'Perugia', 'Venezia', 'Pescara', 'Juve Stabia',
                               'Cremonese', 'Ascoli', 'Cosenza', 'Trapani', 'Livorno' ]}

    # links were we find odds of next games
    link_odds_next = {'premiere_league': 'https://www.betexplorer.com/soccer/england/premier-league/',
                      'la_liga': 'https://www.betexplorer.com/soccer/spain/laliga/',
                      'serie-a': 'https://www.betexplorer.com/soccer/italy/serie-a/',
                      'bundesliga': 'https://www.betexplorer.com/soccer/germany/bundesliga/',
                      'championship': 'https://www.betexplorer.com/soccer/england/championship/',
                      'segunda_division': 'https://www.betexplorer.com/soccer/spain/laliga2/',
                      'serie-b': 'https://www.betexplorer.com/soccer/italy/serie-b/'
                      }

    """dict to link info of next games to odds df per league
         keys: name of teams in games data frame
         values: name of teams in odds data frame"""
    dict_odds_next = {'premiere_league': {'Arsenal': 'Arsenal',
                                         'Aston Villa': 'Aston Villa',
                                         'Bournemouth': 'AFC Bournemouth',
                                         'Brighton': 'Brighton & Hove Albion',
                                         'Burnley': 'Burnley',
                                         'Chelsea': 'Chelsea',
                                         'Crystal Palace': 'Crystal Palace',
                                         'Everton': 'Everton',
                                         'Leicester': 'Leicester City',
                                         'Liverpool': 'Liverpool',
                                         'Manchester City': 'Manchester City',
                                         'Manchester Utd': 'Manchester United',
                                         'Norwich': 'Norwich City',
                                         'Newcastle': 'Newcastle United',
                                         'Sheffield Utd': 'Sheffield United',
                                         'Southampton': 'Southampton',
                                         'Tottenham': 'Tottenham Hotspur',
                                         'Watford': 'Watford',
                                         'West Ham': 'West Ham United',
                                         'Wolves': 'Wolverhampton Wanderers'},
                      'la_liga':    {'Ath Bilbao': 'Athletic Club Bilbao',
                                     'Atl. Madrid': 'Atlético Madrid',
                                     'Osasuna': 'CA Osasuna',
                                     'Celta Vigo': 'Celta de Vigo',
                                     'Alaves': 'Deportivo Alavés',
                                     'Barcelona': 'FC Barcelona',
                                     'Getafe': 'Getafe CF',
                                     'Granada CF': 'Granada CF',
                                     'Leganes': 'Leganés',
                                     'Levante': 'Levante UD',
                                     'Espanyol': 'RCD Espanyol',
                                     'Mallorca': 'RCD Mallorca',
                                     'Betis': 'Real Betis',
                                     'Real Madrid': 'Real Madrid',
                                     'Real Sociedad': 'Real Sociedad',
                                     'Valladolid': 'Real Valladolid',
                                     'Eibar': 'SD Eibar',
                                     'Sevilla': 'Sevilla FC',
                                     'Valencia': 'Valencia CF',
                                     'Villarreal': 'Villarreal'},
                      'serie-a': {'AC Milan': 'AC Milan',
                                 'Atalanta': 'Atalanta',
                                 'Bologna': 'Bologna',
                                 'Brescia': 'Brescia',
                                 'Cagliari': 'Cagliari',
                                 'Fiorentina': 'Fiorentina',
                                 'Genoa': 'Genoa',
                                 'Verona': 'Hellas Verona',
                                 'Inter': 'Inter Milan',
                                 'Juventus': 'Juventus',
                                 'Lazio': 'Lazio',
                                 'Lecce': 'Lecce',
                                 'Napoli': 'Napoli',
                                 'Parma': 'Parma',
                                 'AS Roma': 'Roma',
                                 'Spal': 'SPAL',
                                 'Sampdoria': 'Sampdoria',
                                 'Sassuolo': 'Sassuolo',
                                 'Torino': 'Torino',
                                 'Udinese': 'Udinese'},
                      'bundesliga': {'Augsburg': 'Augsburg',
                                     'Bayer Leverkusen': 'Bayer Leverkusen',
                                     'Bayern Munich': 'Bayern München',
                                     'Dortmund': 'Borussia Dortmund',
                                     'B. Monchengladbach': "Borussia M'gladbach",
                                     'Eintracht Frankfurt': 'Eintracht Frankfurt',
                                     'Dusseldorf': 'Fortuna Düsseldorf',
                                     'Freiburg': 'Freiburg',
                                     'Hertha Berlin': 'Hertha BSC',
                                     'Hoffenheim': 'Hoffenheim',
                                     'FC Koln': 'Köln',
                                     'Mainz': 'Mainz 05',
                                     'Paderborn': 'Paderborn',
                                     'RB Leipzig': 'RB Leipzig',
                                     'Schalke': 'Schalke 04',
                                     'Union Berlin': 'Union Berlin',
                                     'Werder Bremen': 'Werder Bremen',
                                     'Wolfsburg': 'Wolfsburg'},
                      'championship': {'Barnsley': 'Barnsley',
                                     'Birmingham': 'Birmingham City',
                                     'Blackburn': 'Blackburn Rovers',
                                     'Brentford': 'Brentford',
                                     'Bristol City': 'Bristol City',
                                     'Cardiff': 'Cardiff City',
                                     'Charlton': 'Charlton Athletic',
                                     'Derby': 'Derby County',
                                     'Fulham': 'Fulham',
                                     'Huddersfield': 'Huddersfield Town',
                                     'Hull': 'Hull City',
                                     'Leeds': 'Leeds United',
                                     'Luton': 'Luton Town',
                                     'Middlesbrough': 'Middlesbrough',
                                     'Millwall': 'Millwall',
                                     'Nottingham': 'Nottingham Forest',
                                     'Preston': 'Preston North End',
                                     'QPR': 'Queens Park Rangers',
                                     'Reading': 'Reading',
                                     'Sheffield Wed': 'Sheffield Wednesday',
                                     'Stoke': 'Stoke City',
                                     'Swansea': 'Swansea City',
                                     'West Brom': 'West Bromwich Albion',
                                     'Wigan': 'Wigan Athletic'},
                      'segunda_division': {'Alcorcon': 'AD Alcorcón',
                                         'Albacete': 'Albacete Balompié',
                                         'Almeria': 'Almería',
                                         'Lugo': 'CD Lugo',
                                         'Numancia': 'CD Numancia',
                                         'Tenerife': 'CD Tenerife',
                                         'Fuenlabrada': 'CF Fuenlabrada',
                                         'Cadiz CF': 'Cádiz',
                                         'Dep. La Coruna': 'Deportivo La Coruña',
                                         'Elche': 'Elche CF',
                                         'Extremadura UD': 'Extremadura UD',
                                         'Girona': 'Girona FC',
                                         'Mirandes': 'Mirandés',
                                         'Malaga': 'Málaga CF',
                                         'Racing Santander': 'Racing Santander',
                                         'Rayo Vallecano': 'Rayo Vallecano',
                                         'R. Oviedo': 'Real Oviedo',
                                         'Zaragoza': 'Real Zaragoza',
                                         'Huesca': 'SD Huesca',
                                         'Ponferradina': 'SD Ponferradina',
                                         'Gijon': 'Sporting Gijón',
                                         'Las Palmas': 'UD Las Palmas'},
                      'serie-b': {'Ascoli': 'Ascoli',
                                 'Benevento': 'Benevento',
                                 'Chievo': 'Chievo',
                                 'Cittadella': 'Cittadella',
                                 'Cosenza': 'Cosenza',
                                 'Cremonese': 'Cremonese',
                                 'Crotone': 'Crotone',
                                 'Empoli': 'Empoli',
                                 'Frosinone': 'Frosinone',
                                 'Juve Stabia': 'Juve Stabia',
                                 'Livorno': 'Livorno',
                                 'Perugia': 'Perugia',
                                 'Pescara': 'Pescara',
                                 'Pisa': 'Pisa',
                                 'Pordenone': 'Pordenone',
                                 'Salernitana': 'Salernitana',
                                 'Spezia': 'Spezia',
                                 'Trapani': 'Trapani',
                                 'Venezia': 'Venezia',
                                 'Entella': 'Virtus Entella'}}
