import json
import random


def dice_roll_generator(n_times):    

    object_list = []
    DC_values = [11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]
    id = 1
    dc_increment = 0
    type = [1,2,3]
    type_picker = 0
    dice_value = [4, 6, 8, 10]
    n_dices = [1,2,3,4]
    n_dices_dist_weights = [
        [0.8, 0.15, 0.04, 0.01]
        ,[0.75, 0.18, 0.06, 0.01]
        ,[0.70, 0.23, 0.06, 0.01]
        ,[0.65, 0.28, 0.06, 0.01]
        ,[0.60, 0.33, 0.06, 0.01]
        ,[0.55, 0.38, 0.06, 0.01]
        ,[0.50, 0.43, 0.06, 0.01]
        ,[0.45, 0.48, 0.06, 0.01]
        ,[0.40, 0.53, 0.06, 0.01]
        ,[0.30, 0.54, 0.13, 0.03]
        ,[0.30, 0.54, 0.13, 0.03],
        [0.30, 0.54, 0.13, 0.03]]
    dice_value_dist_weights = [
        [0.8, 0.15, 0.04, 0.01]
        ,[0.75, 0.18, 0.06, 0.01]
        ,[0.70, 0.23, 0.06, 0.01]
        ,[0.65, 0.28, 0.06, 0.01]
        ,[0.60, 0.33, 0.06, 0.01]
        ,[0.55, 0.38, 0.06, 0.01]
        ,[0.50, 0.43, 0.06, 0.01]
        ,[0.45, 0.48, 0.06, 0.01]
        ,[0.35, 0.55, 0.07, 0.03]
        ,[0.20, 0.6, 0.15, 0.05]
        ,[0.0, 0.70, 0.2, 0.1],
        [0.0, 0.60, 0.3, 0.1]]

    for n in range(1, n_times):
        dc_increment = 0
        for i in range(0, 48):
            new_dr = {
                'id': id,
                'dc': DC_values[dc_increment],
                'effect': {
                    'type': random.choices([1, 2])[0],
                    'condition': '',
                    'side-effect': ''
                },
                'gp': dc_increment,
                'n_dices': random.choices(n_dices, n_dices_dist_weights[dc_increment])[0],
                'dice_value': random.choices(dice_value, dice_value_dist_weights[dc_increment])[0]
            }
            
            if i % 4 == 0 and dc_increment != 11:
                dc_increment += 1
                
            
            
            id += 1
            object_list.append(new_dr)
    return object_list
    


def conditions_roll_generator(n_times, start_id):    

    object_list = []
    DC_values = [11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]
    id = start_id
    dc_increment = 0
    rare_conditions = get_rare_conditions()
    common_conditions = get_common_conditions()
    base_condition_rarity_dist_weights = [1.0, 0.0]
    


    for n in range(1, n_times):

        dc_increment = 0
        base_condition_rarity_dist_weights = [1.0, 0.0]

        for i in range(0, 48):
            r1 = random.choices(common_conditions)[0]
            r2 = random.choices(rare_conditions)[0]    
            
           

            new_dr = {
                'id': id,
                'dc': DC_values[dc_increment],
                'effect': {
                    'type': 3,
                    'condition': random.choices([r1, r2], base_condition_rarity_dist_weights, k=1 )[0],
                    'side-effect': ''
                },
                'gp': dc_increment,
                'n_dices': 0,
                'dice_value': 0
            }
            
            if i % 4 == 0 and dc_increment != 11:
                dc_increment += 1
                base_condition_rarity_dist_weights[0] = base_condition_rarity_dist_weights[0] - 0.02
                base_condition_rarity_dist_weights[1] = base_condition_rarity_dist_weights[1] + 0.02
            
            id += 1
            object_list.append(new_dr)
    return object_list
    

def get_common_conditions():
    common_conditions = [
"Might. It gives a +1 bonus to attack rolls after drinking for 1 hour.",
"Courage. Gives immunity to fear and some advantage on DEX ability checks for 1 hour.",
"Giant Strength. It gives the user +3 strength for 1 minute.",
"Flame Resistance. It gives resistance to fire damage.",
"Cold Resistance. It gives resistance to cold damage for 1 hour.",
"Necro Resistance. Gives resistance to necrotic damage for 1 hour.",
"Lightning Resistance. Gives resistance to lightning damage for 1 hour.",
"Acid Resistance. Gives resistance to acid for 1 hour.",
"Stoneskin. Gives resistance to martial damage for 1 hour.",
"Radiant Resistance. Gives resistance to radiant damage.",
"Necro Resistance. Gives resistance to necrotic damage.",
"Growth. Makes the user double in size, gaining +4 strength but -3 dexterity for 3 hours."
"Intimidation. Gives the user a huge booming voice that terrifies those around. +3 on intimation rolls for 1 hour."
"Arcane. Gives the user more powerful spells. Gain 1d4 on all spells that do spell damage, and gain advantage on Arcana checks for 1 hour.",
"Fleet foot. Makes the user have +10ft speed every turn.",
"Nightmares. Makes the user get lost in a hallucinary dream world of their worst nightmares.",
"Knowledge. Increases the users intelligence by +1 for 1 hour.",
"Eagle Sight. Gives the user strong vision and a advantage on perception and insight rolls for 1 hour.",
"Bowmanship. Makes the user more effective with a bow or ranged weapon. Removes disadvantage limit on ranged weapons for 1 hour.",
"Furnace. Makes the user radiate with a damaging aura (1d6) every turn for 1 minute.",
"Hels Leech. Heals 1d4 portion every turn."
"Petrified. Makes the user become petrified for 1 minute.",
"Exhaustive. Makes the user lose 1 exhaustion point for 1 hour.",
"Spiders Feet. The user can climb almost any surface for 1 hour.",
"Gracefulness. Makes the user have advantage on acrobatics and althetics skills for 1 hour."
]
    return common_conditions

def get_rare_conditions():

    rare_conditions = [

"Flame Breath. Gives the user fire breath for a short time, dealing 1d8 fire damage.",
"Shielding. Gives the user a magical shield of energy, blocking 1d6 damage total of every incoming attack.",
"Comprehension. Lets the user understand all languages for 1 hour.",
"Animal form. Makes the user turn into a random animal. The effect wears off 5 minutes after it has been consumed.",
"Furnace+. Makes the user radiate with a damaging aura (1d10) every turn for 1 minute."
"Invulnerability. Freezes the user in stasis that makes them immune to damage but they cannot move or act for 1 minute.",
"Hels Leech+. Heals for half of all damage the user deals.",
"Paralyzed! Makes the user paralyzed for 1 minute.",
]
    return rare_conditions


healing_poison_rolls = dice_roll_generator(20)
start_id = len(healing_poison_rolls)
condition_rolls = conditions_roll_generator(20, start_id)

diceroll_docs = healing_poison_rolls + condition_rolls



print(len(diceroll_docs))

json_docs = json.dumps(diceroll_docs, indent=4)

with open("dicerolls.json", "w") as outfile:
    outfile.write(json_docs)


