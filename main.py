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
    15 : "Crimson Doubles",
    19 : "IronBanner",
    25 : "Mayhem",
    31 : "Supremacy",
    32 : "PrivateMatchesAll",
    37 : "Survival",
    38 : "Countdown",
    39 : "Trials",
    41 : "Trials Countdown",
    42 : "Trials Survival",
    43 : "IB Control",
    44 : "IB Clash",
    45 : "IB Supremacy",
    48 : "Rumble",
    49 : "All Doubles",
    50 : "Doubles",
    51 : "PM Clash",
    52 : "PM Control",
    53 : "PM Supremacy",
    54 : "PM Countdown",
    55 : "PM Survival",
    56 : "PM Mayhem",
    57 : "PM Rumble",
    59 : "Showdown",
    60 : "Lockdown",
    61 : "Scorched",
    62 : "ScorchedTeam",
    65 : "Breakthrough",
    67 : "Salvage",
    68 : "IB Salvage",
    69 : "Comp",
    70 : "Quickplay",
    71 : "QP Clash",
    72 : "Comp Clash",
    73 : "QP Control",
    74 : "Comp Control"
}

# Get user id by PSN
search_user = '/Destiny2/SearchDestinyPlayer/' + mem_type + '/' + user + '/'
r           = json.loads(requests.get(base_url + search_user, headers = headers).content)

d2_membership_id = r['Response'][0]['membershipId']

profile   = '/Destiny2/' + mem_type + '/Profile/' + d2_membership_id + '/?components=100'
r         = json.loads(requests.get(base_url + profile, headers = headers).content)
characters = r['Response']['profile']['data']['characterIds']

instances = []

for character in characters:
    matches = '/Destiny2/' + mem_type + '/Account/' + d2_membership_id + '/Character/' + character + '/Stats/Activities/?mode=5&count=250'
    # print(requests.get(base_url + matches, headers = headers).content)
    r       = json.loads(requests.get(base_url + matches, headers = headers).content)
    if 'activities' in r['Response']:
        with open('matches.csv', 'a') as csvfile:
            output = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            for match in r['Response']['activities']:
                date     = match['period']
                mode     = modes_dict[match['activityDetails']['mode']]
                map_name = maps_dict[match['activityDetails']['referenceId']]
                instance = match['activityDetails']['instanceId']
                kills    = match['values']['kills']['basic']['value']
                deaths   = match['values']['deaths']['basic']['value']
                win      = (match['values']['standing']['basic']['displayValue'] == "Victory")

                instances.append(instance)

                output.writerow((date, instance, mode, map_name, kills, deaths, win))

with open('teammates.csv', 'a') as csvfile:
    output = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)

    for instance in instances:
        activity_url = '/Destiny2/Stats/PostGameCarnageReport/' + instance
        # print(requests.get(base_url + activity_url, headers = headers).content)
        r = json.loads(requests.get(base_url + activity_url, headers = headers).content)
        team_dict = {}
        choice = ''

        for entry in r['Response']['entries']:
            try:
                team = str(entry['values']['team']['basic']['value'])
            except KeyError:
                continue
            name = entry['player']['destinyUserInfo']['displayName']

            if team not in team_dict:
                team_dict[team] = []
            team_dict[team].append(name)

            if user == name:
                choice = team

        if choice != '':
            for teammate in team_dict[choice]:
                if teammate != user:
                    output.writerow((instance, teammate))
