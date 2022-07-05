import random as rand
import time
import os
import datetime
import traceback
def init_battle(char1,char2,dist,*weaponX):
    expGain=0
    dmgMod=0
    hitMod=0
    cont=False
    active_art=None
    z='End'
    if weaponX:
        weapon1=weaponX[0]
        startHP=char1.hp
        cont=True
    else:
        startHP=char2.hp
        viable_arts=[]
        art_types={}
        viable_weapons=[]
        for j in char1.weapon_arts:
            if dist in j.range:
                for i in char1.inventory:
                    if isinstance(i,weapon):
                        if i.weapontype==j.weapontype and i.curUses>=j.cost:
                            if j.weapontype not in art_types:
                                art_types[j.weapontype]=j.cost
                            elif j.weapontype in art_types:
                                if j.cost<art_types[j.weapontype]:
                                   art_types[j.weapontype]=j.cost
                            if j not in viable_arts:
                                viable_arts.append(j)                                         
        for i in range(0,len(char1.inventory)):
            if isinstance(char1.inventory[i],weapon):
                if dist in char1.inventory[i].rng or (char1.inventory[i].weapontype in art_types and char1.inventory[i].curUses>=art_types[char1.inventory[i].weapontype]):
                    if char1.inventory[i].weapontype in char1.weaponType:
                        if char1.weaponType[char1.inventory[i].weapontype]>=char1.inventory[i].weaponlevel:
                            print(str(i)+ " "+char1.inventory[i].name + " " + str(char1.inventory[i].curUses) + " " + str(char1.inventory[i].dmg) + " "+ char1.inventory[i].dmgtype + " " + str(char1.inventory[i].rng) + " " + str(char1.inventory[i].crit))
                            viable_weapons.append(char1.inventory[i])
    while cont==False:
        selection=input('Choose a weapon to use \n')
        try:
            if char1.inventory[int(selection)] in viable_weapons:                
                weapon1=char1.inventory[int(selection)]
                char1.active_item=weapon1
            possible_arts=[]
            for i in viable_arts:
                if i.weapontype==weapon1.weapontype and i.cost<=weapon1.curUses:
                    possible_arts.append(i)
            if len(possible_arts)>0:
                art=input('Input Y to use a weapon art \n')
                if art.lower()=='y':
                    for i in range(0,len(possible_arts)):
                        print(f'{i} {possible_arts[i].name}')
                    choice=input('Choose the weapon art to use \n')
                    try:
                        active_art=possible_arts[int(choice)]
                    except Exception as e:
                        print(traceback.format_exc())
                        print('Bad choice, try again')
            cont=True
        except Exception as e:
            print(traceback.format_exc())
            pass                
    if char2.active_item==None:
        weapon2=empty
    else:
        weapon2=char2.active_item
    if isinstance(char1,player_char):
        hitMod+=char1.check_support_bonus()
    elif isinstance(char2,player_char):
        hitMod-=char2.check_support_bonus()
    if weapon1.weapontype=='Sword' and weapon2.weapontype=='Lance':
        dmgMod+=-1
        hitMod+=-10
    elif weapon1.weapontype=='Sword' and weapon2.weapontype=='Axe':
        dmgMod+=1
        hitMod+=10
    elif weapon1.weapontype=='Axe' and weapon2.weapontype=='Lance':
        dmgMod+=1
        hitMod+=10
    elif weapon1.weapontype=='Axe' and weapon2.weapontype=='Sword':
        dmgMod+=-1
        hitMod+=-10
    elif weapon1.weapontype=='Lance' and weapon2.weapontype=='Sword':
        dmgMod+=1
        hitMod+=10
    elif weapon1.weapontype=='Lance' and weapon2.weapontype=='Axe':
        dmgMod1=-1
        hitMod1=-10
    if battle(char1,weapon1,char2,dmgMod,hitMod,active_art)=='Continue':
        if weapon2!=None and dist in weapon2.rng:
            z=battle(char2,weapon2,char1,-dmgMod,-hitMod)
        else:
            z='Continue'
            input(f"{char2.name} was unable to counter \n")
    if z=='Continue' and char1.spd-5>=char2.spd and weapon1 in char1.inventory:
        input(f"{char1.name} made a follow up attack \n")
        battle(char1,weapon1,char2,dmgMod,hitMod,active_art)
    if z=='Continue' and char2.spd-5>=char1.spd and weapon2 in char2.inventory:
        input(f"{char2.name} made a follow up attack \n")
        battle(char2,weapon2,char1,-dmgMod,-hitMod)
    print(char1.name + " HP: "+str(char1.curhp)+'\n')
    input(char2.name+ " HP: "+str(char2.curhp))
    char1.battles+=1
    char2.battles+=1
    if weaponX:
        if char1.status=='Dead':
            char2.weaponType[weapon2.weapontype]+=10
            expGain=30+char1.hp
        else:
            char2.weaponType[weapon2.weapontype]+=1
            expGain=startHP-char1.curhp
        if char1.status!='Dead':
            char1.moved=True
        if char2.status!='Dead':
            if char2.level<20:
                char2.exp+=expGain
            if char2.exp>=100:
                char2.level_up()
    else:
        if char2.status=='Dead':
            char1.weaponType[weapon1.weapontype]+=10
            expGain=30+char2.hp
        else:
            char1.weaponType[weapon1.weapontype]+=1
            expGain=startHP-char2.curhp
        if char1.status!='Dead':
            char1.moved=True
            if char1.level<20:
                char1.exp+=expGain
            if char1.exp>=100:
                char1.level_up()
def battle(char1,weapon1,char2,dmgMod,hitMod,*active_art):
    input(f'{char1.name} attacked {char2.name} with a {weapon1.name} \n')
    try:
        hitMod-=curMap.objectList[char2.location[0],char2.location[1]].avoidBonus
    except Exception as e:
        pass
    if active_art:
        if active_art[0]!=None:
            hitMod+=active_art[0].accuracy
            dmgMod=dmgMod+eval(f'{active_art[0].effect_change}')
    hit=1.5*char1.skill+.5*char1.luck+weapon1.hit+hitMod
    avoid=1.5*char2.spd+.5*char2.luck
    crit=.5*char1.skill+weapon1.crit
    dodge=char2.luck
    randohit=rand.randrange(0,100)
    randocrit=rand.randrange(0,100)
    truehit=hit-avoid
    truecrit=crit-dodge
    crit=False
    if char2.classType.name in weapon1.super_effective:
        dmgMod+=weapon1.dmg*weapon1.super_effective[char2.classType.name]
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
        input(f"{char1.name}'s attack missed")
        return("Continue")
    if randocrit <= truecrit:
        crit=True
    player_dict,enemy_dict=char1.skill_roll(char2)
    if weapon1.dmgtype=='Phys':
        for i in char2.inventory:
            if isinstance(i,armor):
                if i.stat=='def':
                    dmgMod-=i.effect
        try:
            dmgMod-=curMap.objectList[char2.location[0],char2.location[1]].defBonus
        except Exception as e:
            pass
        damage=char1.atk+weapon1.dmg+dmgMod-char2.defense
        if damage<0:
            damage=0
        if crit==True:
            damage*=3
            input("Critical hit!")
        if char2.curhp-damage>0:
            char2.curhp=char2.curhp-damage
            input(f"{char1.name} attacked {char2.name} and did {damage} damage \n")
            weapon1.curUses-=1
            if weapon1.curUses<=0:
                weapon1.breakX(char1)
            for i in player_dict:
                setattr(char1,i,player_dict[i])
            for j in enemy_dict:
                setattr(char2,j,enemy_dict[j])
            return("Continue")
        else:
            char2.die(char1)
            weapon1.curUses-=1
            if weapon1.curUses<=0:
                weapon1.breakX(char1)
            for i in player_dict:
                setattr(char1,i,player_dict[i])
            for j in enemy_dict:
                setattr(char2,j,enemy_dict[j])
            return("End")
    if weapon1.dmgtype=='Magic':
        for i in char2.inventory:
            if isinstance(i,armor):
                if i.stat=='res':
                    dmgMod-=i.effect
        damage=char1.atk+weapon1.dmg+dmgMod-char2.res
        if damage<0:
            damage=0
        if crit==True:
            damage*=3
            input("Critical hit!")
        if char2.curhp-damage>0:
            char2.curhp=char2.curhp-damage
            input(f"{char1.name} attacked {char2.name} and did {damage} damage \n")
            weapon1.curUses-=1
            if weapon1.curUses<=0:
                weapon1.breakX(char1)
            for i in player_dict:
                setattr(char1,i,player_dict[i])
            for j in enemy_dict:
                setattr(char2,j,enemy_dict[j])
            return("Continue")
        else:
            char2.die(char1)
            weapon1.curUses-=1
            if weapon1.curUses<=0:
                weapon1.breakX(char1)
            for i in player_dict:
                setattr(char1,i,player_dict[i])
            for j in enemy_dict:
                setattr(char2,j,enemy_dict[j])
            return("End")
