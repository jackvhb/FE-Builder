import random as rand
import time
import os
import datetime
import traceback
def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False
def init_battle(char1,char2,dist,fore,*weaponX):
    expGain=0
    cont=False
    active_art=None
    dualwielding_weapon=None
    if char2.alignment==player:
        startHP=char1.hp
        player_unit=char2
    elif char1.alignment==player:
        viable_arts=[]
        art_types={}
        startHP=char2.hp
        player_unit=char1
        for j in player_unit.weapon_arts:
            if dist in j.range:
                if j.weapontype in player_unit.weaponType:
                    for i in player_unit.inventory:
                        if isinstance(i,weapon):
                            if i.weapontype==j.weapontype and i.curUses>=j.cost:
                                if j.weapontype not in art_types:
                                    art_types[j.weapontype]=j.cost
                                elif j.weapontype in art_types:
                                    if j.cost<art_types[j.weapontype]:
                                       art_types[j.weapontype]=j.cost
                                if j not in viable_arts:
                                    viable_arts.append(j)
    else:
        player_unit=None
    if weaponX:
        weapon1=weaponX[0]
        cont=True
    else:
        viable_weapons=[]
        for i in range(0,len(player_unit.inventory)):
            if isinstance(player_unit.inventory[i],weapon):
                if dist in player_unit.inventory[i].rng or\
                (player_unit.inventory[i].weapontype in art_types and\
                 player_unit.inventory[i].curUses>=art_types[player_unit.inventory[i].weapontype]):
                    if player_unit.inventory[i].weapontype in player_unit.weaponType:
                        if player_unit.weaponType[player_unit.inventory[i].weapontype]>=player_unit.inventory[i].weaponlevel:
                            print(f'{i}: {player_unit.inventory[i].name} {player_unit.inventory[i].curUses} dur, {player_unit.inventory[i].dmg} might, {player_unit.inventory[i].hit} accuracy, {player_unit.inventory[i].dmgtype} damage,{player_unit.inventory[i].rng} range, {player_unit.inventory[i].crit} crit')
                            viable_weapons.append(player_unit.inventory[i])
    while cont==False:
        selection=input('Choose a weapon to use \n')
        if selection.isdigit():
            selection=int(selection)
            if selection>=0 and selection<len(char1.inventory):
                if char1.inventory[selection] in viable_weapons:
                    weapon1=char1.inventory[selection]
                    char1.active_item=weapon1
                    if dualwield in char1.skills:
                        contX=False
                        while contX==False:
                            dual=input('Input Y to dualwield or anything else to skip')
                            if dual.lower()=='y':
                                selection2=input('Choose a weapon to use \n')
                                if selection2.isdigit():
                                    selection2=int(selection2)
                                    if selection2>=0 and selection2<len(char1.inventory) and selection2!=selection:
                                        if char1.inventory[selection2] in viable_weapons:
                                            dualwielding_weapon=char1.inventory[selection2]
                                            contX=True
                                        else:
                                            print('Invalid input')
                                    else:
                                        print('Invalid input')
                                else:
                                    print('Invalid input')
                            else:
                                contX=False
                    cont=True
                else:
                    print('Invalid input, try again')
            else:
                print('Invalid input, try again')
        else:
            print('Invalid input, try again')
    cont=True
    needed=False
    if player_unit!=None:
        possible_arts=[]
        for i in viable_arts:
            if i.weapontype==weapon1.weapontype and i.cost<=weapon1.curUses:
                possible_arts.append(i)
        if len(possible_arts)>0:
            cont=False
    if dist not in weapon1.rng:
        needed=True
    while cont==False:
        ###    #Weapon Arts (name,weapontype,cost,damage,accuracy,crit
        ###,avoid,super_effective,rng,damageType(can be 'Same','Magic','Phys'),
        ###*[effect_stat,effect_change,effect_operator,target]):
        art='n'
        if not needed:
            art=input('Input Y to use a weapon art or anything else to skip\n')
        if art.lower()=='y' or needed:
            for i in range(0,len(possible_arts)):
                print(f'{i} {possible_arts[i].name}, {possible_arts[i].cost} cost, +{possible_arts[i].damage} damage, +{possible_arts[i].accuracy} accuracy, +{possible_arts[i].crit} crit, +{possible_arts[i].avoid} avoid')
            choice=input('Choose the weapon art to use \n')
            if choice.isdigit():
                choice=int(choice)
                if choice>=0 and choice<len(possible_arts):
                    active_art=possible_arts[choice]
                    cont=True
                else:
                    print('Invalid input, try again')
            else:
                print('Invalid input, try again')
        elif art.lower()!='y' and not needed:
            cont=True
    if char2.active_item==None:
        weapon2=empty
    else:
        weapon2=char2.active_item
    if active_art!=None:
        guarentee_double1=active_art.guarenteed_double
    else:
        guarentee_double1=guarenteed_double[weapon1.weapontype]
    guarentee_double2=guarenteed_double[weapon2.weapontype]
    dmgMod1,hitMod1=mod_checker(char1,char2,weapon1,weapon2,dist)
    dmgMod2,hitMod2=mod_checker(char2,char1,weapon2,weapon1,dist)
    # if not nosupport:
    #     if isinstance(char1,player_char):
    #         hitMod+=char1.check_support_bonus()
    #     elif isinstance(char2,player_char):
    #         hitMod-=char2.check_support_bonus()
    # if not notriangle:
    #     if (weapon1.weapontype=='Sword' and weapon2.weapontype=='Lance') or (weapon1.weapontype=='Axe' and weapon2.weapontype=='Sword') or (weapon1.weapontype=='Lance' and weapon2.weapontype=='Axe'):
    #         dmgMod+=-weapon_triangle_damage_bonus
    #         hitMod+=-weapon_triangle_hit_bonus
    #     elif (weapon1.weapontype=='Sword' and weapon2.weapontype=='Axe') or (weapon1.weapontype=='Axe' and weapon2.weapontype=='Lance') or (weapon1.weapontype=='Lance' and weapon2.weapontype=='Sword'):
    #         dmgMod+=weapon_triangle_damage_bonus
    #         hitMod+=weapon_triangle_hit_bonus
    # if (axebreaker in char1.skills and weapon2.weapontype=='Axe') or (swordbreaker in char1.skills and weapon2.weapontype=='Sword') or \
    #     (lancebreaker in char1.skills and weapon2.weapontype=='Lance') or (bowbreaker in char1.skills and weapon2.weapontype=='Bow') or (tomebreaker in char1.skills and weapon2.weapontype=='Tome')\
    #         or (fistbreaker in char1.skills and weapon2.weapontype=='Fist'):
    #             hitMod+=25
    # if (axebreaker in char2.skills and weapon1.weapontype=='Axe') or (swordbreaker in char2.skills and weapon1.weapontype=='Sword') or \
    #     (lancebreaker in char2.skills and weapon1.weapontype=='Lance') or (bowbreaker in char2.skills and weapon1.weapontype=='Bow') or (tomebreaker in char2.skills and weapon1.weapontype=='Tome')\
    #         or (fistbreaker in char2.skills and weapon1.weapontype=='Fist'):
    #             hitMod-=25
    if fore==False:
        if vantage not in char2.skills or char2.curhp>=char2.hp/2 or dist not in weapon2.rng:
            cont=battle(char1,weapon1,char2,dmgMod1,hitMod1,active_art,dist)
            if guarentee_double1 and cont:
                print(f"{char1.name} made a follow up attack")
                cont=battle(char1,weapon1,char2,dmgMod1,hitMod1,active_art,dist)
            if dist in weapon2.rng and cont:
                cont=battle(char2,weapon2,char1,dmgMod2,hitMod2,active_art,dist)
                if guarentee_double2 and cont:
                    print(f"{char2.name} made a follow up attack")
                    cont=battle(char2,weapon2,char1,dmgMod2,hitMod2,active_art,dist)
            elif dist not in weapon2.rng:
                print(f"{char2.name} was unable to counter \n")
        else:
            print(f'{char2.name} got the jump with vantage!')
            cont=battle(char2,weapon2,char1,dmgMod2,hitMod2,active_art,dist)
            if guarentee_double2 and cont:
                print(f"{char2.name} made a follow up attack")
                cont=battle(char2,weapon2,char1,dmgMod2,hitMod2,active_art,dist)
            if dist in weapon1.rng and cont:
                cont=battle(char1,weapon1,char2,dmgMod1,hitMod1,active_art,dist)
                if guarentee_double1 and cont:
                    print(f"{char1.name} made a follow up attack")
                    cont=battle(char1,weapon1,char2,dmgMod1,hitMod1,active_art,dist)
        if cont and (char1.spd-doubling_threshold>=char2.spd and weapon1 in char1.inventory and active_art==None and dualwielding_weapon==None):
            print(f"{char1.name} made a follow up attack")
            cont=battle(char1,weapon1,char2,dmgMod1,hitMod1,None,dist)
            if guarentee_double1 and cont:
                print(f"{char1.name} made another follow up attack")
                battle(char1,weapon1,char2,dmgMod1,hitMod1,None,dist)
        elif dualwielding_weapon!=None:
            print(f"{char1.name} made a follow up attack")
            cont=battle(char1,dualwielding_weapon,char2,dmgMod1,hitMod1,None,dist)
        if cont and char2.spd-doubling_threshold>=char1.spd and weapon2 in char2.inventory:
            print(f"{char2.name} made a follow up attack")
            cont=battle(char2,weapon2,char1,dmgMod2,hitMod2,active_art,dist)
            if guarentee_double2 and cont:
                print(f"{char2.name} made another follow up attack")
                battle(char2,weapon2,char1,dmgMod2,hitMod2,active_art,dist)
        char1.battles+=1
        char2.battles+=1
        #need to update this to account for third alignment
        cont=True
        if char2.alignment==player:
            player_weapon=weapon2
            enemy_unit=char1
        elif char1.alignment==player:
            player_unit=char1
            enemy_unit=char2
            player_weapon=weapon1
        else:
            cont=False
        if cont==True:
            if enemy_unit.status=='Dead':
                player_unit.weaponType[player_weapon.weapontype]+=eval(kill_wep_lev_formula)
                expGain=eval(kill_exp_formula)
            else:
                player_unit.weaponType[player_weapon.weapontype]+=eval(wep_lev_formula)
                expGain=eval(exp_formula)
            if isinstance(player_weapon,dark_magic):
                if player_weapon.charged:
                    player_weapon.charged=False
            if paragon_mode:
                expGain*=2
            if paragon in player_unit.skills:
                expGain*=2
            if player_unit.status!='Dead':
                if (player_unit.level<level_cap and 'Low Cap' not in player_unit.classType.attributes) or \
                    (player_unit.level<level_cap+10 and 'High Cap' in player_unit.classType.attributes) or \
                        (player_unit.level<level_cap-10 and 'Low Cap' in player_unit.classType.attributes):
                    player_unit.exp+=expGain
                    print(f'{player_unit.name} EXP +{expGain}')
                #elif player_unit.level<level_cap
                while player_unit.exp>=needed_exp:
                    player_unit.level_up()
                # if player_unit.exp>=needed_exp:
                #     player_unit.level_up()
        if char1.status!='Dead':
            if galeforce not in char1.skills or char2.status!='Dead':
                char1.moved=True
            else:
                print(f'Due to Galeforce {char1.name} can move again')
        print(f'{char1.name} HP: {char1.curhp}')
        input(f'{char2.name} HP: {char2.curhp} \nEnter to continue\n')
    else:
        forecast(char1,weapon1,char2,weapon2,active_art,dist)
        return weapon1


def battle(char1,weapon1,char2,dmgMod,hitMod,active_art,dist):
    ###    #Weapon Arts (name,weapontype,cost,damage,accuracy,crit,avoid,super_effective,rng,damageType(can be 'Same','Magic','Phys'),*[effect_stat,effect_change,effect_operator,target]):
    statusX=True
    print(f'{char1.name} attacked {char2.name} with a {weapon1.name}')
    time.sleep(1*text_speed)
    critMod=0
    if char2.location in curMap.objectList:
        hitMod-=curMap.objectList[char2.location].avoidBonus
    if char1.alignment==player:
        player_unit=char1
    elif char2.alignment==player:
        player_unit=char2
    else:
        player_unit=None
    damageType=weapon1.dmgtype
    if active_art!=None:
        if player_unit==char1:
            hitMod+=active_art.accuracy
            dmgMod+=active_art.damage
            critMod+=active_art.crit
            if active_art.damageType!='Same':
                damageType=active_art.damageType
            dmgMod+=weapon1.dmg*super_effective_checker(active_art,char2,'Art')
        else:
            hitMod-=active_art.avoid
    hit=hit_function(char1, char2, weapon1, char2.active_item, hitMod, dist)
    avoid=avoid_function(char1, char2, weapon1, char2.active_item, 0, dist)
    crit=crit_function(char1, char2, weapon1, char2.active_item, critMod, dist)
    dodge=dodge_function(char1, char2, weapon1, char2.active_item, 0, dist)
    if not true_hit:
        randohit=rand.randrange(0,100)
    else:
        randohit=(rand.randrange(0,100)+rand.randrange(0,100))/2
    randocrit=rand.randrange(0,100)
    truehit=hit-avoid
    truecrit=crit+critMod-dodge
    crit=False
    dmgMod+=weapon1.dmg*super_effective_checker(weapon1,char2,'Weapon')
    if truehit>100:
        truehit=100
    elif truehit<0:
        truehit=0
    if truecrit>100:
        truecrit=100
    elif truecrit<0:
        truecrit=0
    print(f"Hit chance of {truehit}")
    print(f"Crit chance of {truecrit}")
    if randohit <= truehit:
        pass
    else:
        input(f"{char1.name}'s attack missed\nInput enter to continue\n")
        return(True)
    if randocrit <= truecrit:
        crit=True
    player_dict,enemy_dict,weapon_dict=char1.skill_roll(char2)
    if damageType=='Phys':
        for i in char2.inventory:
            if isinstance(i,armor):
                if i.stat=='def':
                    dmgMod-=i.effect
        if char2.location in curMap.objectList:
            dmgMod-=curMap.objectList[char2.location].defBonus
        damage=phys_damage_function(char1, char2, weapon1, char2.active_item, dmgMod, dist)
    elif damageType=='Magic':
        for i in char2.inventory:
            if isinstance(i,armor):
                if i.stat=='res':
                    dmgMod-=i.effect
        damage=magic_damage_function(char1, char2, weapon1, char2.active_item, dmgMod, dist)
    if damage<0:
        damage=0
    if crit==True:
        damage*=crit_multiplier
        print("Critical hit!")
        time.sleep(1*text_speed)
    if (active_art==None or player_unit==char2) and weapon_durability:
        weapon1.curUses-=1
    elif weapon_durability:
        weapon1.curUses-=active_art.cost
    if weapon1.curUses<=0:
        weapon1.breakX(char1)
    for i in player_dict:
        setattr(char1,i,player_dict[i])
    for j in enemy_dict:
        setattr(char2,j,enemy_dict[j])
    for k in weapon_dict:
        setattr(weapon1,k,weapon_dict[k])
    if char2.curhp-damage>0:
        char2.curhp=char2.curhp-damage
        print(f"{char1.name} attacked {char2.name} and did {damage} damage")
    else:
        char2.die(char1)
        statusX=False
    if isinstance(weapon1,dark_magic):
        if 'vamp' in weapon1.bonus_effect:
            char1.curhp+=damage
            print(f'{char1.name} healed {damage} HP with their Nosferatu ability')
        if 'blind' in weapon1.bonus_effect:
            char2.debuff['blind']=2
            print(f'{char2.name} has had their accuracy temporarily reduced')
        if 'mute' in weapon1.bonus_effect:
            char2.debuff['mute']=2
            print(f'{char2.name} is now temporarily unable to use magic')
        if 'cripple' in weapon1.bonus_effect:
            char2.debuff['cripple']=2
            print(f'{char2.name} has had their stats temporarily reduced')
    if char1.curhp>char1.hp:
        char1.curhp=char1.hp
    input("Input enter to continue\n")
    return(statusX)

