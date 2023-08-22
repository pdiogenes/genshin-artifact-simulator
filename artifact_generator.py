import random
import json

slots = ['sands', 'feather', 'flower', 'circlet', 'goblet']
max_substats = {'HP':298.75,'ATK':19.45,'DEF':23.15,'HP%':5.83,'ATK%':5.83,'DEF%':7.29,'Elemental Mastery':23.31,'Energy Recharge%':6.48,'CRIT Rate%':3.89,'CRIT DMG%':7.77}

# open data for stats
f = open('mainstat_probs.json')
mainstat_probs = json.load(f)
f = open('substat_probs.json')
substat_probs = json.load(f)

def selectLines():
    n = randomize()
    if(n <= 66):
        return 3
    else:
        return 4

def randomize():
    return random.randint(1, 100)

def generateSubstat(substat):
    n = randomize()
    if n <= 25:
        return round(max_substats[substat]*0.7, 1)
    elif n <= 50:
        return round(max_substats[substat]*0.8, 1)
    elif n <= 75:
        return round(max_substats[substat]*0.9, 1)
    else:
        return round(max_substats[substat], 1)

def selectSubstat():
    n = randomize()
    if n <= 25:
        return 0
    elif n <= 50:
        return 1
    elif n <= 75:
        return 2
    else:
        return 3

# function to generate a random artifact
def generate(setName):
    slot = random.choice(slots)
    lines = selectLines()
    chances = mainstat_probs[slot]
    mainStat = random.choices(chances['stats'], chances['probs'])[0]
    substats = []
    for i in range(0, lines):
        substat = random.choices(substat_probs[slot][mainStat]['substats'], substat_probs[slot][mainStat]['probs'])[0]
        while any(d['key'] == substat for d in substats) :
            substat = random.choices(substat_probs[slot][mainStat]['substats'], substat_probs[slot][mainStat]['probs'])[0]
        subval = generateSubstat(substat)
        substats.append({"key": substat, "value": subval})
    # returns artifact in GOOD format (kinda)
    return {'setKey': setName, 'slotKey': slot, 'rarity': 5, 'mainStatKey': mainStat, 'level': 0, 'substats': substats}

# levels an artifact to 20
def level(artifact):
    artifact['level'] = 20
    levels = 5
    if len(artifact['substats']) == 3:
        substat = random.choices(substat_probs[artifact['slotKey']][artifact['mainStatKey']]['substats'], substat_probs[artifact['slotKey']][artifact['mainStatKey']]['probs'])[0]
        while any(d['key'] == substat for d in artifact['substats']):
            substat = random.choices(substat_probs[artifact['slotKey']][artifact['mainStatKey']]['substats'], substat_probs[artifact['slotKey']][artifact['mainStatKey']]['probs'])[0]
        subval = generateSubstat(substat)
        artifact['substats'].append({"key": substat, "value": subval})
        levels = 4
    for i in range(0, levels):
        subNum = selectSubstat()
        subToLevel = artifact['substats'][subNum]['key']
        print(artifact['substats'], subToLevel, subNum)
        artifact['substats'][subNum]['value'] = round(artifact['substats'][subNum]['value'] + generateSubstat(subToLevel), 1)



artifact = generate("EmblemOfSeveredFate")
level(artifact)
for i in artifact:
    if i != 'substats':
        print(i, artifact[i])
    else:
        for j in artifact['substats']:
            print(j['key'], j['value'])