def menu(self):
    atkRange=[0]
    targetRange=[]
    end=False
    while end==False:
        tradeRange=[]
        supportRange=[]
        charTriggerRange=[]
        doors=[]
        triggerRange=False
        openable=False
        openableDoor=False
        for i in self.inventory:
            if isinstance(i,weapon):
                if i.weapontype in self.weaponType:
                    for j in i.rng:
                        if j not in atkRange:
                            atkRange.append(j)
                    for k in self.weapon_arts:
                        if k.weapontype==i.weapontype and k.cost<=i.curUses:
                            for m in k.range:
                                if m not in atkRange:
                                    atkRange.append(m)
        for i in curMap.spaces:
            if abs(i[0]-self.location[0])+abs(i[1]-self.location[1])==1:
                if (i[0],i[1]) in curMap.objectList:
                    if isinstance(curMap.objectList[i[0],i[1]],door):
                        if curMap.objectList[i[0],i[1]].opened==False:
                            doors.append([i,curMap.objectList[i[0],i[1]]])
            if curMap.spaces[i][0]==True:
                if abs(i[0]-self.location[0])+abs(i[1]-self.location[1]) in atkRange:
                    if curMap.spaces[i][1].alignment!=self.alignment and [i,curMap.spaces[i][1]] not in targetRange:
                        targetRange.append([i,curMap.spaces[i][1]])
                if abs(i[0]-self.location[0])+abs(i[1]-self.location[1])==1:
                    if curMap.spaces[i][1].alignment==self.alignment:
                        if [i,curMap.spaces[i][1]] not in tradeRange:
                            tradeRange.append([i,curMap.spaces[i][1]])
                        if curMap.spaces[i][1].name in self.support_list:
                            if (self.name, curMap.spaces[i][1].name) in self.alignment.support_master:
                                if int(self.support_list[curMap.spaces[i][1].name]/10)>self.alignment.support_master[self.name, curMap.spaces[i][1].name][0] and self.alignment.support_master[self.name, curMap.spaces[i][1].name][0]<len(self.alignment.support_master[self.name, curMap.spaces[i][1].name])-1 and [self.name, curMap.spaces[i][1].name] not in supportRange:
                                    supportRange.append([self.name, curMap.spaces[i][1].name])
                            elif (curMap.spaces[i][1].name,self.name) in self.alignment.support_master:
                                if int(self.support_list[curMap.spaces[i][1].name]/10)>self.alignment.support_master[curMap.spaces[i][1].name,self.name][0] and self.alignment.support_master[curMap.spaces[i][1].name,self.name][0]<len(self.alignment.support_master[curMap.spaces[i][1].name,self.name])-1 and [curMap.spaces[i][1].name,self.name] not in supportRange:
                                    supportRange.append([curMap.spaces[i][1].name,self.name])
                        if (self.name, curMap.spaces[i][1].name) in curMap.char_trigger_list:
                            charTriggerRange.append([self.name, curMap.spaces[i][1].name])
                        elif (curMap.spaces[i][1].name,self.name) in curMap.char_trigger_list:
                            charTriggerRange.append([curMap.spaces[i][1].name,self.name])
        if (self.location[0],self.location[1]) in curMap.triggerList:
            if curMap.triggerList[self.location[0],self.location[1]].triggered==False and (self.name in curMap.triggerList[self.location[0],self.location[1]].character or 'All' in curMap.triggerList[self.location[0],self.location[1]].character):
                print('E : Event')
                triggerRange=True
        if len(targetRange)>0:
            print("0 : Battle")
        if len(tradeRange)>0:
            print("T : Trade")
        if len(supportRange)>0:
            print("B : Support")
        if len(charTriggerRange)>0:
            print("C : Character Event")
        print("1 : Inventory")
        print("2 : Equip")
        print("3 : Consume")
        print("4 : Check Stats")
        print("5 : End Turn")
        print("6 : Exit Menu")
        try:
            if isinstance(curMap.objectList[self.location[0],self.location[1]],throne):
                print("7 : Sieze Throne")
            elif isinstance(curMap.objectList[self.location[0],self.location[1]],shop):
                print("S : Shop")
            elif isinstance(curMap.objectList[self.location[0],self.location[1]],treasure_chest):
                for i in self.inventory:
                    if isinstance(i,key):
                        keyX=i
                        openable==True
                if curMap.objectList[self.location[0],self.location[1]].opened==True:
                    openable==False
                if openable==True:
                    print("Z : Open Chest")
        except Exception as e:
            pass
        if len(doors)>0:
            for i in self.inventory:
                if isinstance(i,key):
                    keyY=i
                    openableDoor==True
            if openableDoor:
                print('D : Open Door')
        v=input("Press the key of the action you wish to take \n")
        if v.lower()=='b' and len(supportRange)>0:
            for i in range(0,len(supportRange)):
                print(f"{i} : {supportRange[i]}")
            choiceSupport=input("Press the number of the support you wish to view or x to cancel \n")
            if choiceSupport=='x':
                print('Returning to menu')
            else:
                try:
                    print(self.alignment.support_master[supportRange[int(choiceSupport)][0],supportRange[int(choiceSupport)][1]][self.alignment.support_master[supportRange[int(choiceSupport)][0],supportRange[int(choiceSupport)][1]][0]+1])
                    self.alignment.support_master[supportRange[int(choiceSupport)][0],supportRange[int(choiceSupport)][1]][0]+=1
                    self.moved=True
                    end=True
                except Exception as e:
                    print(traceback.format_exc())
                    print('Invalid input, returning to menu')
        elif v.lower()=='e' and triggerRange==True:
            print(curMap.triggerList[self.location[0],self.location[1]].event)
            curMap.triggerList[self.location[0],self.location[1]].triggered=True
        elif v.lower()=='z' and openable==True:
            self.add_item(curMap.objectList[self.location[0],self.location[1]].contents)
            curMap.objectList[self.location[0],self.location[1]].opened=True
            keyX.use(self)
            self.moved=True
            end=True
        elif v.lower()=='d' and openableDoor==True:
            for i in range(0,len(doors)):
                print(f'{i} : {doors[i][0]}')
            doorChoice=input('Input the door you would like to open or X to cancel \n')
            try:
                if choiceChar=='x':
                    pass
                elif doors[int(doorChoice)]:
                    doors[int(doorChoice)].opened=True
                    keyY.use(self)
                    self.moved=True
                    end=True
            except Exception as e:
                print(traceback.format_exc())
                print('Invalid input, returning to menu')
        elif v.lower()=='c' and len(charTriggerRange)>0:
            contChar=True
            while contChar==True:
                for j in range(0,len(charTriggerRange)):
                    print(f'{j} : {curMap.char_trigger_list[charTriggerRange[j][0],charTriggerRange[j][1]].name}')
                choiceChar=input("Input the event you wish to view or x to cancel \n")
                try:
                    if choiceChar=='x':
                        contChar=False
                    elif charTriggerRange[int(choiceChar)]:
                        print(f'{curMap.char_trigger_list[charTriggerRange[int(choiceChar)][0],charTriggerRange[int(choiceChar)][1]].event}')
                        contChar=False
                except Exception as e:
                    print(traceback.format_exc())
                    print('Bad selection, try again')            
        elif v=='0' and len(targetRange)>0:
            contBattle=True
            while contBattle==True:
                for j in range(0,len(targetRange)):
                    print(str(j)+": "+targetRange[j][1].name+" at "+str(targetRange[j][0]))
                choiceBattle=input("Input the enemy you wish to fight or x to cancel \n")
                try:
                    if choiceBattle=='x':
                        contBattle=False
                    elif targetRange[int(choiceBattle)][1]:
                        dis=abs(self.location[0]-targetRange[int(choiceBattle)][1].location[0])+abs(self.location[1]-targetRange[int(choiceBattle)][1].location[1])
                        init_battle(self,targetRange[int(choiceBattle)][1],dis)
                        end=True
                        contBattle=False
                except Exception as e:
                    print(traceback.format_exc())
                    print('Bad selection, try again')
        elif v.lower()=='t' and len(tradeRange)>0:
            for i in range(0,len(tradeRange)):
                print(i,' ',tradeRange[i][1].name)
            choiceTrade=input("Input the unit you wish to trade with or x to cancel \n")
            if choiceTrade.lower=='x':
                break
            else:
                try:
                    self.trade_items(tradeRange[int(choiceTrade)][1])
                except Exception as e:
                    print(traceback.format_exc())
                    print('Invalid input, returning to menu')
        elif v.lower()=='s':
            try:
                if isinstance(curMap.objectList[self.location[0],self.location[1]],shop):
                    self.enter_shop(curMap.objectList[self.location[0],self.location[1]])
                    self.moved=True
                    end=True
                    return
            except Exception as e:
                print(traceback.format_exc())
                print('Bad selection, try again')
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
            try:
                if isinstance(curMap.objectList[self.location[0],self.location[1]],throne):
                    global levelComplete
                    levelComplete=True
                    end=True
                    return
            except Exception as e:
                print(traceback.format_exc())
                print('Bad selection, try again')
        else:
            print(traceback.format_exc())
            print("Bad selection, try again")
                                           
            
