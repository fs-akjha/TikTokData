no_of_lines = 2
lines = ""
new_lines=""
self_po=[]
all_input=[]
new_list=[]
self_data=[]
opp_data=[]
opponents=[]
type_based=[]
win=0
for i in range(no_of_lines):
    lines+=input()+"\n"
self_po=lines.split("\n")
self_pokemons=self_po[0]

opp_pokemons=self_po[1]
print(self_pokemons)
print()
print()
print(opp_pokemons)

for data1 in self_pokemons.split(';'):
    self_data.append(data1.split('#'))
print("List of our own Pokemons with Type and Level",self_data)

for data2 in opp_pokemons.split(';'):
    opp_data.append(data2.split('#'))
print("List of Opponents Pokemons with Type and Level",opp_data)
for data3 in self_data:
    all_input.append(data3[0])
for data4 in opp_data:
    new_list.append(data4[0])
print("My Pokemons",all_input)
print("Opponent Pokemons",new_list)
print(len(all_input))
print(len(new_list))

def check_input_opp_length(all_input,new_list):
    if(len(all_input)<5):
        print("Our Pokemon is less than requested")
        return False
    elif(len(new_list)<5):
        print("Opponent  Pokemon is less than requested")
        return False
    else:
        print("Everything is fine")
        return True

def check_duplicates_input(all_input_data):
    all_input_set=set()
    for elem in all_input:
        if elem in all_input_set:
            return True
        else:
            all_input_set.add(elem) 
    return False

def check_duplicates_opp(new_list_data):
    new_list_set=set()
    for elem in new_list:
        if elem in new_list_set:
            return True
        else:
            new_list_set.add(elem) 
    return False

all_input_data=all_input
new_list_data=new_list

result1 = check_duplicates_input(all_input_data)
result2 = check_duplicates_opp(new_list_data)

print(result1)
print(result2)

def check_input_opp_dupp(result1,result2):
    if result1:
        print('Yes, Input contains duplicates')
        return result1
    elif result2:
        print('Yes, Opponent contains duplicates')
        return result1
    else:
        print('No duplicates found in list')
        return True

duplicacy_check=check_input_opp_dupp(result1,result2)
print(duplicacy_check)


length_check=check_input_opp_length(all_input,new_list)
print(length_check)

def based_on_type(self_data,opp_data,all_input,new_list,win):
    for d1 in opp_data:
        if d1[0]=="Water":
            for d2 in self_data:
                if d2[0]=="Electric":
                    if d2[1]>=(2*d1[1]):
                        type_based.append(d2[0]+"#"+d2[1])
                        self_data.remove(d2)
                        win=win+1
                    else:
                        pass
                else:
                    if d2[0]=="Grass":
                        if d2[1]>d1[1]:
                            type_based.append(d2[0]+"#"+d2[1])
                            self_data.remove(d2)
                            win=win+1
                    else:
                        pass
        elif d1[0]=="Fighting":
            for d2 in self_data:
                if d2[0]=="Grass":
                    if d2[1]>=(2*d1[1]):
                        type_based.append(d2[0]+"#"+d2[1])
                        self_data.remove(d2)
                        win=win+1
                elif d2[0]=="Ghost":
                    if d2[1]>=(2*d1[1]):
                        type_based.append(d2[0]+"#"+d2[1])
                        self_data.remove(d2)
                        win=win+1
                elif d2[0]=="Fire":
                    if d2[1]>d1[1]:
                        type_based.append(d2[0]+"#"+d2[1])
                        self_data.remove(d2)
                        win=win+1
                    else:
                        pass
                else:
                    type_based.append(d2[0]+"#"+d2[1])
                    self_data.remove(d2)
        elif d1[0]=="Psychic":
            for d2 in self_data:
                if d2[0]=="Psychic":
                    print("done")

    return win

def actual_logic(duplicacy_check,length_check,self_data,opp_data,all_input,new_list):
    if(duplicacy_check is True and length_check is True):
    #    based_on_type(self_data,opp_data,all_input,new_list)
        print("ac")
    return "200"
final=actual_logic(duplicacy_check,length_check,self_data,opp_data,all_input,new_list)
win_total=based_on_type(self_data,opp_data,all_input,new_list,win)
print(all_input)
print(final)
print(type_based)
print(self_data)
print(win_total)