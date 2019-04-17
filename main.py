import requests
import json
import time
import csv

headers  = {'X-API-Key' : '53bd4b2f43ba42ab93608343956cd09b'}
base_url = 'https://www.bungie.net/Platform'
user     = 'TheAlpacalyps'
mem_type = str(2)
maps_dict = {
    332234118 : "Vostok",
    399506119 : "Endless Vale",
    532383918 : "Radiant Cliffs",
    750001803 : "Altar of Flame",
    777592567 : "Midtown",
    778271008 : "Emperor's Respite",
    806094750 : "Javelin-4",
    2233665874 : "Eternity",
    2262757213 : "Solitude",
    2473919228 : "Meltdown",
    2591737171 : "Gambler's Ruin",
    2666761222 : "Distant Shore",
    2748633318 : "Wormhaven",
    2810171920 : "Bannerfall",
    3164915257 : "The Dead Cliffs",
    3292922825 : "Firebase Echo",
    3404623499 : "The Citadel",
    3849796864 : "Retribution",
    4012915511 : "The Burnout",
    1153409123 : "Convergence",
    1583254851 : "The Fortress",
    1673114595 : "Pacifica",
    1711620427 : "Legion's Gulch",
    1815340083 : "Equinox"
}

modes_dict = {
    15 : "CrimsonDoubles",
    19 : "IronBanner",
    25 : "AllMayhem",
    31 : "Supremacy",
    32 : "PrivateMatchesAll",
    37 : "Survival",
    38 : "Countdown",
    39 : "TrialsOfTheNine",
    41 : "TrialsCountdown",
    42 : "TrialsSurvival",
    43 : "IronBannerControl",
    44 : "IronBannerClash",
    45 : "IronBannerSupremacy",
    48 : "Rumble",
    49 : "AllDoubles",
    50 : "Doubles",
    51 : "PrivateMatchesClash",
    52 : "PrivateMatchesControl",
    53 : "PrivateMatchesSupremacy",
    54 : "PrivateMatchesCountdown",
    55 : "PrivateMatchesSurvival",
    56 : "PrivateMatchesMayhem",
    57 : "PrivateMatchesRumble",
    59 : "Showdown",
    60 : "Lockdown",
    61 : "Scorched",
    62 : "ScorchedTeam",
    65 : "Breakthrough",
    67 : "Salvage",
    68 : "IronBannerSalvage",
    69 : "PvPCompetitive",
    70 : "PvPQuickplay",
    71 : "ClashQuickplay",
    72 : "ClashCompetitive",
    73 : "ControlQuickplay",
    74 : "ControlCompetitive"
}

# Get user id by PSN
search_user = '/Destiny2/SearchDestinyPlayer/' + mem_type + '/' + user + '/'
r           = json.loads(requests.get(base_url + search_user, headers = headers).content)

d2_membership_id = r['Response'][0]['membershipId']
# print(d2_membership_id)

profile   = '/Destiny2/' + mem_type + '/Profile/' + d2_membership_id + '/?components=100'
r         = json.loads(requests.get(base_url + profile, headers = headers).content)
character = r['Response']['profile']['data']['characterIds'][1]
# print(character)

matches = '/Destiny2/' + mem_type + '/Account/' + d2_membership_id + '/Character/' + character + '/Stats/Activities/?mode=5&count=250'
r       = json.loads(requests.get(base_url + matches, headers = headers).content)

with open('matches.csv', 'w') as csvfile:
    output = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    for match in r['Response']['activities']:
        date = match['period']
        mode = modes_dict[match['activityDetails']['mode']]
        map_name = maps_dict[match['activityDetails']['referenceId']]
        kills = match['values']['kills']['basic']['value']
        deaths = match['values']['deaths']['basic']['value']
        win = (match['values']['standing']['basic']['displayValue'] == "Victory")

        output.writerow((date, mode, map_name, kills, deaths, win))