class character:
    character_list=[]
    def __init__(self,name,curhp,hp,hpG,atk,atkG,skill,skillG,luck,luckG,defense,defG,res,resG,spd,spdG,mov,alignment,classType,weaponType,joinMap,inventory,level):
        self.name=name
        self.curhp=curhp
        self.hp=hp
        self.hpG=hpG
        self.atk=atk
        self.atkG=atkG
        self.skill=skill
        self.skillG=skillG
        self.luck=luck
        self.luckG=luckG
        self.defense=defense
        self.defG=defG
        self.res=res
        self.resG=resG
        self.spd=spd
        self.spdG=spdG
        self.mov=classType.moveRange+mov
        self.movModifier=mov
        self.level=level
        self.exp=0
        self.kills=0
        self.battles=0
        self.status='Alive'
        self.joinMap=joinMap
        self.alignment=alignment
        self.inventory=inventory
        if len(inventory)>0:
            self.active_item=inventory[0]
        else:
            self.active_item=None
        self.classType=classType
        if classType.skill_list[0]!=placeholder:
            self.skills=[classType.skill_list[0]]
            self.skills_all=[classType.skill_list[0]]
        else:
            self.skills=[]
            self.skills_all=[]
        self.weaponType=weaponType
        for i in self.classType.weaponType:
            if i not in self.weaponType:
                self.weaponType[i]=self.classType.weaponType[i]
        self.location=[-1,-1]
        self.moved=False
        self.placed=False
        self.deployed=False
        self.alignment.roster_roster[joinMap].append(self)
        self.character_list.append(self)        
    def add_item(self,item):
        if len(self.inventory)<5:
            self.inventory.append(item)
            if self.active_item==None and type(item)==weapon:
                if item.weapontype in self.weaponType:
                    self.active_item=item
        else:
            print('0 '+ item.name)
            for i in range(0,len(self.inventory)):
                print(str(i+1)+' '+self.inventory[i].name)            
            drop=input('Choose an item to send to the convoy with the number key \n')
            if int(drop)==0:
                self.alignment.convoy.append(item)
                return
            else:
                self.alignment.convoy.append(self.inventory[int(drop)-1])
                self.inventory.pop(int(drop)-1)
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
            drop=input('Choose an item to send to the convoy with the number key, or exit by inputing x \n')
            if drop.lower()=='x':
                end=True
                return
            else:
                try:
                    item=self.inventory.pop(int(drop)-1)
                    if self.active_item==item:
                        self.active_item=None
                    self.alignment.convoy.append(item)
                except Exception as e:
                    print('Invalid input, try again')
        return
    def enter_shop(self,shop):
        end=False
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
            try:
                confirm=input(f"Would you like to sell the {self.inventory[int(sell)].name} for {(self.inventory[int(sell)].cost/2)*(self.inventory[int(sell)].curUses/self.inventory[int(sell)].maxUses)} gold? Input Y to confirm, anything else to cancel \n")
                if confirm.lower()=='y':
                    print(f"Sold {self.inventory[int(sell)].name} for {(self.inventory[int(sell)].cost/2)*(self.inventory[int(sell)].curUses/self.inventory[int(sell)].maxUses)} gold")
                    item=self.inventory.pop(int(sell))
                    if self.active_item==item:
                        self.active_item=None
                    self.alignment.gold+=(item.cost/2)*(item.curUses/item.maxUses)
            except Exception as e:
                print(traceback.format_exc())
                print('Invalid input, please try again')
    def buy_item(self,shop):
        end=False
        while end==False:
            if len(shop.contents)==0:
                print("We're fresh out of items, sorry chum")
                return
            print(f"{self.alignment.gold} gold")
            for i in range(0,len(shop.contents)):
                print(f"{i} : {shop.contents[i][0].name}, {shop.contents[i][0].cost} gold x{shop.contents[i][1]}")
            buy=input('Input the number of the item you would like to buy or x to exit \n')
            if buy.lower()=='x':
                return
            try:
                if shop.contents[int(buy)][0].cost<=self.alignment.gold:
                    confirm=input(f"Would you like to buy the {shop.contents[int(buy)][0].name} for {shop.contents[int(buy)][0].cost} gold? Input Y to confirm, anything else to cancel \n")
                    if confirm.lower()=='y':
                        print(f"{shop.contents[int(buy)][0].name} bought!")
                        z=shop.contents[int(buy)][0].name
                        z=z.replace(' ','_')
                        z=z.lower()
                        p=globals()[z](False)
                        self.add_item(p)
                        shop.contents[int(buy)][1]-=1
                        if shop.contents[int(buy)][1]<=0:
                            shop.contents.pop(int(buy))
                        self.alignment.gold-=p.cost
                else:
                    print("That item is too expensive for you! Buy something else, will ya?")
            except Exception as e:
                print(traceback.format_exc())
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
                route2=input(f"Input the item to trade or x to cancel \n")
                if route2.lower()=='x':
                    break
                else:
                    try:
                        item=self.inventory.pop(int(route2))
                        if self.active_item==item:
                            self.active_item=None
                        trade_partner.inventory.append(item)
                        while len(trade_partner.inventory)>5:
                            routeFix=input(f"{trade_partner.name} has too many items, input 0 to send one to the convoy or 1 to trade an item to {self.name} \n")
                            if routeFix=='0':
                                for i in range(0,len(trade_partner.inventory)):
                                    print(f"{i} {trade_partner.inventory.name}")
                                routeConvoyFix=input(f"Input the item to store \n")
                                try:
                                    itemX=trade_partner.inventory.pop(int(routeConvoyFix))
                                    if trade_partner.active_item==itemX:
                                        trade_partner.active_item=None
                                    trade_partner.alignment.convoy.append(itemX)
                                except Exception as e:
                                    print('Invalid input, try again')
                            elif routeFix=='1':
                                for i in range(0,len(trade_partner.inventory)):
                                    print(f"{i} {trade_partner.inventory.name}")
                                routeTradeFix=input(f"Input the item to trade \n")
                                try:
                                    itemX=trade_partner.inventory.pop(int(routeTradeFix))
                                    if trade_partner.active_item==itemX:
                                        trade_partner.active_item=None
                                    self.inventory.append(itemX)
                                except Exception as e:
                                    print('Invalid input, try again')
                            else:
                                print('Invalid input, try again')
                    except Exception as e:
                        print(traceback.format_exc())
            elif route=='1':
                for i in range(0,len(trade_partner.inventory)):
                    print(f"{i} {trade_partner.inventory[i].name}")
                route2=input(f"Input the item to trade or x to cancel \n")
                if route2.lower()=='x':
                    break
                else:
                    try:
                        item=trade_partner.inventory.pop(int(route2))
                        if trade_partner.active_item==item:
                            trade_partner.active_item=None
                        self.inventory.append(item)
                        while len(self.inventory)>5:
                            routeFix=input(f"{self.name} has too many items, input 0 to send one to the convoy or 1 to trade an item to {trade_partner.name} \n")
                            if routeFix=='0':
                                for i in range(0,len(self.inventory)):
                                    print(f"{i} {self.inventory.name}")
                                routeConvoyFix=input(f"Input the item to store \n")
                                try:
                                    itemX=self.inventory.pop(int(routeConvoyFix))
                                    if self.active_item==itemX:
                                        self.active_item=None
                                    self.alignment.convoy.append(itemX)
                                except Exception as e:
                                    print('Invalid input, try again')
                            elif routeFix=='1':
                                for i in range(0,len(self.inventory)):
                                    print(f"{i} {self.inventory.name}")
                                routeTradeFix=input(f"Input the item to trade \n")
                                try:
                                    itemX=self.inventory.pop(int(routeTradeFix))
                                    if self.active_item==itemX:
                                        self.active_item=None
                                    trade_partner.inventory.append(itemX)
                                except Exception as e:
                                    print('Invalid input, try again')
                            else:
                                print('Invalid input, try again')
                    except Exception as e:
                        print(traceback.format_exc())
                pass
            else:
                print(route)
                print('Invalid input, please try again')
    def withdraw_items(self):
        end=False
        if len(self.alignment.convoy)==0:
            end=True
        while end==False:
            if len(self.alignment.convoy)==0:
                end=True
                return
            if len(self.inventory)<5:
                for i in range(0,len(self.alignment.convoy)):
                    print(f'{i} {self.alignment.convoy[i].name}')
                item=input('Enter the number of the item you want to add or input x to exit \n')
                if item.lower()=='x':
                    end=True
                    return
                else:
                    try:
                        self.alignment.convoy[int(item)].info()
                        confirm=input(f"Input Y to confirm that you want to add this item to {self.name}'s inventory \n")
                        if confirm.lower()=='y':
                            addition=self.alignment.convoy.pop(int(item))
                            self.inventory.append(addition)
                            print(f"{addition.name} added to {self.name}'s inventory")
                        else:
                            pass
                    except Exception as e:
                        print('Invalid input, try again')
            else:
                print(f"{self.name}'s inventory is full, returning to menu")
                end=True
                return                    
    def add_skill(self,skill):
        if skill not in self.skills_all:
            self.skills_all.append(skill)
        if skill not in self.skills:
            if len(self.skills)<5:
                self.skills.append(skill)
            else:
                print('0 '+ skill.name)
                for i in range(0,len(self.skills)):
                    print(str(i+1)+' '+self.skills[i].name)            
                drop=input('Choose a skill to forget with the number key \n')
                if drop==0:
                    return
                else:
                    self.skills.pop(int(drop)-1)
                    self.skills.append(skill)
    def swap_skills(self):
        end=False
        while end==False:
            for i in range(0,len(self.skills_all)):
                if self.skills_all[i] not in self.skills:
                    print(f"{i} : {self.skills_all[i].name}")
            add=input(f"Input the number of the skill you want to add or x to cancel")
            if add.lower()=='x':
                return
            else:
                try:
                    self.add_skill(self.skills_all[int(add)])
                except Exception as e:
                    print(traceback.format_exc())
                    print('Invalid input, try again')
    def level_up(self):
        self.exp-=100
        self.level+=1
        if self.level>20:
            self.level=20
            self.exp=0
            return
        print('Level up!')
        if self.level==10:
            skillX=self.classType.skill_list[1]
            print(f'You have unlocked the skill {skillX.name}')
            self.add_skill(skillX)
        if self.level==20:
            skillY=self.classType.skill_list[2]
            print(f'You have unlocked the skill {skillY.name}')
            self.add_skill(skillY)
        print('Current level: '+str(self.level))
        if rand.random()<=self.hpG:
            self.hp+=1
            print("+1 HP " + str(self.hp))
        if rand.random()<=self.atkG:
            self.atk+=1
            print("+1 ATK " + str(self.atk))
        if rand.random()<=self.skillG:
            self.skill+=1
            print("+1 SKILL " + str(self.skill))
        if rand.random()<=self.luckG:
            self.luck+=1
            print("+1 LUCK " + str(self.luck))
        if rand.random()<=self.defG:
            self.defense+=1
            print("+1 DEF " + str(self.defense))
        if rand.random()<=self.resG:
            self.res+=1
            print("+1 RES " + str(self.res))
        if rand.random()<=self.spdG:
            self.spd+=1
            print("+1 SPD " + str(self.spd))
    def skill_roll(self,enemy):
        changed_stats_player={}
        changed_stats_enemy={}
        for i in self.skills:
            roll=rand.randrange(0,100)
            stat=getattr(self,i.trigger_stat)
            if roll<=stat*i.trigger_chance:
                print(f'{i.name} has procced!')
                time.sleep(1)
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
                    final_num=round(eval(f'{cur}{i.effect_operator}{i.effect_change}'))
                    setattr(weap,i.effect_stat,final_num)                    
        return changed_stats_player,changed_stats_enemy
    def show_inventory(self):
        print(self.name + "'s inventory: ")
        for i in self.inventory:
            i.info()
    def move(self,location):
        if (location[0],location[1]) not in curMap.spaces:
            print("That location is out of bounds")
            dest=input('Type where you want to move the character to in X,Y form \n')
            dest=dest.split(',')
            self.move([int(dest[0]),int(dest[1])])
            return 
        if curMap.spaces[location[0],location[1]][0]==True and curMap.spaces[location[0],location[1]][1]!=self:
            print("Theres already something there, try again")
            dest=input('Type where you want to move the character to in X,Y form \n')
            dest=dest.split(',')
            self.move([int(dest[0]),int(dest[1])])
            return       
        if location[0]==self.location[0] and location[1]==self.location[1]:
            input(f"Opening menu for {self.name}")
            menu(self)
        elif abs(location[0]-self.location[0])+abs(location[1]-self.location[1])<=self.mov:
            self.update_location(location)
            input(f'{self.name} moved')
            self.moved=True
            menu(self)
        else:
            print("Bad move, try again")
            dest=input('Type where you want to move the character to in X,Y form \n')
            dest=dest.split(',')
            self.move([int(dest[0]),int(dest[1])])
    def update_location(self,location):
        try:
            if curMap.spaces[self.location[0],self.location[1]][1]==self:
                curMap.spaces[self.location[0],self.location[1]]=[False]
        except Exception as e:
            pass
        self.location=location
        curMap.spaces[location[0],location[1]]=[True,self]
    def use_consumable(self):
        for i in range(0,len(self.inventory)):
            if isinstance(self.inventory[i],consumable):
                print(i)
                self.inventory[i].info()
            elif isinstance(self.inventory[i],promotion_item):
                if self.level>=10 and len(self.classType.promotions) >0 and ('All' in self.inventory[i].classType or self.classType.name in self.inventory[i].classType):
                    print(i)
                    self.inventory[i].info()
        path=input('Choose a item to use with their number, or input X to cancel \n')
        if path.lower()=='x':
            return
        else:
            if isinstance(self.inventory[int(path)],consumable):
                self.inventory[int(path)].active=True
                self.inventory[int(path)].curUses-=1
                if self.inventory[int(path)].stat=='curhp':
                   if self.curhp+self.inventory[int(path)].effect>self.hp:
                       self.curhp=self.hp
                       if self.inventory[int(path)].curUses<=0:
                           self.inventory[int(path)].breakX(self)
                       return
                statO=getattr(self,self.inventory[int(path)].stat)
                update=statO+self.inventory[int(path)].effect
                setattr(self,self.inventory[int(path)].stat,update)
                print(getattr(self,self.inventory[int(path)].stat))
                if self.inventory[int(path)].curUses<=0:
                   self.inventory[int(path)].breakX(self)
            elif isinstance(self.inventory[i],promotion_item):
                if self.level>=10 and len(self.classType.promotions) >0 and ('All' in self.inventory[i].classType or self.classType.name in self.inventory[i].classType):
                    self.promote()
    def consumable_turn(self,consumable):
        if consumable.active==False or consumable.dur<0:
            return
        elif consumable.active==True and consumable.curdur>1:
            consumable.curdur-=1
            return
        elif consumable.active==True and consumable.curdur==1:
            statO=getattr(self,consumable.stat)
            update=statO-consumable.effect
            setattr(self,consumable.stat,update)
            consumable.curdur=consumable.dur
            consumable.active=False
    def equip_weapon(self):
        for i in range(0,len(self.inventory)):
            if isinstance(self.inventory[i],weapon):
                print(i)
                self.inventory[i].info()
        path=input('Choose a item to use with their number, or input X to cancel \n')
        if path.lower()=='x':
            return
        else:
           if isinstance(self.inventory[int(path)],weapon):
               self.active_item=self.inventory[int(path)]
    def die(self,killer):
        self.status='Dead'
        self.alignment.roster.remove(self)
        print(f"{killer.name} attacked {self.name} and did over {self.curhp} damage, defeating the foe")
        self.curhp=0
        curMap.spaces[self.location[0],self.location[1]]=[False]
        killer.kills+=1
        for i in self.inventory:
            if i.droppable==True:
                print(f"{self.name} dropped {i.name}")
                killer.add_item(i)
        if self.classType==lord:
            global lordDied
            lordDied=True
    def check_stats(self):
        print('\n')
        print("Name: " + self.name)
        print("HP: "+str(self.curhp)+"/"+str(self.hp))
        print("Atk: "+str(self.atk))
        print("Skill: "+str(self.skill))
        print("Luck: "+str(self.luck))
        print("Def: "+str(self.defense))
        print("Res: "+str(self.res))
        print("Speed: "+str(self.spd))
        print("Move: "+str(self.mov))
        print("Moved: "+str(self.moved))
        print("Class: "+self.classType.name)
        print("Level: "+str(self.level)+" Exp: "+str(self.exp))
        print("Skills:")
        for i in self.skills:
            print(i.name)
        print("Weapon Levels")
        for i in self.weaponTypes:
            print(f'{i}: {self.weaponTypes[i]}')
    def promote(self):
        cont=False
        while cont==False:
            try:
                for i in range(0,len(self.classType.promotions)):
                    print(f'{i}: {self.classType.promotions[i].name}')
                choice=input('Choose the class to promote to')
                self.classType=self.classType.promotions[int(choice)]
                self.mov=classType.moveRange+self.movModifier
                for i in self.classType.promotionBonuses:            
                    statO=getattr(self,i)
                    update=statO+self.classType.promotionBonuses[i]
                    setattr(self,i,update)
                self.add_skill(self.classType.skill_list[0])
                for i in self.classType.promotions[int(choice)].weaponType:
                    if i in self.weaponType:
                        if self.classType.promotions[int(choice)].weaponType[i]>self.weaponType[i]:
                            self.weaponType[i]=self.classType.promotions[int(choice)].weaponType[i]
                self.level=1
                self.exp=0
                return
            except Exception as e:
                print(traceback.format_exc())