def init_heal(char1,char2,dist):
    viable_targets={}
    j=0
    for i in char1.inventory:
        if isinstance(i,staff):
            if i.weaponlevel<=char1.weapon_level['Staff']:
                print(f'{j}: {i.name}, heal {i.might+(char1.mag//2)}')
                viable_targets[j]=i
                j+=1
    cont=False
    while cont==False:
        path=input('Input the number of the staff that you would like to use or X to cancel\n')
        if path.lower()=='x':
            cont=True
        elif path.isdigit():
            path=int(path)
            if path in viable_targets:
                origin_hp=char2.curhp
                char2.curhp=char2.curhp+viable_targets[path].might+(char1.mag//2)
                if char2.curhp>char2.hp:
                    char2.curhp=char2.hp
                print(f'{char2.name} was healed by {char2.curhp-origin_hp} HP')
                cont=True
            else:
                print('Invalid input, try again')
        else:
            print('Invalid input, try again')

def super_effective_checker(item,char2,item_type):
    super_mult=1
    if isinstance(item,dark_magic):
        if item.charged:
            super_mult*=2
    if char2.classType.name in item.super_effective:
        if item_type=='Weapon':
            if item.super_effective[char2.classType.name]> super_mult:
                super_mult*=item.super_effective[char2.classType.name]
        elif item_type=='Art':
            super_mult*=3
    for i in item.super_effective:
        if i in char2.classType.attributes:
            if item_type=='Weapon':
                if item.super_effective[i]>super_mult:
                    super_mult*=item.super_effective[i]
            elif item_type=='Art':
                super_mult*=3
    return super_mult

def mod_checker(char1,char2,weapon1,weapon2,dist):
    dmgMod=0
    hitMod=0
    if not nosupport:
        if isinstance(char1,player_char):
            hitMod+=char1.check_support_bonus()
        elif isinstance(char2,player_char):
            hitMod-=char2.check_support_bonus()
    if not notriangle:
        if (weapon1.weapontype=='Sword' and weapon2.weapontype=='Lance') or (weapon1.weapontype=='Axe' and weapon2.weapontype=='Sword') or (weapon1.weapontype=='Lance' and weapon2.weapontype=='Axe'):
            dmgMod+=-weapon_triangle_damage_bonus
            hitMod+=-weapon_triangle_hit_bonus
        elif (weapon1.weapontype=='Sword' and weapon2.weapontype=='Axe') or (weapon1.weapontype=='Axe' and weapon2.weapontype=='Lance') or (weapon1.weapontype=='Lance' and weapon2.weapontype=='Sword'):
            dmgMod+=weapon_triangle_damage_bonus
            hitMod+=weapon_triangle_hit_bonus
    if (axebreaker in char1.skills and weapon2.weapontype=='Axe') or (swordbreaker in char1.skills and weapon2.weapontype=='Sword') or \
        (lancebreaker in char1.skills and weapon2.weapontype=='Lance') or (bowbreaker in char1.skills and weapon2.weapontype=='Bow') or (tomebreaker in char1.skills and weapon2.weapontype=='Tome')\
            or (fistbreaker in char1.skills and weapon2.weapontype=='Fist'):
                hitMod+=25
    if (axebreaker in char2.skills and weapon1.weapontype=='Axe') or (swordbreaker in char2.skills and weapon1.weapontype=='Sword') or \
        (lancebreaker in char2.skills and weapon1.weapontype=='Lance') or (bowbreaker in char2.skills and weapon1.weapontype=='Bow') or (tomebreaker in char2.skills and weapon1.weapontype=='Tome')\
            or (fistbreaker in char2.skills and weapon1.weapontype=='Fist'):
                hitMod-=25
    if (swordfaire in char1.skills and weapon1.weapontype=='Sword') or (lancefaire in char1.skills and weapon1.weapontype=='Lance') or (axefaire in char1.skills and weapon1.weapontype=='Axe')\
        or (bowfaire in char1.skills and weapon1.weapontype=='Bow') or (tomefaire in char1.skills and weapon1.weapontype=='Tome') or (fistfaire in char1.skills and weapon1.weapontype=='Fist'):
            dmgMod+=5
    return dmgMod,hitMod

def forecast(char1,weapon1,char2,weapon2,active_art,dist,*silent):
    dmgMod1,hitMod1=mod_checker(char1,char2,weapon1,weapon2,dist)
    dmgMod2,hitMod2=mod_checker(char2,char1,weapon2,weapon1,dist)
    double1=1
    double2=1
    if guarenteed_double[weapon1.weapontype] and active_art==None:
        double1=2
    if guarenteed_double[weapon2.weapontype]:
        double2=2
    if char1.spd>=char2.spd+doubling_threshold and active_art==None:
        double1*=2
    if char2.spd>=char1.spd+doubling_threshold:
        double2*=2
    if active_art!=None:
        if active_art.guarenteed_double==True:
            double1=2
    dmgMod1+=weapon1.dmg*super_effective_checker(weapon1,char2,'Weapon')
    #finding player damage to enemy
    if weapon1.dmgtype=='Phys':
        for i in char2.inventory:
            if isinstance(i,armor):
                if i.stat=='def':
                    dmgMod1-=i.effect
        if char2.location in curMap.objectList:
            dmgMod1-=curMap.objectList[char2.location[0]].defBonus
        damage1=phys_damage_function(char1,char2,weapon1,weapon2,dmgMod1,dist)
    elif weapon1.dmgtype=='Magic':
        for i in char2.inventory:
            if isinstance(i,armor):
                if i.stat=='res':
                    dmgMod1=dmgMod1-i.effect
        damage1=magic_damage_function(char1,char2,weapon1,weapon2,dmgMod1,dist)
    hit1=hit_function(char1,char2,weapon1,weapon2,hitMod1,dist)
    crit1=crit_function(char1,char2,weapon1,weapon2,0,dist)
    #Finding enemy damage to player
    dmgMod2+=weapon2.dmg*super_effective_checker(weapon2,char1,'Weapon')
    if dist in weapon2.rng:
        if weapon2.dmgtype=='Phys':
            for i in char1.inventory:
                if isinstance(i,armor):
                    if i.stat=='def':
                        dmgMod2=dmgMod2-i.effect
            if char1.location in curMap.objectList:
                dmgMod2-=curMap.objectList[char1.location[0]].defBonus
            damage2=phys_damage_function(char2,char1,weapon2,weapon1,dmgMod2,dist)
        elif weapon2.dmgtype=='Magic':
            for i in char1.inventory:
                if isinstance(i,armor):
                    if i.stat=='res':
                        dmgMod2-=i.effect
            damage2=magic_damage_function(char2,char1,weapon2,weapon1,dmgMod2,dist)
        hit2=hit_function(char2,char1,weapon2,weapon1,hitMod2,dist)
        crit2=crit_function(char2,char1,weapon2,weapon1,0,dist)
    else:
        damage2=0
        hit2=0
        crit2=0
    if damage1<0:
        damage1=0
    if damage2<0:
        damage2=0
    if hit1>100:
        hit1=100
    elif hit1<0:
        hit1=0
    if hit2>100:
        hit2=100
    elif hit2<0:
        hit2=0
    if crit1<0:
        crit1=0
    if crit2<0:
        crit2=0
    if not silent:
        print(f'{char1.name} NAME {char2.name}\n{char1.curhp} HP {char2.curhp}\n{damage1}x{double1} DMG {damage2}x{double2}\n{hit1} HIT {hit2}\n{crit1} CRIT {crit2}\nENEMY SKILLS: {char2.check_skills()}')
    return damage1*double1,damage2*double2

def menu(self):
    atkRange=[0]
    targetRange=[]
    healTargetRange=[]
    end=False
    while end==False:
        tradeRange=[]
        danceRange=[]
        supportRange=[]
        charTriggerRange=[]
        doors=[]
        healRange=[]
        triggerRange=False
        openable=False
        charge=False
        openableDoor=False
        here=self.location
        for i in self.inventory:
            if isinstance(i,weapon):
                if i.weapontype in self.weaponType:
                    if i.weaponlevel<=self.weaponType[i.weapontype]:
                        if i.weapontype=='Dark Magic':
                            if i.charged!=True:
                                charge=True
                        for j in i.rng:
                            if j not in atkRange:
                                atkRange.append(j)
                    for k in self.weapon_arts:
                        if k.weapontype==i.weapontype and k.cost<=i.curUses:
                            for m in k.range:
                                if m not in atkRange:
                                    atkRange.append(m)
            if isinstance(i,staff):
                if 'Staff' in self.weaponType:
                    if i.weaponlevel<=self.weapontype['Staff']:
                        for j in i.rng:
                            if j not in healRange:
                                healRange.append(j)
        for i in curMap.spaces:
            dist=abs(i[0]-self.location[0])+abs(i[1]-self.location[1])
            if dist==1:
                if i in curMap.objectList:
                    if isinstance(curMap.objectList[i],door):
                        if curMap.objectList[i].opened==False:
                            doors.append([i,curMap.objectList[i]])
            if curMap.spaces[i][0]==True:
                if dist in atkRange:
                    if (curMap.spaces[i][1].alignment==enemy or curMap.spaces[i][1].alignment==bounty_hunter) and [i,curMap.spaces[i][1]] not in targetRange:
                        targetRange.append([i,curMap.spaces[i][1]])
                if dist in healRange:
                    if curMap.spaces[i][1].alignment==self.alignment and [i,curMap.spaces[i][1]] not in healTargetRange:
                        healTargetRange.append([i,curMap.spaces[i][1]])
                if dist==1 and curMap.spaces[i][1].alignment==self.alignment:
                    if [i,curMap.spaces[i][1]] not in tradeRange:
                        tradeRange.append([i,curMap.spaces[i][1]])
                        if curMap.spaces[i][1].moved==True:
                            danceRange.append([i,curMap.spaces[i][1]])
                    if curMap.spaces[i][1].name in self.support_list:
                        if (self.name, curMap.spaces[i][1].name) in self.alignment.support_master:
                            if int(self.support_list[curMap.spaces[i][1].name]/support_level_threshold)>\
                                self.alignment.support_master[self.name, curMap.spaces[i][1].name][0] and\
                                    self.alignment.support_master[self.name, curMap.spaces[i][1].name][0]<\
                                        len(self.alignment.support_master[self.name, curMap.spaces[i][1].name])-1 and\
                                            (self.name, curMap.spaces[i][1].name) not in supportRange:
                                supportRange.append((self.name, curMap.spaces[i][1].name))
                        elif (curMap.spaces[i][1].name,self.name) in self.alignment.support_master:
                            if int(self.support_list[curMap.spaces[i][1].name]/support_level_threshold)>self.alignment.support_master[curMap.spaces[i][1].name,self.name][0] and self.alignment.support_master[curMap.spaces[i][1].name,self.name][0]<len(self.alignment.support_master[curMap.spaces[i][1].name,self.name])-1 and (curMap.spaces[i][1].name,self.name) not in supportRange:
                                supportRange.append((curMap.spaces[i][1].name,self.name))
                    if (self.name, curMap.spaces[i][1].name) in curMap.char_trigger_list:
                        charTriggerRange.append((self.name, curMap.spaces[i][1].name))
                    elif (curMap.spaces[i][1].name,self.name) in curMap.char_trigger_list:
                        charTriggerRange.append((curMap.spaces[i][1].name,self.name))
        if here in curMap.triggerList:
            if curMap.triggerList[here].triggered==False and (self.name in curMap.triggerList[here].character or 'All' in curMap.triggerList[here].character):
                print('E : Event')
                triggerRange=True
        if len(targetRange)>0:
            print("0 : Battle")
        if len(healTargetRange)>0:
            print('H : Heal')
        if len(tradeRange)>0:
            print("T : Trade")
        if len(tradeRange)>0 and self.classType==dancer:
            print("D : Dance")
        if len(supportRange)>0 and not nosupport:
            print("B : Support")
        if len(charTriggerRange)>0:
            print("C : Character Event")
        if 'Convoy' in self.classType.attributes:
            print('A: Convoy')
        if style_switch in self.skills:
            print('Style : Style Switch')
        if charge:
            print('Q : Charge')
        print("1 : Inventory")
        print("2 : Equip")
        print("3 : Consume")
        print("4 : Check Stats")
        print("5 : End Turn")
        print("6 : Exit Menu")
        if here in curMap.objectList:
            if isinstance(curMap.objectList[here],throne) and 'Sieze' in self.classType.attributes:
                print("7 : Sieze Throne")
            elif isinstance(curMap.objectList[here],shop):
                print("S : Shop")
            elif isinstance(curMap.objectList[here],treasure_chest):
                for i in self.inventory:
                    if isinstance(i,key):
                        keyX=i
                        openable==True
                if self.classType==thief or locktouch in self.skills:
                    openable=True
                if curMap.objectList[here].opened==True:
                    openable==False
                if openable==True:
                    print("Z : Open Chest")
        if len(doors)>0:
            for i in self.inventory:
                if isinstance(i,key):
                    keyY=i
                    openableDoor=True
            if self.classType==thief or locktouch in self.skills:
                openableDoor=True
            if openableDoor:
                print('D : Open Door')
        v=input("Press the key of the action you wish to take \n")
        if v.lower()=='b' and len(supportRange)>0 and not nosupport:
            for i in range(0,len(supportRange)):
                print(f"{i} : {supportRange[i]}")
            choiceSupport=input("Press the number of the support you wish to view or x to cancel \n")
            if choiceSupport=='x':
                print('Returning to menu')
            elif choiceSupport.isdigit():
                choiceSupport=int(choiceSupport)
                if choiceSupport>=0 and choiceSupport<len(supportRange):
                    #active_support=self.alignment.support_master[support_range[choiceSupport][0],supportRange[choiceSupport][1]]
                    print(self.alignment.support_master[supportRange[choiceSupport]][self.alignment.support_master[supportRange[choiceSupport]][0]+1])
                    self.alignment.support_master[supportRange[choiceSupport]][0]+=1
                    self.moved=True
                    end=True
        elif v.lower()=='q' and charge:
            j=0
            dm=[]
            for i in self.inventory:
                if isinstance(i,dark_magic):
                    if i.charged==False:
                        print(f'{j} : {i.name}')
                        dm.append(i)
                        j+=1
            path=input('Enter the tome that you would like to charge\n')
            if path.isdigit():
                path=int(path)
                if path<j:
                    print(f'{self.name} charged up, preparing to unleash {dm[path].name}.')
                    dm[path].charged=True
                    self.moved=True
                    end=True
        elif v.lower()=='style switch' and style_switch in self.skills:
            route=input('W: Trickster\nD: Swordmaster\nS: General\nA:Sniper\nInput the class you would like to switch to\n')
            if route.lower()=='w':
                self.reclass(trickster)
            elif route.lower()=='a':
                self.reclass(sniper)
            elif route.lower()=='s':
                self.reclass(general)
            elif route.lower()=='d':
                self.reclass(swordmaster)
        elif v.lower()=='h' and len(healTargetRange)>0:
            contHeal=True
            while contHeal==True:
                htr=len(healTargetRange)
                for j in range(0,htr):
                    print(f"{j} {healTargetRange[j][1].name} at {healTargetRange[j][0]}")
                choiceBattle=input("Input the unit you wish to heal or x to cancel \n")
                if choiceBattle=='x':
                    contBattle=False
                elif choiceBattle.isdigit():
                    choiceBattle=int(choiceBattle)
                    if choiceBattle>=0 and choiceBattle<htr:
                        dis=abs(self.location[0]-healTargetRange[choiceBattle][1].location[0])+abs(self.location[1]-healTargetRange[choiceBattle][1].location[1])
                        confirm=input('Input Y to confirm that you wish to heal or anything else to cancel\n')
                        if confirm.lower()=='y':
                            init_heal(self,healTargetRange[choiceBattle][1],dis)
                            end=True
                            contBattle=False
                        else:
                            print('Healing canceled')
                else:
                    print('Invalid input, try again')
        elif v.lower()=='a' and 'Convoy' in self.classType.attributes:
            route=input('Input 1 to withdraw items or 2 to store items\n')
            if route=='1':
                self.withdraw_items()
            elif route=='2':
                self.store_item()
        elif v.lower()=='e' and triggerRange==True:
            print(curMap.triggerList[here].event)
            curMap.triggerList[here].triggered=True
        elif v.lower()=='z' and openable==True:
            self.add_item(curMap.objectList[here].contents)
            curMap.objectList[here].opened=True
            if self.classType!=thief and locktouch not in self.skills:
                keyX.use(self)
            self.moved=True
            end=True
        elif v.lower()=='d' and openableDoor==True:
            for i in range(0,len(doors)):
                print(f'{i} : {doors[i][0]}')
            doorChoice=input('Input the door you would like to open or X to cancel \n')
            if doorChoice.lower()=='x':
                pass
            elif doorChoice.isdigit():
                doorChoice=int(doorChoice)
                if doorChoice>=0 and doorChoice<len(doors):
                    doors[doorChoice].opened=True
                    if self.classType!=thief and locktouch not in self.skills:
                        keyY.use(self)
                    self.moved=True
                    end=True
            else:
                print('Invalid input, try again')
        elif v.lower()=='c' and len(charTriggerRange)>0:
            contChar=True
            while contChar==True:
                for j in range(0,len(charTriggerRange)):
                    print(f'{j} : {curMap.char_trigger_list[charTriggerRange[j][0],charTriggerRange[j][1]].name}')
                choiceChar=input("Input the event you wish to view or x to cancel \n")
                if choiceChar.lower()=='x':
                    contChar=False
                elif choiceChar.isdigit():
                    choiceChar=int(choiceChar)
                    if choiceChar>=0 and choiceChar<len(charTriggerRange):
                        print(f'{curMap.char_trigger_list[charTriggerRange[choiceChar][0],charTriggerRange[choiceChar][1]].event}')
                        contChar=False
                else:
                    print('Invalid input, try again')
        elif v=='0' and len(targetRange)>0:
            contBattle=True
            while contBattle==True:
                for j in range(0,len(targetRange)):
                    print(f"{j} {targetRange[j][1].name} at {targetRange[j][0]}")
                choiceBattle=input("Input the enemy you wish to fight or x to cancel \n")
                if choiceBattle=='x':
                    contBattle=False
                elif choiceBattle.isdigit():
                    choiceBattle=int(choiceBattle)
                    if choiceBattle>=0 and choiceBattle<len(targetRange):
                        dis=abs(self.location[0]-targetRange[choiceBattle][1].location[0])+abs(self.location[1]-targetRange[choiceBattle][1].location[1])
                        weaponX=init_battle(self,targetRange[choiceBattle][1],dis,True)
                        confirm=input('Input Y to confirm that you wish to battle\n')
                        if confirm.lower()=='y':
                            init_battle(self,targetRange[choiceBattle][1],dis,False,weaponX)
                            end=True
                            contBattle=False
                else:
                    print('Invalid input, try again')
        elif v.lower()=='t' and len(tradeRange)>0:
            for i in range(0,len(tradeRange)):
                print(f'{i} {tradeRange[i][1].name}')
            choiceTrade=input("Input the unit you wish to trade with or x to cancel \n")
            if choiceTrade.lower=='x':
                break
            elif choiceTrade.isdigit():
                choiceTrade=int(choiceTrade)
                if choiceTrade>=0 and choiceTrade<len(tradeRange):
                    self.trade_items(tradeRange[choiceTrade][1])
            else:
                print('Invalid input, try again')
        #dancing
        elif v.lower()=='d' and len(danceRange)>0:
            for i in range(0,len(danceRange)):
                print(f'{i} {danceRange[i][1].name}')
            choiceTrade=input("Input the unit you wish to dance for or x to cancel \n")
            if choiceTrade.lower=='x':
                break
            elif choiceTrade.isdigit():
                choiceTrade=int(choiceTrade)
                if choiceTrade>=0 and choiceTrade<len(danceRange):
                    danceRange[choiceTrade][1].moved=False
                    print(f'{danceRange[choiceTrade][1].name} can move again now')
                    self.moved=True
                    end=True
                    return
            else:
                print('Invalid input, try again')
        elif v.lower()=='s':
            if here in curMap.objectList:
                if isinstance(curMap.objectList[here],shop):
                    self.enter_shop(curMap.objectList[here])
                    self.moved=True
                    end=True
                    return
        elif v=='1':
            self.show_inventory()
        elif v=='2':
            self.equip_weapon()
        elif v=='3':
            self.use_consumable()
            end=True
            return
        elif v=='5':
            self.moved=True
            end=True
            return
        elif v=='6':
            end=True
            return
        elif v=='4':
            self.check_stats()
        elif v=='7':
            if here in curMap.objectList  and 'Sieze' in self.classType.attributes:
                if isinstance(curMap.objectList[here],throne):
                    global levelComplete
                    levelComplete=True
                    end=True
                    return
        else:
            print(traceback.format_exc())
            print("Invalid input, try again")


class character:
    character_list=[]
    stats=['hp','atk','mag','skill','luck','defense','res','spd','movModifier']
    growths={'hpG':'hp','atkG':'atk','magG':'mag','skillG':'skill','luckG':'luck','defG':'defense','resG':'res','spdG':'spd'}
    def __init__(self,name,curhp,hp,hpG,atk,atkG,mag,magG,skill,skillG,luck,luckG,defense,defG,res,resG,spd,spdG,mov,alignment,classtype,weaponType,joinMap,inventory,level):
        self.name=name
        self.curhp=curhp
        self.hp=hp
        self.hpG=hpG
        self.atk=atk
        self.eff_atk=atk
        self.atkG=atkG
        self.mag=mag
        self.eff_mag=mag
        self.magG=magG
        self.skill=skill
        self.eff_skill=skill
        self.skillG=skillG
        self.luck=luck
        self.eff_luck=luck
        self.luckG=luckG
        self.defense=defense
        self.eff_def=defense
        self.defG=defG
        self.res=res
        self.eff_res=res
        self.resG=resG
        self.spd=spd
        self.eff_spd=spd
        self.spdG=spdG
        self.movModifier=mov
        self.level=level
        self.exp=0
        self.kills=0
        self.battles=0
        self.status='Alive'
        self.debuff={}
        self.joinMap=joinMap
        self.bonus={}
        self.stole=False
        self.bounty=0
        if isinstance(alignment,str):
            self.alignment=eval(alignment.lower())
        else:
            self.alignment=alignment
        self.classType=None
        for i in classType.class_list:
            if i.name==classtype or i==classtype:
                self.classType=i
        self.skills=[]
        self.skills_all=[]
        for j in self.classType.skill_list:
            if j<=level:
                self.skills.append(self.classType.skill_list[j])
                self.skills_all.append(self.classType.skill_list[j])
        # if self.classType.skill_list[0]!=placeholder:
        #     self.skills=[self.classType.skill_list[0]]
        #     self.skills_all=[self.classType.skill_list[0]]
        #     if self.level>=10:
        #         self.skills.append(self.classType.skill_list[1])
        #         self.skills_all.append(self.classType.skill_list[1])
        #     if self.level==20:
        #         self.skills.append(self.classType.skill_list[2])
        #         self.skills_all.append(self.classType.skill_list[2])
        # else:
        #     self.skills=[]
        #     self.skills_all=[]
        self.mov=self.classType.moveRange+mov
        self.remainingMove=self.mov
        self.weaponType=weaponType
        for i in self.classType.weaponType:
            if i not in self.weaponType:
                self.weaponType[i]=self.classType.weaponType[i]
        self.weaponTypeFree=self.weaponType
        self.active_item=None
        self.recently_attacked=None
        if len(inventory)>0:
            if isinstance(inventory[0],weapon):
                if inventory[0].weapontype in self.weaponType:
                    if inventory[0].weaponlevel>=self.weaponType[inventory[0].weapontype]:
                        self.active_item=inventory[0]
        self.inventory=inventory
        self.deathMap=None
        self.location=(-1,-1)
        self.moved=False
        self.placed=False
        self.deployed=False
        reinforcement=False
        if reinforcement==False:
            for i in mapLevel.map_list:
                if i.mapNum==joinMap:
                    if alignment==player:
                        i.player_roster.append(self)
                    elif alignment==enemy:
                        i.enemy_roster.append(self)
                    elif alignment==green:
                        i.green_roster.append(self)
                    elif alignment==bounty_hunter:
                        i.bounty_hunter_roster.append(self)
        self.character_list.append(self)
    def add_item(self,item):
        if len(self.inventory)<inventory_max_size:
            self.inventory.append(item)
            if self.active_item==None and type(item)==weapon:
                if item.weapontype in self.weaponType:
                    self.active_item=item
        else:
            print('0 '+ item.name)
            for i in range(0,len(self.inventory)):
                print(f'{i+1}: {self.inventory[i].name}')
            drop=input('Choose an item to send to the convoy with the number key \n')
            if int(drop)==0:
                self.alignment.convoy.append(item)
                return
            else:
                self.alignment.convoy.append(self.drop_item(self.inventory[int(drop)-1]))
                self.inventory.append(item)
                if self.active_item==None and type(item)==weapon:
                    if item.weapontype in self.weaponType:
                        self.active_item=item
    def store_item(self):
        end=False
        while end==False:
            if len(self.inventory)==0:
                end=True
                return
            for i in range(0,len(self.inventory)):
                print(f'{i+1}')
                self.inventory[i].info()
            dropY=input('Choose an item to send to the convoy with the number key, or exit by inputing x \n')
            if dropY.lower()=='x':
                end=True
                return
            elif dropY.isdigit():
                if int(dropY)>=1 and int(dropY)<=len(self.inventory):
                    item=self.drop_item(self.inventory[int(dropY)-1])
                    self.alignment.convoy.append(item)
                    print('Item stored')
            else:
                print('Invalid input, try again')
        return
    def enter_shop(self,shop):
        end=False
        if self.stole==True:
            print('I dont think it would be a very good idea to go in here')
        while end==False:
            buysell=input('Input 0 to buy, 1 to sell, or x to exit \n')
            if buysell=='0':
                self.buy_item(shop)
            elif buysell=='1':
                self.sell_item()
            elif buysell.lower()=='x':
                return
    def sell_item(self):
        end=False
        while end==False:
            if len(self.inventory)==0:
                print(f"{self.name}'s inventory is empty, exiting the shop")
                return
            print(f"{self.alignment.gold} gold")
            for i in range(0,len(self.inventory)):
                print(f"{i}: {self.inventory[i].name} {(self.inventory[i].cost/2)*(self.inventory[i].curUses/self.inventory[i].maxUses)}")
            sell=input('Input the number of the item you would like to sell or x to exit \n')
            if sell.lower()=='x':
                return
            elif sell.isdigit():
                if int(sell)>=0 and int(sell)<len(self.inventory):
                    confirm=input(f"Would you like to sell the {self.inventory[int(sell)].name} for {(self.inventory[int(sell)].cost/2)*(self.inventory[int(sell)].curUses/self.inventory[int(sell)].maxUses)} gold? Input Y to confirm, anything else to cancel \n")
                    if confirm.lower()=='y':
                        print(f"Sold {self.inventory[int(sell)].name} for {(self.inventory[int(sell)].cost/2)*(self.inventory[int(sell)].curUses/self.inventory[int(sell)].maxUses)} gold")
                        item=self.drop_item(self.inventory[int(sell)])
                        self.alignment.gold+=(item.cost/2)*(item.curUses/item.maxUses)
                    else:
                        print('Sale canceled')
            else:
                print('Invalid input, try again')
    def buy_item(self,shop):
        end=False
        while end==False:
            if len(shop.contents)==0:
                print("We're fresh out of items, sorry chum")
                return
            print(f"{self.alignment.gold} gold")
            for i in range(0,len(shop.contents)):
                print(f"{i} : {shop.contents[i][0].name}, {shop.contents[i][0].cost} gold x{shop.contents[i][1]}")
            if self.classType==thief:
                rng=rand.randrange(0,100)
                if rng>=90:
                    print('Ive been pretty bored lately. Maybe I should STEAL some stuff...')
            buy=input('Input the number of the item you would like to buy or x to exit \n')
            if buy.lower()=='x':
                return
            elif buy.lower()=='steal':
                print(f"'I dont feel like paying for any of this garbage' {self.name} thought to themselves\n'But that doesnt mean that I dont want it'")
                print("Im sure I could get away with knicking all this stuff, but I dont know if that would be a good idea...")
                confirm=input('Input Y to steal or anything else to back off\n')
                if confirm.lower()=='y':
                    self.stole=True
                    bounty=0
                    for i in shop.contents:
                        bounty+=shop.contents[i][0].cost
                        self.add_item(shop.contents[i][0])
                    shop.contents=[]
                    print('YOU THIEF! YOULL PAY FOR THAT!')
                    self.bounty=bounty
                    print(f"{self.name} now has a bounty on their head for {bounty} gold")
                    return
            elif buy.isdigit():
                if int(buy)>=0 and int(buy)<len(shop.contents):
                    if shop.contents[int(buy)][0].cost<=self.alignment.gold:
                        confirm=input(f"Would you like to buy the {shop.contents[int(buy)][0].name} for {shop.contents[int(buy)][0].cost} gold? Input Y to confirm, anything else to cancel \n")
                        if confirm.lower()=='y':
                            print(f"{shop.contents[int(buy)][0].name} bought!")
                            if shop.contents[int(buy)] in unique_weapons:
                                p=shop.contents[int(buy)][0]
                            else:
                                z=shop.contents[int(buy)][0].name.replace(' ','_').lower()
                                p=globals()[z](False)
                            self.add_item(p)
                            if limited_shop_items:
                                shop.contents[int(buy)][1]-=1
                            if shop.contents[int(buy)][1]<=0 or (shop.contents[int(buy)] in unique_weapons):
                                shop.contents.pop(int(buy))
                            self.alignment.gold-=p.cost
                    else:
                        print("That item is too expensive for you! Buy something else, will ya?")
            else:
                print('Invalid input, try again')
    def trade_items(self,trade_partner):
        cont=False
        while cont==False:
            if len(self.inventory)==0 and len(trade_partner.inventory)==0:
                cont=True
                return
            self.show_inventory()
            trade_partner.show_inventory()
            route=input(f"Input 0 to trade from {self.name}'s inventory, 1 to trade from {trade_partner.name}'s inventory, or x to exit \n")
            if route.lower()=='x':
                cont=True
                return
            elif route=='0':
                for i in range(0,len(self.inventory)):
                    print(f"{i} {self.inventory[i].name}")
                route2=input("Input the item to trade or x to cancel \n")
                if route2.lower()=='x':
                    break
                elif route2.isdigit():
                    if int(route2)<len(self.inventory):
                        trade_partner.inventory.append(self.drop_item(self.inventory[int(route2)]))
                        while len(trade_partner.inventory)>inventory_max_size:
                            routeFix=input(f"{trade_partner.name} has too many items, input 0 to send one to the convoy or 1 to trade an item to {self.name} \n")
                            if routeFix=='0':
                                for i in range(0,len(trade_partner.inventory)):
                                    print(f"{i} {trade_partner.inventory.name}")
                                routeConvoyFix=input("Input the item to store \n")
                                try:
                                    itemX=trade_partner.drop_item(trade_partner.inventory[int(routeConvoyFix)])
                                    trade_partner.alignment.convoy.append(itemX)
                                except:
                                    print('Invalid input, try again')
                            elif routeFix=='1':
                                for i in range(0,len(trade_partner.inventory)):
                                    print(f"{i} {trade_partner.inventory.name}")
                                routeTradeFix=input("Input the item to trade \n")
                                try:
                                    itemX=trade_partner.drop_item(trade_partner.inventory[int(routeTradeFix)])
                                    self.inventory.append(itemX)
                                except:
                                    print('Invalid input, try again')
                            else:
                                print('Invalid input, try again')
                    else:
                        print('Invalid input, try again')
                else:
                    print('Invalid input, try again')
            elif route=='1':
                # len_partner_inventory=len(trade_partner.inventory)
                # len_inventory=len(inventory)
                for i in range(0,len(trade_partner.inventory)):
                    print(f"{i} {trade_partner.inventory[i].name}")
                route2=input("Input the item to trade or x to cancel \n")
                if route2.lower()=='x':
                    break
                elif route2.isdigit():
                    if int(route2)<len(trade_partner.inventory):
                        self.inventory.append(trade_partner.drop_item(trade_partner.inventory[int(route2)]))
                        while len(self.inventory)>inventory_max_size:
                            routeFix=input(f"{self.name} has too many items, input 0 to send one to the convoy or 1 to trade an item to {trade_partner.name} \n")
                            if routeFix=='0':
                                for i in range(0,len(self.inventory)):
                                    print(f"{i} {self.inventory.name}")
                                routeConvoyFix=input("Input the item to store \n")
                                if routeConvoyFix.isdigit():
                                    if int(routeConvoyFix)>=0 and int(routeConvoyFix)<len(self.inventory):
                                        itemX=self.drop_item(self.inventory[int(routeConvoyFix)])
                                        self.alignment.convoy.append(itemX)
                                else:
                                    print('Invalid input, try again')
                            elif routeFix=='1':
                                for i in range(0,len(self.inventory)):
                                    print(f"{i} {self.inventory.name}")
                                routeTradeFix=input("Input the item to trade \n")
                                if routeTradeFix.isdigit():
                                    if int(routeTradeFix)>=0 and int(routeTradeFix)<len(self.inventory):
                                        itemX=self.drop_item(self.inventory[int(routeTradeFix)])
                                        trade_partner.inventory.append(itemX)
                                else:
                                    print('Invalid input, try again')
                            else:
                                print('Invalid input, try again')
            else:
                print(route)
                print('Invalid input, please try again')
    def withdraw_items(self):
        end=False
        if len(self.alignment.convoy)==0:
            print('The convoy is empty')
            end=True
        while end==False:
            if len(self.alignment.convoy)==0:
                end=True
                return
            if len(self.inventory)<inventory_max_size:
                for i in range(0,len(self.alignment.convoy)):
                    print(f'{i} {self.alignment.convoy[i].name}')
                item=input('Enter the number of the item you want to add or input x to exit \n')
                if item.lower()=='x':
                    end=True
                    return
                elif item.isdigit():
                    if int(item)>=0 and int(item)<len(self.alignment.convoy):
                        self.alignment.convoy[int(item)].info()
                        confirm=input(f"Input Y to confirm that you want to add this item to {self.name}'s inventory \n")
                        if confirm.lower()=='y':
                            addition=self.alignment.convoy.pop(int(item))
                            self.inventory.append(addition)
                            print(f"{addition.name} added to {self.name}'s inventory")
                        else:
                            print('Addition canceled')
                else:
                    print('Invalid input, try again')
            else:
                print(f"{self.name}'s inventory is full, returning to menu")
                end=True
                return
    def drop_item(self,item):
        self.inventory.remove(item)
        if self.active_item==item:
            self.active_item=None
            print(f'{self.name} has no active item equipped')
        return item
    def add_skill(self,skill):
        if skill not in self.skills_all:
            self.skills_all.append(skill)
        if skill not in self.skills:
            if len(self.skills)<skill_max_size:
                self.skills.append(skill)
            else:
                cont=False
                while cont==False:
                    print(f'0: {skill.name}')
                    for i in range(0,len(self.skills)):
                        print(f'{i+1}: {self.skills[i].name}')
                    drop=input('Choose a skill to unequip with the number key \n')
                    if drop==0:
                        return
                    elif drop.isdigit():
                        if int(drop)>=1 and int(drop)<len(self.skills)+1:
                            self.skills.pop(int(drop)-1)
                            self.skills.append(skill)
                            return
                        else:
                            print('Invalid input, try again')
                    else:
                        print('Invalid input, try again')
    def swap_skills(self):
        end=False
        while end==False:
            for i in range(0,len(self.skills_all)):
                if self.skills_all[i] not in self.skills:
                    print(f"{i} : {self.skills_all[i].name}")
            add=input("Input the number of the skill you want to add or x to cancel")
            if add.lower()=='x':
                return
            elif add.isdigit():
                if int(add)>=0 and int(add)<len(self.skills_all):
                    self.add_skill(self.skills_all[int(add)])
            else:
                print('Invalid input, try again')
    def level_up(self,*silent):
        self.exp-=needed_exp
        self.level+=1
        if (self.level>level_cap and 'High Cap' not in self.classType.attributes):
            self.level=level_cap
            self.exp=0
            return
        elif (self.level>level_cap+10 and 'High Cap' in self.classType.attributes):
            self.level=level_cap+10
            self.exp=0
            return
        elif (self.level>level_cap-10 and 'Low Cap' in self.classType.attributes):
            self.level=level_cap-10
            self.exp=0
            return
        if not silent:
            print('Level up!')
        if self.level in self.classType.skill_list:
            print(f'You have unlocked the skill {self.classType.skill_list[self.level].name}')
            self.add_skill(self.classType.skill_list[self.level])
        # if self.level==10 or self.level==20:
        #     if self.level==10:
        #         skillX=self.classType.skill_list[1]
        #     else:
        #         skillX=self.classType.skill_list[2]
        #     if not silent:
        #         print(f'You have unlocked the skill {skillX.name}')
        #     self.add_skill(skillX)
        if not silent:
            print(f'Current level: {self.level}')
        for i in self.growths:
            if getattr(self,i)>=1 or getattr(self,i)<=-1:
                if getattr(self,self.growths[i])+int(getattr(self,i))>=0:
                    setattr(self,i,getattr(self,self.growths[i])+int(getattr(self,i)))
                    if not silent:
                        print(f'+{int(i)} {self.growths[i]} {getattr(self,i)}')
            if rand.random()<=getattr(self,i) and getattr(self,i)>=0:
                setattr(self,i,getattr(self,self.growths[i])+1)
                if not silent:
                    print(f'+1 {self.growths[i]} {getattr(self,i)}')
            elif getattr(self,i)<0:
                if -rand.random()>=getattr(self,i):
                    if getattr(self,self.growths[i])>1:
                        setattr(self,i,getattr(self,self.growths[i])-1)
                        if not silent:
                            print(f'-1 {self.growths[i]} {getattr(self,i)}')
    def skill_roll(self,enemy):
        changed_stats_player={}
        changed_stats_enemy={}
        changed_stats_weapon={}
        for i in self.skills:
            roll=rand.randrange(0,100)
            stat=getattr(self,i.trigger_stat)
            if roll<=stat*i.trigger_chance:
                print(f'{i.name} has procced!')
                time.sleep(1*text_speed)
                if i.effect_target=='self':
                    cur=getattr(self,i.effect_stat)
                    if i.effect_temp==True:
                        changed_stats_player[i.effect_stat]=cur
                    final_num=round(eval(f'{cur}{i.effect_operator}{i.effect_change}'))
                    setattr(self,i.effect_stat,final_num)
                elif i.effect_target=='enemy':
                    cur=getattr(enemy,i.effect_stat)
                    if i.effect_temp==True:
                        changed_stats_enemy[i.effect_stat]=cur
                    final_num=round(eval(f'{cur}{i.effect_operator}{i.effect_change}'))
                    setattr(enemy,i.effect_stat,final_num)
                elif i.effect_target=='weapon':
                    weap=self.active_item
                    cur=getattr(weap,i.effect_stat)
                    if i.effect_temp==True:
                        changed_stats_weapon[i.effect_stat]=cur
                    final_num=round(eval(f'{cur}{i.effect_operator}{i.effect_change}'))
                    setattr(weap,i.effect_stat,final_num)
        return changed_stats_player,changed_stats_enemy,changed_stats_weapon
    def show_inventory(self):
        print(f"{self.name}'s inventory: ")
        for i in self.inventory:
            i.info()
    def move(self,location):
        if location not in curMap.spaces:
            print("That location is out of bounds")
            dest=input('Type where you want to move the character to in X,Y form \n')
            dest=dest.split(',')
            self.move((int(dest[0]),int(dest[1])))
            return
        if curMap.spaces[location][0]==True and curMap.spaces[location][1]!=self:
            print("Theres already something there, try again")
            dest=input('Type where you want to move the character to in X,Y form \n')
            dest=dest.split(',')
            self.move((int(dest[0]),int(dest[1])))
            return
        if location==self.location:
            print(f"Opening menu for {self.name}")
            time.sleep(.25*text_speed)
            menu(self)
        elif abs(location[0]-self.location[0])+abs(location[1]-self.location[1])<=self.mov:
            self.update_location(location)
            print(f'{self.name} moved')
            time.sleep(.25)
            self.moved=True
            menu(self)
        else:
            print("Invalid input, try again")
            cont=False
            while cont==False:
                dest=input('Type where you want to move the character to in X,Y form \n')
                dest=dest.split(',')
                if len(dest)==2:
                    if dest[0].isdigit() and dest[1].isdigit():
                        self.move((int(dest[0]),int(dest[1])))
                        cont=True
                    else:
                        print('Invalid input, you must input numbers seperated by a comma')
                else:
                    print('Invalid input, you must only input 2 numbers')
    def update_location(self,location):
        if self.location in curMap.spaces:
            if curMap.spaces[self.location][0]==True:
                if curMap.spaces[self.location][1]==self:
                    curMap.spaces[self.location]=[False]
        if location in curMap.spaces:
            self.location=location
            curMap.spaces[location]=[True,self]
        else:
            cont=False
            while cont==False:
                loc=input(f'{self.name} has been wrongly placed, please enter a new location for them to be in x,y form\n')
                loc=loc.split(',')
                if len(loc)==2:
                    if loc[0].isdigit() and loc[1].isdigit():
                        loc[0]=int(loc[0])
                        loc[1]=int(loc[1])
                        self.update_location((loc[0],loc[1]))
                        return
                    else:
                        print('Invalid input, try again')
                else:
                    print('Invalid input, try again')
    def use_consumable(self):
        count=[]
        for i in range(0,len(self.inventory)):
            if isinstance(self.inventory[i],consumable):
                print(i)
                self.inventory[i].info()
                count.append(i)
            elif isinstance(self.inventory[i],promotion_item):
                if self.level>=promotion_level and len(self.classType.promotions) >0 and ('All' in self.inventory[i].classType or self.classType.name in self.inventory[i].classType):
                    print(i)
                    self.inventory[i].info()
                    count.append(i)
        path=input('Choose a item to use with their number, or input X to cancel \n')
        if path.lower()=='x':
            return
        elif path.isdigit():
            path=int(path)
            if path in count:
                if isinstance(self.inventory[path],consumable):
                    self.inventory[path].active=True
                    self.inventory[path].curUses-=1
                    if self.inventory[path].stat=='curhp':
                       if self.curhp+self.inventory[path].effect>self.hp:
                           self.curhp=self.hp
                           if self.inventory[path].curUses<=0:
                               self.inventory[path].breakX(self)
                           return
                    setattr(self,self.inventory[path].stat,getattr(self,self.inventory[path].stat)+self.inventory[path].effect)
                    print(getattr(self,self.inventory[path].stat))
                    if self.inventory[path].curUses<=0:
                       self.inventory[path].breakX(self)
                elif isinstance(self.inventory[path],promotion_item):
                    if self.level>=promotion_level and len(self.classType.promotions) >0 and ('All' in self.inventory[path].classType or self.classType.name in self.inventory[path].classType):
                        self.promote()
            else:
                print('Invalid input')
        else:
            print('Invalid input')
    def consumable_turn(self,consumable):
        if consumable.active==False or consumable.dur<0:
            return
        elif consumable.active==True and consumable.curdur>1:
            consumable.curdur-=1
            return
        elif consumable.active==True and consumable.curdur==1:
            setattr(self,consumable.stat,getattr(self,consumable.stat)-consumable.effect)
            consumable.curdur=consumable.dur
            consumable.active=False
    def equip_weapon(self):
        cont=False
        while cont==False:
            pos=[]
            for i in range(0,len(self.inventory)):
                if isinstance(self.inventory[i],weapon):
                    if self.inventory[i].weapontype in self.weaponType:
                        if self.inventory[i].weaponlevel<=self.weaponType[self.inventory[i].weapontype]:
                            print(i)
                            self.inventory[i].info()
                            pos.append(i)
            path=input('Choose a item to use with their number, or input X to cancel \n')
            if path.lower()=='x':
                return
            elif path.isdigit():
                if int(path) in pos:
                    self.active_item=self.inventory[int(path)]
                    return
                else:
                    print('Invalid input, try again')
            else:
                print('Invalid input, try again')
    def die(self,killer):
        global lordDied
        if permadeath or self.alignment==enemy:
            self.status='Dead'
            self.alignment.roster.remove(self)
            print(f"{killer.name} attacked {self.name} and did over {self.curhp} damage, defeating the foe\n")
            self.curhp=0
            self.deathMap=curMap.mapNum
            curMap.spaces[self.location]=[False]
            killer.kills+=1
            for i in self.inventory:
                if i.droppable==True:
                    print(f"{self.name} dropped {i.name}\n")
                    killer.add_item(i)
            if (self.alignment==player or self.alignment==green) and 'Lord' in self.classType.attributes:
                lordDied=True
        else:
            self.status='KO'
            print(f"{killer.name} attacked {self.name} and did over {self.curhp} damage, causing {self.name} to retreat\n")
            self.curhp=0
            curMap.spaces[self.location]=[False]
            killer.kills+=1
            if 'Lord' in self.classType.attributes:
                lordDied=True
    def check_skills(self):
        for i in self.skills:
            print(f'{i.name}')
    def check_stats(self):
        print('\n')
        print(f"Name: {self.name}")
        for i in self.stats:
            print(f'{i.capitalize()}: {getattr(self,i)}')
        print(f"Move: {self.mov}")
        print(f"Moved: {self.moved}")
        print(f"Class: {self.classType.name}")
        print(f"Level: {self.level} Exp: {self.exp}")
        print("Skills:")
        for i in self.skills:
            print(i.name)
        print("Weapon Levels")
        for i in self.weaponType:
            print(f'{i}: {self.weaponType[i]}')
        print('\n')
    def promote(self):
        cont=False
        while cont==False:
            for i in range(0,len(self.classType.promotions)):
                print(f'{i}: {self.classType.promotions[i]}')
            choice=input('Choose the class to promote to\n')
            if choice.isdigit():
                if int(choice)>=0 and int(choice)<len(self.classType.promotions):
                    for i in classType.class_list:
                        if i.name==self.classType.promotions[int(choice)]:
                            newClass=i
                    self.reclass(newClass)
                    self.level=1
                    self.exp=0
                    return
            else:
                print('Invalid input')
    def reclass(self,newClass):
        allow=False
        if neggrowth:
            allow=True
        mov_change=newClass.moveRange-self.classType.moveRange
        self.mov+=mov_change
        if self.mov<1:
            self.mov=1
        print(f'MOV +{mov_change}')
        for i in self.stats:
            stat_change=getattr(newClass,i)-getattr(self.classType,i)
            setattr(self,i,getattr(self,i)+stat_change)
            print(f'{i} +{stat_change}')
            if i=='hp':
                if self.hp==0:
                    self.hp=1
                if self.curhp>self.hp:
                    self.curhp=self.hp
            else:
                if getattr(self,i)<0:
                    setattr(self,i,0)
        for j in self.growths:
            if getattr(self,j)<0:
                allow=True
            growth_change=getattr(newClass,j)-getattr(self.classType,j)
            setattr(self,j,getattr(self,j)+growth_change)
            print(f'{j} +{growth_change}')
            if getattr(self,j)<0 and allow==False:
                setattr(self,j,0)
        self.add_skill(newClass.skill_list[0])
        print(f'Learned {newClass.skill_list[0].name}')
        for i in newClass.weaponType:
            if i not in self.weaponType:
                self.weaponType[i]=newClass.weaponType[i]
        self.classType=newClass

class enemy_char(character):
    enemy_char_list=[]
    nameClass='enemy_char'
    def __init__(self,name,classX,joinMap,inventory,level,spawn):
        self.name=name
        self.spawn=spawn
        for i in classType.class_list:
            if i.name==classX:
                classtype=i
        super().__init__(name,classtype.hp,classtype.hp,classtype.hpG,classtype.atk,classtype.atkG,classtype.mag,classtype.magG,
                         classtype.skill,classtype.skillG,classtype.luck,classtype.luckG,classtype.defense,classtype.defG,classtype.res,classtype.resG,classtype.spd,classtype.spdG,0,enemy,classX,{},joinMap,inventory,1)
        while self.level<level:
            self.level_up(1)
        if self not in self.enemy_char_list:
            self.enemy_char_list.append(self)
class bounty_char(character):
    bounty_char_list=[]
    nameClass='bounty_hunter'
    def __init__(self,name,classX,joinMap,inventory,level,spawn,target):
        self.name=name
        self.spawn=spawn
        self.target=target
        for i in classType.class_list:
            if i.name==classX:
                classtype=i
        super().__init__(name,classtype.hp,classtype.hp,classtype.hpG,classtype.atk,classtype.atkG,classtype.mag,classtype.magG,
                         classtype.skill,classtype.skillG,classtype.luck,classtype.luckG,classtype.defense,classtype.defG,classtype.res,classtype.resG,classtype.spd,classtype.spdG,0,bounty_hunter,classX,{},joinMap,inventory,1)
        while self.level<level:
            self.level_up(1)
        if self not in self.bounty_char_list:
            self.bounty_char_list.append(self)
class boss(character):
    boss_list=[]
    nameClass='boss'
    def __init__(self,name,curhp,hp,atk,mag,skill,luck,defense,res,spd,mov,classType,weaponType,joinMap,inventory,level,spawn):
        self.name=name
        self.spawn=spawn
        super().__init__(name,curhp,hp,0,atk,0,mag,0,skill,0,luck,0,defense,0,res,0,spd,0,mov,enemy,classType,weaponType,joinMap,inventory,level)
        if self not in self.boss_list:
            self.boss_list.append(self)
class recruitable(character):
    recruitable_list=[]
    nameClass='recruitable'
    def __init__(self,name,curhp,hp,hpG,atk,atkG,mag,magG,skill,skillG,luck,luckG,defense,defG,res,resG,spd,spdG,mov,classType,weaponType,joinMap,inventory,level,spawn,support_list,weapon_arts,ending,recruit_convo):
        self.name=name
        self.support_list=support_list
        self.weapon_arts=weapon_arts
        self.spawn=spawn
        self.ending=ending
        self.recruit_convo=recruit_convo
        super().__init__(name,curhp,hp,hpG,atk,atkG,mag,magG,skill,skillG,luck,luckG,defense,defG,res,resG,spd,spdG,mov,enemy,classType,weaponType,joinMap,inventory,level)
        if self not in self.recruitable_list:
            self.recruitable_list.append(self)
    def check_support_bonus(self):
        support_bonus=0
        for i in range(-support_range,support_range+1):
            for j in range(-support_range,support_range+1):
                if abs(i+j)==support_range:
                    if (self.location[0]+i,self.location[1]+j) in curMap.spaces:
                        if curMap.spaces[self.location[0]+i,self.location[1]+j][0]==True:
                            if curMap.spaces[self.location[0]+i,self.location[1]+j][1].name in self.support_list:
                                support_bonus+=self.support_list[curMap.spaces[self.location[0]+i,self.location[1]+j][1].name]
        return support_bonus
class player_char(character):
    player_char_list=[]
    nameClass='player_char'
    def __init__(self,name,curhp,hp,hpG,atk,atkG,mag,magG,skill,skillG,luck,luckG,defense,defG,res,resG,spd,spdG,mov,classType,weaponType,joinMap,inventory,level,support_list,weaponarts,ending):
        self.name=name
        self.support_list=support_list
        self.weapon_arts=[]
        self.ending=ending
        for i in weapon_art.weapon_art_list:
            for j in weaponarts:
                if i.name==j:
                    self.weapon_arts.append(i)
        super().__init__(name,curhp,hp,hpG,atk,atkG,mag,magG,skill,skillG,luck,luckG,defense,defG,res,resG,spd,spdG,mov,player,classType,weaponType,joinMap,inventory,level)
        if self not in self.player_char_list:
            self.player_char_list.append(self)
    def check_support_bonus(self):
        support_bonus=0
        for i in range(-support_range,support_range+1):
            for j in range(-support_range,support_range+1):
                if abs(i+j)==support_range:
                    if (self.location[0]+i,self.location[1]+j) in curMap.spaces:
                        if curMap.spaces[self.location[0]+i,self.location[1]+j][0]==True:
                            if curMap.spaces[self.location[0]+i,self.location[1]+j][1].name in self.support_list:
                                support_bonus+=self.support_list[curMap.spaces[self.location[0]+i,self.location[1]+j][1].name]
        return support_bonus

class green_passive(character):
    green_passive_list=[]
    nameClass='green_passive'
    def __init__(self,name,classX,joinMap,inventory,level,spawn):
        self.name=name
        self.spawn=spawn
        for i in classType.class_list:
            if i.name==classX:
                classtype=i
        super().__init__(name,classtype.hp,classtype.hp,classtype.hpG,classtype.atk,classtype.atkG,classtype.mag,classtype.magG,
                         classtype.skill,classtype.skillG,classtype.luck,classtype.luckG,classtype.defense,classtype.defG,classtype.res,
                         classtype.resG,classtype.spd,classtype.spdG,0,green,classX,{},joinMap,inventory,1)
        while self.level<level:
            self.level_up(1)
        if self not in self.green_passive_list:
            self.green_passive_list.append(self)

class green_active(character):
    green_active_list=[]
    nameClass='green_active'
    def __init__(self,name,classX,joinMap,inventory,level,spawn):
        self.name=name
        self.spawn=spawn
        for i in classType.class_list:
            if i.name==classX:
                classtype=i
        super().__init__(name,classtype.hp,classtype.hp,classtype.hpG,classtype.atk,classtype.atkG,classtype.mag,classtype.magG,
                         classtype.skill,classtype.skillG,classtype.luck,classtype.luckG,classtype.defense,classtype.defG,classtype.res,
                         classtype.resG,classtype.spd,classtype.spdG,0,green,classX,{},joinMap,inventory,1)
        while self.level<level:
            self.level_up(1)
        if self not in self.green_active_list:
            self.green_active_list.append(self)

class turnwheel_ghost:
    nameClass='turnwheel_ghost'
    def __init__(self,name,curhp,hp,classType,alignment,level,attr):
        self.name=name
        self.curhp=curhp
        self.hp=hp
        self.classType=classType
        self.alignment=alignment
        #self.location=location
        self.level=level
        self.attr={}
        for i in attr:
            self.attr[i[0]]=i[1]

class turnwheel_map:
    def __init__(self,spaces,objectList,player_roster,enemy_roster,bounty_roster,green_roster,roster):
        self.spaces=spaces
        self.objectList=objectList
        self.player_roster=player_roster
        self.enemy_roster=enemy_roster
        self.bounty_roster=bounty_roster
        self.green_roster=green_roster
        self.roster=roster
    def display(self):
        prev=-1
        rows=[]
        cur=[]
        cont=False
        while cont==False:
            for i in self.spaces:
                if i[1]==0:
                    if i[0]==0:
                        cur=[0]
                    cur.append(str(i[0]))
                    prev=i[1]
            cont=True
        rows.append(cur)
        prev=-1
        for i in self.spaces:
            char=None
            if (i[0],i[1]) in self.objectList:
                char=self.objectList[i]
            if(i[1]!=prev):
                if prev!=-1:
                    rows.append(cur)
                cur=[i[1]]
            if char==None:
                char=" "
            if self.spaces[i][0]==True:
                if self.spaces[i][1].alignment==enemy:
                    char="E"
                elif self.spaces[i][1].alignment==bounty_hunter:
                    char='B'
                elif self.spaces[i][1].alignment==player:
                    char="P"
                elif self.spaces[i][1].alignment==green:
                    char='A'
            if i[0]>=10:
                char+=' '
            cur.append(char)
            prev=i[1]
        rows.append(cur)
        for j in rows:
            print(j)


class classType:
    class_list=[]
    def __init__(self,name,moveType,hp,hpG,atk,atkG,mag,magG,skillX,skillG,luck,luckG,defense,defG,res,resG,spd,spdG,moveRange,weaponType,promotions,skill_list,attributes):
        self.name=name
        self.moveType=moveType
        self.hp=hp
        self.hpG=hpG
        self.atk=atk
        self.atkG=atkG
        self.mag=mag
        self.magG=magG
        self.skill=skillX
        self.skillG=skillG
        self.luck=luck
        self.luckG=luckG
        self.defense=defense
        self.defG=defG
        self.res=res
        self.resG=resG
        self.spd=spd
        self.spdG=spdG
        self.moveRange=moveRange
        self.weaponType=weaponType
        self.promotions=promotions
        self.skill_list={}
        self.attributes=attributes
        for i in skill_list:
            for j in skill.skill_list:
                if j.name==skill_list[i] or j==skill_list[i]:
                    self.skill_list[i]=j
                    #self.skill_list.append(j)
        self.class_list.append(self)
    def info(self):
        print(f'Name: {self.name}')
        print(f'Movement Type: {self.moveType}')
        print(f'Weapon Types: {self.weaponType}')
        print('Promotions:')
        for i in self.promotions:
            print(i.name)
        print('Skills:')
        for i in self.skill_list:
            print(self.skill_list[i].name)
        print('\n')

class weapon:
    weapon_list=[]
    stats=['curUses','maxUses','dmg','crit','hit','cost','weaponlevel']
    def __init__(self,name,maxUses,dmg,dmgtype,rng,crit,hit,weapontype,droppable,cost,rank,super_effective):
        self.name=name
        self.curUses=maxUses
        self.maxUses=maxUses
        self.dmg=dmg
        self.dmgtype=dmgtype
        self.rng=rng
        self.crit=crit
        self.hit=hit
        self.weapontype=weapontype
        self.super_effective=super_effective
        self.droppable=droppable
        self.cost=cost
        self.weaponlevel=rank
        self.weapon_list.append(self)
    def info(self):
        print(f"Name: {self.name}")
        print(f"Weapon Type: {self.weapontype}")
        print(f"Current durability: {self.curUses}")
        print(f"Max durability: {self.maxUses}")
        print(f"Weapon level: {self.weaponlevel}")
        print(f"Power: {self.dmg}")
        print(f"Hit: {self.hit}")
        print(f"Crit: {self.crit}")
        print(f"Range: {self.rng}")
        print('\n')
    def breakX(self,char):
        input(self.name + " Broke!")
        char.inventory.remove(self)
        char.active_item=None
empty=weapon('Empty',0,0,'Empty',[0],0,0,'Empty',False,0,0,{})
unique_weapons=[empty]
weapon_types=['Sword','Axe','Lance','Bow','Tome','Fist','Dark Magic','Knife','Staff']
base_misc=[]
class sword(weapon):
    def __init__(self,name,maxUses,dmg,dmgtype,rng,crit,hit,droppable,cost,rank,super_effective):
        super().__init__(name,maxUses,dmg,dmgtype,rng,crit,hit,'Sword',droppable,cost,rank,super_effective)
base_sword=[]
class lance(weapon):
    def __init__(self,name,maxUses,dmg,dmgtype,rng,crit,hit,droppable,cost,rank,super_effective):
        super().__init__(name,maxUses,dmg,dmgtype,rng,crit,hit,'Lance',droppable,cost,rank,super_effective)
base_lance=[]
class axe(weapon):
    def __init__(self,name,maxUses,dmg,dmgtype,rng,crit,hit,droppable,cost,rank,super_effective):
        super().__init__(name,maxUses,dmg,dmgtype,rng,crit,hit,'Axe',droppable,cost,rank,super_effective)
base_axe=[]
class bow(weapon):
    def __init__(self,name,maxUses,dmg,dmgtype,rng,crit,hit,droppable,cost,rank,super_effect):
        super_effective={'Wyvern':2}
        for i in super_effect:
            super_effective[i]=super_effect[i]
        super().__init__(name,maxUses,dmg,dmgtype,rng,crit,hit,'Bow',droppable,cost,rank,super_effective)
base_bow=[]
class fist(weapon):
    def __init__(self,name,maxUses,dmg,crit,hit,droppable,cost,rank,super_effective):
        super().__init__(name,maxUses,dmg,'Phys',[1],crit,hit,'Fist',droppable,cost,rank,super_effective)
base_fist=[]
class tome(weapon):
    def __init__(self,name,maxUses,dmg,rng,crit,hit,droppable,cost,rank,super_effective):
        super().__init__(name,maxUses,dmg,'Magic',rng,crit,hit,'Tome',droppable,cost,rank,super_effective)
base_tome=[]
'''
Dark Magic bonus effects:
vamp: hp steal
pierce: ignore res
charge: take a round of combat/turn to charge up
blind: lower enemy's accuracy
mute: silence enemy
cripple: halve enemys stats
'''
class dark_magic(weapon):
    def __init__(self,name,maxUses,dmg,rng,crit,hit,droppable,cost,rank,super_effective,bonus_effect):
        self.bonus_effect=bonus_effect
        self.charged=False
        super().__init__(name,maxUses,dmg,'Magic',rng,crit,hit,'Dark Magic',droppable,cost,rank,super_effective)
base_dark_magic=[]
class knife(weapon):
    def __init__(self,name,maxUses,dmg,dmgtype,rng,crit,hit,droppable,cost,rank,super_effective):
        super().__init__(name,maxUses,dmg,dmgtype,rng,crit,hit,'Knife',droppable,cost,rank,super_effective)
base_knife=[]
class iron_knife(knife):
    def __init__(self,droppable):
        super().__init__('Iron Knife',30,1,'Phys',[1,2],25,100,droppable,500,0,{})
base_iron_knife=iron_knife(False)
base_knife.append(base_iron_knife)
class nosferatu(dark_magic):
    def __init__(self,droppable):
        super().__init__('Nosferatu',25,5,[1,2],0,100,droppable,1000,10,{},'vamp')
base_nosferatu=nosferatu(False)
base_dark_magic.append(base_nosferatu)
class iron_sword(sword):
    def __init__(self,droppable):
        super().__init__('Iron Sword',30,4,'Phys',[1],10,85,droppable,500,0,{})
base_iron_sword=iron_sword(False)
base_sword.append(base_iron_sword)
class silver_sword(sword):
    def __init__(self,droppable):
        super().__init__('Silver Sword',20,10,'Phys',[1],25,105,droppable,1500,25,{})
base_silver_sword=silver_sword(False)
base_sword.append(base_silver_sword)
class levin_sword(sword):
    def __init__(self,droppable):
        super().__init__('Levin Sword',25,10,'Magic',[1,2],0,100,droppable,750,0,{})
base_levin_sword=levin_sword(False)
base_sword.append(base_levin_sword)
class iron_lance(lance):
    def __init__(self,droppable):
        super().__init__('Iron Lance',30,6,'Phys',[1],0,70,droppable,500,0,{})
base_iron_lance=iron_lance(False)
base_lance.append(base_iron_lance)
class javelin(lance):
    def __init__(self,droppable):
        super().__init__('Javelin',30,5,'Phys',[1,2],0,65,droppable,750,10,{})
base_javelin=javelin(False)
base_lance.append(base_javelin)
class silver_lance(lance):
    def __init__(self,droppable):
        super().__init__('Silver Lance',20,14,'Phys',[1],0,90,droppable,1500,25,{})
base_silver_lance=silver_lance(False)
base_lance.append(base_silver_lance)
class iron_axe(axe):
    def __init__(self,droppable):
        super().__init__('Iron Axe',30,8,'Phys',[1],0,60,droppable,400,0,{})
base_iron_axe=iron_axe(False)
base_axe.append(base_iron_axe)
class silver_axe(axe):
    def __init__(self,droppable):
        super().__init__('Silver Axe',20,16,'Phys',[1],0,80,droppable,1500,25,{})
base_silver_axe=silver_axe(False)
base_axe.append(base_silver_axe)
class hand_axe(axe):
    def __init__(self,droppable):
        super().__init__('Hand Axe',25,6,'Phys',[1,2],0,55,droppable,750,10,{})
base_hand_axe=hand_axe(False)
base_axe.append(base_hand_axe)
class iron_bow(bow):
    def __init__(self,droppable):
        super().__init__('Iron Bow',40,4,'Phys',[2],0,100,droppable,250,0,{})
base_iron_bow=iron_bow(False)
base_bow.append(base_iron_bow)
class silver_bow(bow):
    def __init__(self,droppable):
        super().__init__('Silver Bow',20,12,'Phys',[2],0,110,droppable,1000,25,{})
base_silver_bow=silver_bow(False)
base_bow.append(base_silver_bow)
class fire(tome):
    def __init__(self,droppable):
        super().__init__('Fire',30,5,[1,2],0,90,droppable,600,0,{"Laguz":2})
base_fire=fire(False)
base_tome.append(base_fire)
class forsetti(tome):
    def __init__(self,droppable):
        super().__init__('Forsetti',25,25,[1,2],25,100,droppable,10000,50,{"Wyvern":2})
base_forsetti=forsetti(False)
base_tome.append(base_forsetti)
class gauntlet(fist):
    def __init__(self,droppable):
        super().__init__('Gauntlet',100,2,20,100,droppable,250,0,{})
base_gauntlet=gauntlet(False)
base_fist.append(base_gauntlet)
base_weapon_dict={'sword':base_sword,'lance':base_lance,'axe':base_axe,'tome':base_tome,'fist':base_fist,'dark_magic':base_dark_magic,'knife':base_knife}

class staff:
    staff_list=[]
    stats=['curUses','maxUses','might','cost','weaponlevel']
    def __init__(self,name,maxUses,might,rng,droppable,cost,rank):
        self.name=name
        self.curUses=maxUses
        self.maxUses=maxUses
        self.might=might
        self.rng=rng
        self.droppable=droppable
        self.cost=cost
        self.weaponlevel=rank
        self.staff_list.append(self)
    def info(self):
        print(f"Name: {self.name}")
        print(f"Current durability: {self.curUses}")
        print(f"Max durability: {self.maxUses}")
        print(f"Weapon level: {self.weaponlevel}")
        print(f"Healing Amount: {self.might}")
        print(f"Range: {self.rng}")
        print('\n')
    def breakX(self,char):
        input(self.name + " Broke!")
        char.inventory.remove(self)
        char.active_item=None
base_staff=[]
class heal(staff):
    def __init__(self,droppable):
        super().__init__('Heal',25,10,[1],droppable,500,0)
base_heal=heal(False)
base_staff.append(base_heal)


class key:
    key_list=[]
    def __init__(self,droppable):
        self.name='Key'
        self.curUses=5
        self.maxUses=5
        self.droppable=droppable
    def info(self):
        print(f"Name: {self.name}")
        print(f"Current durability: {self.curUses}")
        print(f"Max durability: {self.maxUses}\n")
    def use(self,char):
        self.curUses-=1
        if self.curUses<=0:
            self.breakX(char)
    def breakX(self,char):
        print(f"{self.name} Broke!")
        char.inventory.remove(self)
base_key=key(False)
base_misc.append(base_key)

class consumable:
    consumable_list=[]
    def __init__(self,name,maxUses,itemType,effect,stat,droppable,cost,*dur):
        self.name=name
        self.curUses=maxUses
        self.maxUses=maxUses
        self.itemType=itemType
        self.effect=effect
        self.stat=stat
        self.droppable=droppable
        self.cost=cost
        self.active=False
        if dur:
            self.dur=dur
            self.curdur=dur
        else:
            self.dur=-1
            self.curdur=-1
        self.consumable_list.append(self)
    def info(self):
        print(f"Name: {self.name}")
        print(f"Current durability: {self.curUses}")
        print(f"Max durability: {self.maxUses}")
        print(f"Item type: {self.itemType}")
        print(f"Amount of change: {self.effect}")
        print(f"Stat to change: {self.stat}")
        print('\n')
    def breakX(self,char):
        print(f"{self.name} Broke!")
        char.inventory.remove(self)
class vulnary(consumable):
    def __init__(self,droppable):
        super().__init__('Vulnary',3,'Healing',10,'curhp',droppable,100)
base_vulnary=vulnary(False)
base_misc.append(base_vulnary)
class mystic_water(consumable):
    def __init__(self,droppable):
        super().__init__('Mystic Water',5,'Buff',7,'res',5,droppable,250)
base_mystic_water=mystic_water(False)
base_misc.append(base_mystic_water)

class promotion_item:
    promotion_item_list=[]
    def __init__(self,name,classType,droppable,cost):
        self.name=name
        self.classType=classType
        self.droppable=droppable
        self.curUses=1
        self.maxUses=1
        self.cost=cost
        self.promotion_item_list.append(self)
    def info(self):
        print(f'Name: {self.name}')
        print('Classes this item promotes: /n')
        for i in self.classType:
            print(i.name)
        print('\n')
class master_seal(promotion_item):
    def __init__(self,droppable):
        super().__init__('Master Seal',['All'],droppable,10000)
base_master_seal=master_seal(False)
base_misc.append(base_master_seal)

class armor:
    armor_list=[]
    def __init__(self,name,effect,stat,droppable,cost):
        self.name=name
        self.effect=effect
        self.stat=stat
        self.droppable=droppable
        self.cost=cost
        self.armor_list.append(self)
        self.curUses=1
        self.maxUses=1
    def info(self):
        print(f"Name: {self.name}")
        print(f"Stat bonus of {self.effect} in {self.stat}")
        print('\n')
base_armor=[]
class shield(armor):
    def __init__(self,droppable):
        super().__init__('Shield',3,'def',droppable,1000)
base_shield=shield(False)
base_armor.append(base_shield)

class skill:
    skill_list=[]
    def __init__(self,name,trigger_chance,trigger_stat,effect_stat,effect_change,effect_operator,effect_temp,effect_target,*relative_stat):
        self.name=name
        self.trigger_chance=trigger_chance
        self.trigger_stat=trigger_stat
        self.effect_stat=effect_stat
        self.effect_change=effect_change
        self.effect_operator=effect_operator
        self.effect_target=effect_target
        self.effect_temp=effect_temp
        self.description=None
        self.skill_list.append(self)

    #Weapon Arts (name,weapontype,cost,damage,accuracy,crit,avoid,super_effective,rng,damageType(can be 'Same','Magic','Phys'),*[effect_stat,effect_change,effect_operator,target]):
class weapon_art:
    weapon_art_list=[]
    def __init__(self,name,weapontype,cost,damage,accuracy,crit,avoid,super_effective,rng,damageType,guarenteed_double,*bonus):
        self.name=name
        self.weapontype=weapontype
        self.cost=cost
        self.damage=damage
        self.accuracy=accuracy
        self.crit=crit
        self.avoid=avoid
        self.super_effective=super_effective
        self.range=rng
        self.damageType=damageType
        self.guarenteed_double=guarenteed_double
        if bonus:
            self.bonus=bonus
        else:
            self.bonus=None
        self.weapon_art_list.append(self)
    def info(self):
        print(f"Name: {self.name}")
        print(f"Weapon Type: {self.weapontype}")
        print(f"Durability cost: {self.cost}")
        print(f"Damage: {self.damage}")
        print(f"Accuracy: {self.accuracy}")
        print(f"Crit: {self.crit}")
        print(f"Avoid: {self.avoid}")
        print(f'Guarenteed Double: {self.guarenteed_double}')
        print(f"Super Effective: {self.super_effective}")
        print(f"Range: {self.range}")
        print(f"Damage Type: {self.damage_type}\n")

class alignment:
    alignment_list=[]
    def __init__(self,name):
        self.name=name
        self.roster=[]
        self.convoy=[]
        self.gold=starting_gold
        self.alignment_list.append(self)
        self.support_master={}
    def show_convoy(self):
        if len(self.convoy)==0:
            print('The convoy is empty')
            return
        for i in self.convoy:
            i.info()
    def buy_item(self,shop):
        sale=1
        sale_int=rand.randrange(0,100)
        if sale_int<=5:
            sale=rand.randrange(2,5)
        end=False
        while end==False:
            print(f"{self.gold} gold")
            if sale>1:
                print(f'Lucky you! Theres a sale going on, everything is {100/sale}% off!')
            for i in range(0,len(shop.contents)):
                print(f"{i} : {shop.contents[i][0].name}, {shop.contents[i][0].cost//sale} gold{' x'+str(shop.contents[i][1]) if limited_shop_items else ''}")
            buy=input('Input the number of the item you would like to buy or x to exit \n')
            if buy.lower()=='x':
                return
            elif buy.isdigit():
                if int(buy)>=0 and int(buy)<len(shop.contents):
                    if shop.contents[int(buy)][0].cost<=self.gold:
                        confirm=input(f"Would you like to buy the {shop.contents[int(buy)][0].name} for {shop.contents[int(buy)][0].cost//sale} gold? Input Y to confirm, anything else to cancel \n")
                        if confirm.lower()=='y':
                            print(f"{shop.contents[int(buy)][0].name} bought!")
                            if shop.contents[int(buy)][0] in unique_weapons:
                                p=shop.contents[int(buy)][0]
                            else:
                                z=shop.contents[int(buy)][0].name
                                z=z.replace(' ','_')
                                z=z.lower()
                                p=globals()[z](False)
                            self.convoy.append(p)
                            if limited_shop_items:
                                shop.contents[int(buy)][1]-=1
                            if shop.contents[int(buy)][1]<=0 or shop.contents[int(buy)][0] in unique_weapons:
                                shop.contents.pop(int(buy))
                            self.gold-=p.cost//sale
                    else:
                        print("That item is too expensive for you! Buy something else, will ya?")
            else:
                print('Invalid input, try again')
    def sell_item(self):
        end=False
        while end==False:
            if len(self.convoy)==0:
                print('The convoy is empty')
                return
            print(f"{self.gold} gold")
            for i in range(0,len(self.convoy)):
                print(f"{i}: {self.convoy[i].name} {(self.convoy[i].cost*shop_sell_price_multiplier)*(self.convoy[i].curUses/self.convoy[i].maxUses)}")
            sell=input('Input the number of the item you would like to sell or x to exit \n')
            if sell.lower()=='x':
                return
            elif sell.isdigit():
                if int(sell)>=0 and int(sell)<len(self.convoy):
                    confirm=input(f"Would you like to sell the {self.convoy[int(sell)].name} for {(self.convoy[int(sell)].cost*shop_sell_price_multiplier)*(self.convoy[int(sell)].curUses/self.convoy[int(sell)].maxUses)} gold? Input Y to confirm, anything else to cancel \n")
                    if confirm.lower()=='y':
                        print(f"Sold {self.convoy[int(sell)].name} for {(self.convoy[int(sell)].cost*shop_sell_price_multiplier)*(self.convoy[int(sell)].curUses/self.convoy[int(sell)].maxUses)} gold")
                        item=self.convoy.pop(int(sell))
                        self.gold+=(item.cost*shop_sell_price_multiplier)*(item.curUses/item.maxUses)
                        print('Item sold')
                    else:
                        print('Sale canceled')
            else:
                print('Invalid input, please try again')
    def show_roster(self):
        for i in self.roster:
            if i.deployed==True:
                i.check_stats()
    def turn_end(self):
        for i in self.roster:
            if i.location in curMap.objectList:
                if i.curhp+curMap.objectList[i.location].hpBonus<i.hp:
                    i.curhp+=curMap.objectList[i.location].hpBonus
                else:
                    i.curhp=i.hp
            for j in i.inventory:
                if isinstance(j,consumable):
                    i.consumable_turn(j)
            i.moved=False
            i.remainingMove=i.mov
            if self==player:
                for j in curMap.spaces:
                    if curMap.spaces[j][0]==True:
                        if abs(j[0]-i.location[0])+abs(j[1]-i.location[1])<=support_range and curMap.spaces[j][1].alignment==i.alignment and curMap.spaces[j][1].name in i.support_list:
                            i.support_list[curMap.spaces[j][1].name]+=support_growth_multiplier

class mapLevel:
    map_list=[]
    def __init__(self,name,y_size,x_size,mapNum,spawns,player_roster,enemy_roster):
        self.name=name
        self.objectList={}
        self.spaces={}
        self.triggerList={}
        self.char_trigger_list={}
        self.spawns=spawns
        self.mapNum=mapNum
        self.turn_count=1
        self.battle_saves=0
        self.y_size=y_size
        self.x_size=x_size
        for i in range(0,y_size):
            for j in range(0,x_size):
                self.spaces[j,i]=[False]
        self.completion_turns=0
        self.player_roster=[]
        self.enemy_roster=[]
        self.green_roster=[]
        self.bounty_hunter_roster=[]
        self.turnwheel={}
        self.map_list.append(self)
#init green
    def start_map(self):
        global levelComplete
        levelComplete=False
        for i in self.player_roster:
            if i not in player.roster:
                player.roster.append(i)
        enemy.roster=self.enemy_roster
        for i in enemy.roster:
            i.update_location(i.spawn)
        for i in green.roster:
            i.update_location(i.spawn)
        for i in player.roster:
            i.deployed=False
            i.curhp=i.hp
            if not permadeath and i.status=='KO':
                i.status='Alive'
            i.debuff={}
            #bonus
            #self.bonus={}
            #self.bonus.append({'atk':})
            #self.bonus{'atk':[{'len':whaver,'blah':whaetet},{}],'mag':[]}
            #eff_def=enemy.def
            #for i in enemy.bonus[def]:
                #eff_def=eval(f'{eff_def}{operator}{stat_bonus}')
            #if eff_def<0:
                #eff_def=0
            '''
            for i in self.bonus:
                self.bonus[i]=[x for x in self.bonus[i] if x[incrementor]=='map']
                for j in self.bonus[i]:
                    if j[incrementor]=='Map':
                        j[length]-=1
                    else:
                        ppop(j)
                    if j[lenth]<=0:
                        pop(j)
            '''
            #for j in i.bonus
            hgkjhgkhg
        inventory=True
        while inventory==True:
            print('0 Trade Items')
            print('1 Store Items')
            print('2 Withdraw Items')
            print('3 Buy Items')
            print('4 Sell Items')
            print('5 Use Items')
            print('6 Swap Skills')
            if not nosupport:
                print('7 Support')
            if saveallowed:
                print('8 Save')
            print('9 Place Units And Start Map')
            inventory_input=input('Input the number key of the path you want to take or input x to exit \n')
            if inventory_input=='0':
                possibilities=[]
                for j in range(0,len(player.roster)):
                    if player.roster[j].status=='Alive':
                        print(f'{j} {player.roster[j].name}')
                        possibilities.append(j)
                p1=input('Enter the number of the first unit you want to participate in the trade or x to cancel \n')
                p2=input('Enter the number of the second unit you want to participate in the trade or x to cancel \n')
                if p1.lower()=='x' or p2.lower=='x':
                    pass
                elif p1.isdigit() and p2.isdigit():
                    if int(p1) in possibilities and int(p2) in possibilities and int(p1)!=int(p2):
                      player.roster[int(p1)].trade_items(player.roster[int(p2)])
                else:
                    print('Invalid input, returning to menu')
            elif inventory_input=='5':
                possibilities=[]
                for j in range(0,len(player.roster)):
                    if player.roster[j].status=='Alive':
                        print(f'{j} {player.roster[j].name}')
                        possibilities.append(j)
                choice=input("Enter the number of the unit you want to use items or x to cancel \n")
                if choice.lower()=='x':
                    pass
                elif choice.isdigit():
                    if int(choice) in possibilities:
                        player.roster[int(choice)].use_consumable()
                else:
                    print('Invalid input, returning to menu')
            elif inventory_input=='1':
                possibilities=[]
                for j in range(0,len(player.roster)):
                    if player.roster[j].status=='Alive':
                        print(f'{j} {player.roster[j].name}')
                        possibilities.append(j)
                choice=input("Enter the number of the unit you want to store items or x to cancel \n")
                if choice.lower()=='x':
                    pass
                elif choice.isdigit():
                    if int(choice) in possibilities:
                        player.roster[int(choice)].store_item()
                else:
                    print('Invalid input, returning to menu')
            elif inventory_input=='2':
                if len(player.convoy)==0:
                    print('The convoy is empty, returning to menu')
                else:
                    possibilities=[]
                    for j in range(0,len(player.roster)):
                        if player.roster[j].status=='Alive':
                            print(f'{j} {player.roster[j].name}')
                            possibilities.append(j)
                    choice=input("Enter the number of the unit you want to withdraw items or x to cancel \n")
                    if choice.lower()=='x':
                        pass
                    elif choice.isdigit():
                        if int(choice) in possibilities:
                            player.roster[int(choice)].withdraw_items()
                    else:
                        print('Invalid input')
            elif inventory_input=='3':
                #Buy items
                print('0 Convoy')
                possibilities=[]
                for j in range(0,len(player.roster)):
                    if player.roster[j].status=='Alive':
                        print(f'{j+1} {player.roster[j].name}')
                        possibilities.append(j+1)
                choice=input("Enter who you want to buy items or x to cancel \n")
                if choice=='0':
                    player.buy_item(baseShop)
                elif choice.lower()=='x':
                    pass
                elif choice.isdigit():
                    if int(choice) in possibilities:
                        player.roster[int(choice)-1].buy_item(baseShop)
                else:
                    print('Invalid input')
            elif inventory_input=='4':
                #Sell Items
                print('0 Convoy')
                possibilities=[]
                for j in range(0,len(player.roster)):
                    if player.roster[j].status=='Alive':
                        print(f'{j+1} {player.roster[j].name}')
                        possibilities.append(j+1)
                choice=input("Enter who you want to sell items or x to cancel \n")
                if choice=='0':
                    player.sell_item()
                elif choice.lower()=='x':
                    pass
                elif choice.isdigit():
                    if int(choice) in possibilities:
                        player.roster[int(choice)-1].sell_item()
                else:
                    print('Invalid input, returning to menu')
            elif inventory_input=='6':
                #Swap skills
                possibilities=[]
                for j in range(0,len(player.roster)):
                    if player.roster[j].status=='Alive' and len(player.roster[j].skills)!=len(player.roster[j].skills_all):
                        print(f'{j} {player.roster[j].name}')
                        possibilities.append(j)
                if len(possibilities)==0:
                    print('Noone has any skills to swap. Returning to menu')
                else:
                    choice=input("Enter the number of the unit you want to swap skills or x to cancel \n")
                    if choice.lower()=='x':
                        pass
                    elif choice.isdigit():
                        if int(choice) in possibilities:
                            player.roster[int(choice)].swap_skills()
                    else:
                        print('Invalid input, returning to menu')
            elif inventory_input=='7' and not nosupport:
                supportRange=[]
                for unit in player.roster:
                    for support_partner in unit.support_list:
                        if (unit.name, support_partner) in player.support_master:
                            if int(unit.support_list[support_partner]/support_level_threshold)>player.support_master[unit.name, support_partner][0] and player.support_master[unit.name, support_partner][0]<len(player.support_master[unit.name, support_partner])-1 and[unit.name, support_partner] not in supportRange:
                                supportRange.append([unit.name, support_partner])
                        elif (support_partner,unit.name) in player.support_master:
                            if int(unit.support_list[support_partner]/support_level_threshold)>player.support_master[support_partner,unit.name][0] and player.support_master[support_partner,unit.name][0]<len(player.support_master[support_partner,unit.name])-1 and[support_partner,unit.name] not in supportRange:
                                supportRange.append([support_partner,unit.name])
                if len(supportRange)==0:
                    print('There are no supports available at this time')
                else:
                    for i in range(0,len(supportRange)):
                        print(f'{i} {supportRange[i]}')
                    choiceSupport=input('Enter the number of the support you would like to view or x to cancel \n')
                    if choiceSupport.lower()=='x':
                        pass
                    elif choiceSupport.isdigit():
                        if int(choiceSupport)>=0 and int(choiceSupport)<len(supportRange):
                            print(player.support_master[supportRange[int(choiceSupport)][0],
                                                        supportRange[int(choiceSupport)][1]][player.support_master[supportRange[int(choiceSupport)][0],
                                                                                                                   supportRange[int(choiceSupport)][1]][0]+1])
                            player.support_master[supportRange[int(choiceSupport)][0],supportRange[int(choiceSupport)][1]][0]+=1
                    else:
                        print('Invalid input, returning to menu')
            elif inventory_input=='8' and saveallowed:
                save()
            elif inventory_input.lower()=='x' or inventory_input=='9':
                inventory=False
            else:
                print('Invalid input, please try again')
        self.display('cur')
        choice=None
        for i in self.spawns:
            if choice!='x':
                cont=False
            else:
                cont=True
            while cont==False:
                possible=[]
                for j in range(0,len(player.roster)):
                    if player.roster[j].placed==False and player.roster[j].status=='Alive':
                        print(f'{j} {player.roster[j].name}')
                        possible.append(j)
                if len(possible)==0:
                    cont=True
                    break
                choice=input(f"Enter the number of the unit you want at {i} or X to finish placing units\n")
                if choice.lower()=='x':
                    cont=True
                elif choice.isdigit():
                    if int(choice) in possible:
                       player.roster[int(choice)].update_location(i)
                       player.roster[int(choice)].placed=True
                       player.roster[int(choice)].deployed=True
                       cont=True
                    else:
                       print("Invalid input, try again")
                else:
                    print("Invalid input, try again")
        for i in player.roster:
            i.placed=False
            i.moved=False
    def display(self,mode,*dj):
        prev=-1
        rows=[]
        cur=[]
        cont=False
        while cont==False:
            for i in self.spaces:
                if i[1]==0:
                    if i[0]==0:
                        cur=[0]
                    cur.append(str(i[0]))
                    prev=i[1]
            cont=True
        rows.append(cur)
        prev=-1
        for i in self.spaces:
            char=None
            if (i[0],i[1]) in self.objectList:
                char=self.objectList[i].display
            if dj:
                if i in dj[0]:
                    char='#'
            if(i[1]!=prev):
                if prev!=-1:
                    rows.append(cur)
                cur=[i[1]]
            if char==None:
                char=" "
            if self.spaces[i][0]==True:
                if mode.lower()=='cur' or mode.lower()=='djik':
                    if self.spaces[i][1].alignment==enemy:
                        char="E"
                    elif self.spaces[i][1].alignment==bounty_hunter:
                        char='B'
                    elif self.spaces[i][1].alignment==player:
                        char="P"
                    elif self.spaces[i][1].alignment==green:
                        char='A'
            if mode.lower()=='base':
                for j in self.enemy_roster:
                    if [i[0],i[1]]==j.spawn:
                        char='E'
                for k in self.green_roster:
                    if [i[0],i[1]]==k.spawn:
                        char='A'
                if [i[0],i[1]] in self.spawns:
                    char='P'
            if i[0]>=10:
                char+=' '
            cur.append(char)
            prev=i[1]
        rows.append(cur)
        for j in rows:
            print(j)
    def add_map_objects(self):
        cont=False
        while cont==False:
            obj_list=[]
            for i in display_list:
                if isinstance(i,mapObject):
                    print(f'{i.display}: {i.name}')
                    obj_list.append(i)
            self.display('base')
            object_place=input('Input the display character for the map object you wish to place, 1 to view details of an object, or 0 to finish\n')
            if object_place=='0':
                confirm=input('Input Y to confirm that you are done editing this map and quit, anything else to cancel\n')
                if confirm.lower()=='y':
                    return
            elif object_place=='1':
                for i in obj_list:
                    print(f'{i.display}: {i.name}')
                object_info=input('Input the display character for the map object you wish to view details on')
                for i in obj_list:
                    if object_info==i.display:
                        i.info()
            else:
                cont=True
                while cont==True:
                    possibility=None
                    for i in obj_list:
                        if object_place==i.display:
                            possibility=i
                    if possibility==None:
                        print('Invalid input, try again')
                    else:
                        print(f'Input the coordinates where you would like the {possibility.name} to be placed on the map in x,y integer form, with 0,0 being the top left and 1,1 being down and to the right of that')
                        print('Any x,y pair will work as long as its on the map and not currently occupied, not just 0,0 or 1,1')
                        print('Input x to cancel')
                        location=input('Enter the coordinates now\n')
                        if location.lower()!='x':
                            location=location.split(',')
                            if len(location)==2:
                                if location[0].isdigit() and location[1].isdigit:
                                    location[0]=int(location[0])
                                    location[1]=int(location[1])
                                    if (location[0],location[1]) in self.spaces:
                                        moveOn=True
                                        if (location[0],location[1]) in self.objectList:
                                            print(f'There is already a {self.objectList[location[0],location[1]].name} at {location[0]},{location[1]}.')
                                            confirm=input('Input Y to confirm that you want to overwrite this object or anything else to cancel\n')
                                            if confirm.lower()=='y':
                                                pass
                                            else:
                                                moveOn=False
                                        for i in self.spawns:
                                            if location==i and possibility.name=='Void' or possibility.name=='Water' or possibility.name=='Door':
                                                print('There is a spawn at this location, you cant add this object there')
                                                moveOn=False
                                        for i in self.enemy_roster:
                                            if location==i.spawn:
                                                if i.classType.moveType!='Pirate' and i.classType.moveType!='Flying' and possibility.name=='Water':
                                                    print('There is a enemy spawn at this location, you cant add this object there')
                                                    moveOn=False
                                                elif i.classType.moveType!='Flying' and possibility.name=='Void':
                                                    print('There is a enemy spawn at this location, you cant add this object there')
                                                    moveOn=False
                                                elif possibility.name=='Door':
                                                    print('There is a enemy spawn at this location, you cant add this object there')
                                                    moveOn=False
                                        if moveOn==True:
                                            contI=False
                                            if possibility.name=='Chest' or possibility.name=='Shop':
                                                contI=True
                                                inventory=[]
                                            while contI==True:
                                                if possibility.name=='Chest':
                                                    inventory=stock_inventory('chest')
                                                    if inventory==[]:
                                                        cont=False
                                                        contI=False
                                                elif possibility.name=='Shop':
                                                    inventory=edit_shop()
                                            z=possibility.name.replace(' ','_')
                                            z=z.lower()
                                            if possibility.name=='Shop':
                                                globals()[z](self,[location],inventory)
                                            elif possibility.name=='Treasure Chest':
                                                globals()[z](self,[location],inventory[0])
                                            else:
                                                globals()[z](self,[location])
                                        else:
                                            print('Invalid input, try again')
                                    else:
                                        print('That space is out of bounds!')
                            else:
                                print('The location must be entered in x,y form where x and y are integers seperated by a comma')
    def delete_map_objects(self):
        cont=True
        while cont==True:
            self.display('base')
            for i in self.objectList:
                print(f'{i}: {self.objectList[i].name}')
            path=input('Input the x,y coordinates of the object you want to delete or x to finish\n')
            if path.lower()=='x':
                cont=False
            else:
                path=path.split(',')
                if len(path)==2:
                    if path[0].isdigit() and path[1].isdigit():
                        path[0]=int(path[0])
                        path[1]=int(path[1])
                        if (path[0],path[1]) in self.objectList:
                            confirm=input(f'Input Y to confirm that you want to delete the {self.objectList[path[0],path[1]].name} at {path[0]},{path[1]} or anything else to cancel\n')
                            if confirm.lower()=='y':
                                del self.objectList[path[0],path[1]]
                                print('Object deleted')
                            else:
                                print('Deletion canceled, returning to menu')
                        else:
                            print('Theres nothing there!')
                else:
                    print('The x,y form must be 2 integers seperated by a comma')


class tempMap:
    def __init__(self,name,mapLevel):
        self.name=name
        self.mapLevel=mapLevel

class mapObject:
    objectList=[]
    def __init__(self,name,mapLevel,location,defBonus,avoidBonus,hpBonus,moveCost,display):
        self.name=name
        self.mapLevel=mapLevel
        self.location=location
        self.defBonus=defBonus
        self.avoidBonus=avoidBonus
        self.hpBonus=hpBonus
        self.moveCost=moveCost
        self.display=display
        self.objectList.append(self)
        if mapLevel!=None:
            self.mapLevel.objectList[self.location]=self
    def info(self):
        print(f'Name: {self.name}')
        print(f'Defense Bonus: {self.defBonus}')
        print(f'Avoid Bonus: {self.avoidBonus}')
        print(f'Healing: {self.hpBonus} per turn')
        print(f'Move Cost: {self.moveCost}')
display_list=[]
special_objects=[]
###WHEN ADDING NEW OBJECTS
###IF THEY ARE IMPASSIBLE ADD THEM TO THE add_map_objects EXCEPTION LIST
###AND ADD IN BASE FORMS AND APPEND THOSE BASE FORMS TO THE DISPLAY LIST
class fort(mapObject):
    def __init__(self,mapLevel,location):
        super().__init__('Fort',mapLevel,location,1,10,10,1,'F')
base_fort=fort(None,None)
display_list.append(base_fort)
class forest(mapObject):
    def __init__(self,mapLevel,location):
        super().__init__('Forest',mapLevel,location,1,15,0,2,'^')
base_forest=forest(None,None)
display_list.append(base_forest)
class throne(mapObject):
    def __init__(self,mapLevel,location):
        super().__init__('Throne',mapLevel,location,3,5,0,1,'h')
    def info(self):
        super().info()
        print('Sieze this with your Lord to complete a level')
base_throne=throne(None,None)
display_list.append(base_throne)
class void(mapObject):
    def __init__(self,mapLevel,location):
        super().__init__('Void',mapLevel,location,0,0,0,9999,'X')
    def info(self):
        super().info()
        print('Only crossable by flyers')
base_void=void(None,None)
display_list.append(base_void)
class water(mapObject):
    def __init__(self,mapLevel,location):
        super().__init__('Water',mapLevel,location,0,0,0,998,'~')
    def info(self):
        super().info()
        print('Pirates can walk on this and flyers can fly over it')
base_water=water(None,None)
display_list.append(base_water)
class desert(mapObject):
    def __init__(self,mapLevel,location):
        super().__init__('Desert',mapLevel,location,0,0,0,2,'.')
base_desert=desert(None,None)
display_list.append(base_desert)
class treasure_chest(mapObject):
    def __init__(self,mapLevel,location,contents):
        self.contents=contents
        self.opened=False
        super().__init__('Treasure Chest',mapLevel,location,0,0,0,1,'H')
    def info(self):
        super().info()
        print('Can be opened by a key to gain the treasure inside')
    def edit_contents(self):
        print(f'The current item in this chest is {self.contents.name}')
        print('Choose the new item for this chest')
        new_item=stock_inventory('chest')
        if len(new_item)>0:
            self.contents=new_item[0]
            print(f'{self.contents.name} is now in the chest')
        else:
            print('No new item added to chest')
base_treasure_chest=treasure_chest(None,None,None)
display_list.append(base_treasure_chest)
class shop(mapObject):
    def __init__(self,mapLevel,location,contents):
        self.contents=contents
        super().__init__('Shop',mapLevel,location,0,0,0,1,'S')
    def info(self):
        super().info()
        print('Can enter these to buy and sell items with gold')
    def edit_contents(self):
        self.contents=edit_shop(self)
base_shop=shop(None,None,None)
display_list.append(base_shop)
class door(mapObject):
    def __init__(self,mapLevel,location):
        self.opened=False
        super().__init__('Door',mapLevel,location,0,0,0,999,'D')
    def info(self):
        super().info()
        print('Can open these with a key while standing by them to open up a path')
base_door=door(None,None)
display_list.append(base_door)
class arena(mapObject):
    def __init__(self,mapLevel,location,roster):
        self.roster=roster
        super().__init__('Arena',mapLevel,location,0,0,0,1,'C')
    def info(self):
        super().info()
        print('Fight enemies until one of you drops')
base_arena=arena(None,None,None)
display_list.append(base_arena)

class map_fake:
    def __init__(self,name,display):
        self.name=name
        self.display=display
        global display_list
        display_list.append(self)
map_fake('Player','P')
map_fake('Enemy','E')

class trigger:
    triggerList=[]
    def __init__(self,name,mapLevel,location,event,*character):
        self.name=name
        self.mapLevel=mapLevel
        self.location=location
        self.event=event
        self.triggered=False
        if character:
            self.character=character
        else:
            self.character=['All']
        self.triggerList.append(self)
        if mapLevel!=None:
            self.mapLevel.triggerList[location]=self
class char_trigger:
    char_trigger_list=[]
    def __init__(self,name,mapLevel,event,characters,*location):
        self.name=name
        self.mapLevel=mapLevel
        self.event=event
        self.triggered=False
        self.characters=characters
        if location:
            self.location=location
        else:
            self.location=(-1,-1)
        self.char_trigger_list.append(self)
        if mapLevel!=None:
            self.mapLevel.char_trigger_list[characters[0],characters[1]]=self
class event:
    event_list=[]
    def __init__(self,name,mapLevel,event,turn,phase):
        self.name=name
        self.mapLevel=mapLevel
        self.event=event
        self.triggered=False
        self.turn=turn
        self.phase=phase
class reinforcements:
    reinforcements_list=[]
    def __init__(self,characters,alignment):
        self.characters=characters
        self.alignment=alignment
    def spawn_in(self):
        for i in self.characters:
            if curMap[i.spawn][0]==False:
                i.update_location(i.spawn)
                self.alignment.roster.append(i)


def gameplay(align):
    count=0
    if curMap.turn_count%5==0:
        checkpoint=True
    else:
        checkpoint=False
    global levelComplete
    if levelComplete==True:
        return
    for i in range(0,len(align.roster)):
        if align.roster[i].moved==False and align.roster[i].status=='Alive' and align.roster[i].deployed==True:
            count+=1
        elif align.roster[i].moved==True and align.roster[i].status=='Alive' and align.roster[i].deployed==True and checkpoint==True:
            checkpoint=False
    if curMap.mapNum==1 and curMap.turn_count==5 and checkpoint==True:
        print('You can save the game once every 5 turns for free, but only if you havent moved any units. Use this wisely!')
    while checkpoint==True:
        saveQue=input('Would you like to save? Input Y to save or X to pass\n')
        if saveQue.lower()=='y':
            save('_battle')
            checkpoint=False
        elif saveQue.lower()=='x':
            checkpoint=False
        else:
            print('Invalid input, try again')
    if count==0:
        align.turn_end()
        return
    for i in player.roster:
        if i.deployed==True and i.status=='Alive':
            print(f'Player unit {i.name} at {i.location} {i.curhp}/{i.hp} HP')
    for i in enemy.roster:
        if i.status=='Alive':
            print(f'Enemy unit {i.name} level {i.level} {i.classType.name} at {i.location} {i.curhp}/{i.hp} HP')
    for i in bounty_hunter.roster:
        if i.status=='Alive':
            print(f'Bounty hunter {i.name} level {i.level} {i.classType.name} at {i.location} {i.curhp}/{i.hp} HP\nCurrent Targets: {i.targets}')
    for i in green.roster:
        if i.status=='Alive':
            print(f'Allied unit {i.name} level {i.level} {i.classType.name} at {i.location} {i.curhp}/{i.hp} HP')
    cont2=False
    global move_num
    move_num+=1
    ol={}
    s={}
    roster=[]
    player_roster=[]
    enemy_roster=[]
    bounty_roster=[]
    green_roster=[]
    #inventory=[]
    for i in player.roster:
        player_roster.append(i)
    for i in enemy.roster:
        enemy_roster.append(i)
    for i in bounty_hunter.roster:
        bounty_roster.append(i)
    for i in green_roster:
        green_roster.append(i)
    for i in curMap.objectList:
        ol[i]=curMap.objectList[i].display
    for i in curMap.spaces:
        s[i]=curMap.spaces[i]
        if curMap.spaces[i][0]!=False:
            char=turnwheel_ghost(curMap.spaces[i][1].name,curMap.spaces[i][1].curhp,curMap.spaces[i][1].hp,curMap.spaces[i][1].classType,curMap.spaces[i][1].alignment,curMap.spaces[i][1].level,curMap.spaces[i][1].__dict__.items())
            roster.append(char)
    for i in curMap.objectList:
        ol[i]=curMap.objectList[i]
    turn_map=turnwheel_map(curMap.spaces,curMap.objectList,player_roster,enemy_roster,bounty_roster,green_roster,roster)
    #print(enemy.roster)
    if curMap.turn_count not in curMap.turnwheel:
        curMap.turnwheel[curMap.turn_count]={move_num:turn_map}
    else:
        curMap.turnwheel[curMap.turn_count][move_num]=turn_map
    while cont2==False:
        curMap.display('cur')
        print(f'There are {count} units that can still move')
        print('0: View Character Key')
        print("1: Move unit")
        print("2: View an enemies range")
        print("3: Check an enemies stats")
        print("4: View roster")
        print("5: View convoy")
        print("6: View map features")
        print("7: End Turn")
        if curMap.battle_saves<1 and saveallowed:
            print("S: Save (you get 1 battle save per map)")
        if turnwheel:
            print("T: Activate Turnwheel")
        path=input('Enter the number of the path you want to take \n')
        if path=='4':
            align.show_roster()
        elif path.lower()=='t' and turnwheel:
            #turnwheel
            for i in curMap.turnwheel:
                for j in curMap.turnwheel[i]:
                    print(f'{i},{j}')
                    curMap.turnwheel[i][j].display()
            revert=input('Input the turn, move you wish to revert to\n')
            revert=revert.split(',')
            curMap.turnwheel[int(revert[0])][int(revert[1])].display()
            for i in curMap.turnwheel[int(revert[0])][int(revert[1])].roster:
                for j in character.character_list:
                    if j.name==i.name:
                        for at in i.attr:
                            setattr(j,at,i.attr[at])
            #print(enemy.roster)
            #print(curMap.turnwheel[int(revert[0])][int(revert[1])].enemy_roster)
            enemy.roster=curMap.turnwheel[int(revert[0])][int(revert[1])].enemy_roster
            player.roster=curMap.turnwheel[int(revert[0])][int(revert[1])].player_roster
            green.roster=curMap.turnwheel[int(revert[0])][int(revert[1])].green_roster
            bounty_hunter.roster=curMap.turnwheel[int(revert[0])][int(revert[1])].bounty_hunter_roster
            curMap.spaces=curMap.turnwheel[int(revert[0])][int(revert[1])].spaces
            curMap.objectList=curMap.turnwheel[int(revert[0])][int(revert[1])].objectList
            print(hao.status)
            cont2=True
        elif path=='0':
            for i in display_list:
                print(f'{i.name} : {i.display}')
        elif path.lower()=='s' and curMap.battle_saves<1 and saveallowed:
            curMap.battle_saves+=1
            save('_battle')
        elif path=='5':
            align.show_convoy()
        elif path=='6':
            curMap.display('map')
        elif path=='7':
            align.turn_end()
            return
        elif path=='2':
            erl=len(enemy_roster)
            for i in range(0,erl):
                print(f'{i} : {enemy.roster[i].name} {enemy.roster[i].location}')
            for j in range(0,len(bounty_hunter.roster)):
                print(f'{j+erl} : {bounty_hunter.roster[j].name} {bounty_hunter.roster[j].location}')
            enemy_checked=input('Enter the number of the enemy whose range you want to check \n')
            if enemy_checked.isdigit():
                cont=False
                enemy_checked=int(enemy_checked)
                if enemy_checked>=0 and enemy_checked<erl:
                    ec_r=djikstra(enemy.roster[enemy_checked])
                    cont=True
                elif enemy_checked>=erl and enemy_checked+erl<len(bounty_hunter.roster):
                    ec_r=djikstra(bounty_hunter.roster[enemy_checked-erl])
                    cont=True
                if cont:
                    curMap.display('djik',ec_r)
                    listX=[]
                    for i in ec_r:
                        listX.append(i)
                    print(listX)
                else:
                    print('Invalid input')
            else:
                print('Invalid input')
        elif path=='3':
            erl=len(enemy_roster)
            for i in range(0,erl):
                print(f'{i} : {enemy.roster[i].name} {enemy.roster[i].location}')
            for j in range(0,len(bounty_hunter.roster)):
                print(f'{j+erl} : {bounty_hunter.roster[j].name} {bounty_hunter.roster[j].location}')
            enemy_checked=input('Enter the number of the enemy whose stats you want to check \n')
            if enemy_checked.isdigit():
                enemy_checked=int(enemy_checked)
                if enemy_checked>=0 and enemy_checked<erl:
                    enemy.roster[enemy_checked].info()
                elif enemy_checked>=erl and enemy_checked+erl<len(bounty_hunter.roster):
                    bounty_hunter.roster[enemy_checked-erl].info()
                else:
                    print('Invalid input')
            else:
                print('Invalid input')
        elif path=='1':
            possible=[]
            for i in range(0,len(align.roster)):
                if align.roster[i].moved==False and align.roster[i].status=='Alive' and align.roster[i].deployed==True:
                    print(f'{i} {align.roster[i].name} {align.roster[i].location}')
                    possible.append(i)
            cont1=False
            while cont1==False:
                choice=input("Enter the number of the unit you want to move \n")
                if choice.isdigit():
                    if int(choice) in possible:
                        print(f"The current location of {align.roster[int(choice)].name} is {align.roster[int(choice)].location} and they can move {align.roster[int(choice)].remainingMove} spaces")
                        cont1=True
                    else:
                        print('Invalid input')
                else:
                    print('Invalid input')
            dj=djikstra(align.roster[int(choice)])
            curMap.display('djik',dj)
            listY=[]
            for i in dj:
                listY.append(i)
            print(listY)
            cont=False
            while cont==False:
                dest=input('Type where you want to move the character to in X,Y form \n')
                dest=dest.split(',')
                if len(dest)==2:
                    if dest[0].isdigit() and dest[1].isdigit():
                        if (int(dest[0]),int(dest[1])) in dj:
                            align.roster[int(choice)].remainingMove-=dj[int(dest[0]),int(dest[1])]
                            align.roster[int(choice)].move([int(dest[0]),int(dest[1])])
                            cont=True
                            cont2=True
                        else:
                           print('Invalid input, try again')
                else:
                    print('Invalid input, try again')
    if count!=0 and levelComplete==False and lordDied==False:
        gameplay(align)

def ai_green(align):
    #The goal here is to make an ai that, if it can attack a player character, it will attack the one that it does the most hp percentage damage to
    #If it cant, it will move towards the nearest player character
    #we need to only make the active ones agro
    count=0
    global levelComplete
    if levelComplete==True or lordDied==True:
        return
    print('\n')
    for i in range(0,len(align.roster)):
        if align.roster[i].moved==False and align.roster[i].status=='Alive':
            j=i
            count+=1
    if count==0:
        align.turn_end()
        return
    for i in player.roster:
        if i.deployed==True and i.status=='Alive':
            print(f'Player unit {i.name} at {i.location} {i.curhp}/{i.hp} HP')
    for i in enemy.roster:
        if i.status=='Alive':
            print(f'Enemy unit {i.name} level {i.level} {i.classType.name} at {i.location} {i.curhp}/{i.hp} HP')
    for i in bounty_hunter.roster:
        if i.status=='Alive':
            print(f'Bounty hunter {i.name} level {i.level} {i.classType.name} at {i.location} {i.curhp}/{i.hp} HP\nCurrent Targets: {i.targets}')
    for i in green.roster:
        if i.status=='Alive':
            print(f'Allied unit {i.name} level {i.level} {i.classType.name} at {i.location} {i.curhp}/{i.hp} HP')
    #We just choose the last item in the list cuz its easiest this way
    curMap.display('cur')
    self=align.roster[j]
    #dist, weapon
    atkRange=[]
    #So here we want to find the attack range of a character
    for i in self.inventory:
        if isinstance(i,weapon):
            if i.weapontype in self.weaponType:
                if i.weaponlevel<=self.weaponType[i.weapontype]:
                    for j in i.rng:
                        atkRange.append([j,i])
    #closest= dist, location
    closest=[9999,(0,0)]
    furthest=[0,(0,0)]
    #maxDamage has character to attack, damage done, location,weapon being used, and distance
    maxDamage=[None,0,(0,0),None,0]
    #We check every map tile
    potential_spaces=djikstra(self)
    for i in potential_spaces:
        for j in curMap.spaces:
            #We find all the spaces with enemies on them
            if curMap.spaces[j][0]==True:
                destToPlayer=abs(j[0]-i[0])+abs(j[1]-i[1])
                for k in atkRange:
                    if k[0]==destToPlayer:
                        if curMap.spaces[j][1].alignment==enemy:
                            damage=forecast(self,k[1],curMap.spaces[j][1],curMap.spaces[j][1].active_item,None,k[0],True)[0]
                            if damage>=maxDamage[1]:
                                maxDamage=[curMap.spaces[j][1],damage,i,k[1],k[0]]
                        # bonus=0
                        # if k[1].dmgtype=='Magic' and curMap.spaces[j][1].alignment==enemy:
                        #     if curMap.spaces[j][1].classType.name in k[1].super_effective:
                        #         bonus+=k[1].dmg*k[1].super_effective[curMap.spaces[j][1].classType.name]
                        #     if self.mag+k[1].dmg+bonus-curMap.spaces[j][0][1].res>=maxDamage[1]:
                        #         maxDamage=[curMap.spaces[j][1],self.mag+k[1].dmg+bonus-curMap.spaces[j][1].res,i,k[1],k[0]]
                        # elif k[1].dmgtype=='Phys' and curMap.spaces[j][1].alignment==enemy:
                        #     if curMap.spaces[j][1].classType.name in k[1].super_effective:
                        #         bonus+=k[1].dmg*k[1].super_effective[curMap.spaces[j][1].classType.name]
                        #     if self.atk+k[1].dmg+bonus-curMap.spaces[j][1].defense>=maxDamage[1]:
                        #         maxDamage=[curMap.spaces[j][1],self.atk+bonus+k[1].dmg-curMap.spaces[j][1].defense,i,k[1],k[0]]
                #We then calculate the distance from this point to every player, and if its lower than the previous closest to a player we make it the new destination
                if curMap.spaces[j][1].alignment==enemy and destToPlayer<=closest[0]:
                    closest=[destToPlayer,i]
                #We then calculate the distance from this point to every player, and if its further we have it as a potential destination if this unit needs to retreat
                if curMap.spaces[j][1].alignment==enemy and destToPlayer>furthest[0]:
                    furthest=[destToPlayer,i]
    print('\n')
    if maxDamage[0]==None:
        self.update_location(closest[1])
        print(f'{self.name} moved to {closest[1]}')
        self.moved=True
        time.sleep(1.5*text_speed)
    else:
        self.update_location(maxDamage[2])
        print(f'{self.name} moved to {maxDamage[2]}')
        init_battle(self,maxDamage[0],maxDamage[4],maxDamage[3],False)
    if count!=0 and levelComplete==False and lordDied==False:
        ai_green(align)

def ai(align):
    #The goal here is to make an ai that, if it can attack a player character, it will attack the one that it does the most hp percentage damage to
    #If it cant, it will move towards the nearest player character
    count=0
    global levelComplete
    if levelComplete==True or lordDied==True:
        return
    print('\n')
    for i in range(0,len(align.roster)):
        if align.roster[i].moved==False and align.roster[i].status=='Alive':
            j=i
            count+=1
    if count==0:
        align.turn_end()
        return
    for i in player.roster:
        if i.deployed==True and i.status=='Alive':
            print(f'Player unit {i.name} at {i.location} {i.curhp}/{i.hp} HP')
    for i in enemy.roster:
        if i.status=='Alive':
            print(f'Enemy unit {i.name} level {i.level} {i.classType.name} at {i.location} {i.curhp}/{i.hp} HP')
    for i in bounty_hunter.roster:
        if i.status=='Alive':
            print(f'Bounty hunter {i.name} level {i.level} {i.classType.name} at {i.location} {i.curhp}/{i.hp} HP\nCurrent Targets: {i.targets}')
    for i in green.roster:
        if i.status=='Alive':
            print(f'Allied unit {i.name} level {i.level} {i.classType.name} at {i.location} {i.curhp}/{i.hp} HP')
    #We just choose the last item in the list cuz its easiest this way
    curMap.display('cur')
    self=align.roster[j]
    #dist, weapon
    atkRange=[]
    #So here we want to find the attack range of a character
    for i in self.inventory:
        try:
            if i.weaponlevel<=self.weaponType[i.weapontype]:
                for j in i.rng:
                    atkRange.append([j,i])
        except:
            pass
        # if isinstance(i,weapon):
        #     if i.weapontype in self.weaponType:
        #         if i.weaponlevel<=self.weaponType[i.weapontype]:
        #             for j in i.rng:
        #                 atkRange.append([j,i])
    #closest= dist, location
    closest=[9999,(0,0)]
    furthest=[0,(0,0)]
    #maxDamage has character to attack, damage done, location,weapon being used, and distance
    maxDamage=[None,0,(0,0),None,0]
    #We check every map tile
    potential_spaces=djikstra(self)
    for i in potential_spaces:
        for j in curMap.spaces:
            #We find all the spaces with enemies on them
            if curMap.spaces[j][0]==True:
                destToPlayer=abs(j[0]-i[0])+abs(j[1]-i[1])
                for k in atkRange:
                    if k[0]==destToPlayer:
                        if curMap.spaces[j][1].alignment==green or curMap.spaces[j][1].alignment==player:
                            damage=forecast(self,k[1],curMap.spaces[j][1],curMap.spaces[j][1].active_item,None,k[0],True)[0]
                            if damage>=maxDamage[1]:
                                maxDamage=[curMap.spaces[j][1],damage,i,k[1],k[0]]
                        # bonus=0
                        # if k[1].dmgtype=='Magic' and curMap.spaces[j][1].alignment!=enemy:
                        #     if curMap.spaces[j][1].classType.name in k[1].super_effective:
                        #         bonus+=k[1].dmg*k[1].super_effective[curMap.spaces[j][1].classType.name]
                        #     if self.mag+k[1].dmg+bonus-curMap.spaces[j][0][1].res>=maxDamage[1]:
                        #         maxDamage=[curMap.spaces[j][1],self.mag+k[1].dmg+bonus-curMap.spaces[j][1].res,i,k[1],k[0]]
                        # elif k[1].dmgtype=='Phys' and curMap.spaces[j][1].alignment!=enemy:
                        #     if curMap.spaces[j][1].classType.name in k[1].super_effective:
                        #         bonus+=k[1].dmg*k[1].super_effective[curMap.spaces[j][1].classType.name]
                        #     if self.atk+k[1].dmg+bonus-curMap.spaces[j][1].defense>=maxDamage[1]:
                        #         maxDamage=[curMap.spaces[j][1],self.atk+bonus+k[1].dmg-curMap.spaces[j][1].defense,i,k[1],k[0]]
                #We then calculate the distance from this point to every player, and if its lower than the previous closest to a player we make it the new destination
                if (curMap.spaces[j][1].alignment==green or curMap.spaces[j][1].alignment==player) and destToPlayer<=closest[0]:
                    closest=[destToPlayer,i]
                #We then calculate the distance from this point to every player, and if its further we have it as a potential destination if this unit needs to retreat
                if (curMap.spaces[j][1].alignment==green or curMap.spaces[j][1].alignment==player) and destToPlayer>furthest[0]:
                    furthest=[destToPlayer,i]
    print('\n')
    if maxDamage[0]==None:
        self.update_location(closest[1])
        print(f'{self.name} moved to {closest[1]}')
        self.moved=True
        time.sleep(1.5*text_speed)
    else:
        self.update_location(maxDamage[2])
        print(f'{self.name} moved to {maxDamage[2]}')
        init_battle(self,maxDamage[0],maxDamage[4],maxDamage[3],False)
    if count!=0 and levelComplete==False and lordDied==False:
        ai(align)

def bounty_hunt(align):
    #The goal here is to make an ai that, if it can attack a player character, it will attack the one that it does the most hp percentage damage to
    #If it cant, it will move towards the nearest player character
    count=0
    global levelComplete
    if levelComplete==True or lordDied==True:
        return
    print('\n')
    for i in range(0,len(align.roster)):
        if align.roster[i].moved==False and align.roster[i].status=='Alive':
            j=i
            count+=1
    if count==0:
        align.turn_end()
        return
    for i in player.roster:
        if i.deployed==True and i.status=='Alive':
            print(f'Player unit {i.name} at {i.location} {i.curhp}/{i.hp} HP')
    for i in enemy.roster:
        if i.status=='Alive':
            print(f'Enemy unit {i.name} level {i.level} {i.classType.name} at {i.location} {i.curhp}/{i.hp} HP')
    for i in bounty_hunter.roster:
        if i.status=='Alive':
            print(f'Bounty hunter {i.name} level {i.level} {i.classType.name} at {i.location} {i.curhp}/{i.hp} HP\nCurrent Targets: {i.targets}')
    for i in green.roster:
        if i.status=='Alive':
            print(f'Allied unit {i.name} level {i.level} {i.classType.name} at {i.location} {i.curhp}/{i.hp} HP')
    #We just choose the last item in the list cuz its easiest this way
    curMap.display('cur')
    self=align.roster[j]
    #dist, weapon
    atkRange=[]
    #So here we want to find the attack range of a character
    for i in self.inventory:
        if isinstance(i,weapon):
            if i.weapontype in self.weaponType:
                if i.weaponlevel<=self.weaponType[i.weapontype]:
                    for j in i.rng:
                        atkRange.append([j,i])
    #closest= dist, location
    closest=[9999,(0,0)]
    furthest=[0,(0,0)]
    #maxDamage has character to attack, damage done, location,weapon being used, and distance
    maxDamage=[None,0,(0,0),None,0]
    #We check every map tile
    potential_spaces=djikstra(self)
    for i in potential_spaces:
        for j in curMap.spaces:
            #We find all the spaces with enemies on them
            if curMap.spaces[j][0]==True:
                if curMap.spaces[j][1].name in self.targets:
                    destToPlayer=abs(j[0]-i[0])+abs(j[1]-i[1])
                    for k in atkRange:
                        if k[0]==destToPlayer:
                            damage=forecast(self,k[1],curMap.spaces[j][1],curMap.spaces[j][1].active_item,None,k[0],True)[0]
                            if damage>=maxDamage[1]:
                                maxDamage=[curMap.spaces[j][1],damage,i,k[1],k[0]]
                            # bonus=0
                            # if k[1].dmgtype=='Magic' and curMap.spaces[j][1].alignment!=enemy:
                            #     if curMap.spaces[j][1].classType.name in k[1].super_effective:
                            #         bonus+=k[1].dmg*k[1].super_effective[curMap.spaces[j][1].classType.name]
                            #     if self.mag+k[1].dmg+bonus-curMap.spaces[j][0][1].res>=maxDamage[1]:
                            #         maxDamage=[curMap.spaces[j][1],self.mag+k[1].dmg+bonus-curMap.spaces[j][1].res,i,k[1],k[0]]
                            # elif k[1].dmgtype=='Phys' and curMap.spaces[j][1].alignment!=enemy:
                            #     if curMap.spaces[j][1].classType.name in k[1].super_effective:
                            #         bonus+=k[1].dmg*k[1].super_effective[curMap.spaces[j][1].classType.name]
                            #     if self.atk+k[1].dmg+bonus-curMap.spaces[j][1].defense>=maxDamage[1]:
                            #         maxDamage=[curMap.spaces[j][1],self.atk+bonus+k[1].dmg-curMap.spaces[j][1].defense,i,k[1],k[0]]
                    #We then calculate the distance from this point to every player, and if its lower than the previous closest to a player we make it the new destination
                    if destToPlayer<=closest[0]:
                        closest=[destToPlayer,i]
                    #We then calculate the distance from this point to every player, and if its further we have it as a potential destination if this unit needs to retreat
                    if destToPlayer>furthest[0]:
                        furthest=[destToPlayer,i]
    print('\n')
    if maxDamage[0]==None:
        self.update_location(closest[1])
        print(f'{self.name} moved to {closest[1]}')
        self.moved=True
        time.sleep(1.5*text_speed)
    else:
        self.update_location(maxDamage[2])
        print(f'{self.name} moved to {maxDamage[2]}')
        init_battle(self,maxDamage[0],maxDamage[4],maxDamage[3],False)
    if count!=0 and levelComplete==False and lordDied==False:
        bounty_hunt(align)



def djikstra(self):
    viable_spaces=[]
    shortest_path={}
    previous_nodes={}
    for i in curMap.spaces:
        distFromAI=abs(i[0]-self.location[0])+abs(i[1]-self.location[1])
        if distFromAI<=self.remainingMove:
            viable_spaces.append([i[0],i[1]])
            if distFromAI==1:
                moveCost=1
                if i in curMap.objectList:
                    moveCost=curMap.objectList[i].moveCost
                if curMap.spaces[i][0]==True:
                    if curMap.spaces[i][1].alignment!=self.alignment:
                        moveCost=999
                shortest_path[i]=moveCost
            else:
                shortest_path[i]=999
    shortest_path[self.location]=0
    while viable_spaces:
        cur_min=None
        for node in viable_spaces:
            if cur_min== None:
                cur_min= node
            elif shortest_path[node[0],node[1]] < shortest_path[cur_min[0],cur_min[1]]:
                cur_min=node
        neighbors=[]
        for i in range(-1,2):
            for j in range(-1,2):
                if abs(i+j)==1:
                    if (cur_min[0]+i,cur_min[1]+j) in curMap.spaces:
                        neighbors.append([cur_min[0]+i,cur_min[1]+j])
        for neighbor in neighbors:
            tenative_value = shortest_path[cur_min[0],cur_min[1]]
            moveCost=1
            if (neighbor[0],neighbor[1]) in curMap.objectList:
                moveCost=curMap.objectList[neighbor[0],neighbor[1]].moveCost
            if curMap.spaces[neighbor[0],neighbor[1]][0]==True:
                if curMap.spaces[neighbor[0],neighbor[1]][1].alignment!=self.alignment:
                    moveCost=999
            if moveCost!=999 and moveCost!=1 and (curMap.objectList[neighbor[0],neighbor[1]].name in move_cost_dict[self.classType.moveType]) or ('All' in move_cost_dict[self.classType.moveType]):
                #if curMap.objectList[neighbor[0],neighbor[1]].name in move_cost_dict[self.classType.moveType]:
                try:
                    moveCost=eval(move_cost_dict[self.classType.moveType][curMap.objectList[neighbor[0],neighbor[1]].name])
                except:
                    moveCost=eval(move_cost_dict[self.classType.moveType]['All'])
##                if self.classType.moveType=='Flying':
##                    moveCost=1
##                elif self.classType.moveType=='Horse':
##                    moveCost*=2
##                elif self.classType.moveType=='Mage' and curMap.objectList[neighbor[0],neighbor[1]].name=='Desert':
##                    moveCost=1
##                elif self.classType.moveType=='Pirate' and curMap.objectList[neighbor[0],neighbor[1]].name=='Water':
##                    moveCost=2
            tenative_value+=moveCost
            if (neighbor[0],neighbor[1]) in shortest_path:
                if tenative_value < shortest_path[neighbor[0],neighbor[1]]:
                    shortest_path[neighbor[0],neighbor[1]]=tenative_value
                    if (neighbor[0],neighbor[1]) not in previous_nodes:
                       previous_nodes[neighbor[0],neighbor[1]]=[cur_min]
                    else:
                        previous_nodes[neighbor[0],neighbor[1]].append(cur_min)
            if ([cur_min[0],cur_min[1]]) in viable_spaces:
                viable_spaces.remove([cur_min[0],cur_min[1]])
    for i in list(shortest_path):
        if shortest_path[i]>self.remainingMove:
            shortest_path.pop(i)
            #shortest_path.remove(i)
        elif curMap.spaces[i][0]==True:
            if curMap.spaces[i][1]!=self:
                shortest_path.pop(i)
                #shortest_path.remove(i)
    return shortest_path

def append_shop(base_class,*weapon):
    if base_class==base_weapon_dict:
        for i in range(0,len(base_class[weapon[0]])):
            print(f'{i} {base_class[weapon[0]][i].name}')
            i.info()
        inventoryX=input(f'Input the number of the {weapon} you wish to add.\n')
        count=input('Input how many of this item you want this shop to have\n')
        if inventoryX.isdigit() and count.isdigit():
            inventoryX=int(inventoryX)
            count=int(count)
            if count>0 and inventoryX>=0 and inventoryX<len(base_class[weapon[0]]):
                return [base_class[weapon[0]][inventoryX],count]
    else:
        for i in range(0,len(base_class)):
            print(f'{i} {base_class[i].name}')
            i.info()
        inventoryX=input('Input the number of the item you wish to add.\n')
        count=input('Input how many of this item you want this shop to have\n')
        if inventoryX.isdigit() and count.isdigit():
            inventoryX=int(inventoryX)
            count=int(count)
            if count>0 and inventoryX>=0 and inventoryX<len(base_class):
                return [base_class[inventoryX],count]

def edit_shop(*shop):
    if shop:
        inventory=shop[0].contents
    else:
        inventory=[]
    contI=True
    while contI==True:
        len_inven=len(inventory)
        if len_inven>0:
            print('Current inventory:')
            for i in range(0,len_inven):
                print(f'{i}: {inventory[i][0].name}')
        item_inventory=input('Press 1 to add a weapon to this shop, 2 to add armor, 3 to add misc, 4 to remove items, or x to finish.\n')
        if item_inventory.lower()=='x':
            return(inventory)
        elif item_inventory=='4' and len_inven>0:
            for i in range(0,len_inven):
                print(f'{i}: {inventory[i][0].name}')
            path=input('Input the item number that you would like to drop or X to cancel\n')
            if path.lower()=='x':
                pass
            elif path.isdigit():
                path=int(path)
                if path>=0 and path<len_inven:
                    confirm=input(f'Input Y to confirm that you would like to remove {inventory[path][0].name} or anything else to cancel\n')
                    if confirm.lower()=='y':
                        inventory.pop(path)
                        print('Item removed')
                    else:
                        print("Removal canceled")
                else:
                    print('Invalid input, returning to menu')
            else:
                print('Invalid input, returning to menu')
        elif item_inventory=='1':
            for i in base_weapon_dict:
                print(f'Category {i}: {base_weapon_dict[i].name}')
            weapon_inventory=input('Input the name of the weapon category that you want to add or Unique to add a unique weapon\n')
            if weapon_inventory.lower()=='unique':
                for i in range(0,len(unique_weapons)):
                    print(f'{i}: {unique_weapons[i].name}')
                unique_inventory=input('Input the number of the unique item you wish to add to this shop or X to cancel\n')
                if unique_inventory.lower()=='x':
                    pass
                else:
                    if unique_inventory.isdigit():
                        unique_inventory=int(unique_inventory)
                        if unique_inventory in range(0,len(unique_weapons)):
                            confirm=input(f'Input Y to confirm that you wish to add {unique_weapons[unique_inventory]} to the shop or anything else to cancel\n')
                            if confirm.lower()=='y':
                                inventory.append([unique_weapons.pop(unique_inventory),1])
                        else:
                            print('That number doesnt exist')
                    else:
                        print('Invalid input, returning to menu')
            elif weapon_inventory.lower() in ['sword','lance','axe','bow','tome','fist']:
                inventory.append(append_shop(base_weapon_dict,weapon_inventory.lower()))
            else:
                print('Invalid input')
        elif item_inventory=='2':
            inventory.append(append_shop(base_armor))
        elif item_inventory=='3':
            inventory.append(append_shop(base_misc))
        else:
            print('Invalid input')

def append_stock_inventory(base_class,*weapon):
    if base_class==base_weapon_dict:
        cont=False
        while cont==False:
            for i in range(0,len(base_class[weapon[0]])):
                print(f'{i} {base_class[weapon[0]][i].name}')
                i.info()
            inventoryX=input(f'Input the number of the {weapon[0]} you wish to add.\n')
            droppable=input('Input Y to make this item droppable when the unit holding it dies or anything else to have it not be droppable\n')
            if inventoryX.isdigit():
                inventoryX=int(inventoryX)
                if inventoryX>=0 and inventoryX<len(base_class[weapon[0]]):
                    x=base_class[weapon[0]][inventoryX].name
                    cont=True
            else:
                print('Invalid input')
    else:
        cont=False
        while cont==False:
            for i in range(0,len(base_class)):
                print(f'{i}: {base_class[i].name}')
            inventoryX=input('Input the number of the item you wish to add\n')
            droppable=input('Input Y to make this item droppable when the unit holding it dies or anything else to have it not be droppable\n')
            if inventoryX.isdigit():
                inventoryX=int(inventoryX)
                if inventoryX>=0 and inventoryX<len(base_class):
                    x=base_class[inventoryX].name
                    cont=True
            else:
                print('Invalid input')
    z=x.replace(' ','_')
    z=z.lower()
    if droppable.lower()=='y':
        return globals()[z](True)
    else:
        return globals()[z](False)

def stock_inventory(name,*inventory):
    contI=True
    if not inventory:
        inventory=[]
    else:
        inventory=inventory[0]
    while contI==True:
        if name.lower()=='chest':
            if len(inventory)==1:
                contI=False
        elif name.lower()=='inventory':
            if len(inventory)==inventory_max_size:
                print(f"The {name} is full")
                contI=False
        print('Current inventory:')
        for i in inventory:
            print(i.name)
        item_inventory=input(f'Press 1 to add a weapon to this {name}, 2 to add armor, 3 to add misc, or x to finish.\n')
        if item_inventory.lower()=='x':
            contI=False
        elif item_inventory=='1':
            weapon_inventory=input('Press 1 to view the swords, 2 to view the lances, 3 to view the axes, 4 to view the bows, 5 to view the tomes, 6 to view the fists, 7 to view the unique weapons, or anything else to cancel\n')
            if weapon_inventory=='1':
                inventory.append(append_stock_inventory(base_weapon_dict,'sword'))
            elif weapon_inventory=='2':
                inventory.append(append_stock_inventory(base_weapon_dict,'lance'))
            elif weapon_inventory=='3':
                inventory.append(append_stock_inventory(base_weapon_dict,'axe'))
            elif weapon_inventory=='4':
                inventory.append(append_stock_inventory(base_weapon_dict,'bow'))
            elif weapon_inventory=='5':
                inventory.append(append_stock_inventory(base_weapon_dict,'tome'))
            elif weapon_inventory=='6':
                inventory.append(append_stock_inventory(base_weapon_dict,'fist'))
            elif weapon_inventory=='7':
                for i in range(0,len(unique_weapons)):
                    print(f'{i}:{unique_weapons[i].name}')
                    unique_weapons[i].info()
                unique_inventory=input('Input the number of the item you wish to add or x to cancel.\n')
                if unique_inventory.lower()=='x':
                    pass
                elif unique_inventory.isdigit():
                    if int(unique_inventory)>=0 and int(unique_inventory)<len(unique_weapons):
                        inventory.append(unique_weapons.pop(int(unique_inventory)))
                        print('Item added')
                    else:
                        print('Invalid input')
            else:
                print('Invalid input')
        elif item_inventory=='2':
            inventory.append(append_stock_inventory(base_armor))
        elif item_inventory=='3':
            inventory.append(append_stock_inventory(base_misc))
    return inventory


def map_ordering(name,map_num,*map_lev):
    #delete=None
    for i in mapLevel.map_list:
        if i.mapNum==map_num:
            cont=False
            while cont==False:
                new=input(f'Map {i.name} has the same map number as {name}. Input X to delete {i.name}, Y to renumber {i.name}, or Z to renumber {name}\n')
                if new.lower()=='x':
                    confirm=input(f'You are about to delete {i.name}, input Y to confirm or anything else to cancel\n')
                    if confirm.lower()=='y':
                        mapLevel.map_list.pop(i)
                elif new.lower()=='y':
                    taken_nums=[]
                    if not map_lev:
                        taken_nums.append(tempMap(name,map_num))
                    for j in mapLevel.map_list:
                        if j!=i:
                            taken_nums.append(j.mapNum)
                    print(f'The currently taken map numbers are {taken_nums}')
                    new_num=input(f'Input the new number that you want {i.name} to be\n')
                    new_num=int(new_num)
                    if new_num>0:
                        if new_num not in taken_nums:
                            i.map_num=new_num
                            return map_num
                        else:
                            i.map_num=map_ordering(i.name,new_num,i)
                    else:
                        print('Invalid input, try again')
                elif new.lower()=='z':
                    taken_nums=[]
                    for j in mapLevel.map_list:
                        if j.name!=name:
                            taken_nums.append(j.mapNum)
                    print(f'The currently taken map numbers are {taken_nums}')
                    new_num=input('Input the new number that you want {name} to be\n')
                    new_num=int(new_num)
                    if new_num>0:
                        if new_num not in taken_nums:
                            return new_num
                        else:
                            if map_lev:
                                map_lev[0].mapNum=map_ordering(name,new_num,map_lev[0])
                            else:
                                return map_ordering(name,new_num)
                    else:
                        print('Invalid input, try again')
                else:
                    print('Invalid input')

def save(kind=''):
    #weapon arts, unique weapons, skills, classes, units, player roster, maps, supports list
    if saveallowed:
        print("Saving data, please don't turn off the power")
        if not os.path.exists(f'save_data{kind}_{campaign}.txt'):
            open(f'save_data{kind}_{campaign}.txt', 'w')
        with open(f'save_data{kind}_{campaign}.txt', 'r+') as f:
            f.truncate(0)
            toc = time.perf_counter()
            playtime=int(toc-tic)
            playtime+=timemodifier
            f.write(f'time\n{playtime}\nmap\n{mapNum}\n')
            f.write('roster\n')
            for i in player.roster:
                f.write(i.name)
                f.write('\n')
            f.write(f'support\n{player.support_master}')
        f.close()
        with open(f'save_data_maps{kind}_{campaign}.txt', 'w') as f:
            for i in mapLevel.map_list:
                count=0
                for attr, value in i.__dict__.items():
                    if attr=='objectList':
                        for j in value:
                            if value[j].name=='Door':
                                f.write(f'{attr}XYZCYX{value[j].name}/{value[j].location}/{value[j].opened}\n')
                            elif value[j].name=='Treasure Chest':
                                f.write(f'{attr}XYZCYX{value[j].name}/{value[j].location}/{value[j].contents.name}\n')
                            elif value[j].name=='Shop':
                                f.write(f'{attr}XYZCYX{value[j].name}/{value[j].location}')
                                for k in value[j].contents:
                                    f.write(f'/{k[0].name}/{k[1]}')
                                f.write('\n')
                            else:
                                f.write(f'{attr}XYZCYX{value[j].name}/{value[j].location}\n')
                    elif attr=='spaces' or attr=='triggerList' or attr=='char_trigger_list' or attr=='player_roster' or attr=='enemy_roster':
                        pass
                    else:
                        try:
                            f.write(f'{attr}XYZCYX{value.name}\n')
                        except:
                            f.write(f'{attr}XYZCYX{str(value)}\n')
                f.write('BREAK\n')
        #Here we write the type of the character, then the name of the character, then we go through and write all their stuff
        #Weapon arts, inventory, skills, and skills_all are broken up into multiple parts that will need to be combined later
        with open(f'save_data_other{kind}_{campaign}.txt', 'w') as f:
            f.truncate(0)
            f.write('CHARACTERS\n')
            f.write('BREAKX\n')
            for i in character.character_list:
                count=0
                for attr, value in i.__dict__.items():
                    if count==1:
                        f.write(f'{i.nameClass}\n')
                    if attr=='inventory':
                        for j in value:
                            if j in unique_weapons:
                                f.write(f'{attr}XYZCYXUNIQUE{j.name}/{str(j.curUses)}/{str(j.droppable)}\n')
                            else:
                                f.write(f'{attr}XYZCYX{j.name}/{str(j.curUses)}/{str(j.droppable)}\n')
                    elif attr=='weapon_arts' or attr=='skills' or attr=='skills_all':
                        for j in value:
                            f.write(f'{attr}XYZCYX{j.name}\n')
                    else:
                        try:
                            if attr=='active_item':
                                f.write(f'{attr}XYZCYX{value.name}/{str(value.curUses)}/{str(value.droppable)}\n')
                            else:
                                f.write(f'{attr}XYZCYX{value.name}\n')
                        except:
                            f.write(f'{attr}XYZCYX{str(value)}\n')
                    count+=1
                f.write('BREAK\n')
            f.write('BREAKX\n')
            f.write('WEAPONS\n')
            f.write('BREAKX\n')
            for i in unique_weapons:
                for attr, value in i.__dict__.items():
                    f.write(f'{attr}XYZCYX{str(value)}\n')
                f.write('BREAK\n')
            f.write('BREAKX\n')
            f.write('SKILLS\n')
            f.write('BREAKX\n')
            for i in skill.skill_list:
                for attr, value in i.__dict__.items():
                    try:
                        f.write(f'{attr}XYZCYX{value.name}\n')
                    except:
                        f.write(f'{attr}XYZCYX{str(value)}\n')
                f.write('BREAK\n')
            f.write('BREAKX\n')
            f.write('WEAPONARTS\n')
            f.write('BREAKX\n')
            for i in weapon_art.weapon_art_list:
                for attr, value in i.__dict__.items():
                    try:
                        f.write(f'{attr}XYZCYX{value.name}\n')
                    except:
                        f.write(f'{attr}XYZCYX{str(value)}\n')
                f.write('BREAK\n')
            f.write('BREAKX\n')
            f.write('CLASSES\n')
            f.write('BREAKX\n')
            for i in classType.class_list:
                for attr, value in i.__dict__.items():
                    if attr=='skill_list':
                        for j in value:
                            f.write(f'{attr}XYZCYX{j.name}\n')
                    else:
                        try:
                            f.write(f'{attr}XYZCYX{value.name}\n')
                        except:
                            f.write(f'{attr}XYZCYX{str(value)}\n')
                f.write('BREAK\n')
        f.close()
        if not os.path.exists('campaign_list.txt'):
            open('campaign_list.txt', 'w')
        with open('campaign_list.txt', 'r+') as f:
            campaigns=f.read().splitlines()
            if campaign not in campaigns:
                f.write(f'{campaign}\n')
        f.close()
        print('Save complete!')

def load(kind=''):
    global curMap
    j = open(f"save_data{kind}_{campaign}.txt", "r")
    saveData=j.read().splitlines()
    j.close()
    mapChoice=False
    for i in saveData:
        if i=='map':
            path='map'
        elif i=='time':
            path='time'
        elif i=='roster':
            path='roster'
        elif i=='support':
            path='support'
        elif i=='battlesaves':
            path='battlesaves'
        elif i=='turncount':
            path='turncount'
        else:
            if path=='map':
                if mapChoice==False:
                    global mapNum
                    mapNum=int(i)
                    mapChoice=True
    weapon.weapon_list=[]
    consumable.consumable_list=[]
    player.roster=[]
    j = open(f"save_data_other{kind}_{campaign}.txt", "r")
    listX=j.read().split('BREAKX\n')
    j.close()
    char_dict={}
    weapon_art_dict={}
    class_dict={}
    weapon_dict={}
    skill_dict={}
    dicts_dict=[char_dict,weapon_art_dict,class_dict,weapon_dict,skill_dict]
    cur=None
    for i in listX:
        if i=='CHARACTERS\n':
            cur_dict=char_dict
        elif i=='WEAPONS\n':
            cur_dict=weapon_dict
        elif i=='WEAPONARTS\n':
            cur_dict=weapon_art_dict
        elif i=='CLASSES\n':
            cur_dict=class_dict
        elif i=='SKILLS\n':
            cur_dict=skill_dict
        else:
            i=i.split('BREAK\n')
            for k in i:
                k=k.split('\n')
                for j in k:
                    j=j.split('XYZCYX')
                    if j[0]=='name':
                        cur=j[1]
                        cur_dict[cur]=[]
                    else:
                        try:
                            if j[0]!='':
                                cur_dict[cur].append(j)
                        except:
                            print(traceback.format_exc())
                            print(j)
    for i in weapon_dict:
        j=weapon(i,eval(weapon_dict[i][0][1]),eval(weapon_dict[i][2][1]),weapon_dict[i][3][1],
               eval(weapon_dict[i][4][1]),eval(weapon_dict[i][5][1]),eval(weapon_dict[i][6][1]),weapon_dict[i][7][1],
               eval(weapon_dict[i][8][1]),eval(weapon_dict[i][9][1]),eval(weapon_dict[i][10][1]),eval(weapon_dict[i][11][1]))
        unique_weapons.append(j)
        j.curUses=eval(weapon_dict[i][1][1])
    j=open(f"save_data_maps{kind}_{campaign}.txt", "r")
    listZ=j.read().split('BREAK\n')
    j.close()
    map_dict={}
    for i in listZ:
        i=i.split('\n')
        for j in i:
            j=j.split('XYZCYX')
            if j[0]=='name':
                cur=j[1]
                map_dict[cur]={}
            else:
                try:
                    if j[0]=='objectList':
                        if 'objectList' in map_dict[cur]:
                            map_dict[cur]['objectList'].append(j[1])
                        else:
                            map_dict[cur]['objectList']=[j[1]]
                    elif j[0]!='':
                        map_dict[cur][j[0]]=eval(j[1])
                except:
                    print(j)
    mapLevel.map_list=[]
    mapObject.objectList=[]
    for k in map_dict:
        newMap=mapLevel(k,map_dict[k]['y_size'],map_dict[k]['x_size'],map_dict[k]['mapNum'],map_dict[k]['spawns'],None,None)
        if map_dict[k]['mapNum']==mapNum:
            curMap=newMap
        newMap.turn_count=map_dict[k]['turn_count']
        newMap.battle_saves=map_dict[k]['battle_saves']
        for j in map_dict[k]['objectList']:
            j=j.split('/')
            j[0]=j[0].lower()
            j[0]=j[0].replace(' ','_')
            if j[0]!='door' and j[0]!='shop' and j[0]!='treasure_chest':
                p=globals()[j[0]](newMap,eval(j[1]))
            elif j[0]=='door':
                p=globals()[j[0]](newMap,eval(j[1]))
                p.opened==eval(j[2])
                if p.opened:
                    p.moveCost=1
            elif j[0]=='treasure_chest':
                j[2]=j[2].lower()
                j[2]=j[2].replace(' ','_')
                try:
                    p=globals()[j[0]](newMap,eval(j[1]),globals()[j[2]](False))
                except:
                    for i in unique_weapons:
                        if i.name.lower.replace(' ',',')==j[2]:
                            itemX=i
                    p=globals()[j[0]](newMap,eval(j[1]),itemX)
            elif j[0]=='shop':
                contents=[]
                for k in range(2,len(j)):
                    if k%2==0:
                        try:
                            contents.append([eval(f'base_{j[k].lower().replace(" ","_")}'),eval(j[k+1])])
                        except:
                            for L in unique_weapons:
                                if L.name==j[k]:
                                    item=L
                            contents.append([item,1])
                p=globals()[j[0]](newMap,eval(j[1]),contents)
    for i in weapon_art_dict:
        new=True
        for j in weapon_art.weapon_art_list:
            if j.name==i:
                new=False
                exist=j
        if new==False:
            exist.cost=eval(weapon_art_dict[i][1][1])
            exist.accuracy=eval(weapon_art_dict[i][3][1])
            exist.damage=eval(weapon_art_dict[i][2][1])
            exist.crit=eval(weapon_art_dict[i][4][1])
            exist.avoid=eval(weapon_art_dict[i][5][1])
            exist.weapontype=weapon_art_dict[i][0][1]
            exist.super_effective=eval(weapon_art_dict[i][6][1])
            exist.range=eval(weapon_art_dict[i][7][1])
            exist.damageType=weapon_art_dict[i][8][1]
            exist.bonus=eval(weapon_art_dict[i][9][1])
        else:
            ###    #Weapon Arts (name,weapontype,cost,damage,accuracy,crit,avoid,super_effective,rng,damageType(can be 'Same','Magic','Phys'),*[effect_stat,effect_change,effect_operator,target]):
            weapon_art(i,weapon_art_dict[i][0][1],eval(weapon_art_dict[i][1][1]),eval(weapon_art_dict[i][2][1]),eval(weapon_art_dict[i][3][1]),
                       weapon_art_dict[i][4][1],weapon_art_dict[i][5][1],eval(weapon_art_dict[i][6][1]),eval(weapon_art_dict[i][7][1]),weapon_art_dict[i][8][1],eval(weapon_art_dict[i][9][1]))
    for i in skill_dict:
        new=True
        for j in skill.skill_list:
            if j.name==i:
                new=False
                exist=j
        if new==False:
            for k in skill_dict[i]:
                if k[0]!='trigger_stat' and k[0]!='effect_stat':
                    try:
                        setattr(exist,k[0],eval(k[1]))
                    except:
                        setattr(exist,k[0],k[1])
                else:
                    setattr(exist,k[0],k[1])
        else:
            ###Skills (name,trigger_chance,trigger_stat,effect_stat,effect_change,effect_operator,effect_temp,effect_target,*relative_stat):
            if len(skill_dict[i])==7:
                skill(i,eval(skill_dict[i][0]),skill_dict[i][1],skill_dict[i][2],eval(skill_dict[i][3]),skill_dict[i][4],eval(skill_dict[i][6]),skill_dict[i][5])
            else:
                skill(i,eval(skill_dict[i][0]),skill_dict[i][1],skill_dict[i][2],eval(skill_dict[i][3]),skill_dict[i][4],eval(skill_dict[i][6]),skill_dict[i][5],skill_dict[i][7])
    for i in class_dict:
        new=True
        for j in classType.class_list:
            if j.name==i:
                new=False
                exist=j
        #print(class_dict[i])
        if new==False:
            exist.skill_list=[]
            for k in class_dict[i]:
                if k[0]!='skill_list':
                    try:
                        setattr(exist,k[0],eval(k[1]))
                    except:
                        setattr(exist,k[0],k[1])
                else:
                    for L in skill.skill_list:
                        if L.name==k[1]:
                            skillX=L
                    exist.skill_list.append(skillX)
        else:
            #(name,moveType,hp,hpG,atk,atkG,mag,magG,skillX,skillG,luck,luckG,defense,defG,res,resG,spd,spdG,moveRange,weaponType,promotions,skill_list)
            skill_list=[]
            for k in class_dict[i]:
                if k[0]=='skill_list':
                    skill_list.append(k[1])
            p=classType(i,class_dict[i][0],eval(class_dict[i][1]),eval(class_dict[i][2]),eval(class_dict[i][3]),eval(class_dict[i][4]),
                        eval(class_dict[i][5]),eval(class_dict[i][6]),eval(class_dict[i][7]),eval(class_dict[i][8]),eval(class_dict[i][9]),
                        eval(class_dict[i][10]),eval(class_dict[i][11]),eval(class_dict[i][12]),eval(class_dict[i][13]),eval(class_dict[i][14]),
                        eval(class_dict[i][15]),eval(class_dict[i][16]),eval(class_dict[i][17]),eval(class_dict[i][18]),eval(class_dict[i][19]),skill_list)
    for i in char_dict:
        new=True
        for j in character.character_list:
            if j.name==i:
                new=False
                exist=j
        if new==False:
            equipped_count=0
            exist.skills=[]
            skills_placed=[]
            exist.skills_all=[]
            exist.inventory=[]
            exist.weapon_arts=[]
            for j in char_dict[i]:
                if len(j)>1:
                    if j[0]!='alignment' and j[0]!='active_item' and j[0]!='inventory' and j[0]!='skills' and j[0]!='skills_all' and j[0]!='classType' and j[0]!='weapon_arts':
                        try:
                            setattr(exist,j[0],eval(j[1]))
                        except:
                            setattr(exist,j[0],j[1])
                    elif j[0]=='weapon_arts':
                        for k in weapon_art.weapon_art_list:
                            if k.name==j[1]:
                                exist.weapon_arts.append(k)
                    elif j[0]=='classType':
                        for k in classType.class_list:
                            if k.name==j[1]:
                                exist.classType=k
                    elif j[0]=='alignment':
                        z=j[1]
                        z=z.replace(' ','_')
                        z=z.lower()
                        setattr(exist,j[0],eval(z))
                    elif j[0]=='active_item' and j[1]!='None':
                        x=j[1]
                        x=x.split('/')
                        uses=x[1]
                        z=x[0]
                        z=z.replace(' ','_')
                        z=z.lower()
                        try:
                            p=globals()[z](eval(x[2]))
                        except:
                            for k in unique_weapons:
                                if k.name==x[0]:
                                    p=k
                        p.curUses=int(uses)
                        setattr(exist,j[0],p)
                        exist.add_item(p)
                    elif j[0]=='inventory':
                        x=j[1]
                        x=x.split('/')
                        uses=x[1]
                        z=x[0]
                        z=z.replace(' ','_')
                        z=z.lower()
                        try:
                            p=globals()[z](eval(x[2]))
                        except:
                            for k in unique_weapons:
                                if k.name==x[0]:
                                    p=k
                        p.curUses=int(uses)
                        if eval(z)==type(exist.active_item) and equipped_count==0 and p.curUses==exist.active_item.curUses:
                            equipped_count+=1
                        else:
                            exist.add_item(p)
                    elif j[0]=='active_item' and j[1]=='None':
                        setattr(exist,j[0],None)
                    elif j[0]=='skills':
                        for k in skill.skill_list:
                            if k.name==j[1]:
                                exist.add_skill(k)
                                skills_placed.append(j[1])
                    elif j[0]=='skills_all':
                        if j[1] not in skills_placed:
                            for k in skill.skill_list:
                                if k.name==j[1]:
                                  exist.skills_all.append(k)
                else:
                    unitType=j[0]
        elif new==True:
            ###player_char(name,curhp,hp,hpG,atk,atkG,mag,magG,skill,skillG,luck,luckG,defense,defG,res,resG,spd,spdG,mov,classType,{weaponType},joinMap,[inventory],level,{supports},[weapon_arts])
###enemy_char(name,classType,joinMap,[inventory],level,[spawn])
###recruitable(name,curhp,hp,hpG,atk,atkG,mag,magG,skill,skillG,luck,luckG,defense,defG,res,resG,spd,spdG,mov,classType,weaponType,joinMap,inventory,level,spawn,support_list,weapon_arts,recruit_convo)
###boss(name,curhp,hp,atk,mag,skill,luck,defense,res,spd,mov,classType,weaponType,joinMap,inventory,level,spawn):
            boss_needed_fields_reg=['name','hp','atk','mag','skill','luck','defense','res','spd','movModifier','classType','weaponType','joinMap','level','spawn']
            recruitable_needed_fields_reg=['name','curhp','hp','hpG','atk','atkG','mag','magG','skill','skillG','luck','luckG','defense','defG','res',
                                       'resG','spd','spdG','movModifier','classType','weaponType','joinMap','level','spawn','supports','ending','recruit_convo']
            enemy_char_needed_fields_reg=['name','classType','joinMap','level','spawn']
            player_char_needed_fields_reg=['name','hp','hpG','atk','atkG','mag','magG','skill','skillG','luck','luckG','defense','defG','res',
                                       'resG','spd','spdG','movModifier','classType','weaponType','joinMap','level','supports','ending']
            i_dict_reg={'supports':{}}
            i_dict_mult={'inventory':[],'weapon_arts':[]}
            i_dict_upd={}
            i_dict_upd_mult={'skills':[],'skills_all':[]}
            if char_dict[i][0][0]=='enemy_char':
                for k in char_dict[i]:
                    if k[0] in enemy_char_needed_fields_reg:
                        try:
                            i_dict_reg[k[0]]=eval(k[1])
                        except:
                            i_dict_reg[k[0]]=k[1]
                    elif k[0] in i_dict_mult:
                        i_dict_mult[k[0]].append(k[1])
                    elif k[0]!='alignment':
                        if k[0] in i_dict_upd_mult:
                            i_dict_upd_mult[k[0]].append(k[1])
                        elif k[0]!='alignment' and len(k)>1:
                            try:
                                i_dict_upd[k[0]]=eval(k[1])
                            except:
                                i_dict_upd[k[0]]=k[1]
                inventory=[]
                for L in i_dict_mult['inventory']:
                        x=L.split('/')
                        uses=x[1]
                        z=x[0]
                        z=z.replace(' ','_')
                        z=z.lower()
                        try:
                            p=globals()[z](eval(x[2]))
                        except:
                            for k in unique_weapons:
                                if k.name==x[0]:
                                    p=k
                        p.curUses=int(uses)
                        inventory.append(p)
                char=enemy_char(i,i_dict_reg['classType'],i_dict_reg['joinMap'],inventory,i_dict_reg['level'],i_dict_reg['spawn'])

            ###player_char(name,curhp,hp,hpG,atk,atkG,mag,magG,skill,skillG,luck,luckG,defense,defG,res,resG,spd,spdG,mov,classType,{weaponType},joinMap,[inventory],level,{supports},[weapon_arts],ending)
            elif char_dict[i][0][0]=='player_char':
                for k in char_dict[i]:
                    if k[0] in player_char_needed_fields_reg:
                        try:
                            i_dict_reg[k[0]]=eval(k[1])
                        except:
                            i_dict_reg[k[0]]=k[1]
                    elif k[0] in i_dict_mult:
                        i_dict_mult[k[0]].append(k[1])
                    else:
                        if k[0] in i_dict_upd_mult:
                            i_dict_upd_mult[k[0]].append(k[1])
                        elif k[0]!='alignment' and len(k)>1:
                            try:
                                i_dict_upd[k[0]]=eval(k[1])
                            except:
                                i_dict_upd[k[0]]=k[1]
                                pass
                inventory=[]
                for L in i_dict_mult['inventory']:
                        x=L.split('/')
                        uses=x[1]
                        z=x[0]
                        z=z.replace(' ','_')
                        z=z.lower()
                        try:
                            p=globals()[z](eval(x[2]))
                        except:
                            for k in unique_weapons:
                                if k.name==x[0]:
                                    p=k
                        p.curUses=int(uses)
                        inventory.append(p)
                char=player_char(i,i_dict_reg['hp'],i_dict_reg['hp'],i_dict_reg['hpG'],i_dict_reg['atk'],i_dict_reg['atkG'],
                                      i_dict_reg['mag'],i_dict_reg['magG'],i_dict_reg['skill'],i_dict_reg['skillG'],i_dict_reg['luck'],i_dict_reg['luckG'],
                                      i_dict_reg['defense'],i_dict_reg['defG'],i_dict_reg['res'],i_dict_reg['resG'],i_dict_reg['spd'],i_dict_reg['spdG'],
                                      i_dict_reg['movModifier'],i_dict_reg['classType'],i_dict_reg['weaponType'],i_dict_reg['joinMap'],inventory,
                                      i_dict_reg['level'],i_dict_reg['supports'],i_dict_mult['weapon_arts'],i_dict_reg['ending'])

###boss(name,curhp,hp,atk,mag,skill,luck,defense,res,spd,mov,classType,weaponType,joinMap,inventory,level,spawn):
            elif char_dict[i][0][0]=='boss':
                for k in char_dict[i]:
                    if k[0] in boss_needed_fields_reg:
                        try:
                            i_dict_reg[k[0]]=eval(k[1])
                        except:
                            i_dict_reg[k[0]]=k[1]
                    elif k[0] in i_dict_mult:
                        i_dict_mult[k[0]].append(k[1])
                    else:
                        if k[0] in i_dict_upd_mult:
                            i_dict_upd_mult[k[0]].append(k[1])
                        elif k[0]!='alignment' and len(k)>1:
                            try:
                                i_dict_upd[k[0]]=eval(k[1])
                            except:
                                i_dict_upd[k[0]]=k[1]
                inventory=[]
                for L in i_dict_mult['inventory']:
                        x=L.split('/')
                        uses=x[1]
                        z=x[0]
                        z=z.replace(' ','_')
                        z=z.lower()
                        try:
                            p=globals()[z](eval(x[2]))
                        except:
                            for k in unique_weapons:
                                if k.name==x[0]:
                                    p=k
                        p.curUses=int(uses)
                        inventory.append(p)
                char=boss(i,i_dict_reg['hp'],i_dict_reg['hp'],i_dict_reg['atk'],i_dict_reg['mag'],i_dict_reg['skill'],
                               i_dict_reg['luck'],i_dict_reg['defense'],i_dict_reg['res'],i_dict_reg['spd'],i_dict_reg['movModifier'],
                               i_dict_reg['classType'],i_dict_reg['weaponType'],i_dict_reg['joinMap'],inventory,i_dict_reg['level'],i_dict_reg['spawn'])

###recruitable(name,curhp,hp,hpG,atk,atkG,mag,magG,skill,skillG,luck,luckG,defense,defG,res,resG,spd,spdG,mov,classType,weaponType,joinMap,inventory,level,spawn,support_list,weapon_arts,recruit_convo)
            elif char_dict[i][0][0]=='recruitable':
                for k in char_dict[i]:
                    if k[0] in recruitable_needed_fields_reg:
                        try:
                            i_dict_reg[k[0]]=eval(k[1])
                        except:
                            i_dict_reg[k[0]]=k[1]
                    elif k[0] in i_dict_mult:
                        i_dict_mult[k[0]].append(k[1])
                    else:
                        if k[0] in i_dict_upd_mult:
                            i_dict_upd_mult[k[0]].append(k[1])
                        elif k[0]!='alignment' and len(k)>1:
                            try:
                                i_dict_upd[k[0]]=eval(k[1])
                            except:
                                i_dict_upd[k[0]]=k[1]
                inventory=[]
                for L in i_dict_mult['inventory']:
                        x=L.split('/')
                        uses=x[1]
                        z=x[0]
                        z=z.replace(' ','_')
                        z=z.lower()
                        try:
                            p=globals()[z](eval(x[2]))
                        except:
                            for k in unique_weapons:
                                if k.name==x[0]:
                                    p=k
                        p.curUses=int(uses)
                        inventory.append(p)
                char=recruitable(i,i_dict_reg['hp'],i_dict_reg['hp'],i_dict_reg['hpG'],i_dict_reg['atk'],i_dict_reg['atkG'],
                      i_dict_reg['mag'],i_dict_reg['magG'],i_dict_reg['skill'],i_dict_reg['skillG'],i_dict_reg['luck'],i_dict_reg['luckG'],
                      i_dict_reg['defense'],i_dict_reg['defG'],i_dict_reg['res'],i_dict_reg['resG'],i_dict_reg['spd'],i_dict_reg['spdG'],
                      i_dict_reg['movModifier'],i_dict_reg['classType'],i_dict_reg['weaponType'],i_dict_reg['joinMap'],inventory,
                      i_dict_reg['level'],i_dict_reg['spawn'],i_dict_reg['supports'],i_dict_mult['weapon_arts'],i_dict_reg['ending'],i_dict_reg['recruit_convo'])
            else:
                print('Illegal')

            for M in i_dict_upd:
                if M!='active_item':
                    setattr(char,M,i_dict_upd[M])
                else:
                    x=i_dict_upd[M].split('/')
                    uses=x[1]
                    z=x[0]
                    z=z.replace(' ','_')
                    z=z.lower()
                    for S in char.inventory:
                        if isinstance(S,eval(z)):
                            if S.curUses==int(uses):
                                char.active_item=S
            non_equipped_skills=[]
            for N in i_dict_upd_mult['skills_all']:
                if N not in i_dict_upd_mult['skills']:
                    non_equipped_skills.append(N)
            for O in i_dict_upd_mult['skills']:
                for P in skill.skill_list:
                    if P.name==O:
                        if P not in char.skills:
                            char.add_skill(P)
            for Q in non_equipped_skills:
                for R in skill.skill_list:
                    if R.name==Q:
                        if R not in char.skills_all:
                            char.skills_all.append(R)
    for i in character.character_list:
        for j in mapLevel.map_list:
            if i.joinMap==j.mapNum:
                if i.alignment==player and i not in j.player_roster:
                    j.player_roster.append(i)
                elif i.alignment==enemy and i not in j.enemy_roster:
                    j.enemy_roster.append(i)
            else:
                if i.alignment==player and i in j.player_roster:
                    j.player_roster.pop(i)
                elif i.alignment==enemy and i in j.enemy_roster:
                    j.enemy_roster.pop(i)
    j = open(f"save_data{kind}_{campaign}.txt", "r")
    saveData=j.read().splitlines()
    j.close()
    for i in saveData:
        if i=='map':
            path='map'
        elif i=='time':
            path='time'
        elif i=='roster':
            path='roster'
        elif i=='support':
            path='support'
        elif i=='battlesaves':
            path='battlesaves'
        elif i=='turncount':
            path='turncount'
        else:
            if path=='roster':
                for j in character.character_list:
                    if j.name==i:
                        player.roster.append(j)
            elif path=='support':
               player.support_master=eval(i)
            elif path=='time':
                global timemodifier
                timemodifier+=int(i)
    if curMap.battle_saves>0:
        for i in curMap.enemy_roster:
            if i.status=='Alive':
                enemy.roster.append(i)
        for i in enemy.roster:
            i.update_location(i.location)
        for i in player.roster:
            if i.deployed==True:
               i.update_location(i.location)



def create_character(*name):
    #Choosing alignment
    print('Welcome to the character creator')
    cont=False
    while cont==False:
        if not name:
            align_input=input('Input P to make this a player unit, E to make this a generic enemy unit with autoleveled stats, B to make this a unique enemy unit with set stats, or R to make this a recruitable enemy unit\n')
        else:
            align_input=input('Input P to make this a player unit or R to make this a recruitable enemy unit\n')
        if align_input.lower()=='p':
            confirm=input('To confirm your character will be a player unit input Y, input anything else to cancel\n')
            if confirm.lower()=='y':
                align=player
                unit_type='Player'
                #manual=True
                cont=True
        elif align_input.lower()=='e' and not name:
            confirm=input('To confirm your character will be a generic enemy input Y, input anything else to cancel\n')
            if confirm.lower()=='y':
                unit_type='Generic'
                align=enemy
                cont=True
        elif align_input.lower()=='b' and not name:
            confirm=input('To confirm your character will be a unique enemy input Y, input anything else to cancel\n')
            if confirm.lower()=='y':
                unit_type='Unique'
                align=enemy
                cont=True
        elif align_input.lower()=='r':
            confirm=input('To confirm your character will be a recruitable enemy input Y, input anything else to cancel\n')
            if confirm.lower()=='y':
                unit_type='Recruitable'
                align=enemy
                cont=True
        else:
            print('Invalid input, try again')
    #naming character
    cont=False
    if name:
        name=name[0]
        cont=True
    while cont==False:
        name=input('Input the name for your character\n')
        end_name=input(f'Your character will be named {name}, input Y to confirm or anything else to reenter the name\n')
        contX=True
        for i in character.character_list:
            if i.name==name:
                print(f'There already exists a character with the name {name}, choose something else')
                contX=False
        if end_name.lower()=='y' and contX:
            cont=True
    #set level
    cont=False
    while cont==False:
        level=input('Input what level you would like your character to be\n')
        try:
            level=int(level)
            if level>0 and level<=level_cap:
                cont=True
        except:
            print(traceback.format_exc())
            print('Invalid input, try again')
    #set join map
    cont=False
    while cont==False:
        #existing_maps=[]
        for i in mapLevel.map_list:
            print(f'Map Number {i.mapNum}: {i.name}')
        join_map=input('Input the number of the map that you would like this character to join/be on, for example if you want them to join in the first map enter 1\n')
        try:
            join_map=int(join_map)
            for i in mapLevel.map_list:
                if join_map==i.mapNum:
                    mapX=i
                    cont=True
            if cont!=True:
                print('Invalid input, try again')
        except:
            print(traceback.format_exc())
            print('Invalid input, try again')
    #Choosing class
    cont=False
    while cont==False:
        print('Choose a class')
        for i in range(0,len(classType.class_list)):
            print(f'{i}: {classType.class_list[i].name}')
        class_choice=input('Input the number of the class you want this character to be\n')
        try:
            classType.class_list[int(class_choice)].info()
            end_class=input(f'Input Y to confirm you wish {name} to be a {classType.class_list[int(class_choice)].name}, and anything else to cancel\n')
            if end_class.lower()=='y':
                class_type=classType.class_list[int(class_choice)]
                class_name=classType.class_list[int(class_choice)].name
                cont=True
            else:
                pass
        except:
            print(traceback.format_exc())
            print('Invalid input, try again')
    #Setting weapon levels
    cont=False
    weapon_type={}
    if unit_type=='Generic':
        cont=True
    while cont==False:
        for i in class_type.weaponType:
            print(f'{i} : Level {class_type.weaponType[i]}')
        for i in weapon_type:
            print(f'{i} : Level {weapon_type[i]}')
        print(f"The current usable weapon types and weapon level for {name} are printed above\n")
        print('Here you can add new usable types or change the weapon level for existing ones\n')
        weapon_type_add=input('Input 1 to add/edit Sword, 2 for Lance, 3 for Axe, 4 for Bow, 5 for Tome, 6 for Fist, or x to exit\n')
        if weapon_type_add.lower()=='x':
            cont=True
        elif weapon_type_add=='1':
            weapon_level=input('Input the weapon level for Swords\n')
            try:
                weapon_type['Sword']=int(weapon_level)
            except:
                print(traceback.format_exc())
                print('Invalid input, returning to choice')
        elif weapon_type_add=='2':
            weapon_level=input('Input the weapon level for Lances\n')
            try:
                weapon_type['Lance']=int(weapon_level)
            except:
                print(traceback.format_exc())
                print('Invalid input, returning to choice')
        elif weapon_type_add=='3':
            weapon_level=input('Input the weapon level for Axes\n')
            try:
                weapon_type['Axe']=int(weapon_level)
            except:
                print(traceback.format_exc())
                print('Invalid input, returning to choice')
        elif weapon_type_add=='4':
            weapon_level=input('Input the weapon level for Bows\n')
            try:
                weapon_type['Bow']=int(weapon_level)
            except:
                print(traceback.format_exc())
                print('Invalid input, returning to choice')
        elif weapon_type_add=='5':
            weapon_level=input('Input the weapon level for Tomes\n')
            try:
                weapon_type['Tome']=int(weapon_level)
            except:
                print(traceback.format_exc())
                print('Invalid input, returning to choice')
        elif weapon_type_add=='6':
            weapon_level=input('Input the weapon level for Fists\n')
            try:
                weapon_type['Fist']=int(weapon_level)
            except:
                print(traceback.format_exc())
                print('Invalid input, returning to choice')
    #Creating the inventory
    cont=False
    print(f"Now you will stock {name}'s inventory")
    inventory=stock_inventory('inventory')
    #Setting active item
    cont=False
    while cont==False:
        possible_active_items={}
        for i in range(0,len(inventory)):
            if isinstance(inventory[i],weapon):
                if (inventory[i].weapontype in class_type.weaponType and inventory[i].weaponlevel>=class_type.weaponType[inventory[i].weapontype]) or (inventory[i].weapontype in weapon_type and inventory[i].weaponlevel>=weapon_type[inventory[i].weapontype]):
                    possible_active_items[i]=inventory[i]
        if len(possible_active_items)==0:
            cont=True
        else:
            for i in possible_active_items:
                print(f'{i} : {possible_active_items[i].name}')
            active_choice=input(f"Input the item that you want to be {name}'s active item\n")
            try:
                possible_active_items[int(active_choice)]
                inventory.insert(0,inventory.pop(int(active_choice)))
                cont=True
            except:
                print(traceback.format_exc())
                print('Invalid input, please try again')
    #Supports
    if unit_type=='Player' or unit_type=='Recruitable':
        supports={}
        cont=False
        print('In this step you will enter the names of all characters that you want this character to support one at a time. This is for all possible support partners, not just characters you have currently made')
        while cont==False:
            support_char=input(f'Enter the name of one character you would like {name} to support, or x to finish\n')
            if support_char.lower()=='x':
                end=input('Input X to confirm you are finished, Y to cancel, or Z to name a character X\n')
                if end.lower()=='x':
                    cont=True
                elif end.lower()=='y':
                    pass
                elif end.lower()=='z':
                    supports[support_char]=0
            else:
                confirm=input(f'Input Y to confirm that you want to add {support_char} as a support option for {name} or anything else to cancel\n')
                if confirm.lower()=='y':
                    supports[support_char]=0
        weapon_arts=[]
        cont=False
        print(f"In this step you will choose {name}'s starting weapon arts")
        while cont==False:
            if len(weapon_arts)==len(weapon_art.weapon_art_list):
                cont=True
            for i in range(0,len(weapon_art.weapon_art_list)):
                if weapon_art.weapon_art_list[i] not in weapon_arts:
                    print(f"{i}: {weapon_art.weapon_art_list[i].name}")
            weapon_art_add=input("Input the number of the weapon art you would like to add or X to finish\n")
            if weapon_art_add.lower()=='x':
                confirm=input("Input Y to confirm that you're done adding weapon arts and anything else to cancel")
                if confirm.lower()=='y':
                    cont=True
            else:
                try:
                    if weapon_art.weapon_art_list[int(weapon_art_add)] not in weapon_arts:
                        weapon_arts.append(weapon_art.weapon_art_list[int(weapon_art_add)])
                    else:
                        print('Invalid input, try again')
                except:
                    print(traceback.format_exc())
                    print('Invalid input, try again')
    #Enemy exclusive path
    if align==enemy:
        #setting spawn
        cont=False
        while cont==False:
            print('Input the coordinates where you would like this unit to spawn on their map in x,y integer form, with 0,0 being the top left and 1,1 being down and to the right of that')
            print('Any x,y pair will work as long as its on the map, not just 0,0 or 1,1')
            spawn=input('Enter the coordinates now\n')
            try:
                spawn=spawn.split(',')
                spawn[0]=int(spawn[0])
                spawn[1]=int(spawn[1])
                spawn=(spawn[0],spawn[1])
                contCont=True
                if (spawn[0],spawn[1]) not in mapX.spawns and (spawn[0],spawn[1]) in mapX.spaces:
                    if (spawn[0],spawn[1]) in mapX.objectList:
                        if mapX.objectList[spawn[0],spawn[1]].name=='Door':
                            contCont=False
                        elif mapX.objectList[spawn[0],spawn[1]].name=='Void' and class_choice.moveType!='Flying':
                            contCont=False
                        elif mapX.objectList[spawn[0],spawn[1]].name=='Void' and (class_choice.moveType!='Flying' and class_choice.moveType!='Pirate'):
                            contCont=False
                    if contCont==True:
                        cont=True
                elif (spawn[0],spawn[1]) in mapX.spawns:
                    print('A player unit spawns there, invalid input')
                else:
                    print('Invalid spawn, try again')
            except:
                print(traceback.format_exc())
                print('Invalid input, try again')
    #Creating the recruitment convo
    if unit_type=='Recruitable':
        cont=False
        while cont==False:
            recruit_convo=input('Write out the dialogue you would like to play when this character is recruited\n')
            confirm=input(f'Input Y to confirm that the following is what you want to play or any other input to rewrite it\n{recruit_convo}\n')
            if confirm.lower()=='y':
                cont=True
    #creating the ending
    if unit_type=='Recruitable' or unit_type=='Player':
        cont=False
        while cont==False:
            ending=input('Write out the text you would like to play for this characters ending\n')
            confirm=input(f'Input Y to confirm that the following is what you want to play or any other input to rewrite it\n{recruit_convo}\n')
            if confirm.lower()=='y':
                cont=True
    #setting bases and growths
    bases={}
    growth={}
    if unit_type=='Player' or unit_type=='Unique' or unit_type=='Recruitable':
        print('Here you will set the bases and growths of your character.\nGrowths should be input in decimal notation, and represent the probability of acquiring a stat on level up.\nFor example a .65 HP growth would make it so that a character has a 65% chance of gaining +1 in HP on level up.')
        for i in character.stats:
            cont=False
            while cont==False:
                if i!='movModifier':
                    stat=input(f'{i}\n')
                else:
                    stat=input('Move modifier (how many more spaces this character can move than normal units of their class)\n')
                if stat.isdigit():
                    if i!='hp':
                        if int(stat)>=0:
                            bases[i]=int(stat)
                            cont=True
                        else:
                            print('Stats must be positive integers')
                    else:
                        if int(stat)>0:
                            bases[i]=int(stat)
                            cont=True
                        else:
                            print('HP must be above 0')
        if unit_type!='Unique':
            for i in character.growths:
                cont=False
                while cont==False:
                    stat=input(f'{character.growths[i]} Growth (decimal notation)\n')
                    if isfloat(stat):
                        growth[i]=float(stat)
                        cont=True
                    else:
                        print("The growth must be a number")
        #Creating the character
#player_char(name,curhp,hp,hpG,atk,atkG,mag,magG,skill,skillG,luck,luckG,defense,defG,res,resG,spd,spdG,mov,classType,weaponType,joinMap,inventory,level,support_list,weapon_arts,ending)
#enemy_char(name,classType,joinMap,[inventory],level,[spawn])
#recruitable(name,curhp,hp,hpG,atk,atkG,mag,magG,skill,skillG,luck,luckG,defense,defG,res,resG,spd,spdG,mov,classType,weaponType,joinMap,inventory,level,spawn,support_list,weapon_arts,ending,recruit_convo)
#boss(name,curhp,hp,atk,mag,skill,luck,defense,res,spd,mov,classType,weaponType,joinMap,inventory,level,spawn)
        if unit_type=='Player':
            player_char(name,bases['hp'],bases['hp'],growth['hpG'],bases['atk'],growth['atkG'],
                        bases['mag'],growth['magG'],bases['skill'],growth['skillG'],bases['luck'],growth['luckG'],
                        bases['defense'],growth['defG'],bases['res'],growth['resG'],bases['spd'],growth['spdG'],
                        bases['movModifier'],class_name,weapon_type,join_map,inventory,level,supports,weapon_arts,ending)
        elif unit_type=='Unique':
            boss(name,bases['hp'],bases['hp'],bases['atk'],bases['mag'],bases['skill'],bases['luck'],bases['defense'],bases['res'],bases['spd'],bases['movModifier'],class_name,weapon_type,join_map,inventory,level,spawn)
        elif unit_type=='Recruitable':
            recruitable(name,bases['hp'],bases['hp'],growth['hpG'],bases['atk'],growth['atkG'],
                        bases['mag'],growth['magG'],bases['skill'],growth['skillG'],bases['luck'],growth['luckG'],
                        bases['defense'],growth['defG'],bases['res'],growth['resG'],bases['spd'],growth['spdG'],
                        bases['movModifier'],class_name,weapon_type,join_map,inventory,level,spawn,supports,weapon_arts,ending,recruit_convo)
    elif unit_type=='Generic':
        enemy_char(name,class_name,join_map,inventory,level,spawn)
    print('Character created!')


def create_map(*num):
    print('Welcome to the map creator')
    #naming the map
    cont=False
    while cont==False:
        name=input('Input the name for this map\n')
        confirm=input(f'Input Y to confirm {name} as this maps name, anything else to rename it\n')
        for i in mapLevel.map_list:
            if i.name==name:
                confirm='There already exists a level with that name'
        if confirm.lower()=='y':
            cont=True
        elif confirm=='There already exists a level with that name':
            print(confirm)
    #setting the map number
    cont=False
    if num:
        map_num=num[0]
        cont=True
    while cont==False:
        existing_list=[]
        for i in mapLevel.map_list:
            existing_list.append(i.mapNum)
        existing_list.sort()
        print(f'The existing maps are {existing_list}')
        map_num=input('Input the number map that you want this to be. For example, if you want this to be the 23rd map you play in the story you would enter 23 here\n')
        try:
            base_name=name
            #delete=None
            map_num=int(map_num)
            map_num=map_ordering(name,int(map_num))
            for i in mapLevel.map_list:
                if isinstance(i,tempMap):
                    mapLevel.map_list.remove(i)
            cont=True
        except:
            print(traceback.format_exc())
            print('Invalid input, try again')
    #setting the map size
    cont=False
    while cont==False:
        x_size=input('Input how many tiles wide you want this map to be\n')
        y_size=input('Input how many tiles tall you want this map to be\n')
        try:
            x_size=int(x_size)
            y_size=int(y_size)
            if x_size>0 and y_size>0:
                cont=True
            else:
                print('Map dimensions must be above 0 in each direction')
        except:
            print(traceback.format_exc())
            print('Invalid input, please try again')
    #setting deployment number
    cont=False
    while cont==False:
        spawn_count=input('Input how many player units you want allowed for this map\n')
        try:
            spawn_count=int(spawn_count)
            confirm=input(f'Are you sure you want {spawn_count} units? Input Y to confirm and anything else to cancel\n')
            if confirm.lower()=='y' and spawn_count<x_size*y_size and spawn_count>0:
                cont=True
        except:
            print(traceback.format_exc())
            print('Invalid input, try again')
    #setting spawns
    cont=False
    spawns=[]
    while len(spawns)<spawn_count:
        print('Input the coordinates where you would like a unit to spawn on their map in x,y integer form, with 0,0 being the top left and 1,1 being down and to the right of that')
        print('Any x,y pair will work as long as its on the map, not just 0,0 or 1,1')
        if len(spawns)>0:
            print(f'The current spawn points are {spawns}')
        spawn=input('Enter the coordinates now\n')
        try:
            spawn=spawn.split(',')
            spawn[0]=int(spawn[0])
            spawn[1]=int(spawn[1])
            if spawn[0]<x_size and spawn[1]<y_size and spawn[0]>=0 and spawn[1]>=0:
                confirm=input(f'Input Y to confirm adding a spawn at {spawn} or anything else to cancel\n')
                if confirm.lower()=='y' and spawn not in spawns:
                    spawns.append(spawn)
            else:
                print(f'Invalid input, your map dimensions are {x_size} wide by {y_size} tall')
        except:
            print(traceback.format_exc())
            print('Invalid input, try again')
    #creating the map
    mapCreated=mapLevel(name,y_size,x_size,map_num,spawns,[],[])
    #Adding objects to the map
    mapCreated.add_map_objects()
    print('Map Created!')


def create_unique_weapon():
    #(name,maxUses,dmg,dmgtype,rng,crit,hit,weapontype,droppable,cost,rank,super_effective):
    print('Welcome to the weapon creator')
    #Name
    cont=True
    while cont==True:
        name=input('Enter the name for this weapon\n')
        confirm=input(f'Input Y to confirm that you wish to name this weapon {name} or anything else to cancel\n')
        if confirm.lower()=='y':
            cont=False
    #Weapon type
    cont=True
    while cont==True:
        weptype=input('Input 1 to make this a sword, 2 a lance, 3 an axe, 4 a bow, 5 a tome, or 6 a gauntlet\n')
        if weptype=='1':
            weapontype='Sword'
            cont=False
        elif weptype=='2':
            weapontype='Lance'
            cont=False
        elif weptype=='3':
            weapontype='Axe'
            cont=False
        elif weptype=='4':
            weapontype='Bow'
            cont=False
        elif weptype=='5':
            weapontype='Tome'
            cont=False
        elif weptype=='6':
            weapontype='Fist'
            cont=False
        else:
            print('Invalid input, try again')
    #Damage type
    cont=True
    while cont==True:
        damagetype=input('Input P to make this a physical weapon or M to make it a magical weapon\n')
        if damagetype.lower()=='p':
            dmgtype='Phys'
            cont=False
        elif damagetype.lower()=='m':
            dmgtype='Magic'
            cont=False
        else:
            print('Invalid input, try again')
    #range
    cont=False
    while cont==False:
        rng=[]
        print('Input the ranges that you want this weapon to be able to attack from seperated by commas.')
        print('For example if you wanted this weapon to be able to attack enemies 1,2, or 3 tiles away you would enter 1,2,3')
        ranges=input('Input the range now\n')
        try:
            ranges=ranges.split(',')
            er=False
            for i in range(0,len(ranges)):
                ranges[i]=int(ranges[i])
                if i<=0:
                    er=True
            if er!=True:
                rng=ranges
                cont=True
            else:
                print('Invalid input, ranges must be 1 or above')
        except:
            print(traceback.format_exc())
            print('Invalid input, try again')
    #stats
    #(maxUses,dmg,crit,hit,droppable,cost,rank,super_effective):
    print('In this step you will set the stats for this weapon. Each stat must be a positive integer')
    cont=False
    while cont==False:
        try:
            maxUses=input('Weapon Uses\n')
            maxUses=int(maxUses)
            if maxUses>0:
                cont=True
        except:
            print(traceback.format_exc())
            print('Invalid input, try again')
    cont=False
    while cont==False:
        try:
            dmg=input('Damage\n')
            dmg=int(dmg)
            if dmg>=0:
                cont=True
        except:
            print(traceback.format_exc())
            print('Invalid input, try again')
    cont=False
    while cont==False:
        try:
            hit=input('Hit Rate (between 0 and 200, higher numbers are more accurate)\n')
            hit=int(hit)
            if hit>=0:
                cont=True
        except:
            print(traceback.format_exc())
            print('Invalid input, try again')
    cont=False
    while cont==False:
        try:
            crit=input('Crit Rate\n')
            crit=int(crit)
            if crit>=0:
                cont=True
        except:
            print(traceback.format_exc())
            print('Invalid input, try again')
    cont=False
    while cont==False:
        try:
            cost=input('Shop Cost\n')
            cost=int(cost)
            if cost>=0:
                cont=True
        except:
            print(traceback.format_exc())
            print('Invalid input, try again')
    cont=False
    while cont==False:
        try:
            rank=input('Weapon Rank (what a characters weapon level has to be to use this)\n')
            rank=int(rank)
            if rank>=0:
                cont=True
        except:
            print(traceback.format_exc())
            print('Invalid input, try again')
    #Droppable
    cont=False
    while cont==False:
        dropY=input('Input y to make this weapon drop on death or x to no\n')
        if dropY.lower()=='y':
            droppable=True
            cont=True
        elif dropY.lower()=='x':
            droppable=False
            cont=True
        else:
            print('Invalid input, try again')
    #super_effective
    cont=False
    super_effective={}
    print('In this step you will choose the classes you want this weapon to be super effective against\n')
    print('If the class you want it to be super effective against hasnt been made yet thats fine, just enter the name now and create that class later')
    print('As long as a class with the input name is made at some point it will work')
    print('You can add multiple classes to be super effective against as long as its done one at a time')
    print('If you dont want this weapon to be super effective against any unit types just immediately input X to finish')
    while cont==False:
        print(f'Current classes this weapon is super effective against: {super_effective}')
        for i in range(0,len(classType.class_list)):
            print(f'{i}: {classType.class_list[i].name}')
        super_effective_route=input('Input the number/name of the class or X to finish\n')
        if super_effective_route.lower()=='x':
            cont=True
        elif super_effective_route.isdigit():
            if int(super_effective_route)>=0 and int(super_effective_route)<len(classType.class_list):
                if classType.class_list[int(super_effective_route)].name not in super_effective:
                    multiplier=input(f'Input the integer damage multiplier for this weapon against {classType.class_list[int(super_effective_route)].name}s or x to cancel\n')
                    if multiplier.isdigit():
                        super_effective[classType.class_list[int(super_effective_route)].name]=int(multiplier)
                    elif multiplier.lower()=='x':
                        pass
                    else:
                        print('The multiplier must be an integer')
                else:
                    print('This weapon is already super effective against that enemy type')
            else:
                print('Class type names cant be numbers!')
        else:
            confirm=(f'Input y to confirm that you want this weapon to be super effective against {super_effective_route}s or anything else to cancel\n')
            if confirm.lower()=='y':
                if super_effective_route not in super_effective:
                    multiplier=input(f'Input the damage multiplier for this weapon against {super_effective_route}s or x to cancel\n')
                    if isfloat(multiplier):
                        super_effective[super_effective_route]=float(multiplier)
                    elif multiplier.lower()=='x':
                        pass
                    else:
                        print('The multiplier must be a number')
                else:
                    print('This weapon is already super effective against that enemy type')
    global unique_weapons
    unique_weapons.append(weapon(name,maxUses,dmg,dmgtype,rng,crit,hit,weapontype,droppable,cost,rank,super_effective))
    print(f'{name} has been created. You can put it in an inventory, chest, or shop via the character/map editors')

def create_skill():
    #Skills (name,trigger_chance,trigger_stat,effect_stat,effect_change,effect_operator,effect_temp,effect_target,*relative_stat):
    print('Welcome to the skill creator')
    #Name
    cont=False
    while cont==False:
        name=input('Enter the name for this skill\n')
        confirm=input(f'Input y to confirm that you want this skill to be called {name} or anything else to cancel\n')
        if confirm.lower()=='y':
            cont=True
    #effect target
    cont=False
    while cont==False:
        print('Here you will set the target for this skill')
        print('For example Sol restores the triggering units HP, so that would affect the triggering unit\nLuna halves the enemies defense, so that would affect the enemy unit\nArmsthrift prevents a weapons durability from being used up, so that would affect the triggering units weapon')
        effect_target=input('Input 1 to make this skill affect the triggering unit, 2 to make it affect the enemy unit, or 3 to make it affect the triggering units weapon\n')
        if effect_target=='1':
            effect_target='self'
            cont=True
        elif effect_target=='2':
            effect_target='enemy'
            cont=True
        elif effect_target=='3':
            effect_target='weapon'
            cont=True
        else:
            print('Invalid input, try again')
    #Trigger stat
    cont=False
    while cont==False:
        print('Here you will set what stat you want this skill to trigger based off of')
        for i in character.bases:
            print(i)
        trigger_stat=input('Input the stat name that you want this skill to trigger based off of\n')
        if trigger_stat in character.bases:
            cont=True
        else:
            print('Invalid input, try again')
    #Trigger chance
    cont=False
    while cont==False:
        print(f'Here you will choose the multiplier that will be applied to the characters {trigger_stat} when determining whether this skill triggers')
        print(f'This is out of 100. For example if this trigger chance is set to 10 and the characters {trigger_stat} is 6 there would be a 60% chance of this skill triggering during any given round of combat')
        trigger_chance=input('Input the trigger chance now\n')
        if isfloat(trigger_chance):
            if float(trigger_chance)>0:
                trigger_chance=float(trigger_chance)
                cont=True
            else:
                print('This must be a positive number')
        else:
            print('This must be a number')
    #effect stat
    cont=False
    while cont==False:
        print('Here you will set the stat that this skill will affect and change')
        if effect_target!='weapon':
            for i in character.bases:
                print(i)
            effect_stat=input('Input the stat that you want this skill to affect\n')
            if effect_stat in character.bases:
                cont=True
            else:
                print('Invalid input, try again')
        else:
            effect_stat=input('Input 1 to make this affect the weapons attack strength or 2 to make it affect the durability\n')
            if effect_stat=='1':
                effect_stat='dmg'
                cont=True
            elif effect_stat=='2':
                effect_stat='curUses'
                cont=True
            else:
                print('Invalid input, try again')
    #Effect operator
    cont=False
    while cont==False:
        print('Here you will set how this skill will affect the {effect_target} {effect_stat}')
        print('The possible options are * if you want this to multiply the {effect_stat}, / if you want it to divide, + if you want it to add, or - if you want it to subtract')
        effect_operator=input('Input the operator you want now\n')
        if effect_operator=='*' or effect_operator=='+' or effect_operator=='-' or effect_operator=='/':
            cont=True
        else:
            print('Invalid input, try again')
    #Effect change
    cont=False
    print('Here you will set by how much this skill will affect the target stat\nFor example if you set the effect operator to *, the effect stat to atk, and the effect change to 5, whenever this skill triggers it would multiply atk by 5')
    while cont==False:
        effect_change=input('Input the effect change now\n')
        if isfloat(effect_change):
            if float(effect_change)>0:
                effect_change=float(effect_change)
                cont=True
            else:
                print('The effect change must be an integer or floating point number above 0')
        else:
            print('The effect change must be an integer or floating point number above 0')
    #effect temp
    cont=False
    print('Skill effects can be temperary or permanent.\nFor example when armsthrift activates the durability not being taken away is permanent, but with Luna the enemys defense being halved goes away after the battle')
    while cont==False:
        temp=input('Input 1 to make the effects of this skill temporary or 2 to make them permament\n')
        if temp=='1':
            effect_temp=True
            cont=True
        elif temp=='2':
            effect_temp=False
            cont=True
        else:
            print('Invalid input, try again')
    #relative stat
    cont=False
    print('Some skills bring in other stats for their calculations other than just the stat that is being affected, like how Ignis adds half of the users magic stat to their strength\nHere you can choose whether or not you want a relative stat, and if so what')
    relative_stat=False
    while cont==False:
        contX=input('Input 1 to add a relative stat or anything else to move on\n')
        if contX=='1':
            for i in character.bases:
                print(i)
            relative_stat=input('Input the stat that you want the effect change to be relative to\n')
            if relative_stat in character.bases:
                cont=True
            else:
                print('Invalid input, try again')
                relative_stat=False
        else:
            cont=False
    #Skills (name,trigger_chance,trigger_stat,effect_stat,effect_change,effect_operator,effect_temp,effect_target,*relative_stat):
    if relative_stat:
        skill(name,trigger_chance,trigger_stat,effect_stat,effect_change,effect_operator,effect_temp,effect_target,relative_stat)
    else:
        skill(name,trigger_chance,trigger_stat,effect_stat,effect_change,effect_operator,effect_temp,effect_target)
    print('Skill created!')


def create_weapon_art():
    #Weapon Arts (name,weapontype,cost,damage,accuracy,crit,avoid,super_effective,rng,damageType(can be 'Same','Magic','Phys'),*[effect_stat,effect_change,effect_operator,target]):
    print('Welcome to the weapon art creator')
    #Name
    cont=False
    while cont==False:
        name=input('Enter the name for this weapon art\n')
        confirm=input(f'Input y to confirm that you want this weapon art to be called {name} or anything else to cancel\n')
        if confirm.lower()=='y':
            cont=True
    #weapontype
    cont=False
    print('In this step you will set what weapon type can use this weapon art')
    while cont==False:
        weapontype=input('Input 1 to make this usable by swords, 2 for lances, 3 axes, 4 bows, 5 tomes, or 6 for fists\n')
        if weapontype=='1':
            weapontype='Sword'
            cont=True
        elif weapontype=='2':
            weapontype='Lance'
            cont=True
        elif weapontype=='3':
            weapontype='Axe'
            cont=True
        elif weapontype=='4':
            weapontype='Bow'
            cont=True
        elif weapontype=='5':
            weapontype='Tome'
            cont=True
        elif weapontype=='6':
            weapontype='Fist'
            cont=True
        else:
            print('Invalid input, try again')
    #cost,accuracy,might,avoid, range,crit
    cont=False
    while cont==False:
        cost=input('Input how much durability you want this weapon art to use, a whole number equal or greater than zero\n')
        if cost.isdigit():
            if int(cost)>=0:
                cost=int(cost)
                cont=True
            else:
                print('Invalid input, cost must be 0 or more')
        else:
            print('Invalid input, cost must be a whole number')
    cont=False
    while cont==False:
        accuracy=input('Input the accuracy bonus you wish this art to give, between -100 and 100\n')
        if accuracy.isdigit():
            if int(accuracy)>=-100 and int(accuracy)<=100:
                accuracy=int(accuracy)
                cont=True
            else:
                print('The number must be between -100 and 100')
        else:
            print('Invalid input, the accuracy bonus must be a number between -100 and 100')

    cont=False
    while cont==False:
        might=input('Input the might bonus that you want this art to give, between -20 and 20\n')
        if might.isdigit():
            if int(might)>=-20 and int(might)<=20:
                might=int(might)
                cont=True
            else:
                print('Invalid input, the bonus must be between -20 and 20')
        else:
            print('Invalid input, the might bonus must be a whole number between -20 and 20')
    cont=False
    while cont==False:
        avoid=input('Input the avoid bonus that you would like this art to give, between -100 and 100\n')
        if avoid.isdigit():
            if int(avoid)>=-100 and int(avoid)<=100:
                avoid=int(avoid)
                cont=True
            else:
                print('Invalid input, dte avoid bonus must be between -100 and 100')
        else:
            print('Invalid input, the avoid bonus must be a whole number between -100 and 100')
    cont=False
    while cont==False:
        crit=input('Input the crit bonus that you want this art to give, between -100 and 100\n')
        if crit.isdigit():
            if int(crit)>=-100 and int(crit)<=100:
                crit=int(crit)
                cont=True
            else:
                print('Invalid input, the number must be between -100 and 100')
        else:
            print('Invalid input, the crit bonus must be a whole number between -100 and 100')
    cont=False
    while cont==False:
        ranges=input('Input the ranges you wish this weapon art to be usable from seperated by a comma\n')
        ranges=ranges.split(',')
        ranges=ranges.replace(' ','')
        cont2=True
        for i in range(0,len(ranges)):
            if not ranges[i].isdigit():
                cont2=False
            else:
                ranges[i]=int(ranges[i])
        if cont2:
            confirm=input(f'Input y to confirm that you wish the usable ranges for this art to be {ranges} or anything else to cancel\n')
            if confirm.lower()=='y':
                cont=True
        else:
            print('Invalid input. Enter the list of ranges that you want this weapon art to be usable at.')
            print('For example, if you wanted this art to be usable on enemies 1 space away, 3 spaces away, and 4 spaces away, you would input 1,3,4')
    #damage type (can be 'Same','Magic','Phys')
    cont=False
    while cont==False:
        damageType=input('Input 1 to make this use the same damage type (magical/physical) as the weapon it is being used with, 2 to make it always physical, or 3 to make it always magical\n')
        if damageType=='1':
            damageType='Same'
            cont=True
        elif damageType=='2':
            damageType='Phys'
            cont=True
        elif damageType=='3':
            damageType='Magic'
            cont=True
        else:
            print('Invalid input, try again')
    #super_effective
    cont=False
    super_effective=[]
    print('In this step you will choose the classes you want this art to be super effective against\n')
    print('If the class you want it to be super effective against hasnt been made yet thats fine, just enter the name now and create that class later')
    print('As long as a class with the input name is made at some point it will work')
    print('You can add multiple classes to be super effective against as long as its done one at a time')
    print('If you dont want this art to be super effective against any unit types just immediately input X to finish')
    while cont==False:
        print(f'Current classes this art is super effective against: {super_effective}')
        for i in range(0,len(classType.class_list)):
            print(f'{i}: {classType.class_list[i].name}')
        super_effective_route=input('Input the number/name of the class or X to finish\n')
        if super_effective_route.lower()=='x':
            cont=True
        elif super_effective_route.isdigit():
            if int(super_effective_route)>=0 and int(super_effective_route)<len(classType.class_list):
                if classType.class_list[int(super_effective_route)].name not in super_effective:
                    super_effective.append(classType.class_list[int(super_effective_route)].name)
                else:
                    print('This art is already super effective against that enemy type')
            else:
                print('Class type names cant be numbers!')
        else:
            confirm=(f'Input y to confirm that you want this art to be super effective against {super_effective_route}s or anything else to cancel\n')
            if confirm.lower()=='y':
                if super_effective_route not in super_effective:
                    super_effective.append(super_effective_route)
                else:
                    print('This weapon is already super effective against that enemy type')
    contX=input('Input Y to add an additional stat change to this weapon or anything else to finish the art creation\n')
    if contX.lower()=='y':
        #effect target
        cont=False
        while cont==False:
            print('Here you will set the target for this weapon art')
            print('For example Sol restores the triggering units HP, so that would affect the triggering unit\nLuna halves the enemies defense, so that would affect the enemy unit\nArmsthrift prevents a weapons durability from being used up, so that would affect the triggering units weapon')
            effect_target=input('Input 1 to make this weapon art affect the triggering unit, 2 to make it affect the enemy unit, or 3 to make it affect the weapon\n')
            if effect_target=='1':
                effect_target='self'
                cont=True
            elif effect_target=='2':
                effect_target='enemy'
                cont=True
            elif effect_target=='3':
                effect_target='weapon'
                cont=True
            else:
                print('Invalid input, try again')
        #effect stat
        cont=False
        while cont==False:
            print('Here you will set the stat that this weapon art will affect and change')
            if effect_target!='weapon':
                for i in character.bases:
                    print(i)
                effect_stat=input('Input the stat that you want this weapon art to affect\n')
                if effect_stat in character.bases:
                    cont=True
                else:
                    print('Invalid input, try again')
            else:
                effect_stat=input('Input 1 to make this affect the weapons attack strength, 2 to make it affect the durability\n')
                if effect_stat=='1':
                    effect_stat='dmg'
                    cont=True
                elif effect_stat=='2':
                    effect_stat='curUses'
                    cont=True
                else:
                    print('Invalid input, try again')
        #Effect operator
        cont=False
        while cont==False:
            print('Here you will set how this weapon art will affect the {effect_target} {effect_stat}')
            print('The possible options are * if you want this to multiply the {effect_stat}, / if you want it to divide, + if you want it to add, or - if you want it to subtract')
            effect_operator=input('Input the operator you want now\n')
            if effect_operator=='*' or effect_operator=='+' or effect_operator=='-' or effect_operator=='/':
                cont=True
            else:
                print('Invalid input, try again')
        #Effect change
        cont=False
        print('Here you will set by how much this skill will affect the target stat\nFor example if you set the effect operator to *, the effect stat to atk, and the effect change to 5, whenever this skill triggers it would multiply atk by 5')
        while cont==False:
            effect_change=input('Input the effect change now\n')
            if isfloat(effect_change):
                if float(effect_change)>0:
                    effect_change=float(effect_change)
                    cont=True
                else:
                    print('The effect change must be an integer or floating point number above 0')
            else:
                print('The effect change must be an integer or floating point number above 0')
        #target
        weapon_art(name,weapontype,cost,might,accuracy,crit,avoid,super_effective,ranges,damageType,[effect_target,effect_stat,effect_operator,effect_change])
    else:
        weapon_art(name,weapontype,cost,might,accuracy,crit,avoid,super_effective,ranges,damageType)
    print('Weapon Art created!')

def create_class(*name):
    #Classes (advanced classes on top) (name,moveType,hp,hpG,atk,atkG,mag,magG,skill,skillG,luck,luckG,defense,defG,res,resG,spd,spdG,moveRange,weaponType,promotions,skill_list)
    print('Welcome to the class creator')
    #Name
    cont=False
    if name:
        name=name[0]
        cont=True
    while cont==False:
        name=input('Enter the name for this class\n')
        confirm=input(f'Input y to confirm that you want this class to be called {name} or anything else to cancel\n')
        if confirm.lower()=='y':
            cont2=True
            for i in classType.class_list:
                if name==i.name:
                    cont2=False
            if cont2:
                cont=True
            else:
                print('There is already a class with this name, choose a different one')
    #move type
    cont=False
    print('Here you will set the move type for this class. Move range and move type are completely seperate, all move type effects is the movement cost for certain tile types')
    while cont==False:
        print('0: Foot, the default move type. No strengths or weaknesses')
        print('1: Flying, nearly every tile type only costs one move')
        print('2: Horse, generally poor at moving through many tile types')
        print('3: Mage, foot but good at moving through deserts')
        print('4: Pirate, foot but good at moving through water')
        route=input('Enter the number of the movement type you want\n')
        if route=='0':
            moveType='Foot'
            cont=True
        elif route=='1':
            moveType='Flying'
            cont=True
        elif route=='2':
            moveType='Horse'
            cont=True
        elif route=='3':
            moveType='Mage'
            cont=True
        elif route=='4':
            moveType='Pirate'
            cont=True
        else:
            print('Invalid input, try again')
    cont=False
    while cont==False:
        moveRange=input('Input the move range for this class\n')
        if moveRange.isdigit():
            if int(moveRange)>0:
                moveRange=int(moveRange)
                cont=True
            else:
                print('Move range must be greater than 0')
        else:
            print('Invalid input, try again')
    #Bases and growths
    bases={}
    growths={}
    for i in character.stats:
        cont=False
        while cont==False:
            stat=input(f'Input what you want the starting level 1 {i} stat for this class to be\n')
            if stat.isdigit():
                if int(stat)<0 or (i=='hp' and int(stat)<1) :
                  print('This must be a number, and is the default level 1 stat for this class. It must be a positive number, and above 0 for hp')
                else:
                    bases[i]=int(stat)
                    print(f'{i} set')
                    cont=True
            else:
                print('This must be a number, and is the default level 1 stat for this class. It must be a positive number, and above 0 for hp')
    for i in character.growths:
        print('Growths are the likelihood of a character gaining a stat on levelup, and are generally decimals between 0 and 1')
        print('For example a .65 hp growth would make it so that there is a 65 percent chance for a character to gain 1 hp point when leveling up')
        cont=False
        while cont==False:
            stat=input(f'Input what you want the {i} growth for this class to be\n')
            if isfloat(stat):
                growths[i]=float(stat)
                print(f'{i} set')
                cont=True
            else:
                print('Invalid input, try again')
    #Weapon type
    print('In this step we will set the usable weapon types and their weapon level for this class')
    print('Weapon level determines what weapons a character is able to use, as they cant use weapons whose level are higher than their weapon level for that type of weapon')
    print('Weapon levels range from 0 to 100')
    weaponType={}
    cont=False
    def set_wep_level(wepType):
        cont=False
        if wepType not in weaponType:
            cont=True
        else:
            confirm=input(f'There is already a weapon level set for {wepType}, input Y to confirm that you want to overwrite it or anything else to cancel\n')
            if confirm.lower()=='y':
                cont=True
            else:
                print('Addition canceled')
        while cont==True:
            st=input(f'Input the weapon level you want for {wepType} or X to cancel\n')
            if st.lower()=='x':
                print('Addition canceled')
                cont=False
            elif st.isdigit():
                if int(st)>=0:
                    confirm=input(f'Input y to confirm that you want {wepType} weapon level to be {st} for this class or anything else to cancel\n')
                    if confirm.lower()=='y':
                        weaponType[wepType]=int(st)
                        cont=False
                        print('Weapon level set')
                    else:
                        print('Addition canceled')
                else:
                    print('Weapon levels must be 0 or above')
    while cont==False:
        if len(weaponType)>0:
            print('The current weapon levels for this class are:')
            for i in weaponType:
                print(f'{i} {weaponType[i]}')
        wep=input('Input 1 to let this class use swords, 2 for lances, 3 for axes, 4 for bows, 5 for tomes, 6 for fists, or x to finish\n')
        if wep.lower()=='x':
            print('The current weapon levels for this class are:')
            for i in weaponType:
                print(f'{i} {weaponType[i]}')
            confirm=input('Input Y to confirm that you are done adding usable weapons for this class\n')
            if confirm.lower()=='y':
                cont=True
        elif wep=='1':
            set_wep_level('Sword')
        elif wep=='2':
            set_wep_level('Lance')
        elif wep=='3':
            set_wep_level('Axe')
        elif wep=='4':
            set_wep_level('Bow')
        elif wep=='5':
            set_wep_level('Tome')
        elif wep=='6':
            set_wep_level('Fist')
        else:
            print('Invalid input, try again')
    #promotions
    promotions=[]
    cont=False
    while cont==False:
        if len(promotions)>0:
            print('Current promotions for this class:')
            print(promotions)
        print('Possible promotions:')
        possible_promotions=[]
        for i in classType.class_list:
            if i.name not in promotions:
                print(i.name)
                possible_promotions.append(i.name)
        print('Here you will enter the names of the classes you want this to promote into')
        print('Its ok if the class you want to promote to isnt listed, just input it exactly as it will be named')
        promo=input('Enter the class name or x to finish adding classes to promote to\n')
        if promo.lower()=='x':
            print(f'Promotions:{promotions}')
            confirm=input('Input y to confirm that you are done adding classes or anything else to cancel\n')
            if confirm.lower()=='y':
                cont=True
        else:
            if promo not in promotions:
                if promo not in possible_promotions:
                    confirm=input(f'{promo} is not a currently existing class, input Y to confirm that you are sure that this class will be added or anything else to cancel\n')
                else:
                    confirm=input(f'Input Y to confirm that you wish to add {promo} as a class to promote to or anything else to cancel\n')
                if confirm.lower()=='y':
                    promotions.append(promo)
            else:
                print('This class can already promote into {promo}')
    #skill_list
    skill_list=[]
    cont=False
    count=0
    print('Each class has 3 skills: a skill that is unlocked at level 1, a skill that is unlocked at level 10, and a skill that is unlocked at level 20')
    print('Here you will set the skills for this class')
    while cont==False:
        if count!=3:
            if len(skill_list)>0:
                print('Current Skills:')
                print(skill_list)
            print('Possible skills:')
            possible_skills=[]
            for i in range(0,len(skill.skill_list)):
                if skill.skill_list[i].name not in skill_list and skill.skill_list[i].name!='Placeholder':
                    print(f'{i}: {skill.skill_list[i].name}')
                    possible_skills.append(i)
            if count==0:
                skillX=input('Input the number of the skill that you want to be the level 1 skill of this class\n')
            elif count==1:
                skillX=input('Input the number of the skill that you want to be the level 10 skill of this class or X to just use placeholders for the remaining skills\n')
            elif count==2:
                skillX=input('Input the number of the skill that you want to be the level 20 skill of this class or X to just use placeholder\n')
            if skillX.lower()=='x':
                while len(skill_list)<3:
                    skill_list.append('Placeholder')
                count=3
            elif skillX.isdigit():
                if int(skillX) in possible_skills:
                    skill_list.append(skill.skill_list[int(skillX)])
                    print(f'{skill.skill_list[int(skillX)]} added')
            else:
                print('Invalid input, try again')
        else:
            cont=True
    while attributes!=fsadkjhfds:
        sddfkjsadlakfj
        #implement attribues here and in the definition
    #Classes (advanced classes on top) (name,moveType,hp,hpG,atk,atkG,mag,magG,skill,skillG,luck,luckG,defense,defG,res,resG,spd,spdG,moveRange,weaponType,promotions,skill_list)
    classType(name,moveType,bases['hp'],growths['hpG'],bases['atk'],growths['atkG'],bases['mag'],growths['magG'],bases['skill'],growths['skillG'],
              bases['luck'],growths['luckG'],bases['defense'],growths['defG'],bases['res'],growths['resG'],bases['spd'],growths['spdG'],moveRange,weaponType,promotions,skill_list)
    print('Class created!')

def write_support():
    print('Welcome to the support writer')
    cont=False
    while cont==False:
        character1=input('Enter the name of the first character for this support\n')
        character2=input('Enter the name of the second character for this support\n')
        confirm=input(f'Input Y to confirm that you want this support to be between {character1} and {character2} or anything else to cancel\n')
        if confirm.lower()=='y':
            cont=True
    cont=False
    while cont==False:
        num_levels=input('Enter how many support conversations you want there to be for this support chain\n')
        if num_levels.isdigit():
            confirm=input(f'Input y to confirm that you want {num_levels} support conversations or anything else to cancel\n')
            if confirm.lower()=='y':
                num_levels=int(num_levels)
                cont=True
    support_convos=[0]
    j=1
    while num_levels>0:
        convo=input(f'Write the conversation you would like to play at level {j}. Use \\n to insert a newline.\n')
        confirm=input(f'Input y to confirm that you want that to be support level {j}\n')
        if confirm.lower()=='y':
            j+=1
            support_convos.appens(convo)
            num_levels-=1
    player.support_master[character1,character2]=support_convos
    print('Support created!')


def edit_map():
    cont=True
    while cont==True:
        for i in range(0,len(mapLevel.map_list)):
            print(f'{i}: {mapLevel.map_list[i].name}')
        map_choice=input('Input the number for the map you would like to edit\n')
        if map_choice.isdigit():
            if int(map_choice)>=0 and int(map_choice)<len(mapLevel.map_list):
                mapX=mapLevel.map_list[int(map_choice)]
                cont=False
        else:
            print('Invalid input, try again')
    cont=True
    while cont==True:
        path=input('Input 1 to edit this maps objects, 2 to edit the map number, 3 to edit the player spawns, 4 to edit the size, 5 to edit the rosters, or x to finish\n')
        if path.lower()=='x':
            cont=False
        elif path=='1':
            #edit objects
            mapX.display('base')
            #add,delete, edit
            object_path=input('Input 1 to add objects, 2 to delete objects, 3 to edit the contents of chests/shops, or X to exit\n')
            if object_path=='1':
                mapX.add_map_objects()
            elif object_path=='2':
                mapX.delete_map_objects()
            elif object_path=='3':
                #edit shop/chest contents
                count=0
                for i in mapX.objectList:
                    if isinstance(mapX.objectList[i],treasure_chest) or isinstance(mapX.objectList[i],shop):
                        print(f'{i}: {mapX.objectList[i].name}')
                        count+=1
                if count>0:
                    route=input('Input the coordinates of the shop or chest whose contents you wish to edit in x,y form or x to cancel\n')
                    if route.lower()=='x':
                        pass
                    else:
                        route=route.split(',')
                        if len(route)==2:
                            if route[0].isdigit() and route[1].isdigit:
                                route[0]=int(route[0])
                                route[1]=int(route[1])
                                if (route[0],route[1]) in mapX.objectList:
                                    if isinstance(mapX.objectList[route[0],route[1]],shop) or isinstance(mapX.objectList[route[0],route[1]],treasure_chest):
                                        mapX.objectList[route[0],route[1]].edit_contents()
                        else:
                            print('Invalid input, try again')
                else:
                    print('There are no shops or chests on this map, returning to menu')
        elif path=='2':
            #edit mapnum
            new_num=input(f'Enter the new number that you want this map to be, its current number is {mapX.mapNum}\n')
            if new_num.isdigit():
                map_ordering(mapX.name,int(new_num),mapX)
            else:
                print('Invalid input, returning to menu')
        elif path=='3':
            #edit spawns
            path=input('Enter 1 to add spawns, 2 to remove spawns, or anything else to cancel\n')
            if path=='1':
                contZ=False
                mapX.display('base')
                while contZ==False:
                    print('Input the coordinates for the new spawn in x,y integer form, with 0,0 being the top left and 1,1 being down and to the right of that')
                    print('Any x,y pair will work as long as its on the map, not just 0,0 or 1,1')
                    spawn=input('Enter the coordinates now, or input X to finish\n')
                    if spawn.lower()=='x':
                        contZ=True
                    spawn=spawn.split(',')
                    if len(spawn)==2:
                        if spawn[0].isdigit() and spawn[1].isdigit():
                            spawn[0]=int(spawn[0])
                            spawn[1]=int(spawn[1])
                            spawn=(spawn[0],spawn[1])
                            contCont=True
                            if (spawn[0],spawn[1]) not in mapX.spawns and (spawn[0],spawn[1]) in mapX.spaces:
                                if (spawn[0],spawn[1]) in mapX.objectList:
                                    if mapX.objectList[spawn[0],spawn[1]].name=='Door':
                                        contCont=False
                                    elif mapX.objectList[spawn[0],spawn[1]].name=='Void':
                                        contCont=False
                                    elif mapX.objectList[spawn[0],spawn[1]].name=='Water':
                                        contCont=False
                                for i in mapX.enemy_roster:
                                    if spawn==i.spawn:
                                        contCont=False
                                if contCont==True:
                                    mapX.spawns.append((spawn[0],spawn[1]))
                                    print('Spawn added')
                                else:
                                    print('Invalid location, theres already something there')
                            elif (spawn[0],spawn[1]) in mapX.spawns:
                                print('There is already a spawn there, invalid input')
                            else:
                                print('Invalid spawn, try again')
            elif path=='2':
                cont=False
                while cont==False:
                    if len(mapX.spawns)==1:
                        print('There are no spawns left to remove, returning to menu')
                        cont=True
                    for i in range(0,len(mapX.spawns)):
                        print(f'{i}: {mapX.spawns[i]}')
                    spawn_to_remove=input('Input the number of the spawn you wish to delete or X to finish\n')
                    if spawn_to_remove.lower()=='x':
                        cont=True
                    elif spawn_to_remove.isdigit():
                        if int(spawn_to_remove)>=0 and int(spawn_to_remove)<len(mapX.spawns):
                            rem=mapX.spawns.pop(int(spawn_to_remove))
                            print(f'{rem} deleted')
                        else:
                            print('Invalid input, try again')
                    else:
                        print('Invalid input, try again')
            else:
                print('Returning to menu')
        elif path=='4':
            #edit size
            print(f'This map is currently {mapX.x_size} wide and {mapX.y_size} tall')
            new_size=input('Input the new map size in X,Y form or input X to cancel\n')
            if new_size.lower()=='x':
                pass
            else:
                new_size=new_size.split(',')
                if len(new_size)==2:
                    if new_size[0].isdigit() and new_size[1].isdigit():
                        new_size[0]=int(new_size[0])
                        new_size[1]=int(new_size[1])
                        missing_enemy=[]
                        missing_spawn=[]
                        missing_object=[]
                        for i in mapX.spaces:
                            if i[0]>new_size[0]-1 or i[1]>new_size[1]-1:
                                del mapX.spaces[i]
                        if new_size[0]>mapX.x_size:
                            for i in range(mapX.x_size,new_size[0]):
                                for j in range(0,mapX.y_size):
                                    mapX.spaces[i,j]=[False]
                        mapX.x_size=new_size[0]
                        if new_size[1]>mapX.y_size:
                            for j in range(mapX.y_size,new_size[1]):
                                for i in range(0,mapX.x_size):
                                    mapX.spaces[i,j]=[False]
                        mapX.y_size=new_size[1]
                        for j in mapX.enemy_roster:
                            if j.spawn not in mapX.spaces:
                                mapX.enemy_roster.remove(j)
                                missing_enemy.append(j)
                        for k in mapX.spawns:
                            if k not in mapX.spaces:
                                mapX.spaces.pop(k)
                                missing_spawn.append(k)
                        for l in mapX.objectList:
                            if l not in mapX.spaces:
                                missing_object.append(mapX.objectList[l])
                                del mapX.objectList[l]
                        contFix=True
                        while contFix==True:
                            if len(missing_enemy)==0 and len(missing_object)==0:
                                contFix=False
                            mapX.display('base')
                            print(f'There are {len(missing_enemy)} enemies that need to have their spawn changed, {len(missing_object)} objects that need to be moved, and {len(missing_spawn)} player spawns have been deleted')
                            while len(missing_enemy)>0:
                                #update spawm
                                length=len(missing_enemy)
                                for aqw in range(0,length):
                                    contZ=False
                                    mapX.display('base')
                                    while contZ==False:
                                        print(f'Input the coordinates where you would like {missing_enemy[0].name} to spawn on their map in x,y integer form, with 0,0 being the top left and 1,1 being down and to the right of that')
                                        print('Any x,y pair will work as long as its on the map, not just 0,0 or 1,1')
                                        spawn=input('Enter the coordinates now, or input X to delete this unit\n')
                                        if spawn.lower()=='x':
                                            missing_enemy.pop(0)
                                            contZ=True
                                        spawn=spawn.split(',')
                                        if len(spawn)==2:
                                            if spawn[0].isdigit() and spawn[1].isdigit():
                                                spawn[0]=int(spawn[0])
                                                spawn[1]=int(spawn[1])
                                                spawn=(spawn[0],spawn[1])
                                                contCont=True
                                                if (spawn[0],spawn[1]) not in mapX.spawns and (spawn[0],spawn[1]) in mapX.spaces:
                                                    if (spawn[0],spawn[1]) in mapX.objectList:
                                                        if mapX.objectList[spawn[0],spawn[1]].name=='Door':
                                                            contCont=False
                                                        elif mapX.objectList[spawn[0],spawn[1]].name=='Void' and missing_enemy[0].classType.moveType!='Flying':
                                                            contCont=False
                                                        elif mapX.objectList[spawn[0],spawn[1]].name=='Void' and (missing_enemy[0].classType.moveType!='Flying' and missing_enemy[0].classType.moveType!='Pirate'):
                                                            contCont=False
                                                    for i in mapX.enemy_roster:
                                                        if spawn==i.spawn:
                                                            contCont=False
                                                    if contCont==True:
                                                        missing_enemy[0].spawn=(spawn[0],spawn[1])
                                                        missing_enemy.pop(0)
                                                        contZ=True
                                                    else:
                                                        print('Invalid location, theres already something there')
                                                elif (spawn[0],spawn[1]) in mapX.spawns:
                                                    print('A player unit spawns there, invalid input')
                                                else:
                                                    print('Invalid spawn, try again')
                            while len(missing_object)>0:
                                length=len(missing_object)
                                for acq in range(0,length):
                                    contZ=False
                                    mapX.display('base')
                                    while contZ==False:
                                        print(f'Input the coordinates where you would like {missing_object[0].name} to be in x,y integer form, with 0,0 being the top left and 1,1 being down and to the right of that')
                                        print('Any x,y pair will work as long as its on the map, not just 0,0 or 1,1')
                                        spawn=input('Enter the coordinates now, or input X to delete this object\n')
                                        if spawn.lower()=='x':
                                            missing_object.pop(0)
                                            contZ=True
                                        spawn=spawn.split(',')
                                        if len(spawn)==2:
                                            if spawn[0].isdigit() and spawn[1].isdigit():
                                                spawn[0]=int(spawn[0])
                                                spawn[1]=int(spawn[1])
                                                contCont=True
                                                if (spawn[0],spawn[1]) in mapX.spaces:
                                                    if (spawn[0],spawn[1]) in mapX.objectList:
                                                        print('Theres already an object there, find somewhere else to put this')
                                                        contCont=False
                                                    if (spawn[0],spawn[1]) in mapX.spawns:
                                                        if missing_object[0].name=='Void' or missing_object[0].name=='Water' or missing_object[0].name=='Door':
                                                            print('Theres already a player unit spawn there, find somewhere else to put this')
                                                            contCont=False
                                                    for i in mapX.enemy_roster:
                                                        if i.spawn==(spawn[0],spawn[1]) and (missing_object[0].name=='Void' or missing_object[0].name=='Water' or missing_object[0].name=='Door'):
                                                            print('Theres already an enemy unit spawn there, find somewhere else to put this')
                                                            contCont=False
                                                    if contCont==True:
                                                        missing_object[0].location=[spawn[0],spawn[1]]
                                                        mapX.objectList[spawn[0],spawn[1]]=missing_enemy.pop(0)
                                                        contZ=True
                                                else:
                                                    print('Invalid location, try again')
                        print('Map resized')
        elif path=='5':
            #edit rosters
            path=input('Input 1 to remove units from this map, 2 to add units to this map, or x to cancel\n')
            if path.lower()=='x':
                pass
            elif path=='1':
                path2=input('Input 1 to remove player units or 2 to remove enemies\n')
                if path2=='1':
                    for i in range(0,len(mapX.player_roster)):
                        print(f'{i}: {mapX.player_roster[i].name}')
                    route=input('Input the number of the unit that you wish to remove from this maps roster\n')
                    if route.isdigit():
                        if int(route)>=0 and int(route)<len(mapX.player_roster):
                            confirm=input(f'Input Y to confirm that you wish to remove {mapX.player_roster[int(route)].name} from this roster\n')
                            if confirm.lower()=='y':
                                moveXY=input('Input Y to move this character to another map or X to delete this character')
                                if moveXY.lower()=='y':
                                    pass
                                elif moveXY.lower()=='x':
                                    deleted_char=mapX.player_roster.pop(int(route))
                                    character.character_list.remove(deleted_char)
                                    print('Character deleted')
                elif path2=='2':
                    for i in range(0,len(mapX.enemy_roster)):
                        print(f'{i}: {mapX.enemy_roster[i].name}')
                    remove_enemy=input('Input the number of the enemy you wish to remove or x to cancel\n')
                    if remove_enemy.lower()=='x':
                        pass
                    elif remove_enemy.isdigit():
                        if int(remove_enemy)>=0 and int(remove_enemy)<len(mapX.enemy_roster):
                            confirm=input(f'Input Y to confirm that you wish to remove {mapX.enemy_roster[int(remove_enemy)].name} from this maps roster or anything else to cancel\n')
                            if confirm.lower()=='y':
                                removed=mapX.enemy_roster.pop(int(remove_enemy))
                                contX=False
                                while contX==False:
                                    delete=input('Input Y to move this enemy to another map or X to delete this enemy\n')
                                    if delete.lower()=='x':
                                        character.character_list.remove(removed)
                                        print('Character deleted')
                                        contX=True
                                    elif delete.lower()=='y':
                                        acceptable_inputs={}
                                        for i in mapLevel.map_list:
                                            print(f'{i.name}: map number {i.mapNum}')
                                            acceptable_inputs[i.mapNum]=i
                                        new_map=input('Enter the map number that you want to move this character to or X to cancel\n')
                                        if new_map.lower()=='x':
                                            pass
                                        elif new_map.isdigit():
                                            if int(new_map) in acceptable_inputs:
                                                contZ=False
                                                acceptable_inputs[int(new_map)].display('base')
                                                while contZ==False:
                                                    print(f'Input the coordinates where you would like {removed.name} to be in x,y integer form, with 0,0 being the top left and 1,1 being down and to the right of that')
                                                    print('Any x,y pair will work as long as its on the map, not just 0,0 or 1,1')
                                                    spawn=input('Enter the coordinates now, or input X to cancel\n')
                                                    if spawn.lower()=='x':
                                                        contZ=True
                                                    spawn=spawn.split(',')
                                                    if len(spawn)==2:
                                                        if spawn[0].isdigit() and spawn[1].isdigit():
                                                            spawn[0]=int(spawn[0])
                                                            spawn[1]=int(spawn[1])
                                                            contCont=True
                                                            if (spawn[0],spawn[1]) in acceptable_inputs[int(new_map)].spaces:
                                                                if (spawn[0],spawn[1]) in acceptable_inputs[int(new_map)].objectList:
                                                                    print('Theres already an object there, find somewhere else to put this')
                                                                    contCont=False
                                                                if (spawn[0],spawn[1]) in acceptable_inputs[int(new_map)].spawns:
                                                                    print('Theres already a player unit spawn there, find somewhere else to put this')
                                                                    contCont=False
                                                                for i in acceptable_inputs[int(new_map)].enemy_roster:
                                                                    if i.spawn==(spawn[0],spawn[1]):
                                                                        print('Theres already an enemy unit spawning there, find somewhere else to put this')
                                                                        contCont=False
                                                                if contCont==True:
                                                                    removed.spawn=(spawn[0],spawn[1])
                                                                    acceptable_inputs[int(new_map)].enemy_roster.append(removed)
                                                                    contZ=True
                                                            else:
                                                                print('Invalid location, try again')
                                            else:
                                                print('Invalid input, try again')
                                    else:
                                        print('Invalid input, try again')
                            else:
                                print('Removal canceled')
                        else:
                            print('Invalid input, try again')
                    else:
                        print('Invalid input, try again')
                else:
                    pass
            elif path=='2':
                new_old=input('Input 1 to create a new unit or 2 to move an existing unit to this map\n')
                if new_old=='1':
                    create_character()
                elif new_old=='2':
                    eligible_maps={}
                    for i in mapLevel.map_list:
                        print(f'{i.name} map number {i.mapNum}')
                    mapU=input('Enter the map number that you want to take the units from\n')
                    if mapU.isdigit():
                        if int(mapU) in eligible_maps:
                            alig=input('Input 1 to add player units, 2 to add enemy units, or x to cancel\n')
                            if alig=='1':
                                for k in range(0,len(eligible_maps[int(mapU)].player_roster)):
                                    print(f'{k}: {eligible_maps[int(mapU)].player_roster[k].name}')
                                char_add=input('Input the number of the character that you would like to this map')
                                if char_add.isdigit():
                                    if int(char_add)>=0 and int(char_add)<len(eligible_maps[int(mapU)].player_roster):
                                        confirm=input(f'Input Y to confirm that you wish to move {eligible_maps[int(mapU)].player_roster[int(char_add)].name} from map {mapU} to map {mapX.mapNum}\n')
                                        if confirm.lower()=='y':
                                            addition=eligible_maps[int(mapU)].player_roster.pop(int(char_add))
                                            mapX.player_roster.append(addition)
                                            print('Character added!')
                                        else:
                                            print('Movement canceled')
                                    else:
                                        print('Invalid input, try again')
                                else:
                                    print('Invalid input, try again')
                            elif alig=='2':
                                pass
                        else:
                            print('Thats not an option, returning to menu')
                    else:
                        print('Invalid input, returning to menu')
            else:
                pass
        else:
            print('Invalid input')

def edit_char():
    cont=False
    while cont==False:
        for i in range(0,len(character.character_list)):
            print(f'{i}: {character.character_list[i].name}')
        char_choice=input('Input the number for the character you would like to edit\n')
        if char_choice.isdigit():
            if int(char_choice)>=0 and int(char_choice)<len(character.character_list):
                char=character.character_list[int(char_choice)]
                cont=True
        else:
            print('Invalid input, try again')
    cont=True
    while cont==True:
        path=input('Input 1 to edit this characters stats and growths, 2 to edit their join map, 3 to edit their level/experience, 4 to edit their class, 5 to edit their skills, 6 to edit their inventory, or x to finish\n')
        if path=='1':
            #stats and growths
            cont=True
            while cont==True:
                print('The stats you can change are as follows:')
                for i in character.stats:
                    print(i)
                print('The G stats are growths, and movModifer is how many extra spaces a character can move compared to a default member of their class')
                print('Growths are decimals, and represent the change that a character gains that stat when leveling up')
                print('For example a .6 hpG would mean that a character has a 60% chance of gaining 1 hp on level up and a 40% chance of gaining 0')
                stat_change=input("Input the abreviation for the stat you'd like to change or x to finish\n")
                if stat_change in character.stats or stat_change in character.growths:
                    print(f"The current value for {char.name}'s {stat_change} is {getattr(char,eval(stat_change))}")
                    new_value=input(f"Input the new value you want {stat_change} to be\n")
                    if isfloat(new_value):
                        if stat_change in character.stats:
                            if stat_change!='hp' and stat_change!='movModifier':
                                if int(new_value)>=0:
                                    confirm=input(f"Input Y to confirm that you want to change {stat_change} to {new_value} or anything else to cancel\n")
                                    if confirm.lower()=='y':
                                        setattr(char,stat_change,int(new_value))
                                else:
                                    print('Stats must be positive integers')
                            elif stat_change=='hp':
                                if int(new_value)>0:
                                    confirm=input(f"Input Y to confirm that you want to change {stat_change} to {new_value} or anything else to cancel\n")
                                    if confirm.lower()=='y':
                                        setattr(char,stat_change,int(new_value))
                                else:
                                    print('Stats must be positive integers')
                            elif stat_change=='movModifier':
                                if int(new_value)>=-3:
                                    confirm=input(f"Input Y to confirm that you want to change {stat_change} to {new_value} or anything else to cancel\n")
                                    if confirm.lower()=='y':
                                        curMod=getattr(char,stat_change)
                                        setattr(char,stat_change,int(new_value))
                                        char.mov+=new_value-curMod
                                else:
                                    print('The minimum value for the move modifier is -3')
                        elif stat_change in character.growths:
                            if float(new_value)>=0:
                                confirm=input(f"Input Y to confirm that you want to change {stat_change} to {new_value} or anything else to cancel\n")
                                if confirm.lower()=='y':
                                    setattr(char,stat_change,float(new_value))
                            else:
                                print('WARNING: YOU HAVE INPUT A NEGATIVE VALUE AS A GROWTH')
                                print(f'THIS MEANS THAT THIS CHARACTER WILL NEVER GAIN A STAT IN THIS LEVEL, AND HAS A {float(new_value)*100}\% CHANCE OF LOSING A POINT IN THE STAT ON LEVEL UP')
                                confirm=input(f"IF YOU ARE ABSOLUTELY SURE THIS IS WHAT YOU WANT\nInput Y to confirm that you want to change {stat_change} to {new_value} or anything else to cancel\n")
                                if confirm.lower()=='y':
                                    setattr(char,stat_change,float(new_value))
                elif stat_change.lower()=='x':
                    cont=False
                else:
                    print('Invalid input, try again')
        elif path=='2':
            #join map
            existing_levels=[]
            for i in mapLevel.map_list:
                existing_levels.append(i.mapNum)
            existing_levels.sort()
            print(f"The existing levels are {existing_levels}")
            print(f"{char.name}'s current join map is {char.joinMap}")
            new_join=input(f'Input which number level do you want {char.name} to join on\n')
            if new_join.isdigit():
                if int(new_join) in existing_levels:
                    if char.alignment==player:
                        for i in mapLevel.map_list:
                            if i.mapNum==int(new_join):
                                i.player_roster.append(char)
                            elif i.mapNum==char.joinMap:
                                i.player_roster.remove(char)
                    else:
                        for i in mapLevel.map_list:
                            if i.mapNum==int(new_join):
                                i.enemy_roster.append(char)
                                cont2=True
                                while cont2==True:
                                    print(f"{char.name}'s spawn has to be edited for the new map")
                                    taken=[]
                                    for j in i.enemy_roster:
                                        if j!=char:
                                            taken.append(j.spawn)
                                    for k in i.spawns:
                                        taken.append(k)
                                    print(f"The current occupied spaces on this map are {taken}\nAnd the map looks like this")
                                    i.display('base')
                                    new_spawn=input('Input this characters new spawn point in x,y form seperated by a comma\n')
                                    new_spawn=new_spawn.split(',')
                                    if len(new_spawn)==2:
                                        if new_spawn[0].isdigit() and new_spawn[1].isdigit:
                                            new_spawn[0]=int(new_spawn[0])
                                            new_spawn[1]=int(new_spawn[1])
                                            if (new_spawn[0],new_spawn[1]) not in taken:
                                                char.spawn=(new_spawn[0],new_spawn[1])
                                                cont2=True
                                            else:
                                                print('That space is already taken, try again')
                                        else:
                                            print('The x,y form must consist of 2 integers')
                                    else:
                                        print('The x,y form must consist of 2 integers seperated by a comma')
                            elif i.mapNum==char.joinMap:
                                i.enemy_roster.remove(char)
                    char.joinMap=int(new_join)
                    print(f"{char.name}'s join map has been updated")
            else:
                print('Invalid input')
        elif path=='3':
            #level/exp
            print(f"Level: {char.level} Exp: {char.exp}")
            lev=input('Enter their new level\n')
            exp=input('Enter their new EXP\n')
            if lev.isdigit() and exp.isdigit():
                if int(lev)<=level_cap and int(lev)>=1 and int(exp)<needed_exp and int(exp)>=0:
                    if int(lev)>char.level:
                        gain_stats=input('Since you are raising this characters level, input Y to make them gain stats as if leveling up or anything else to keep their stats the same\n')
                        if gain_stats.lower()=='y':
                            while char.level<int(lev):
                                char.level_up(1)
                        else:
                            char.level=int(lev)
                    else:
                        char.level=int(lev)
                    char.exp=int(exp)
                    print(f"{char.name}'s level and exp have been updated")
                else:
                    print('Invalid input, returning to menu')
            else:
                print('Level and exp must be numbers!')
        elif path=='4':
            #class
            for i in range(0,len(classType.class_list)):
                print(f'{i}: {classType.class_list[i].name}')
            class_choice=input('Input the class number that you would like to reclass to\n')
            if class_choice.isdigit():
                if int(class_choice)>=0 and int(class_choice)<len(classType.class_list):
                    newClass=classType.class_list[int(class_choice)]
                    confirm=input(f'Input y to confirm that you wish to change {char.name} to {newClass.name} or anything else to cancel\n')
                    if confirm.lower()=='y':
                        stat_change=input(f"Input Y to update {char.name}'s stats based off of this new clas or anything else to keep them the same\n")
                        if stat_change.lower()=='y':
                            char.reclass(newClass)
                        else:
                            char.classType=newClass
                else:
                    print('That number isnt an option')
            else:
                print('You need to input the number of the class')
        elif path=='5':
            #skills
            skills_path=input('Input A to add a skill, D to drop a skill, or X to finish\n')
            if skills_path.lower()=='a':
                cont=False
                while cont==False:
                    viable=[]
                    for i in range(0,len(skill.skill_list)):
                        if skill.skill_list[i] not in char.skills_all:
                            print(f"{i}: {skill.skill_list[i].name}")
                            viable.append(i)
                    skill_add=input("Input the number of the skill you would like to add or x to finish\n")
                    if skill_add.lower()=='x':
                        cont=True
                    elif skill_add.isdigit():
                        if int(skill_add)>=0 and int(skill_add)<len(skill.skill_list):
                            if int(skill_add) in viable:
                                char.add_skill(skill.skill_list[i])
                                print(f'{skill.skill_list[i].name} added')
                            else:
                                print('Invalid input, try again')
                        else:
                            print('That number isnt an option')
                    else:
                        print('You need to input the number of the skill')
            elif skills_path.lower()=='d':
                cont=False
                while cont==False:
                    for i in range(0,len(char.skills_all)):
                        print(f'{i}: {char.skills_all[i].name}')
                    skill_drop=input('Input the number of the skill you would like to drop or X to finish\n')
                    if skill_drop.lower()=='x':
                        cont=True
                    elif skill_drop.isdigit():
                        if int(skill_drop)>=0 and int(skill_drop)<len(char.skills_all):
                            confirm=input(f'Input Y to confirm that you wish to drop {char.skills_all[int(skill_drop)].name} or anything else to cancel\n')
                            if confirm.lower()=='y':
                                dropped_skill=char.skills_all.pop(int(skill_drop))
                                if dropped_skill in char.skills:
                                    char.skills.pop(dropped_skill)
                                print(f'{dropped_skill.name} dropped')
                            else:
                                print('Drop canceled')
                        else:
                            print(f'This must be an integer between 0 and {len(char.skills_all)}')
                    else:
                        print(f'The input must either be X or an integer between 0 and {len(char.skills_all)}')
        elif path=='6':
            #inventory
            inventory_path=input(f"Input A to add items to {char.name}'s inventory or D to drop items\n")
            if inventory_path.lower()=='a':
                char.inventory=stock_inventory('inventory',char.inventory)
                print(f"{char.name}'s inventory has been updated")
            elif inventory_path.lower()=='d':
                cont2=True
                while cont2==True:
                    for i in range(0,len(char.inventory)):
                        print(f"{i}: {char.inventory[i].name}")
                    drop_route=input("Input the items number that you wish to drop, type info to get info on an item, or X to finish dropping items\n")
                    if drop_route.lower()=='x':
                        cont2=False
                    elif drop_route.lower()=='info':
                        item_info=input("Enter the item number that you want info on\n")
                        if item_info.isdigit():
                            if int(item_info)>=0 and int(item_info)<len(char.inventory):
                                char.inventory[int(item_info)].info()
                            else:
                                print('Invalid input, try again')
                        else:
                            print('Invalid input, try again')
                    elif drop_route.isdigit():
                        if int(drop_route)>=0 and int(drop_route)<len(char.inventory):
                            dropY=char.drop_item(int(drop_route))
                            print(f"{dropY.name} was dropped")
                        else:
                            print('Invalid input, try again')
            else:
                print('Invalid input, returning to menu')
        elif path.lower()=='x':
            cont=False
        else:
            print('Invalid input, try again')

def edit_mechanics():
    global inventory_max_size
    global skill_max_size
    global level_cap
    global promotion_level
    global needed_exp
    global support_range
    global weapon_triangle_damage_bonus
    global weapon_triangle_hit_bonus
    global doubling_threshold
    global max_number_of_doubles
    global super_effective_weapon_art_bonus
    global crit_multiplier
    global support_growth_multiplier
    global support_level_threshold
    global shop_sell_price_multiplier
    global move_cost_dict

    global magic_damage_formula
    global phys_damage_formula
    global hit_formula
    global avoid_formula
    global crit_formula
    global dodge_formula
    global exp_formula
    global wep_lev_formula
    global kill_wep_lev_formula
    global kill_exp_formula

    global guarenteed_double
    global weapon_durability
    global weapon_level_type#true is the individual weapons all have their own level, false is fe1 style
    global true_hit#True is the 2rn style
    global pair_up
    global default_weapon_edit
    global default_map_object
    global create_new_map_objects
    global enemy_priority
    global freewielding
    #char1(attacking character),char2(defending character),weapon1,dist,dmgMod,hit_formula,avoid_formula,crit_formula,hitMod,dodge_formula
    #bases,growths, weapon1.stats
    cont=False
    while cont==False:
        route=input('Input 1 to edit formulas such as the experience formula or the damage formula\n2 to edit number values like the max inventory size or the multiplier applied to sold item price\n3 to toggle options such as whether shops have limited items or whether a weapon type should automatically double\nX to finish editing game mechanics\n')
        if route.lower()=='x':
            cont=True
        elif route=='2':
            print('1: Max character inventory size\n2: Number of skills able to be equipped at once')
            print('3: Level cap\n4: Minimum level to promote\n5: EXP needed to level up\n6: Maximum tile distance to grow and use supports')
            print('7: Weapon triangle advantage damage bonus\n8: Weapon triangle advantage accuracy bonus\n9: Minimum speed difference to double')
            print('10: Number of bonus rounds of combat for doubling\n11: Super effective weapon art damage multiplier\n12: Critical hit damage multiplier')
            print('13: Support growth speed multiplier\n14: Support level up threshold\n15: Shop sell price multiplier')
            route2=input('Input the number that you would like to edit or X to cancel:\n')
            if route2.lower()=='x':
                pass
            elif route2=='1':
                pass
            elif route2=='2':
                pass
            elif route2=='3':
                pass
            elif route2=='4':
                pass
            elif route2=='5':
                pass
            elif route2=='6':
                pass
            elif route2=='7':
                pass
            elif route2=='8':
                pass
            elif route2=='9':
                pass
            elif route2=='10':
                pass
            elif route2=='11':
                pass
            elif route2=='12':
                pass
            elif route2=='13':
                pass
            elif route2=='14':
                pass
            elif route2=='15':
                pass
            else:
                print('Invalid input, returning to menu')
        elif route=='1':
            print('1: Magic attack damage formula')
            print('2: Physical attack damage formula')
            print('3: Attacking accuracy formula')
            print('4: Defending hit avoid formula')
            print('5: Attacking critical hit likelihood formula')
            print('6: Defending critical hit avoid formula')
            print("7: Experience point gain formula in battles that didn't result in a kill")
            print("8: Experience point gain formula in battles that result in a kill")
            print("9: Weapon experience gain formula in battles that didn't result in a kill")
            print("10: Weapon Experiance point gain in battles that result in a kill")
            route2=input('Input the number that you would like to edit or X to cancel\n')
            print('The available variables to use are:')
            print('The attacking character, the defending character, the weapon being attacked with, the tile distance this combat is taking place at')
            print('The damage modifier (additional damage that doesnt come from the attacking characters attack stat or the weapons damage stat, such as weapon triangle bonus or super effective multiplier)')
            print('The accuracy modifier (additional accuracy that doesnt come from the characters skill or weapon accuracy such as weapon triangle bonus')
            print('The hit formula, the avoid formula, the crit formula, the dodge formula')
            print('Numbers and mathematical operators (+-*/)')
            if route2.lower()=='x':
                pass
            elif route2=='1':
                pass
            elif route2=='2':
                pass
            elif route2=='3':
                pass
            elif route2=='4':
                pass
            elif route2=='5':
                pass
            elif route2=='6':
                pass
            elif route2=='7':
                pass
            elif route2=='8':
                pass
            elif route2=='9':
                pass
            elif route2=='10':
                pass
            pass
        elif route=='3':
            print('1: Weapon type guarenteed doubling')
            print('2: Weapon durability')
            print('3 Seperated weapon levels')#weapon_level_type#true is the individual weapons all have their own level, false is fe1 style
            print('4: 2rn hit calculation')
            print('5: Pair up')
            print('6: Enemy priority')
            print('7: Any weapon type can be used by any class')
            route2=input('Input the number that you would like to edit or X to cancel\n')
            if route2.lower()=='x':
                pass
            elif route2=='1':
                pass
            elif route2=='2':
                pass
            elif route2=='3':
                pass
            elif route2=='4':
                pass
            elif route2=='5':
                pass
            elif route2=='6':
                pass
            elif route2=='7':
                pass

def settings():
    global text_speed
    global permadeath
    global phoenix_mode
    global turnwheel
    global paragon_mode
    cont=False
    while cont==False:
        print(f'1: Text speed {text_speed}')
        print(f'2: Permadeath {permadeath}')
        print(f'3: Phoenix Mode {phoenix_mode}')
        print(f'4: Turnwheel {turnwheel}')
        print(f'5: Paragon mode {paragon_mode}')
        path=input('Input the number of the setting that you would like to change or X to finish\n')
        if path.lower()=='x':
            cont=True
        elif path=='1':
            print(f'The current text speed multiplier is {text_speed}')
            spd=input('Input a positive number that you would like the text speed multiplier to be\n')
            if isfloat(spd):
                if spd>=0:
                    text_speed=spd
                else:
                    print('Invalid input')
            else:
                print('Invalid input')
        elif path=='2':
            print(f'The permadeath option is currently set to {permadeath}')
            print('If permadeath is set to true any unit that falls in battle will be gone forever')
            print('If permadeath is set to false your dead units will come back after each map')
            perm=input('Input T to have permadeath on or F to have permadeath off\n')
            if perm.lower()=='t':
                permadeath=True
                if phoenix_mode:
                    phoenix_mode=False
            elif perm.lower()=='f':
                permadeath=False
            else:
                print("Invalid input")
        elif path=='3':
            print(f'The phoenix mode option is currently set to {phoenix_mode}')
            if permadeath==True:
                print('Phoenix mode is only available when permadeath is set to False')
            else:
                print('If phoenix mode is set to true any unit that falls in battle will revive at the start of the next turn')
                print('If phoenix mode is set to false any unit that falls in battle will be lost until the end of the map')
                pho=input('Input T to have phoenix mode on or F to have phoenix mode off\n')
                if pho.lower()=='y':
                    phoenix_mode=True
                elif pho.lower()=='f':
                    phoenix_mode=False
                else:
                    print('Invalid input')
            pass
        elif path=='4':
            print(f'The turnwheel option is currently set to {turnwheel}')
            print('If the turnwheel option is set to true you will be able to rewind your actions to a previous state a limited time for each battle')
            print('If the turnwheel option is set to false you will have to live with the consequences of your actions')
            tur=input('Input T to have the turnwheel on or F to have the turnwheel off')
            if tur.lower()=='t':
                turnwheel=True
            elif tur.lower()=='f':
                turnwheel=False
            else:
                print('Invalid input')
        elif path=='5':
            print(f'The Paragon Mode option is currently set to {paragon_mode}')
            print('If the paragon mode option is set to true all experience gain will be doubled')
            print('If the paragon mode option is set to false experience gain is unaltered')
            tur=input('Input T to have paragon mode on or F to have it off')
            if tur.lower()=='t':
                paragon_mode=True
            elif tur.lower()=='f':
                paragon_mode=False
            else:
                print('Invalid input')
def magic_damage_function(char1,char2,weapon1,weapon2,dmgMod,dist):
    if isinstance(weapon1,dark_magic):
        if 'pierce' in weapon1.bonus_effect:
            dmgMod+=char2.res
    return eval(magic_damage_formula)
def phys_damage_function(char1,char2,weapon1,weapon2,dmgMod,dist):
    return eval(phys_damage_formula)
def hit_function(char1,char2,weapon1,weapon2,hitMod,dist):
    return eval(hit_formula)
def avoid_function(char1,char2,weapon1,weapon2,avoidMod,dist):
    return eval(avoid_formula)
def crit_function(char1,char2,weapon1,weapon2,critMod,dist):
    return eval(crit_formula)
def dodge_function(char1,char2,weapon1,weapon2,dodgeMod,dist):
    return eval(dodge_formula)

"""
water's movecost is 998, void is 9999, enemy is 999
"""
#inherents
starting_gold=0
enemy=alignment('Enemy')
player=alignment('Player')
green=alignment('Green')
bounty_hunter=alignment('Bounty Hunter')
mapNum=1
campaign='Default'
timemodifier=0
move_num=0
lordDied=False
#settings
text_speed=1
permadeath=True
phoenix_mode=False
turnwheel=False
paragon_mode=False
#mechanics
inventory_max_size=5
skill_max_size=5
level_cap=20
promotion_level=10
needed_exp=100

weapon_triangle_damage_bonus=1
weapon_triangle_hit_bonus=15
magic_damage_formula='char1.mag+weapon1.dmg+dmgMod-char2.res'
phys_damage_formula='char1.atk+weapon1.dmg+dmgMod-char2.def'
hit_formula='1.5*char1.skill+.5*char1.luck+weapon1.hit+hitMod'
avoid_formula='1.5*char2.spd+.5*char2.luck'
crit_formula='.5*char1.skill+weapon1.crit'
dodge_formula='char2.luck'
exp_formula='startHP-enemy_unit.curhp'
wep_lev_formula='1'
kill_wep_lev_formula='10'
kill_exp_formula='30+enemy_unit.hp'
guarenteed_double={'Sword':False,'Lance':False,'Axe':False,'Bow':False,'Tome':False,'Fist':True,'Empty':False}
doubling_threshold=5
max_number_of_doubles=2
super_effective_weapon_art_bonus=3
crit_multiplier=3
weapon_durability=True
weapon_level_type=True #true is the individual weapons all have their own level, false is fe1 style
true_hit=False#True is the 2rn style
freewielding=False

support_range=1
pair_up=False
support_growth_multiplier=1
support_level_threshold=10

shop_sell_price_multiplier=.5
limited_shop_items=True #false would make it so that shops have infinity of everything

default_weapon_edit=False
default_map_object=False
create_new_map_objects=False
enemy_priority='Damage'
move_cost_dict={'Foot':{},'Flying':{'All':'1'},'Horse':{'All':'moveCost*2'},'Mage':{'Desert':'1'},'Pirate':{'Water':'1'}}
baseShop=shop(None,[-1,-1],[[base_silver_axe,1],[base_shield,1]])

###Skills (name,trigger_chance,trigger_stat,effect_stat,effect_change,effect_operator,effect_temp,effect_target,*relative_stat):
luna=skill('Luna',1,'skill','defense',.5,'*',True,'enemy')
sol=skill('Sol',1,'skill','curhp',10,'+',False,'self','atk')
astra=skill('Astra',.5,'skill','atk',2.5,'*',True,'self')
mag_up=skill('Mag Up',100,'skill','mag',5,'+',True,'self')
mag_up_2=skill('Mag Up 2',100,'skill','mag',5,'+',True,'self')
armsthrift=skill('Armsthrift',2,'luck','curUses',1,'+',False,'weapon')
placeholder=skill('Placeholder',0,'luck','atk',0,'+',True,'self')
defence_up=skill('Defence Up',100,'skill','defense',2,'+',True,'self')
determination=skill('Determination',1,'skill','defense',2,'*',True,'self')
lethality=skill('Lethality',.25,'skill','atk',100,'*',True,'self')
big_shield=skill('Big Shield',1,'level','defense',100,'*',True,'self')
paragon=skill('Paragon',0,'luck','atk',0,'+',False,'self')#double exp gain
swordbreaker=skill('Swordbreaker',0,'luck','atk',0,'+',False,'self')#+50 avoid/hit vs sword
lancebreaker=skill('Lancebreaker',0,'luck','atk',0,'+',False,'self')#+5 atk when using a sword
axebreaker=skill('Axebreaker',0,'luck','atk',0,'+',False,'self')#+5 atk when using a sword
bowbreaker=skill('Bowbreaker',0,'luck','atk',0,'+',False,'self')#+5 atk when using a sword
tomebreaker=skill('Tomebreaker',0,'luck','atk',0,'+',False,'self')#+5 atk when using a sword
fistbreaker=skill('Fistbreaker',0,'luck','atk',0,'+',False,'self')#+5 atk when using a sword
vantage=skill('Vantage',0,'luck','atk',0,'+',False,'self')#make unit always attack first if under half health
swordfaire=skill('Swordfaire',0,'luck','atk',0,'+',False,'self')#+5 atk when using a sword
lancefaire=skill('Lancefaire',0,'luck','atk',0,'+',False,'self')#+5 atk when using a sword
axefaire=skill('Axefaire',0,'luck','atk',0,'+',False,'self')#+5 atk when using a sword
bowfaire=skill('Bowfaire',0,'luck','atk',0,'+',False,'self')#+5 atk when using a sword
tomefaire=skill('Tomefaire',0,'luck','atk',0,'+',False,'self')#+5 atk when using a sword
fistfaire=skill('Fistfaire',0,'luck','atk',0,'+',False,'self')#+5 atk when using a sword
galeforce=skill('Galeforce',0,'luck','atk',0,'+',False,'self')#unlock the ability to taker another turn after a kill

canto=skill('Canto',0,'luck','atk',0,'+',False,'self')#unlock the ability to move after acting
steal=skill('Steal',0,'luck','atk',0,'+',False,'self')#unlock the steal command
discipline=skill('Discipline',0,'luck','atk',0,'+',False,'self')#double weapon exp gain
counter=skill('Counter',0,'luck','atk',0,'+',False,'self')#reflect physical damage
style_switch=skill('Style Switch',0,'luck','atk',0,'+',False,'self')#switch between trickster, swordmaster, general, and sniper
locktouch=skill('locktouch',0,'luck','atk',0,'+',False,'self')#unlock stuff w/o key
acrobat=skill('Acrobat',0,'luck','atk',0,'+',False,'self')#all terrain costs 1
lifetaker=skill('Lifetaker',0,'luck','atk',0,'+',False,'self')#restore 50% hp on kill
miracle=skill('Miracle',0,'luck','atk',0,'+',False,'self')#survive letal attacks
renewal=skill('Renewal',0,'luck','atk',0,'+',False,'self')#restore 30% hp every turn
aggressor=skill('Aggressor',0,'luck','atk',0,'+',False,'self')#+5 damage when initiating combat
bargin=skill('Bargin',0,'luck','atk',0,'+',False,'self')#shop stuff is half
dualwield=skill('Dualwield',0,'luck','atk',0,'+',False,'self')#can equip 2 weapons at once
false_swipe=skill('False Swipe',0,'luck','atk',0,'+',False,'self')#leave enemies with 1 hp
###Weapon Arts (name,weapontype,cost,damage,accuracy,crit,avoid,super_effective,rng,damageType(can be 'Same','Magic','Phys'),guarenteed_double,*[effect_stat,effect_change,effect_operator,target]):
grounder=weapon_art('Grounder','Sword',4,3,20,5,0,['Flying'],[1],'Same',False)
curved_shot=weapon_art('Curved Shot','Bow',3,1,30,0,0,[],[1,2,3],'Same',False)
sunder=weapon_art('Sunder','Sword',3,4,0,15,0,[],[1],'Same',False)
wrath_strike=weapon_art('Wrath Strike','Sword',3,5,10,0,0,[],[1],'Same',False)
hexblade=weapon_art('Hexblade','Sword',3,7,10,0,0,[],[1],'Magic',False)
haze_slice=weapon_art('Haze Slice','Sword',5,2,0,0,30,[],[1],'Same',False)
bane_of_monsters=weapon_art('Bane Of Monsters','Sword',4,6,0,10,0,['Monster'],[1],'Same',False)
foudroyant_strike=weapon_art('Foudroyant Strike','Sword',3,6,30,30,0,['Armored','Dragon'],[1],'Same',False)
beast_fang=weapon_art('Beast Fang','Sword',3,10,0,30,0,['Horse','Dragon'],[1],'Same',False)
ruptured_heaved=weapon_art('Ruptured Heaven','Sword',3,7,10,10,0,['Dragon'],[1,2],'Magic',False)
sword_dance=weapon_art('Sword Dance','Sword',2,1,0,0,20,[],[1],'Same',False)
tempest_lance=weapon_art('Tempest Lance','Lance',5,8,10,0,0,[],[1],'Same',False)
shatter_slash=weapon_art('Shatter Slash','Lance',5,4,10,0,1,[],[1],'Same',False,['defense',5,'-','enemy'])
knightkneeler=weapon_art('Knightkneeler','Lance',4,5,15,0,0,['Horse'],[1],'Same',False)
monster_piercer=weapon_art('Monster Piercer','Lance',4,7,0,0,10,['Monster'],[1],'Same',False)

###Classes (advanced classes on top) (name,moveType,hp,hpG,atk,atkG,mag,magG,skill,skillG,luck,luckG,defense,defG,res,resG,spd,spdG,moveRange,weaponType,promotions,skill_list,attributes)
wyvern_rider=classType('Wyvern Rider','Flying',19,.8,7,.4,0,0,6,.25,0,.3,8,.3,0,.05,5,.25,7,{'Lance':0},['Wyvern Lord','Griffon Rider'],{1:'Luna'},['Flying','Dragon'])
swordmaster=classType('Swordmaster','Foot',20,.8,7,.4,2,0,11,.5,0,.5,6,.25,4,.3,13,.5,6,{'Sword':0},[],{1:'Sol'},['Advanced'])
hero=classType('Hero','Foot',22,.9,8,.45,1,0,11,.5,0,.4,8,.3,3,.25,10,.45,6,{'Sword':0,'Axe':0,'Fist':0},[],{},['Advanced'])
paladin=classType('Paladin','Horse',25,.9,9,.45,1,0,7,.4,0,.45,10,.35,6,.3,6,.4,8,{'Axe':0,'Lance':0,'Sword':0},[],{},['Horse','Advanced'])
sage=classType('Sage','Mage',20,.7,1,0,7,0.4,5,.4,0,.4,4,.2,5,.25,7,.4,5,{'Tome':0,'Staff':0},[],{1:'Mag Up 2'},['Advanced','Magic'])
myrmidom=classType('Myrmidom','Foot',16,.7,4,.3,1,0,9,.4,0,.4,4,.2,1,.2,10,.4,5,{'Sword':0},['Swordmaster','Assassin'],{1:'Astra'},[])
mercenary=classType('Mercenary','Foot',18,.8,5,.35,0,0,8,.4,0,.3,5,.25,0,.15,7,.35,5,{'Sword':0,'Fist':0},['Hero','Bow Knight'],{1:'Armsthrift'},[])
mage=classType('Mage','Mage',16,.6,0,0,4,0.35,3,.3,0,.3,2,.15,3,.25,4,.3,5,{'Tome':0},['Sage','Dark Knight'],{1:'Mag Up'},['Magic'])
lord=classType('Lord','Foot',18,.7,6,.4,0,0,5,.3,0,.4,7,.25,0,.2,7,.3,6,{'Sword':0},['Great Lord'],{},['Lord','Convoy','Sieze'])
villager=classType('Villager','Foot',16,.8,1,.2,0,0,1,.2,1,.2,1,.2,0,.05,1,.2,5,{},[],{},['Villager'])
fighter=classType('Fighter','Foot',20,.85,8,.4,0,0,5,.3,0,.35,4,.25,0,.1,5,.2,5,{'Axe':0,'Fist':0},['Warrior','Hero'],{},[])
warrior=classType('Warrior','Foot',28,.95,12,.5,0,0,8,.4,0,.35,7,.3,3,.2,7,.2,6,{'Axe':0,'Bow':0,'Fist':0},[],{},[])
archer=classType('Archer','Foot',16,.8,5,.25,0,0,8,.4,0,.25,5,.25,0,.15,6,.25,5,{'Bow':0},['Sniper','Bow Knight'],{},[])
sniper=classType('Sniper','Foot',20,.9,7,.35,1,0,12,.5,0,.35,10,.3,3,.25,9,.4,6,{'Bow':0},[],{},['Advanced'])
knight=classType('Knight','Horse',18,.9,8,.4,0,0,4,.25,0,.3,11,.4,0,.1,2,.15,4,{'Lance':0},['General','Great Knight'],{},['Armor'])
general=classType('General','Horse',28,1,12,.5,0,0,7,.35,0,.4,15,.4,3,.2,4,.25,5,{'Sword':0,'Lance':0},[],{},['Armor','Advanced'])
cavalier=classType('Cavalier','Horse',18,.8,6,.35,0,0,5,.3,0,.35,7,.3,0,.15,6,.3,7,{'Sword':0,'Lance':0},['Paladin','Great Knight'],{},['Horse'])
wyvern_lord=classType('Wyvern Lord','Flying',24,.9,11,.5,0,0,8,.35,0,.4,11,.35,3,.15,7,.35,8,{'Axe':0,'Lance':0},[],{1:'Luna'},['Flying','Dragon','Advanced'])
pegasus_knight=classType('Pegasus Knight','Flying',16,.7,4,.2,2,0,7,.4,0,.5,4,.2,6,.35,8,.4,7,{'Lance':0},['Falcon Knight','Dark Flier'],{1:'Luna'},['Flying'])
falcon_knight=classType('Falcon Knight','Flying',20,.8,6,.35,3,.3,10,.5,0,.6,6,.25,9,.45,11,.5,8,{'Sword':0,'Lance':0},[],{1:'Luna'},['Flying','Advanced'])
thief=classType('Thief','Mage',16,.6,3,.2,0,0,6,.4,0,.2,2,.2,0,.05,8,.4,5,{'Knife':0},['Assassin','Trickster'],{1:'Luna'},[])
assassin=classType('Assassin','Mage',21,.8,8,.4,0,0,13,.5,0,.3,5,.25,1,.15,12,.5,6,{'Knife':0,'Bow':0},[],{1:'Luna'},['Advanced'])
great_knight=classType('Great Knight','Horse',26,.95,11,.45,0,0,6,.3,0,.4,14,.35,1,.15,5,.3,7,{'Axe':0,'Lance':0,'Sword':0},[],{},['Armor','Advanced','Horse'])
berserker=classType('Berserker','Foot',30,1,13,.6,0,0,5,.3,0,.3,5,.25,1,.15,11,.4,6,{'Axe':0},[],{},['Advanced'])
barbarian=classType('Barbarian','Foot',22,.9,8,.4,0,0,3,.2,0,.2,3,.2,0,.05,8,.3,5,{'Axe':0},['Berserker','Warrior'],{},[])
bow_knight=classType('Bow Knight','Horse',24,.9,8,.35,0,0,10,.4,0,.35,6,.25,2,.15,10,.4,8,{'Sword':0,'Bow':0},[],{},['Horse','Advanced'])
dark_flier=classType('Dark Flier','Flying',19,.75,5,.25,6,.35,8,.4,0,.55,5,.25,9,.45,10,.45,8,{'Lance':0,'Tome':0},[],{},['Flying','Advanced'])
dread_fighter=classType('Dread Fighter','Mage',22,.8,9,.4,6,.2,9,.4,0,.4,8,.25,10,.25,10,.4,7,{'Axe':0,'Tome':0,'Sword':0,'Knife':0},[],{},[])
great_lord=classType('Great Lord','Foot',23,.8,10,.5,0,0,7,.4,0,.5,10,.3,3,.25,9,.4,7,{'Lance':0,'Sword':0},[],{},['Lord','Advanced','Convoy','Sieze'])
dancer=classType('Dancer','Foot',16,.35,1,.05,1,0,5,.25,0,.35,3,.05,1,.05,8,.25,5,{'Sword':0},[],{},['Dancer','High Cap','Limited'])
trickster=classType('Trickster','Foot',19,.7,4,.4,4,.35,10,.45,0,.35,3,.25,5,.25,11,.45,6,{'Sword':0,'Bow':0,'Staff':0},[],{},['Advanced','Magic'])
griffon_rider=classType('Griffon Rider','Flying',22,.9,9,.4,0,0,10,0.4,0,0.4,8,0.3,3,0.15,9,0.4,8,{'Axe':0},[],{},['Advanced','Flying'])
troubadour=classType('Troubadour','Horse',16,0.6,0,0,3,0.3,2,0.2,0,0.4,1,0.15,5,0.25,5,0.4,7,{'Staff':0},['Valkyrie','War Monk'],{},['Horse','Magic'])
war_monk=classType('War Monk','Magic',24,0.9,5,0.4,5,0.35,4,0.3,0,0.45,6,0.3,6,0.4,6,0.45,6,{'Fist':0,'Staff':0},[],{},['Magic','Advanced'])
dark_knight=classType('Dark Knight','Horse',25,.95,4,.35,5,0.4,6,0.4,0,0.3,9,0.35,5,0.3,5,0.3,8,{'Sword':1,'Dark Magic':0,'Tome':0},[],{},['Advanced','Horse','Magic'])
dark_mage=classType('Dark Mage','Magic',18,.8,1,0,3,.25,2,.2,0,.2,4,.25,4,.25,3,.2,5,{'Dark Magic':0,'Tome':0},['Dark Knight','Sorcerer'],{},['Magic'])
sorcerer=classType('Sorcerer','Magic',23,.9,2,0,6,.4,4,.3,0,.3,7,.3,7,.35,4,.3,6,{'Dark Magic':0,'Tome':0},[],{},['Magic','Advanced'])
valkyrie=classType('Valkyrie','Horse',19,.7,0,0,5,.4,4,.3,0,.5,3,.2,8,.45,8,.5,8,{'Staff':0,'Tome':0},[],{},['Advanced','Horse','Magic'])
priest=classType('Priest','Mage',16,.6,0,0,3,.2,2,.2,0,.4,1,.15,6,.35,4,.2,5,{'Staff':0},['Sage','War Monk'],{},['Magic'])

pirate=classType('Pirate','Pirate',25,.6,10,.4,0,0,6,.8,2,.35,4,.25,6,.1,7,.5,4,{'Axe':0},[],{},[])
ranger=classType('Ranger','Foot',1,1,1,1,1,1,1,1,1,11,1,1,1,1,1,1,5,{'Sword':0},['Lord'],{},[])
soldier=classType('Soldier','Foot',1,1,1,1,1,1,1,1,1,1,1,11,1,1,1,5,5,{'Lance':0},['Halberdier'],{},[])
halberdier=classType('Halberdier','Foot',1,1,1,1,1,1,1,1,1,11,1,1,1,1,1,8,5,{'Lance':0},[],{},[])
#bishop
#cleric

#transporter


###Loading
print('Welcome to FE Builder, created by Schwa')
if not os.path.exists('campaign_list.txt'):
    print('In this game there are 2 main modes, creative and survival.\nIn creative mode you can create maps, edit characters, write supports, whatever you like.\nIn survival mode you can use your creations, or just use premade ones if you just want to get into the action.')
    print('These are split up into different campaigns, so you can have as many different games as you want!')
loadX='placeholder'
loadbattle=False
tic = time.perf_counter()
save_battle=[f'save_data_battle_{campaign}.txt',f'save_data_maps_battle_{campaign}.txt',f'save_data_other_battle_{campaign}.txt']
save_reg=[f'save_data_{campaign}.txt',f'save_data_other_{campaign}.txt',f'save_data_maps_{campaign}.txt']
if os.path.exists('campaign_list.txt'):
    j = open("campaign_list.txt", "r")
    campaign_list=j.read().splitlines()
    j.close()
else:
    campaign_list=[campaign]
print('\nEnter the number of the campaign you wish to play on today or input X to create a new one from scratch')
cont=False
while cont==False:
    for i in range(0,len(campaign_list)):
        print(f"{i}: {campaign_list[i]}")
    campaign_choice=input()
    if campaign_choice.lower()=='x':
        campaign=input('Enter the name for this campaign or X to cancel\n')
        confirm=input(f'Input y to confirm that you want this campaign to be called {campaign} or anything else to cancel\n')
        if confirm.lower()=='y':
            cont=True
    elif campaign_choice.isdigit():
        if int(campaign_choice)>=0 and int(campaign_choice)<len(campaign_list):
            confirm=input(f'Input Y to confirm that you want to load {campaign} or anything else to cancel\n')
            if confirm.lower()=='y':
                campaign=campaign_list[int(campaign_choice)]
                cont=True
if campaign=='Default':
    #maps (name,x_size,y_size,mapNum,spawns)
    #map objects (name,mapLevel,location,defBonus,avoidBonus,hpBonus,moveCost,display)
    #chartriggers(name,mapLevel,event,characters,*location)
    #triggers(name,mapLevel,location,event,*character)
    #treasure_chest(mapLevel,location,contents)
    #shop(mapLevel,location,contents)
    map1=mapLevel('Tutorial',11,15,1,[(0,0),(0,1)],[],[])
    fort(map1,(0,0))
    throne(map1,(0,1))
    void(map1,(8,0))
    void(map1,(8,1))
    shop(map1,(3,2),[[base_silver_axe,1],[base_shield,1]])
    treasure_chest(map1,(5,4),shield(False))
    trigger('Save Tutorial',map1,(0,0),'Hi \nDid you know you can save?')
    char_trigger('Discussion of games',map1,'Hi King\nGet pwnd Saitama',('Saitama','King'),(0,0))
    map2=mapLevel('Map 2',11,10,2,[(0,0),(0,1),(0,2)],[],[])
    throne(map2,(0,1))
    #supports
    player.support_master={('Saitama','King'):[0,'Hi','Yo','Final'],('King','Zatch'):[0,'Hello','No Way']}
    ###player_char(name,curhp,hp,hpG,atk,atkG,mag,magG,skill,skillG,luck,luckG,defense,defG,res,resG,spd,spdG,mov,classType,{weaponType},joinMap,[inventory],level,{supports},[weapon_arts])
    ###enemy_char(name,classType,joinMap,[inventory],level,[spawn])
    ###recruitable(name,curhp,hp,hpG,atk,atkG,mag,magG,skill,skillG,luck,luckG,defense,defG,res,resG,spd,spdG,mov,classType,weaponType,joinMap,inventory,level,spawn,support_list,weapon_arts,recruit_convo)
    ###boss(name,curhp,hp,atk,mag,skill,luck,defense,res,spd,mov,classType,weaponType,joinMap,inventory,level,spawn):
    garou=enemy_char('Garou','Wyvern Lord',1,[javelin(False),iron_axe(True)],1,(1,1))
    boss=boss('Boss',25,25,13,1,12,4,8,7,10,0,'Hero',{},1,[iron_axe(True)],10,(5,8))
    judas=recruitable('Judas',25,25,.5,13,.7,1,.1,12,.4,4,0,8,.2,7,.4,10,.25,0,'Hero',{},1,[iron_axe(True)],10,(5,8),{},[],'Judas continued betraying, and stabbed King in the back before long','Hey')
    hao=enemy_char('Hao','Pirate',1,[iron_axe(False)],1,(1,0))
    mumen=enemy_char('Mumen','Pirate',1,[iron_axe(False)],1,(1,2))
    ash=enemy_char('Ash','Pirate',1,[silver_axe(False)],1,(9,1))
    yuffie=enemy_char('Yuffie','Wyvern Lord',2,[javelin(False)],2,(9,1))
    saitama=player_char('Saitama',25,700,.6,10,.4,100,.25,6,.8,2,.35,4,.25,6,.1,20,.5,0,'Swordmaster',{},1,[levin_sword(False),levin_sword(False),gauntlet(False),shield(False),vulnary(False)],10,{},['Grounder'],'Saitama defeated everyone in one punch')
    saitama.add_skill(luna)
    saitama.add_skill(armsthrift)
    king=player_char('King',30,700,.6,10,.4,8,.4,6,.8,2,.35,4,.25,6,.1,2,.5,0,'Lord',{},1,[iron_sword(False),key(False)],1,{},[],'King continued his infinite unbeaten streak in Super Bash Bros')
    zatch=player_char('Zatch',25,25,.6,10,.4,12,.5,6,.8,2,.35,4,.25,6,.1,20,.5,0,'Mercenary',{},2,[iron_sword(False)],1,{},[],'The Mamodo King returned to his throne')
#Loading
if os.path.exists(f'save_data_{campaign}.txt') or os.path.exists(f'save_data_battle_{campaign}.txt'):
    if os.path.exists(f'save_data_battle_{campaign}.txt'):
        j = open(f"save_data_battle_{campaign}.txt", "r")
        listY=j.read().splitlines()
        j.close()
        print(f'Battlesave: Chapter {int(listY[3])} Playtime {datetime.timedelta(seconds=float(listY[1]))}')
    if os.path.exists(f'save_data_{campaign}.txt'):
        j = open(f"save_data_{campaign}.txt", "r")
        listX=j.read().splitlines()
        j.close()
        print(f'File 1: Chapter {int(listX[3])} Playtime {datetime.timedelta(seconds=float(listX[1]))}')
    if os.path.exists(f'save_data_battle_{campaign}.txt') and os.path.exists(f'save_data_{campaign}.txt'):
        loadX=input('Would you like to load? Press Y to load, N to start the map over, or X to delete your save file \n')
        if loadX.lower()=='y':
            load('_battle')
            loadbattle=True
            print('Data loaded')
        elif loadX.lower()=='n':
            load()
        elif loadX.lower()=='x':
            for i in save_battle,save_reg:
                if os.path.exists(i):
                    os.remove(i)
            print('Save file deleted')
    elif os.path.exists(f'save_data_battle_{campaign}.txt') and not os.path.exists(f'save_data_{campaign}.txt'):
        loadX=input('Would you like to load? Press Y to load or X to delete your save file \n')
        if loadX.lower()=='y':
            load('_battle')
            loadbattle=True
            print('Data loaded')
        elif loadX.lower()=='x':
            for i in save_battle:
                if os.path.exists(i):
                    os.remove(i)
            print('Save file deleted')
    elif os.path.exists(f'save_data_{campaign}.txt') and not os.path.exists(f'save_data_battle_{campaign}.txt'):
        loadX=input('Would you like to load? Press Y to load or X to delete your save file \n')
        if loadX.lower()=='y':
            load()
            print('Data loaded')
        elif loadX.lower()=='x':
            for i in save_reg:
                if os.path.exists(i):
                    os.remove(i)
            print('Save file deleted')
###Creative mode
zerogrowth=False
neggrowth=False
nosupport=False
fullgrowth=False
notriangle=False
if not os.path.exists('cheatshown.txt'):
    cheatshown=False
else:
    cheatshown=True
saveallowed=True
cheatallowed=True
bighead=False
noskill=False
cheat_codes=['uuddlrlrab','630660714755868972','nobitches','superjack','oldschool','bestboy','ultimatelifeform','edgelord','galaxybrain','gettinghead','alphamale','super secret swordsman']
debug='x'
if loadbattle==False:
    print('In this there are 2 main modes, creative and survival.\nIn creative mode you can create maps, edit characters, write supports, whatever you like.\nIn survival mode you can use your creations, or just use premade ones if you just want to get into the action.')
    debug=input('Input Y for creative mode or anything else for survival\n')
while debug.lower()=='y':
    print('0 Character Creator')
    print('1 Map Creator')
    print('2 Weapon Creator')
    print('3 Class Creator')
    print('4 Weapon Art Creator')
    print('5 Skill Creator')
    print('6 Support Writer')
    print('7 Character Editor')
    print('8 Map Editor')
    if saveallowed:
        print('9 Save')
    path=input('Input which path you would like to take, or x to move to survival mode\n')
    if path=='1':
        create_map()
        cheatallowed=False
    elif path=='0':
        create_character()
        cheatallowed=False
    elif path=='7':
        edit_char()
        cheatallowed=False
    elif path=='8':
        edit_map()
        cheatallowed=False
    elif path=='2':
        create_unique_weapon()
        cheatallowed=False
    elif path=='3':
        create_class()
        cheatallowed=False
    elif path=='4':
        create_weapon_art()
        cheatallowed=False
    elif path=='5':
        create_skill()
        cheatallowed=False
    elif path=='6':
        write_support()
        cheatallowed=False
    elif path=='9' and saveallowed:
        save()
    elif path.lower()=='x':
        debug='x'
    elif cheatshown==False and (path.lower()=='cheat code' or path.lower()=='password' or path.lower()=='secret'):
        print(cheat_codes[rand.randrange(0,len(cheat_codes))])
        cheatshown=True
        open('cheatshown.txt', 'w')
    elif path.lower()=='uuddlrlrab' and zerogrowth==False and fullgrowth==False and cheatallowed:
        #negative growth mode
        #disable saving
        neggrowth=True
        saveallowed=False
        print('Negative growth mode has been activated. Wither away to dust with a smile!')
        print('Saving has been disabled')
    elif path.lower()=='630660714755868972' and fullgrowth==False and fullgrowth==False and cheatallowed:
        #0% growth mode
        #disable saving
        saveallowed=False
        zerogrowth=True
        print('Zero percent growth mode has been activated. Showing no personal growth has never felt so good!')
        print('Saving has been disabled')
    elif path.lower()=='nobitches' or path.lower()=='hoessad' and cheatallowed:
        #no support mode
        nosupport=True
        print('No support mode has been activated. Prepare to die alone!')
    elif path.lower()=='superjack' and zerogrowth==False and neggrowth==False and cheatallowed:
        #100% growth mode
        #disable saving
        print('100% growth mode has been activated. This should be easy, right?')
        print('Saving has been disabled')
    elif path.lower()=='oldschool' or path.lower()=='tri-gone' and cheatallowed:
        #no triangle mode
        notriangle=True
        print("No weapon triangle mode has been activated. Rock paper scisors waifu chess has been reduced to just chess at this point!")
    elif path.lower()=='bestboy' or path.lower()=='whyareyouhere' and cheatallowed:
        #unlock laslow
        laslow=player_char('Laslow',25,25,.6,10,.4,3,.25,6,.8,2,.35,4,.25,6,.1,20,.5,0,'Hero',{},1,[levin_sword(False),levin_sword(False),gauntlet(False),shield(False),vulnary(False)],10,{},['Grounder'],'Laslow once again returned home, having invaded yet another game out of nowhere')
    elif path.lower()=='ultimatelifeform' or path.lower()=='imthecoolest' and cheatallowed:
        #unlock shadow
        shadow=player_char('Shadow',25,25,.6,10,.4,3,.25,6,.8,2,.35,4,.25,6,.1,20,.5,0,'Swordmaster',{},1,[levin_sword(False),levin_sword(False),gauntlet(False),shield(False),vulnary(False)],10,{},['Grounder'],'After the battles were done Shadow teleported away, never to be misused by Sega again')
    elif path.lower()=='edgelord' or path.lower()=='frameofreference' and cheatallowed:
        #unlock schwa
        schwa=player_char('Schwa',25,25,.6,10,.4,3,.25,6,.8,2,.35,4,.25,6,.1,20,.5,0,'Swordmaster',{},1,[levin_sword(False),levin_sword(False),gauntlet(False),shield(False),vulnary(False)],10,{},['Grounder'],'Schwa carried hard af, as always, since he made himself broken af')
    elif path.lower()=='galaxybrain' or path.lower()=='sheepish' and cheatallowed:
        #unlock kie
        kie=player_char('Kie',25,25,.6,10,.4,3,.25,6,.8,2,.35,4,.25,6,.1,20,.5,0,'Swordmaster',{},1,[levin_sword(False),levin_sword(False),gauntlet(False),shield(False),vulnary(False)],10,{},['Grounder'],'Kie continued their adventures across the cosmos, writing chapter after chapter in the legend of the Galaxy Girl')
    elif path.lower()=='gettinghead' or path.lower()=='dkmode' and cheatallowed:
        #unlock big head mode
        bighead=True
    elif path.lower()=='alphamale' or path.lower()=='vizistheleastofmyworries' and cheatallowed:
        #unlock all the alpha characters
        saitama=player_char('Saitama',25,25,.6,10,.4,3,.25,6,.8,2,.35,4,.25,6,.1,20,.5,0,'Swordmaster',{},1,[levin_sword(False),levin_sword(False),gauntlet(False),shield(False),vulnary(False)],10,{},['Grounder'],'Saitama defeated everyone in one punch')
        saitama.add_skill(luna)
        saitama.add_skill(armsthrift)
        king=player_char('King',30,30,.6,10,.4,8,.4,6,.8,2,.35,4,.25,6,.1,2,.5,0,'Lord',{},1,[iron_sword(False),key(False)],1,{},[],'King continued his infinite unbeaten streak in Super Bash Bros')
        zatch=player_char('Zatch',25,25,.6,10,.4,12,.5,6,.8,2,.35,4,.25,6,.1,20,.5,0,'Mercenary',{},2,[iron_sword(False)],1,{},[],'The Mamodo King returned to his throne')
    elif path.lower()=='supersecretswordsman' or path.lower()=='sickslicksix' and cheatallowed:
        dante=player_char('Dante',25,25,.6,10,.4,3,.25,6,.8,2,.35,4,.25,6,.1,20,.5,0,'Swordmaster',{},1,[levin_sword(False),levin_sword(False),gauntlet(False),shield(False),vulnary(False)],10,{},['Grounder'],'Saitama defeated everyone in one punch')
    elif path.lower()=='skillissue' and cheatallowed:
        noskill=True
    else:
        pass
##Cheat setting
if zerogrowth or neggrowth or fullgrowth:
    for char in character.character_list:
        for growth in character.growths:
            if zerogrowth:
                setattr(char,growth,0)
            elif neggrowth:
                if getattr(char,growth)>=0:
                    setattr(char,growth,-getattr(char,growth))
            elif fullgrowth:
                setattr(char,growth,1)
##making sure everything is good
missing_support={}
missing_classes={}
for i in player.support_master:
    #make sure all the chars exist
    exist1=False
    exist2=False
    for j in character.character_list:
        if j.name==i[0]:
            exist1=True
        elif j.name==i[1]:
            exist2=True
    if exist1==False and i[0] not in missing_support:
        missing_support[i[0]]=[i]
    elif exist1==False and i[0] in missing_support:
        missing_support[i[0]].append(i)
    if exist2==False and i[1] not in missing_support:
        missing_support[i[1]]=[i]
    elif exist2==False and i[1] in missing_support:
        missing_support[i[1]].append(i)
for i in classType.class_list:
    #making sure all the promotions exist
    for j in i.promotions:
        exist=False
        for k in classType.class_list:
            if j==k.name:
                exist=True
        if exist==False and j not in missing_classes:
            missing_classes[j]=[i]
        elif exist==False and j in missing_classes:
            missing_classes[j].append(i)
for i in player_char.player_char_list:
    #making sure all the support partners exist
    for j in i.support_list:
        exist=False
        for k in character.character_list:
            if k.name==j:
                exist=True
        if exist==False and j not in missing_support:
            missing_support[j]=[i]
        elif exist==False and j in missing_support:
            missing_support[j].append(i)
for i in recruitable.recruitable_list:
    for j in i.support_list:
        exist=False
        for k in character.character_list:
            if k.name==j:
                exist=True
        if exist==False and j not in missing_support:
            missing_support[j]=[i]
        elif exist==False and j in missing_support:
            missing_support[j].append(i)
for i in missing_support:
    cont=False
    while cont==False:
        route=input(f'{i} does not exist, input 1 to make this character or 2 to delete it\n')
        if route.lower=='1':
            create_character[i]
            cont=True
        else:
            for j in missing_support[i]:
                if isinstance(j,character):
                    del j.support_list[i]
                else:
                    del player.support_master[j]
            cont=True
for i in missing_classes:
    cont=False
    while cont==False:
        route=input(f'{i} does not exist, input 1 to make this class or 2 to delete it\n')
        if route=='1':
            create_class(i)
            cont=True
        elif route=='2':
            for j in missing_classes[i]:
                j.promotions.remove(i)
            cont=True
#making sure all map numbers exist
cont=False
while cont==False:
    missing_maps=[]
    found_maps=[]
    for i in mapLevel.map_list:
        found_maps.append(i.mapNum)
    for i in range(1,len(found_maps)+1):
        if i not in found_maps:
            missing_maps.append(i)
    if len(missing_maps)==0:
        cont=True
    else:
        length=len(missing_maps)
        for i in range(0,length):
            cont2=False
            while cont2==False:
                route=input(f'Map number {missing_maps[0]} does not exist. Input 1 to create a new map to fill this slot or 2 to renumber an existing map to this number\n')
                if route=='1':
                    create_map(missing_maps[0])
                    cont3=False
                    while cont3==False:
                        route=input('Input Y to add more units to this map or X to finish adding units\n')
                        if route.lower()=='y':
                            create_character()
                        elif route.lower()=='x':
                            cont3=True
                        else:
                            print('Invalid input, try again')
                    missing_maps.pop(0)
                    cont2=True
                elif route=='2':
                    for j in range(0,len(mapLevel.map_list)):
                        print(f'{j}: {mapLevel.map_list[j].name}, current map number {mapLevel.map_list[j].mapNum}')
                    route=input(f'Input the number for the map that you would like to be map number {missing_maps[0]}\n')
                    if route.isdigit():
                        if int(route)<len(mapLevel.map_list):
                            confirm=input(f'Input Y to confirm that you would like to renumber {mapLevel.map_list[int(route)].name} from map number {mapLevel.map_list[int(route)].mapNum} to number {missing_maps[0]} or anything else to cancel\n')
                            if confirm.lower()=='y':
                                map_ordering(mapLevel.map_list[int(route)].name,missing_maps[0],mapLevel.map_list[int(route)])
                                print('Map number changed!')
                                missing_maps.pop(0)
                                cont2=True
                            else:
                                print('Operation canceled, returning to choice')
                        else:
                            print('That number isnt an option!')
                    else:
                        print('This must be a number')
                else:
                    print('Invalid input, returning to selection')
#making everything work with freewielding
if freewielding:
    for i in classType.class_list:
        for j in weapon_types:
            if j not in i.weaponType:
                i.weaponType[j]=0
    for i in character.character_list:
        for j in weapon_types:
            if j not in i.weaponType:
                i.weaponType[j]=0
#Gameplay loop
while mapNum<=len(mapLevel.map_list):
    for i in mapLevel.map_list:
        if mapNum==i.mapNum:
            curMap=i
    if curMap.battle_saves==0:
        curMap.start_map()
    else:
        levelComplete=False
    while levelComplete==False and lordDied==False:
        if len(player.roster)>0 and len(enemy.roster)>0:
            gameplay(player)
            ai(enemy)
            curMap.turn_count+=1
            move_num=0
            if phoenix_mode:
                for i in player.roster:
                    if i.status=='KO':
                        i.status='Alive'
        else:
            levelComplete=True
    if len(player.roster)<=0 or lordDied==True:
        print("Your lord has died")
        print("Game over")
        quit()
    else:
        print("You beat the level!")
        curMap.completion_turns=curMap.turn_count
        mapNum+=1
        if saveallowed:
            saveX=input('Would you like to save the game? Input Y to save. \n')
            if saveX.lower()=='y':
                save()
                if os.path.exists(f'save_data_battle_{campaign}.txt'):
                    for i in save_battle:
                        if os.path.exists(i):
                            os.remove(i)
#Ending
print("You beat the game!")
total_turns=0
ordered_maps=[]
for i in range(1,len(mapLevel.map_list)+1):
    for j in mapLevel.map_list:
        if j.mapNum==i:
            ordered_maps.append(j)
for i in ordered_maps:
    print(f'{i.name}: {i.completion_turns} turns')
    time.sleep(1*text_speed)
    total_turns+=i.completion_turns
print(f'Total turns: {total_turns}')
time.sleep(text_speed)
total_kills=0
total_battles=0
for i in player_char.player_char_list:
    print(f"{i.name}: {i.kills} kills in {i.battles} battles, {i.status}")
    if i.status=='Alive' or i.status=='KO':
        print(f'{i.ending}')
    else:
        print(f'Died on map number {i.deathMap}')
    time.sleep(3*text_speed)
    total_kills+=i.kills
    total_battles+=i.battles
for i in recruitable.recruitable_list:
    print(f"{i.name}: {i.kills} kills in {i.battles} battles, {i.status}, {i.alignment.name}")
    if i.alignment==player:
        if i.status=='Alive' or i.status=='KO':
            print(f'{i.ending}')
        else:
            print(f'Died on map number {i.deathMap}')
        time.sleep(3*text_speed)
        total_kills+=i.kills
        total_battles+=i.battles
print(f'Total battles: {total_battles}')
print(f'Total kills: {total_kills}')
