# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 15:04:34 2017

@author: HRUDAY KUMAR
"""

import sys
import operator
import copy

def all_plays(player,play,current_plays):
    current_plays = copy.deepcopy(current_plays)
    data = [play[1],player]
    current_plays[play[0]] = data
    return current_plays
    

def arc_consistency_check(child,current_plays):
    child_colors_list=set()
    unavailable_colors=set()   
    acceptable_colors = set(colors)
    for children in graph[child]:
        if children in current_plays:
            if current_plays[children][0] in acceptable_colors:
                unavailable_colors.add(current_plays[children][0])
                #acceptable_colors.remove(current_plays[children][0])
    acceptable_colors = acceptable_colors-unavailable_colors
    for color in acceptable_colors:
        child_colors_list.add((child,color))
    return set(child_colors_list) 

def terminal_score(current_plays):
    score = 0
    for play in current_plays.values():
        player = int(play[1])
        color = str(play[0])
        if player == 1:
            current_score = P1_color_rating[color]
            score = score + current_score
        if player == 2:
            current_score = P2_color_rating[color]
            score = score - current_score
    return score

def min_value(current_plays,alpha,beta,depth,actions,lastNode,lastColor):
    terminal=0
    plays = set()
    visited = set()
    for node in current_plays.keys():
        for child in graph[node]:
            if child not in current_plays.keys() and child not in visited:
                visited.add(child)
                possible_plays = arc_consistency_check(child,current_plays)
                plays = plays.union(possible_plays)
    plays_list = sorted(list(plays), key = operator.itemgetter(0,1))
    if len(plays_list)==0:
        terminal=1
    else:
        terminal =0  
    
    if depth == height or terminal==1:
        v = terminal_score(current_plays)
        action_occured =  str(lastNode)+', '+str(lastColor)+', '+str(depth)+', '+str(v)+', '+str(alpha)+', '+str(beta)+'\n'
        trace_log.append(action_occured)
        #output.write(action_occured)
        return v
    v = maxInt
    for play in plays_list:
        action_occured =  str(lastNode)+', '+str(lastColor)+', '+str(depth)+', '+str(v)+', '+str(alpha)+', '+str(beta)+'\n'
        trace_log.append(action_occured)
        #output.write(action_occured)
        v = min(v,max_value(all_plays(2,play,current_plays),alpha,beta,depth+1,{},play[0],play[1]))
        if v in actions:
            previous_action = actions[v]
            if (previous_action[0],previous_action[1])<(play[0],play[1]):
                pass
        else:
            actions[v] = play
        if v<=alpha:
            break
        beta = min(v,beta)
    action_occured =  str(lastNode)+', '+str(lastColor)+', '+str(depth)+', '+str(v)+', '+str(alpha)+', '+str(beta)+'\n'
    trace_log.append(action_occured)
    #output.write(action_occured)
    return v
    
def max_value(current_plays,alpha,beta,depth,actions,lastNode,lastColor):
    terminal=0
    plays = set()
    visited = set()
    for node in current_plays.keys():
        for child in graph[node]:
            if child not in current_plays.keys() and child not in visited:
                visited.add(child)
                possible_plays = arc_consistency_check(child,current_plays)
                plays = plays.union(possible_plays)
    plays_list = sorted(list(plays), key = operator.itemgetter(0,1))
    if len(plays_list)==0:
        terminal=1
    else:
        terminal =0
    if depth == height or terminal==1:
    
        v = terminal_score(current_plays)
        action_occured =  str(lastNode)+', '+str(lastColor)+', '+str(depth)+', '+str(v)+', '+str(alpha)+', '+str(beta)+'\n'
        trace_log.append(action_occured)
     #   output.write(action_occured)
        return v
    v = minInt
    for play in plays_list:
        action_occured =  str(lastNode)+', '+str(lastColor)+', '+str(depth)+', '+str(v)+', '+str(alpha)+', '+str(beta)+'\n'
        trace_log.append(action_occured)
      #  output.write(action_occured)
        v = max(min_value(all_plays(1,play,current_plays),alpha,beta,depth+1,{},play[0],play[1]),v)
    
        if v in actions:
            previous_action = actions[v]
            if (previous_action[0],previous_action[1])<(play[0],play[1]):
                pass
        else:
            actions[v] = play
        if v>=beta:
            break
        alpha = max(v,alpha)
    action_occured =  str(lastNode)+', '+str(lastColor)+', '+str(depth)+', '+str(v)+', '+str(alpha)+', '+str(beta)+'\n'
    trace_log.append(action_occured)
    #output.write(action_occured)
    return v
        
def alpha_beta(current_plays,lastNode,lastColor):
    actions = {}
    v = max_value(current_plays,minInt,maxInt,0,actions,lastNode,lastColor)
    final_result = str(actions[v][0])+', '+str(actions[v][1])+', '+str(v)
    trace_log.append(final_result)
    return trace_log
    #output.write(final_result)    

#path = sys.argv[2]
path = 't5.txt'
plays = {}
P1_color_rating = {}
P2_color_rating = {}
graph={}
lastNode = ''
lastColor = ''
trace_log=[]

maxInt = float('inf')
minInt = float('-inf')

with open(path,'r') as data:
    lines = data.readlines()
colors = lines[0].strip().split(', ')

givenPlays = lines[1].strip().split(', ')
for move in givenPlays:
    node = move.split(': ')[0]
    choice = move.split(': ')[1].split('-')
    plays[node] = choice
    lastNode = node
    lastColor = choice[0]

height = int(lines[2])

scoreP1 = lines[3].strip().split(', ')
for each in scoreP1:
    P1_color_rating[each.split(': ')[0]] = int(each.split(': ')[1])
scoreP2 = lines[4].strip().split(', ')
for each in scoreP2:
    P2_color_rating[each.split(': ')[0]] = int(each.split(': ')[1])

for i in range (5,len(lines)):
    node = lines[i].strip().split(': ')[0]
    neighbors = lines[i].strip().split(': ')[1].split(', ')
    graph[node] = neighbors
output = open('output.txt','w')
logs = alpha_beta(plays,lastNode,lastColor)
for log in logs:
    output.write(log)
output.close()