class enemy_char(character):
    def __init__(self,name,curhp,hp,hpG,atk,atkG,skill,skillG,luck,luckG,defense,defG,res,resG,spd,spdG,mov,classType,weaponType,joinMap,inventory,level,spawn):
        self.name=name
        self.spawn=spawn
        super().__init__(name,curhp,hp,hpG,atk,atkG,skill,skillG,luck,luckG,defense,defG,res,resG,spd,spdG,mov,enemy,classType,weaponType,joinMap,inventory,level)
class player_char(character):
    player_char_list=[]
    def __init__(self,name,curhp,hp,hpG,atk,atkG,skill,skillG,luck,luckG,defense,defG,res,resG,spd,spdG,mov,classType,weaponType,joinMap,inventory,level,support_list,weapon_arts):
        self.name=name
        self.support_list=support_list
        self.weapon_arts=weapon_arts
        super().__init__(name,curhp,hp,hpG,atk,atkG,skill,skillG,luck,luckG,defense,defG,res,resG,spd,spdG,mov,player,classType,weaponType,joinMap,inventory,level)
        if self not in self.player_char_list:
            self.player_char_list.append(self)
    def check_support_bonus(self):
        support_bonus=0
        for i in range(-1,2):
            for j in range(-1,2):
                if abs(i+j)==1:
                    try:
                        if curMap.spaces[self.location[0]+i,self.location[1]+j][0]==True:
                            if curMap.spaces[self.location[0]+i,self.location[1]+j][1].name in self.support_list:
                                support_bonus+=self.support_list[curMap.spaces[self.location[0]+i,self.location[1]+j][1].name]
                    except Exception as e:
                        pass
        return support_bonus
    
class classType:
    class_list=[]
    def __init__(self,name,moveType,moveRange,weaponType,promotions,skill_list):
        self.name=name
        self.moveType=moveType
        self.moveRange=moveRange
        self.weaponType=weaponType
        self.promotions=promotions
        self.skill_list=skill_list
        self.class_list.append(self)
   
class weapon:
    weapon_list=[]
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
        print("Name: " +self.name)
        print("Weapon Type: "+self.weapontype)
        print("Current durability: "+str(self.curUses))
        print("Max durability: " +str(self.maxUses))
        print(f"Weapon level: {self.weaponlevel}")
        print("Power: "+str(self.dmg))
        print("Hit: "+str(self.hit))
        print("Crit: "+str(self.crit))
        print("Range: "+str(self.rng))
        print('\n')
    def breakX(self,char):        
        input(self.name + " Broke!")
        char.inventory.remove(self)
        char.active_item=None
empty=weapon('Empty',0,0,'Empty',[0],0,0,'Empty',False,0,0,{})
class sword(weapon):
    def __init__(self,name,maxUses,dmg,dmgtype,rng,crit,hit,droppable,cost,rank,super_effective):
        super().__init__(name,maxUses,dmg,dmgtype,rng,crit,hit,'Sword',droppable,cost,rank,super_effective)
class lance(weapon):
    def __init__(self,name,maxUses,dmg,dmgtype,rng,crit,hit,droppable,cost,rank,super_effective):
        super().__init__(name,maxUses,dmg,dmgtype,rng,crit,hit,'Lance',droppable,cost,rank,super_effective)
class axe(weapon):
    def __init__(self,name,maxUses,dmg,dmgtype,rng,crit,hit,droppable,cost,rank,super_effective):
        super().__init__(name,maxUses,dmg,dmgtype,rng,crit,hit,'Axe',droppable,cost,rank,super_effective)
class bow(weapon):
    def __init__(self,name,maxUses,dmg,dmgtype,rng,crit,hit,droppable,cost,rank,super_effect):
        super_effective={'Wyvern':2}
        for i in super_effect:
            super_effective[i]=super_effect[i]
        super().__init__(name,maxUses,dmg,dmgtype,rng,crit,hit,'Bow',droppable,cost,rank,super_effective)
class fist(weapon):
    def __init__(self,name,maxUses,dmg,crit,hit,droppable,cost,rank,super_effective):
        super().__init__(name,maxUses,dmg,'Phys',[1],crit,hit,'Fist',droppable,cost,rank,super_effective)
class tome(weapon):
    def __init__(self,name,maxUses,dmg,rng,crit,hit,droppable,cost,rank,super_effective):
        super().__init__(name,maxUses,dmg,'Magic',rng,crit,hit,'Tome',droppable,cost,rank,super_effective)
class iron_sword(sword):
    def __init__(self,droppable):
        super().__init__('Iron Sword',30,4,'Phys',[1],10,85,droppable,500,0,{})
class silver_sword(sword):
    def __init__(self,droppable):
        super().__init__('Silver Sword',20,10,'Phys',[1],25,105,droppable,1500,25,{})
class levin_sword(sword):
    def __init__(self,droppable):
        super().__init__('Levin Sword',25,10,'Magic',[1,2],0,100,droppable,750,0,{})
class iron_lance(lance):
    def __init__(self,droppable):
        super().__init__('Iron Lance',30,6,'Phys',[1],0,70,droppable,500,0,{})
class javelin(lance):
    def __init__(self,droppable):
        super().__init__('Javelin',30,5,'Phys',[1,2],0,65,droppable,750,10,{})
class silver_lance(lance):
    def __init__(self,droppable):
        super().__init__('Silver Lance',20,14,'Phys',[1],0,90,droppable,1500,25,{})
class iron_axe(axe):
    def __init__(self,droppable):
        super().__init__('Iron Axe',30,8,'Phys',[1],0,60,droppable,400,0,{})
class silver_axe(axe):
    def __init__(self,droppable):
        super().__init__('Silver Axe',20,16,'Phys',[1],0,80,droppable,1500,25,{})
class iron_bow(bow):
    def __init__(self,droppable):
        super().__init__('Iron Bow',40,4,'Phys',[2],0,100,droppable,250,0,{})
class silver_bow(bow):
    def __init__(self,droppable):
        super().__init__('Silver Bow',20,12,'Phys',[2],0,110,droppable,1000,25,{})
class fire(tome):
    def __init__(self,droppable):
        super().__init__('Fire',30,5,[1,2],0,90,droppable,600,0,{"Laguz":2})
class forsetti(tome):
    def __init__(self,droppable):
        super().__init__('Forsetti',25,25,[1,2],25,100,droppable,10000,50,{"Wyvern":2})
class gauntlet(fist):
    def __init__(self,droppable):
        super().__init__('Gauntlet',100,2,20,100,droppable,250,0,{})
class key:
    key_list=[]
    def __init__(self,droppable):
        self.name='Key'
        self.curUses=5
        self.maxUses=5
        self.droppable=droppable
    def info(self):
        print("Name: "+self.name)
        print("Current durability: "+str(self.curUses))
        print("Max durability: " +str(self.maxUses))
    def use(self,char):
        self.curUses-=1
        if curUses<=0:
            self.breakX(char)
    def breakX(self,char):        
        print(self.name + " Broke!")
        char.inventory.remove(self)
        
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
        print("Name: "+self.name)
        print("Current durability: "+str(self.curUses))
        print("Max durability: " +str(self.maxUses))
        print("Item type: "+self.itemType)
        print("Amount of change: "+str(self.effect))
        print("Stat to change: "+self.stat)
        print('\n')
    def breakX(self,char):        
        print(self.name + " Broke!")
        char.inventory.remove(self)
