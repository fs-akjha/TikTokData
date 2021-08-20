# L = [str(x) for x in input("Enter multiple values\n").split(';')]
# print("\nThe values of input are", L)
# for i in L:
#   print(i.split('#'))
#   print(i.split('#')[0])
#   print(i.split('#')[-1])
#   print("   ")

no_of_lines = 2
lines = ""
new_lines=""
self_po=[]
all_input=[]
new_list=[]
self_data=[]
opp_data=[]
opponents=[]
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
    for data4 in opp_data:
        if(data3[0]):
            print(data3[0])
            print(data3[-1])
# for i in self_pokemons:
#     print(i)
#     print(i.split(';'))
