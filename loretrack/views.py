from . import app
from flask import render_template, request
import random

scorpion_status = [False, True, False, True, False]


@app.route('/scorpion', methods=['GET', 'POST'])
def scorpion():
    global scorpion_status
    if request.method == 'POST':
        change = request.form['change']
        change = int(change) - 1
        if change == 99:
            scorpion_status = [False, True, False, True, False]
        elif change == 0:
            scorpion_status[0] = not scorpion_status[0]
            scorpion_status[1] = not scorpion_status[1]
        else:
            scorpion_status[change - 1] = not scorpion_status[change - 1]
            scorpion_status[change] = not scorpion_status[change]
            try:
                scorpion_status[change + 1] = not scorpion_status[change + 1]
            except IndexError:
                pass
    if all(scorpion_status):
        progress = 'win'
    elif all(not element for element in scorpion_status):
        progress = 'lose'
    else:
        progress = 'wip'
    return render_template('scorpion.html', status=scorpion_status, progress=progress)


@app.route('/race')
def gen_race():
    races = [
        {'sources': ['DMG', 'VOLO'], 'race': 'Aasimar', 'weight': 1},
        {'sources': ['SRD', 'PHB'], 'race': 'Dragonborn', 'weight': 18},
        {'sources': ['PBR', 'SRD', 'PHB'], 'race': 'Dwarf', 'weight': 24},
        {'sources': ['PBR', 'SRD', 'PHB'], 'race': 'Elf', 'weight': 24},
        {'sources': ['PBR', 'SRD', 'PHB'], 'race': 'Drow', 'weight': 9},
        {'sources': ['VOLO'], 'race': 'Firbolg', 'weight': 3},
        {'sources': ['PotA', 'EE'], 'race': 'Earth Genasi', 'weight': 2},
        {'sources': ['PotA', 'EE'], 'race': 'Fire Genasi', 'weight': 2},
        {'sources': ['PotA', 'EE'], 'race': 'Water Genasi', 'weight': 2},
        {'sources': ['PotA', 'EE'], 'race': 'Wind Genasi', 'weight': 2},
        {'sources': ['SRD', 'PHB'], 'race': 'Gnome', 'weight': 12},
        {'sources': ['VOLO'], 'race': 'Goblin', 'weight': 1.5},
        {'sources': ['EE', 'VOLO'], 'race': 'Goliath', 'weight': 9},
        {'sources': ['PBR', 'SRD', 'PHB'], 'race': 'Halfling', 'weight': 12},
        {'sources': ['SRD', 'PHB'], 'race': 'Half-Elf', 'weight': 24},
        {'sources': ['SRD', 'PHB'], 'race': 'Half-Orc', 'weight': 18},
        {'sources': ['VOLO'], 'race': 'Hobgoblin', 'weight': 1.5},
        {'sources': ['PBR', 'SRD', 'PHB'], 'race': 'Human', 'weight': 65},
        {'sources': ['VOLO'], 'race': 'Kenku', 'weight': 4},
        {'sources': ['VOLO'], 'race': 'Kobold', 'weight': 1.5},
        {'sources': ['VOLO'], 'race': 'Lizardfolk', 'weight': 3},
        {'sources': ['VOLO'], 'race': 'Orc', 'weight': 1.5},
        {'sources': ['VOLO'], 'race': 'Tabaxi', 'weight': 3},
        {'sources': ['SRD', 'PHB'], 'race': 'Tiefling', 'weight': 6},
        {'sources': ['VOLO'], 'race': 'Triton', 'weight': 4},
        {'sources': ['VOLO'], 'race': 'Yuan-Ti Pureblood', 'weight': 1},
        {'sources': ['EE'], 'race': 'Aarakocra', 'weight': 9},
        {'sources': ['PS:KLD'], 'race': 'Aetherborn', 'weight': 1},
        {'sources': ['DMG'], 'race': 'Anthropomorphic Mice', 'weight': 1.5},
        {'sources': ['PS:AKH'], 'race': 'Aven', 'weight': 1},
        {'sources': ['UA: "Eberron"'], 'race': 'Changeling', 'weight': 0.2},
        {'sources': ['PS:ZEN'], 'race': 'Goblin', 'weight': 1.5},
        {'sources': ['PS:AKH'], 'race': 'Khenra', 'weight': 1},
        {'sources': ['PS:ZEN'], 'race': 'Kor', 'weight': 1},
        {'sources': ['PS:ZEN'], 'race': 'Merfolk', 'weight': 1},
        {'sources': ['UA: "Waterborne Adventures"', 'PS:AKH'], 'race': 'Minotaur', 'weight': 0.3},
        {'sources': ['PS:AKH'], 'race': 'Naga', 'weight': 1},
        {'sources': ['UA: "Gothic Heroes"'], 'race': 'Revenant', 'weight': 0.3},
        {'sources': ['UA: "Eberron"'], 'race': 'Shifter', 'weight': 0.6},
        {'sources': ['PS:KLD'], 'race': 'Vedalken', 'weight': 1.2},
        {'sources': ['UA: "Eberron"'], 'race': 'Warforged', 'weight': 0.1}
    ]
    #https://rpg.stackexchange.com/questions/77247/what-are-the-playable-dd-races-in-5e
    #https://rpgcharacters.wordpress.com/2009/09/23/random-house-of-ill-repute/
    a = ''
    b = ''
    for i in range(30):
        a += weighted_choice(races)['race'] + '<br>'

    for i in races:
        b += i['race'] + ': ' + str(i['weight']/285.0 * 100) + '<br>'
    return a + b


def weighted_choice(choices):
    total = sum(entry['weight'] for entry in choices)
    print total
    random_number = random.uniform(0, total)
    upto = 0
    for entry in choices:
        if upto + entry['weight'] >= random_number:
            #print entry['race'] + ': ' + str(entry['weight']/total * 100)
            return entry
        upto += entry['weight']


@app.errorhandler(404)
def page_not_found(e):
    return "Error."