class vulnary(consumable):
    def __init__(self,droppable):
        super().__init__('Vulnary',3,'Healing',10,'curhp',droppable,100)
class mystic_water(consumable):
    def __init__(self,droppable):
        super().__init__('Mystic Water',5,'Buff',7,'res',5,droppable,250)

class promotion_item:
    promotion_item_list=[]
    def __init__(self,name,classType,droppable,cost):
        self.name=name
        self.classType=classType
        self.droppable=droppable
        self.curUses=0
        self.cost=cost
        self.promotion_item_list.append(self)
    def info(self):
        print('Name: ',self.name)
        print('Classes this item promotes: /n')
        for i in self.classType:
            print(i.name)
class master_seal(promotion_item):
    def __init__(self,droppable):
        super().__init__('Master Seal',['All'],droppable,10000)

class armor:
    armor_list=[]
    def __init__(self,name,effect,stat,droppable,cost):
        self.name=name
        self.effect=effect
        self.stat=stat
        self.droppable=droppable
        self.cost=cost
        self.armor_list.append(self)
        self.curUses=0
    def info(self):
        print("Name: "+self.name)
        print("Stat bonus of "+str(self.effect)+" in "+self.stat)
        print('\n')
class shield(armor):
    def __init__(self,droppable):
        super().__init__('Shield',3,'def',droppable,1000)
        
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
        self.skill_list.append(self)
        
class weapon_art:
    weapon_art_list=[]
    def __init__(self,name,cost,accuracy,effect_stat,effect_change,effect_operator,weapontype,super_effective,rng):
        self.name=name
        self.cost=cost
        self.accuracy=accuracy
        self.effect_stat=effect_stat
        self.effect_change=effect_change
        self.effect_operator=effect_operator
        self.weapontype=weapontype
        self.super_effective=super_effective
        self.range=rng
        self.weapon_art_list.append(self)
                                    
class alignment:
    alignment_list=[]
    def __init__(self,name):
        self.name=name
        self.roster=[]
        self.convoy=[]
        self.gold=0
        self.alignment_list.append(self)
        #this needs to be equal in size to the number of levels v
        self.roster_roster=[[],[]]
        self.support_master={}
    def show_convoy(self):
        if len(self.convoy)==0:
            print('The convoy is empty')
            return
        for i in self.convoy:
            i.info()
    def buy_item(self,shop):
        end=False
        while end==False:
            print(f"{self.gold} gold")
            for i in range(0,len(shop.contents)):
                print(f"{i} : {shop.contents[i][0].name}, {shop.contents[i][0].cost} gold x{shop.contents[i][1]}")
            buy=input('Input the number of the item you would like to buy or x to exit \n')
            if buy.lower()=='x':
                return
            try:
                if shop.contents[int(buy)][0].cost<=self.gold:
                    confirm=input(f"Would you like to buy the {shop.contents[int(buy)][0].name} for {shop.contents[int(buy)][0].cost} gold? Input Y to confirm, anything else to cancel \n")
                    if confirm.lower()=='y':
                        print(f"{shop.contents[int(buy)][0].name} bought!")
                        z=shop.contents[int(buy)][0].name
                        z=z.replace(' ','_')
                        z=z.lower()
                        p=globals()[z](False)
                        self.convoy.append(p)
                        shop.contents[int(buy)][1]-=1
                        if shop.contents[int(buy)][1]<=0:
                            shop.contents.pop(int(buy))
                        self.gold-=p.cost
                else:
                    print("That item is too expensive for you! Buy something else, will ya?")
            except Exception as e:
                print(traceback.format_exc())
                print('Invalid input, try again')
    def sell_item(self):
        end=False
        while end==False:
            print(f"{self.gold} gold")
            for i in range(0,len(self.convoy)):
                print(f"{i}: {self.convoy[i].name} {(self.convoy[i].cost/2)*(self.convoy[i].curUses/self.convoy[i].maxUses)}")
            sell=input('Input the number of the item you would like to sell or x to exit \n')
            if sell.lower()=='x':
                return
            try:
                confirm=input(f"Would you like to sell the {self.convoy[int(sell)].name} for {(self.convoy[int(sell)].cost/2)*(self.convoy[int(sell)].curUses/self.convoy[int(sell)].maxUses)} gold? Input Y to confirm, anything else to cancel \n")
                if confirm.lower()=='y':
                    print(f"Sold {self.convoy[int(sell)].name} for {(self.convoy[int(sell)].cost/2)*(self.convoy[int(sell)].curUses/self.convoy[int(sell)].maxUses)} gold")
                    item=self.convoy.pop(int(sell))
                    self.gold+=(item.cost/2)*(item.curUses/item.maxUses)
            except Exception as e:
                print(traceback.format_exc())
                print('Invalid input, please try again')
    def show_roster(self):
        for i in self.roster:
            if i.deployed==True:
                i.check_stats()
    def turn_end(self):
        for i in self.roster:
            try:
                if i.curhp+curMap.objectList[i.location[0],i.location[1]].hpBonus<i.hp:
                    i.curhp+=curMap.objectList[i.location[0],i.location[1]].hpBonus
                else:
                    i.curhp=i.hp
            except Exception as e:
                print(traceback.format_exc())
                pass
            for j in i.inventory:
                if isinstance(j,consumable):
                    i.consumable_turn(j)
            i.moved=False
            if self==player:
                for j in curMap.spaces:
                    if curMap.spaces[j][0]==True:
                        if abs(j[0]-i.location[0])+abs(j[1]-i.location[1])==1 and curMap.spaces[j][1].alignment==i.alignment and curMap.spaces[j][1].name in i.support_list:
                            i.support_list[curMap.spaces[j][1].name]+=1
                print(i.name,i.support_list)
            
