# -*- coding: utf-8 -*-
"""
Created on Tue Jul 15 17:02:56 2014

@author: Milad
"""
import simplejson

t = []  
with open("parsed_tweets.txt","r") as readfile:
    readfile.readline()
    for line in readfile:
        l = line.split("\t")
        #grab records that have both source and dest cities and non-zero sent
        if l[3] != "None" and l[4] != "None" and float(l[6].rstrip("\n")) != 0:
                t.append([l[3],l[4],l[6].rstrip("\n")])

#build list of cities with only pos or neg sentiments
cities = []
for tup in t:
    cities.append(tup[0])
    cities.append(tup[1])
    cities = list(set(cities))

#order cities using ordered_cities.txt
quad = {}
cities_dict = {}
count = 0
with open("ordered_cities.txt","r") as readfile:
    for line in readfile:
        quad[line.split(",")[0].lower()] = line.split(",")[1][0:2]
        cities_dict[line.split(",")[0].lower()] = count
        count += 1
        
cities = sorted(cities, key=lambda word: [cities_dict[word]])

#build pos and neg matrices
matrix_pos = []
matrix_neg = []
#matrix2 = []
for i in cities:
    mp, mn = [], []
    #m2 = []
    for j in cities:
        count_pos, count_neg = 0, 0
        #sent_total = 0.0
        for tup in t:
            if tup[0] == i and tup[1] == j:
                if float(tup[2]) > 0:
                    count_pos += 1
                elif float(tup[2]) < 0:
                    count_neg += 1
                    
                #sent_total += float(tup[2])
        mp.append(count_pos)
        mn.append(count_neg)
        
    matrix_pos.append(mp)
    matrix_neg.append(mn)
    #matrix2.append(m2)

#normalize pos and neg matrices
total_vol_pos = sum(matrix_pos)
total_vol_neg = sum(matrix_neg)


for i in range(len(matrix_pos)):
    for j in range(len(matrix_pos[i])):
        matrix_pos[i][j] = float(matrix_pos[i][j])/total_vol_pos

for i in range(len(matrix_neg)):
    for j in range(len(matrix_neg[i])):
        matrix_neg[i][j] = float(matrix_neg[i][j])/total_vol_neg
        
#save to json file
with open("matrix_pos.json","w") as writefile:
    simplejson.dump(matrix_pos, writefile)

with open("matrix_neg.json","w") as writefile:
    simplejson.dump(matrix_neg, writefile)
    
with open("cities.csv","w") as writefile:
    writefile.write("name,quad,ind\n")
    new = False
    count = 0
    for i in range(len(cities)):
        writefile.write(cities[i]+","+quad[cities[i]]+","+str(count)+"\n")

        if i<len(cities)-1 and quad[cities[i]] != quad[cities[i+1]]:
            new = True
        if new:
            count = 0
            new = False
        else:
            count += 1          
            