class mapLevel:
    map_list=[]
    def __init__(self,name,x_size,y_size,spawns):
        self.name=name
        self.objectList={}
        self.spaces={}
        self.triggerList={}
        self.char_trigger_list={}
        self.spawns=spawns
        self.turn_count=1
        self.battle_saves=0
        self.y_size=x_size
        for i in range(0,x_size):
            for j in range(0,y_size):
                self.spaces[j,i]=[False]
        self.completion_turns=0
        self.map_list.append(self)
    def start_map(self):
        global levelComplete
        levelComplete=False
        for i in player.roster_roster[mapNum]:
            if i not in player.roster:
                player.roster.append(i)
        enemy.roster=enemy.roster_roster[mapNum]
        for i in enemy.roster:
            i.update_location(i.spawn)
        for i in player.roster:
            i.deployed=False
            i.curhp=i.hp
        inventory=True
        while inventory==True:
            print('0 Trade Items')
            print('1 Store Items')
            print('2 Withdraw Items')
            print('3 Buy Items')
            print('4 Sell Items')
            print('5 Use Items')
            print('6 Swap Skills')
            print('7 Support')
            print('8 Save')
            print('9 Place Units And Start Map')
            inventory_input=input('Input the number key of the path you want to take or input x to exit \n')
            if inventory_input=='0':
                for j in range(0,len(player.roster)):
                    if player.roster[j].status=='Alive':
                        print(str(j)+" "+player.roster[j].name)
                p1=input('Enter the number of the first unit you want to participate in the trade or x to cancel \n')
                p2=input('Enter the number of the second unit you want to participate in the trade or x to cancel \n')
                if p1.lower()=='x' or p2.lower=='x':
                    pass
                else:
                    try:
                      player.roster[int(p1)].trade_items(player.roster[int(p2)])
                    except:
                        print('Invalid input, returning to menu')
            elif inventory_input=='5':
                for j in range(0,len(player.roster)):
                    if player.roster[j].status=='Alive':
                        print(str(j)+" "+player.roster[j].name)
                choice=input(f"Enter the number of the unit you want to store items or x to cancel \n")
                if choice.lower()=='x':
                    pass
                else:
                    try:
                        player.roster[int(choice)].use_consumable()
                    except Exception as e:
                        print('Invalid input, returning to menu')
            elif inventory_input=='1':
                for j in range(0,len(player.roster)):
                    if player.roster[j].status=='Alive':
                        print(str(j)+" "+player.roster[j].name)
                choice=input(f"Enter the number of the unit you want to store items or x to cancel \n")
                if choice.lower()=='x':
                    pass
                else:
                    try:
                        player.roster[int(choice)].store_item()
                    except Exception as e:
                        print('Invalid input, returning to menu')                
            elif inventory_input=='2':
                if len(player.convoy)==0:
                    print('The convoy is empty, returning to menu')
                else:
                    for j in range(0,len(player.roster)):
                        if player.roster[j].status=='Alive':
                            print(str(j)+" "+player.roster[j].name)
                    choice=input(f"Enter the number of the unit you want to withdraw items or x to cancel \n")
                    if choice.lower()=='x':
                        pass
                    else:
                        try:
                            player.roster[int(choice)].withdraw_items()
                        except Exception as e:
                            print('Invalid input, returning to menu')                 
            elif inventory_input=='3':
                #Buy items
                print('0 Convoy')
                for j in range(0,len(player.roster)):
                    if player.roster[j].status=='Alive':
                        print(str(j+1)+" "+player.roster[j].name)    
                choice=input(f"Enter who you want to buy items or x to cancel \n")
                if choice=='0':
                    player.buy_item(baseShop)
                elif choice.lower()=='x':
                    pass
                else:
                    try:
                        player.roster[int(choice)-1].buy_item(baseShop)
                    except Exception as e:
                        print(traceback.format_exc())
                        print('Invalid input, returning to menu')
                pass
            elif inventory_input=='4':
                #Sell Items
                print('0 Convoy')
                for j in range(0,len(player.roster)):
                    if player.roster[j].status=='Alive':
                        print(str(j+1)+" "+player.roster[j].name)    
                choice=input(f"Enter who you want to sell items or x to cancel \n")
                if choice=='0':
                    player.sell_item()
                elif choice.lower()=='x':
                    pass
                else:
                    try:
                        player.roster[int(choice)-1].sell_item()
                    except Exception as e:
                        print(traceback.format_exc())
                        print('Invalid input, returning to menu')
            elif inventory_input=='6':
                #Swap skills
                skill_count=0
                for j in range(0,len(player.roster)):
                    if player.roster[j].status=='Alive' and len(player.roster[j].skills)!=len(player.roster[j].skills_all):
                        print(str(j)+" "+player.roster[j].name)
                        skill_count+=1
                if skill_count==0:
                    print('Noone has any skills to swap. Returning to menu')
                else:
                    choice=input(f"Enter the number of the unit you want to swap skills or x to cancel \n")
                    try:
                        player.roster[int(choice)].swap_skills()
                    except Exception as e:
                        print(traceback.format_exc())
                        print('Invalid input, returning to menu')
            elif inventory_input=='7':
                supportRange=[]
                for unit in player.roster:
                    for support_partner in unit.support_list:
                        if (unit.name, support_partner) in player.support_master:
                            if int(unit.support_list[support_partner]/10)>player.support_master[unit.name, support_partner][0] and player.support_master[unit.name, support_partner][0]<len(player.support_master[unit.name, support_partner])-1 and [unit.name, support_partner] not in supportRange:
                                supportRange.append([unit.name, support_partner])
                        elif (support_partner,unit.name) in player.support_master:
                            if int(unit.support_list[support_partner]/10)>player.support_master[support_partner,unit.name][0] and player.support_master[support_partner,unit.name][0]<len(player.support_master[support_partner,unit.name])-1 and [support_partner,unit.name] not in supportRange:
                                supportRange.append([support_partner,unit.name])
                if len(supportRange)==0:
                    print('There are no supports available at this time')
                else:
                    for i in range(0,len(supportRange)):
                        print(f'{i} {supportRange[i]}')
                    choiceSupport=input('Enter the number of the support you would like to view or x to cancel \n')
                    if choiceSupport.lower()=='x':
                        pass
                    else:
                        try:
                            print(player.support_master[supportRange[int(choiceSupport)][0],supportRange[int(choiceSupport)][1]][player.support_master[supportRange[int(choiceSupport)][0],supportRange[int(choiceSupport)][1]][0]+1])
                            player.support_master[supportRange[int(choiceSupport)][0],supportRange[int(choiceSupport)][1]][0]+=1
                        except Exception as e:
                            print(traceback.format_exc())
            elif inventory_input=='8':
                save()
            elif inventory_input.lower()=='x' or inventory_input=='9':
                inventory=False
            else:
                print('Invalid input, please try again')   
        self.display()
        for i in self.spawns:
            cont=False
            count=0
            while cont==False:
                for j in range(0,len(player.roster)):
                    if player.roster[j].placed==False and player.roster[j].status=='Alive':
                        print(str(j)+" "+player.roster[j].name)
                        count+=1
                if count==0:
                    cont=True
                    break
                choice=input(f"Enter the number of the unit you want at {i} \n")
                try:
                    if player.roster[int(choice)].placed==False:
                       player.roster[int(choice)].update_location(i)
                       player.roster[int(choice)].placed=True
                       player.roster[int(choice)].deployed=True
                       cont=True
                    else:
                       print("Improper choice, try again") 
                except:
                    print("Improper choice, try again")
        for i in player.roster:
            i.placed=False
            i.moved=False
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
                    else:                   
                        cur.append(str(i[0]))
                        prev=i[1]
            cont=True
        rows.append(cur)
        prev=-1
        for i in self.spaces:
            char=None
            try:
                char=self.objectList[i].display
            except Exception as e:
                pass
            if(i[1]!=prev):
                if prev!=-1:
                    rows.append(cur)
                cur=[i[1]]
                if self.spaces[i][0]==False and char==None:                    
                    char=" "
                elif self.spaces[i][0]==True:
                    if self.spaces[i][1].alignment==enemy:
                        char="E"
                    elif self.spaces[i][1].alignment==player:
                        char="P"
                if i[0]>=10:
                    char+=' '
                cur.append(char)
                prev=i[1]
            else:
                if self.spaces[i][0]==False and char==None:                    
                    char=" "
                elif self.spaces[i][0]==True:
                    if self.spaces[i][1].alignment==enemy:
                        char="E"
                    elif self.spaces[i][1].alignment==player:
                        char="P"
                if i[0]>=10:
                    char+=' '
                cur.append(char)
                prev=i[1]
        rows.append(cur)
        for j in rows:
            print(j)            
    def display_map(self):
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
                    else:                   
                        cur.append(str(i[0]))
                        prev=i[1]
            cont=True
        rows.append(cur)
        prev=-1
        for i in self.spaces:
            char=None
            try:
                char=self.objectList[i].display
            except Exception as e:
                pass
            if(i[1]!=prev):
                if prev!=-1:
                    rows.append(cur)
                cur=[i[1]]
                if char==None:                    
                    char=" "
                if i[0]>=10:
                    char+=' '
                cur.append(char)
                prev=i[1]
            else:
                if char==None:                    
                    char=" "
                if i[0]>=10:
                    char+=' '
                cur.append(char)
                prev=i[1]
        rows.append(cur)
        for j in rows:
            print(j)
    def display_djik(self,dj):
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
                    else:                   
                        cur.append(str(i[0]))
                        prev=i[1]
            cont=True
        rows.append(cur)
        prev=-1
        for i in self.spaces:
            char=None
            try:
                char=self.objectList[i].display
            except Exception as e:
                pass
            if i in dj:
                char='#'
            if(i[1]!=prev):
                if prev!=-1:
                    rows.append(cur)
                cur=[i[1]]
                if self.spaces[i][0]==False and char==None:                    
                    char=" "
                elif self.spaces[i][0]==True:
                    if self.spaces[i][1].alignment==enemy:
                        char="E"
                    elif self.spaces[i][1].alignment==player:
                        char="P"
                if i[0]>=10:
                    char+=' '
                cur.append(char)
                prev=i[1]
            else:
                if self.spaces[i][0]==False and char==None:                    
                    char=" "
                elif self.spaces[i][0]==True:
                    if self.spaces[i][1].alignment==enemy:
                        char="E"
                    elif self.spaces[i][1].alignment==player:
                        char="P"
                if i[0]>=10:
                    char+=' '
                cur.append(char)
                prev=i[1]
        rows.append(cur)
        for j in rows:
            print(j)
            
        
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
            self.mapLevel.objectList[self.location[0],self.location[1]]=self
class fort(mapObject):
    def __init__(self,mapLevel,location):
        super().__init__('Fort',mapLevel,location,1,10,10,1,'F')
class forest(mapObject):
    def __init__(self,mapLevel,location):
        super().__init__('Forest',mapLevel,location,1,15,0,2,'^')        
class throne(mapObject):
    def __init__(self,mapLevel,location):
        super().__init__('Throne',mapLevel,location,3,5,0,1,'h')
class void(mapObject):
    def __init__(self,mapLevel,location):
        super().__init__('Void',mapLevel,location,0,0,0,9999,'X')
class water(mapObject):
    def __init__(self,mapLevel,location):
        super().__init__('Water',mapLevel,location,0,0,0,998,'~')        
class desert(mapObject):
    def __init__(self,mapLevel,location):
        super().__init__('Desert',mapLevel,location,0,0,0,2,'.')
class treasure_chest(mapObject):
    def __init__(self,mapLevel,location,contents):
        self.conents=contents
        self.opened=False
        super().__init__('Treasure Chest',mapLevel,location,0,0,0,1,'H')
class shop(mapObject):
    def __init__(self,mapLevel,location,contents):
        self.contents=contents
        super().__init__('Shop',mapLevel,location,0,0,0,1,'S')
class door(mapObject):
    def __init__(self,mapLevel,location):
        self.opened=False
        super().__init__('Door',mapLevel,location,0,0,0,999,'D')

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
            self.mapLevel.triggerList[location[0],location[1]]=self           
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
            self.location=[-1,-1]
        self.char_trigger_list.append(self)
        if mapLevel!=None:
            self.mapLevel.char_trigger_list[characters[0],characters[1]]=self
        
def gameplay(align):
    count=0
    board=[]
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
    if curMap==map1 and curMap.turn_count==5 and checkpoint==True:
        print('You can save the game once every 5 turns for free, but only if you havent moved any units. Use this wisely!')
    while checkpoint==True:
        saveQue=input('Would you like to save? Input Y to save or X to pass')
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
    for q in curMap.spaces:
        if curMap.spaces[q][0]==False:
            pass
        elif curMap.spaces[q][0]==True:
            if curMap.spaces[q][1].alignment==player:
                print(f"Player unit {curMap.spaces[q][1].name} at {q}")
            elif curMap.spaces[q][1].alignment==enemy:
                print(f"Enemy unit {curMap.spaces[q][1].name} at {q}")
        else:
            print("Error")
    print('X: Void')
    print('F: Fort')
    print('^: Forest')
    print('~: Water')
    print('.: Desert')
    print('h: Throne')
    print('H: Chest')
    print('E: Enemy')
    print('P: Player')
    curMap.display()
    cont2=False
    while cont2==False:
        print(f'There are {count} units that can still move')
        print("1: Move unit")
        print("2: View an enemies range")
        print("3: View roster")
        print("4: View convoy")
        print("5: View map features")
        print("6: End Turn")
        if curMap.battle_saves<1:
            print("7: Save (you get 1 battle save per map)")
        path=input('Enter the number of the path you want to take \n')
        if path=='3':
            align.show_roster()
        elif path=='7' and curMap.battle_saves<1:
            curMap.battle_saves+=1
            save('_battle')
        elif path=='4':
            align.show_convoy()
        elif path=='5':
            curMap.display_map()
        elif path=='6':
            align.turn_end()
            return
        elif path=='2':
            for i in range(0,len(enemy.roster)):
                print(f'{i} : {enemy.roster[i].name} {enemy.roster[i].location}')
            enemy_checked=input('Enter the number of the enemy whose range you want to check \n')
            ec_r=djikstra(enemy.roster[int(enemy_checked)])
            curMap.display_djik(ec_r)
            listX=[]
            for i in ec_r:
                listX.append(i)
            print(listX)
        elif path=='1':
            for i in range(0,len(align.roster)):
                if align.roster[i].moved==False and align.roster[i].status=='Alive' and align.roster[i].deployed==True:
                    print(str(i)+" "+align.roster[i].name+' '+str(align.roster[i].location))
            cont1=False
            while cont1==False:
                try:
                    choice=input("Enter the number of the unit you want to move \n")
                    print(f"The current location of {align.roster[int(choice)].name} is {align.roster[int(choice)].location} and they can move {align.roster[int(choice)].mov} spaces")
                    cont1=True
                except Exception as e:
                    print('Bad selection')
            dj=djikstra(align.roster[int(choice)])
            curMap.display_djik(dj)
            listY=[]
            for i in dj:
                listY.append(i)
            print(listY)
            cont=False
            while cont==False:
                dest=input('Type where you want to move the character to in X,Y form \n')
                try:
                    dest=dest.split(',')
                    if (int(dest[0]),int(dest[1])) in dj:
                        align.roster[int(choice)].move([int(dest[0]),int(dest[1])])
                        cont=True
                        cont2=True
                    else:
                       print('Bad move, try again') 
                except Exception as e:
                    print(traceback.format_exc())
                    print('Bad move, try again')
    if count!=0 and levelComplete==False and lordDied==False:
        gameplay(align)

def ai(align):
    #The goal here is to make an ai that, if it can attack a player character, it will attack the one that it does the most hp percentage damage to
    #If it cant, it will move towards the nearest player character
    count=0
    board=[]
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
    for q in curMap.spaces:
        if curMap.spaces[q][0]==False:
            pass
        elif curMap.spaces[q][0]==True:
            if curMap.spaces[q][1].alignment==player:
                print(f"Player unit {curMap.spaces[q][1].name} at {q}")
            elif curMap.spaces[q][1].alignment==enemy:
                print(f"Enemy unit {curMap.spaces[q][1].name} at {q}")
        else:
            print("Error")
    #We just choose the last item in the list cuz its easiest this way
    curMap.display()
    choice=j
    self=align.roster[j]
    #dist, weapon
    atkRange=[]
    #So here we want to find the attack range of a character
    for i in self.inventory:
        if isinstance(i,weapon):
            if i.weapontype in self.weaponType:
                if i.weaponLevel<=self.weaponType[i.weapontype]:
                    for j in i.rng:
                        atkRange.append([j,i])
    #closest= dist, location
    closest=[9999,[0,0]]
    #maxDamage has character to attack, damage done, location,weapon being used, and distance
    maxDamage=[None,0,[0,0],None,0]
    #We check every map tile
    potential_spaces=djikstra(self)
    for i in potential_spaces:
        for j in curMap.spaces:
            #We find all the spaces with enemies on them
            if curMap.spaces[j][0]==True:
                destToPlayer=abs(j[0]-i[0])+abs(j[1]-i[1])
                for k in atkRange:
                    if k[0]==destToPlayer:
                        bonus=0
                        if k[1].weapontype in self.weaponType and k[1].dmgtype=='Magic' and curMap.spaces[j][1].alignment!=self.alignment:
                            if curMap.spaces[j][1].classType.name in k[1].super_effective:
                                bonus+=k[1].dmg*k[1].super_effective[curMap.spaces[j][1].classType.name]
                            if self.atk+k[1].dmg+bonus-curMap.spaces[j][0][1].res>=maxDamage[1]:
                                maxDamage=[curMap.spaces[j][1],self.atk+k[1].dmg+bonus-curMap.spaces[j][1].res,i,k[1],k[0]]
                        elif k[1].weapontype in self.weaponType and k[1].dmgtype=='Phys' and curMap.spaces[j][1].alignment!=self.alignment:
                            if curMap.spaces[j][1].classType.name in k[1].super_effective:
                                bonus+=k[1].dmg*k[1].super_effective[curMap.spaces[j][1].classType.name]
                            if self.atk+k[1].dmg+bonus-curMap.spaces[j][1].defense>=maxDamage[1]:
                                maxDamage=[curMap.spaces[j][1],self.atk+bonus+k[1].dmg-curMap.spaces[j][1].defense,i,k[1],k[0]]
                #We then calculate the distance from this point to every player, and if its lower than the previous closest to a player we make it the new destination
                if curMap.spaces[j][1].alignment!=self.alignment and destToPlayer<=closest[0]:
                    closest=[destToPlayer,i]
    print('\n')
    if maxDamage[0]==None:
        self.update_location(closest[1])
        print(f'{self.name} moved to {closest[1]}')
        self.moved=True
        time.sleep(1)
    else:
        self.update_location(maxDamage[2])
        print(f'{self.name} moved to {maxDamage[2]}')
        init_battle(self,maxDamage[0],maxDamage[4],maxDamage[3])
    if count!=0 and levelComplete==False and lordDied==False:
        ai(align)

def djikstra(self):
    viable_spaces=[]
    shortest_path={}
    previous_nodes={}
    for i in curMap.spaces:
        distFromAI=abs(i[0]-self.location[0])+abs(i[1]-self.location[1])
        if distFromAI<=self.mov:
            viable_spaces.append([i[0],i[1]])
            if distFromAI==1:
                moveCost=1
                try:
                    moveCost=curMap.objectList[i[0],i[1]].moveCost
                except Exception as e:
                    pass
                try:
                    if curMap.spaces[i[0],i[1]][1].alignment!=self.alignment:
                        moveCost=999
                except Exception as e:
                    pass
                shortest_path[i[0],i[1]]=moveCost
            else:
                shortest_path[i[0],i[1]]=999 
    shortest_path[self.location[0],self.location[1]]=0
    while viable_spaces:
        cur_min=None
        for node in viable_spaces:
            if cur_min== None:
                cur_min= node
            elif shortest_path[node[0],node[1]] < shortest_path[cur_min[0],cur_min[1]]:
                cur_min=node
        neighbors=[]
        try:
            curMap.spaces[cur_min[0]-1,cur_min[1]]
            neighbors.append([cur_min[0]-1,cur_min[1]])
        except Exception as e:
            pass
        try:
            curMap.spaces[cur_min[0]+1,cur_min[1]]
            neighbors.append([cur_min[0]+1,cur_min[1]])
        except Exception as e:
            pass
        try:
            curMap.spaces[cur_min[0],cur_min[1]+1]
            neighbors.append([cur_min[0],cur_min[1]+1])
        except Exception as e:
            pass
        try:
            curMap.spaces[cur_min[0],cur_min[1]-1]
            neighbors.append([cur_min[0],cur_min[1]-1])
        except Exception as e:
            pass
        for neighbor in neighbors:
            tenative_value = shortest_path[cur_min[0],cur_min[1]]
            moveCost=1
            try:
                moveCost=curMap.objectList[neighbor[0],neighbor[1]].moveCost
            except Exception as e:
                pass
            try:
                if curMap.spaces[neighbor[0],neighbor[1]][1].alignment!=self.alignment:
                    moveCost=999
            except Exception as e:
                pass
            if moveCost!=999 and moveCost!=1:
                if self.classType.moveType=='Flying':
                    moveCost=1
                elif self.classType.moveType=='Horse':
                    moveCost*=2
                elif self.classType.moveType=='Mage' and curMap.objectList[neighbor[0],neighbor[1]].name=='Desert':
                    moveCost=1
                elif self.classType.moveType=='Pirate' and curMap.objectList[neighbor[0],neighbor[1]].name=='Water':
                    moveCost=2
            tenative_value+=moveCost
            try:
                if tenative_value < shortest_path[neighbor[0],neighbor[1]]:
                    shortest_path[neighbor[0],neighbor[1]]=tenative_value
                    try:
                        previous_nodes[neighbor[0],neighbor[1]].append(cur_min)
                    except Exception as e:
                        previous_nodes[neighbor[0],neighbor[1]]=[cur_min]
            except Exception as e:
                pass
            try:
                viable_spaces.remove([cur_min[0],cur_min[1]])
            except Exception as e:
                pass
    for i in list(shortest_path):
        if shortest_path[i]>self.mov:
            shortest_path.pop(i)
        elif curMap.spaces[i][0]==True:
            if curMap.spaces[i][1]!=self:
                shortest_path.pop(i)
    return shortest_path

def save(kind=''):
    print("Saving data, please don't turn off the power")
    if not os.path.exists(f'save_data{kind}.txt'):
        open(f'save_data{kind}.txt', 'w')
    with open(f'save_data{kind}.txt', 'r+') as f:
        f.truncate(0)
        toc = time.perf_counter()
        playtime=int(toc-tic)
        playtime+=timemodifier
        f.write(f'time\n{playtime}\nmap\n{mapNum}\n')
        for i in mapLevel.map_list:
            f.write(str(i.completion_turns))
            f.write('\n')
        f.write('roster\n')
        for i in player.roster:
            f.write(i.name)
            f.write('\n')
        f.write(f'support\n{player.support_master}\n')
        f.write(f'turncount\n{mapLevel.map_list[mapNum].turn_count}\nbattlesaves\n{mapLevel.map_list[mapNum].battle_saves}')
    f.close()
    with open(f'save_data_chars{kind}.txt', 'w') as f:
        f.truncate(0)
        for i in character.character_list:
            for attr, value in i.__dict__.items():
                if type(value) is list:
                    for j in value:
                        if attr=='inventory':
                            f.write(f'{attr}XYZCYX{j.name}/{str(j.curUses)}/{str(j.droppable)}\n')
                        else:
                            try:
                                f.write(f'{attr}XYZCYX{j.name}\n')
                            except Exception as e:
                                f.write(f'{attr}XYZCYX{value}\n')
                                pass
                else:
                    try:
                        if attr=='active_item':
                            f.write(f'{attr}XYZCYX{value.name}/{str(value.curUses)}/{str(value.droppable)}\n')
                        else:
                            f.write(f'{attr}XYZCYX{value.name}\n')
                    except Exception as e:
                        f.write(f'{attr}XYZCYX{str(value)}\n')
            f.write('BREAK\n')
    print('Save complete!')

def load(kind=''):
    j = open(f"save_data{kind}.txt", "r")
    listX=j.read().splitlines()
    j.close()    
    weapon.weapon_list=[]
    consumable.consumable_list=[]
    player.roster=[]
    mapChoice=False
    for i in listX:
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
                else:
                    for j in range(4,len(mapLevel.map_list)+3):
                        j=int(j)
                        mapLevel.map_list[j-4].completion_turns=listX[j]
            elif path=='roster':
                player.roster.append(eval(i.lower()))
            elif path=='support':
               player.support_master=eval(i)
            elif path=='battlesaves':
                mapLevel.map_list[mapNum].battle_saves=int(i)
            elif path=='time':
                global timemodifier
                timemodifier+=int(i)
            elif path=='turncount':
                mapLevel.map_list[mapNum].turn_count=int(i)
    j = open(f"save_data_chars{kind}.txt", "r")
    listX=j.read().split('BREAK')
    j.close()
    char_dict={}
    cur=None
    for i in listX:
        i=i.split('\n')
        for j in i:
            j=j.split('XYZCYX')
            if j[0]=='name':
                cur=j[1]
                char_dict[cur]=[]
            else:
                try:
                    if j[0]!='':
                        char_dict[cur].append(j)
                except Exception as e:
                    print(j)
    for i in char_dict:
        equipped_count=0
        eval(i.lower()).skills=[]
        skills_placed=[]
        eval(i.lower()).skills_all=[]
        eval(i.lower()).inventory=[]
        for j in char_dict[i]:
            if j[0]!='alignment' and j[0]!='active_item' and j[0]!='inventory' and j[0]!='skills' and j[0]!='skills_all' and j[0]!='classType':
                try:
                    setattr(eval(i.lower()),j[0],eval(j[1]))
                except Exception as e:
                    setattr(eval(i.lower()),j[0],j[1])
            elif j[0]=='classType' or j[0]=='alignment':
                z=j[1]
                z=z.replace(' ','_')
                z=z.lower()
                setattr(eval(i.lower()),j[0],eval(z))
                if j[0]=='alignment' and mapLevel.map_list[mapNum].battle_saves>0 and j[1]=='Enemy' and mapNum==eval(i.lower()).joinMap:
                    enemy.roster.append(eval(i.lower()))
            elif j[0]=='active_item' and j[1]!='None':
                x=j[1]
                x=x.split('/')
                uses=x[1]
                z=x[0]
                z=z.replace(' ','_')
                z=z.lower()
                p=globals()[z](eval(x[2]))
                p.curUses=int(uses)
                setattr(eval(i.lower()),j[0],p)
                eval(i.lower()).add_item(p)
            elif j[0]=='inventory':
                x=j[1]
                x=x.split('/')
                uses=x[1]
                z=x[0]
                z=z.replace(' ','_')
                z=z.lower()
                p=globals()[z](eval(x[2]))
                p.curUses=int(uses)
                if eval(z)==type(eval(i.lower()).active_item) and equipped_count==0 and p.curUses==eval(i.lower()).active_item.curUses:
                    equipped_count+=1
                else:
                    eval(i.lower()).add_item(p)
            elif j[0]=='active_item' and j[1]=='None':
                setattr(eval(i.lower()),j[0],None)
            elif j[0]=='skills':
                eval(i.lower()).add_skill(eval(j[1].lower()))
                skills_placed.append(j[1])
            elif j[0]=='skills_all':
                if j[1] not in skills_placed:
                  eval(i.lower()).skills_all.append(eval(j[1].lower()))
        if mapLevel.map_list[mapNum].battle_saves>0:
            for i in enemy.roster:
                mapLevel.map_list[mapNum].spaces[i.location[0],i.location[1]]=[True,i]
            for i in player.roster:
                if i.deployed==True:
                   mapLevel.map_list[mapNum].spaces[i.location[0],i.location[1]]=[True,i] 

"""
water's movecost is 998, void is 9999, enemy is 999
"""
timemodifier=0
lordDied=False
#maps (name,x_size,y_size,spawns)
#map objects (name,mapLevel,location,defBonus,avoidBonus,hpBonus,moveCost,display)
#chartriggers(name,mapLevel,event,characters,*location)
#triggers(name,mapLevel,location,event,*character)
#treasure_chest(mapLevel,location,contents)
#shop(mapLevel,location,contents)
baseShop=shop(None,[-1,-1],[[silver_axe(False),1],[shield(False),1]])
map1=mapLevel('Tutorial',11,15,[[0,0],[0,1]])
fort(map1,[0,0])
throne(map1,[0,1])
void(map1,[8,0])
void(map1,[8,1])
shop(map1,[3,2],[[silver_axe(False),1],[shield(False),1]])
treasure_chest(map1,[5,4],shield(False))
trigger('Save Tutorial',map1,[0,0],'Hi \nDid you know you can save?')
char_trigger('Discussion of games',map1,'Hi King\nGet pwnd Saitama',('Saitama','King'),[0,0])
map2=mapLevel('Map 2',11,10,[[0,0],[0,1],[0,2]])
throne(map2,[0,1])
mapNum=0
curMap=mapLevel.map_list[mapNum]
#alignments
enemy=alignment('Enemy')
player=alignment('Player')
player.support_master={('Saitama','King'):[0,'Hi','Yo','Final'],('King','Zatch'):[0,'Hello','No Way']}
#Skills (name,trigger_chance,trigger_stat,effect_stat,effect_change,effect_operator,effect_temp,effect_target,*relative_stat):
luna=skill('Luna',9,'skill','defense',.5,'*',True,'enemy')
sol=skill('Sol',5,'skill','curhp',10,'+',False,'self')
astra=skill('Astra',5,'skill','atk',2.5,'*',True,'self')
mag_up=skill('Mag Up',100,'skill','atk',5,'+',True,'self')
mag_up_2=skill('Mag Up 2',100,'skill','atk',5,'+',True,'self')
armsthrift=skill('Armsthrift',500,'luck','curUses',1,'+',False,'weapon')
placeholder=skill('Placeholder',0,'luck','atk',0,'+',True,'self')
#Weapon Arts (name,cost,accuracy,effect_stat,effect_change,effect_operator,weapontype,super_effective,rng):
grounder=weapon_art('Grounder',3,10,'atk',2,'*','Sword',[],[1,2,3,4])
#Classes (advanced classes on top) (name,moveType,moveRange,weaponType,promotions,skill_list)
wyvern=classType('Wyvern','Flying',8,{'Axe':0,'Lance':0},[],[luna])
swordmaster=classType('Swordmaster','Foot',6,{'Sword':0},[],[sol])
hero=classType('Hero','Foot',6,{'Sword':0,'Axe':0},[],[placeholder])
paladin=classType('Paladin','Horse',7,{'Axe':0,'Lance':0,'Sword':0},[],[placeholder])
sage=classType('Sage','Mage',5,{'Tome':0},[],[mag_up_2])
myrmidom=classType('Myrmidom','Foot',5,{'Sword':0},[swordmaster],[astra])
mercenary=classType('Mercenary','Foot',5,{'Sword':0,'Fist':0},[hero],[armsthrift])
mage=classType('Mage','Mage',4,{'Tome':0},[],[mag_up])
pirate=classType('Pirate','Pirate',4,{'Axe':0},[],[placeholder])
lord=classType('Lord','Foot',6,{'Sword':0},[],[placeholder])
#Characters (name,curhp,hp,hpG,atk,atkG,skill,skillG,luck,luckG,defense,defG,res,resG,spd,spdG,mov,alignment,classType,{weaponType},joinMap,[inventory],level,*{supports}/[spawn],^[weapon_arts])
garou=enemy_char('Garou',25,25,.6,10,.4,6,.8,2,.35,4,.25,6,.1,7,.5,0,wyvern,{},0,[javelin(False),iron_axe(True)],1,[1,1])
hao=enemy_char('Hao',25,25,.6,10,.4,6,.8,2,.35,4,.25,6,.1,7,.5,0,pirate,{},0,[javelin(False),iron_axe(False)],1,[1,0])
mumen=enemy_char('Mumen',25,25,.6,10,.4,6,.8,2,.35,4,.25,6,.1,7,.5,0,pirate,{},0,[iron_axe(False)],1,[1,2])
ash=enemy_char('Ash',25,25,.6,10,.4,6,.8,2,.35,4,.25,6,.1,7,.5,0,pirate,{},0,[silver_axe(False)],1,[9,1])
yuffie=enemy_char('Yuffie',25,25,.6,10,.4,6,.8,2,.35,4,.25,6,.1,7,.5,0,wyvern,{},1,[javelin(False)],1,[9,1])
saitama=player_char('Saitama',25,25,.6,10,.4,6,.8,2,.35,4,.25,6,.1,20,.5,0,swordmaster,{},0,[levin_sword(False),levin_sword(False),gauntlet(False),shield(False),vulnary(False)],10,{'King':0},[grounder])
saitama.add_skill(luna)
saitama.add_skill(armsthrift)
king=player_char('King',3,3,.6,10,.4,6,.8,2,.35,4,.25,6,.1,2,.5,0,lord,{},0,[iron_sword(False),key(False)],1,{'Saitama':0,'Zatch':0},[])
zatch=player_char('Zatch',25,25,.6,10,.4,6,.8,2,.35,4,.25,6,.1,20,.5,0,mercenary,{},1,[iron_sword(False)],1,{'King':0},[])
#Debug mode
##debug=input('Input KGJ to activate debug mode')
##if debug=='630':
##    print('0 battle')
##    print('1 skip to map')
#Loading
loadX='placeholder'    
if os.path.exists('save_data.txt') or os.path.exists('save_data_battle.txt'):
    if os.path.exists('save_data_battle.txt'):
        j = open("save_data_battle.txt", "r")
        listY=j.read().splitlines()
        j.close()
        print(f'Battlesave: Chapter {int(listY[3])+1} {mapLevel.map_list[int(listY[3])].name} Playtime {datetime.timedelta(seconds=float(listY[1]))}')
    if os.path.exists('save_data.txt'):
        j = open("save_data.txt", "r")
        listX=j.read().splitlines()
        j.close()
        print(f'File 1: Chapter {int(listX[3])+1} {mapLevel.map_list[int(listX[3])].name} Playtime {datetime.timedelta(seconds=float(listX[1]))}')
    if os.path.exists('save_data_battle.txt') and os.path.exists('save_data.txt'):
        loadX=input('Would you like to load? Press Y to load, N to start the map over, or X to delete your save file \n')
        if loadX.lower()=='y':
            load('_battle')
        elif loadX.lower()=='n':
            load()
        elif loadX.lower()=='x':
            os.remove('save_data.txt')
            os.remove('save_data_chars.txt')
            os.remove('save_data_battle.txt')
            os.remove('save_data_chars_battle.txt')
            print('Save file deleted')
    elif os.path.exists('save_data_battle.txt') and not os.path.exists('save_data.txt'):
        loadX=input('Would you like to load? Press Y to load or X to delete your save file \n')
        if loadX.lower()=='y':
            load('_battle')
        elif loadX.lower()=='x':
            os.remove('save_data_battle.txt')
            os.remove('save_data_chars_battle.txt')
            print('Save file deleted')
    elif os.path.exists('save_data.txt') and not os.path.exists('save_data_battle.txt'):
        loadX=input('Would you like to load? Press Y to load or X to delete your save file \n')
        if loadX.lower()=='y':
            load()
        elif loadX.lower()=='x':
            os.remove('save_data.txt')
            os.remove('save_data_chars.txt')
            print('Save file deleted')
if loadX.lower()!='y':
    print('Welcome to FE Builder, created by Schwa')
#Gameplay loop
tic = time.perf_counter()
while mapNum<len(mapLevel.map_list):
    curMap=mapLevel.map_list[mapNum]
    if curMap.battle_saves==0:
        curMap.start_map()
    else:
        levelComplete=False
    while levelComplete==False and lordDied==False:
        if len(player.roster)>0 and len(enemy.roster)>0:
            gameplay(player)
            ai(enemy)
            curMap.turn_count+=1
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
        saveX=input('Would you like to save the game? Input Y to save. \n')
        if saveX.lower()=='y':
            save()
            if os.path.exists('save_data_battle.txt'):
                os.remove('save_data_battle.txt')
                os.remove('save_data_chars_battle.txt')
#Ending
print("You beat the game!")
total_turns=0
for i in mapLevel.map_list:
    print(f'{i.name}: {i.completion_turns} turns')
    total_turns+=i.completion_turns
print(f'Total turns: {total_turns}')
total_kills=0
total_battles=0
for i in player_char.player_char_list:
    print(f"{i.name}: {i.kills} kills in {i.battles} battles, {i.status}")
    total_kills+=i.kills
    total_battles+=i.battles
print(f'Total battles: {total_battles}')
print(f'Total kills: {total_kills}')
