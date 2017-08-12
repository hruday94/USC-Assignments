import sys
import collections
import Queue as q
import operator

path1 = sys.argv[2]

search_type = ''
budget = 0
start_state = ''
destination_state = ''
graph = []
line_count =0
graph_dict = {}

def BFS(graph, start,goal,budget):
    explored =[start]
    queue=[start]
    visited=[start]
    
    fuel_left = budget
    while queue:
        nodes = queue.pop(0)
        root = nodes[-1][0]
        if root not in explored and visited:
            explored.append(root)
        if root==goal:
            fuel_left = budget
            for i in range(len(nodes)-1):
                if fuel_left != 0:
                    source = nodes[i]
                    dest = nodes[i+1]
                    fuel =0
                    for each in graph[source]:
                        if each[0]==dest:
                            fuel = each[1]
                    fuel_left = int(fuel_left)-int(fuel)
            if fuel_left < 0:
                continue
            else:
                return((nodes,fuel_left))
        else:
            fill=[]
            for node in graph[root[0]]:
                if node[0] not in visited:
                    fill.append(node[0])
                    visited.append(node[0])
                if node[0]==goal:
                    fill.append(node[0])
            fill.sort()
           
            for x in fill:
                if x not in explored:
                   route = list(nodes)
                   route.append(x)
                   queue.append(route)
        
def DFS(graph, start,goal,budget):
    explored =[start]
    queue=[start]
    while queue:
        nodes = queue.pop(0)
        root = nodes[-1][0]
        if root not in explored:
            explored.append(root)
        if root==goal:
            fuel_left = budget
            for i in range(len(nodes)-1):
                if fuel_left != 0:
                    source = nodes[i]
                    dest = nodes[i+1]
                    fuel =0
                    for each in graph[source]:
                        if each[0]==dest:
                            fuel = each[1]
                    fuel_left = int(fuel_left)-int(fuel)
            if fuel_left < 0:
                continue
            else:
                return(nodes,fuel_left)
        else:
            fill=[]
            for node in graph[root[0]]:
               fill.append(node[0])
            fill.sort(reverse=True)
            for x in fill:
                if x not in explored:
                   route = list(nodes)
                   route.append(x)
                   queue.insert(0,route)

def UCS(graph, start,goal,budget):
    queue = q.PriorityQueue()
    explored =[start]
    visited=[start]
    queue.put((0,[start]))
    budget = int(budget)
    costs={}
    while queue:
        #print (budget)
        cost,nodes = queue.get()
        if cost ==0 :
            cost = cost
        else:
            cost = int(budget)+cost
        
        root = nodes[-1]
        if root not in explored:
            explored.append(root)
        if root==goal:
            fuel_left=budget
            for i in range(len(nodes)-1):
                if fuel_left!=0:
                    source = nodes[i]
                    
                    dest = nodes[i+1]
                  
                    fuel = 0
                    for each in graph[source]:
                        if each[0]==dest:
                            fuel = each[1]
                    fuel_left = int(fuel_left)-int(fuel)
            if fuel_left<0:
                continue
            else:
                return(nodes,fuel_left)
        else:
            fill=[]
            leaves =  sorted(graph[root],key=lambda x: x[1])
            for node in leaves:
                fill.append(node[0])

            for x in fill:
               
                if x not in explored:
                    if x not in visited:
                        visited.append(x)
                        print (x)
                        route = list(nodes)
                        route.append(x)
                        path_cost=0
                        for each in graph[root]:
                            if each[0]==x:
                                path_cost = each[1]
                  #  print (cost)
                        t_cost = (int(cost)+ int(path_cost))-int(budget)
                        costs[x] = t_cost
                    #t_cost = t_cost-int(budget)
                        queue.put((t_cost,route))
                        print (costs)
                    else:
                        route = list(nodes)
                        route.append(x)
                        path_cost=0
                        for each in graph[root]:
                            if each[0]==x:
                                path_cost = each[1]
                  #  print (cost)
                        t_cost = (int(cost)+ int(path_cost))-int(budget)
                        if t_cost<costs[x]:
                            costs[x] = t_cost
                            queue.put((t_cost,route))
                            
                    
            print (sorted(queue.queue,key=lambda x: len(x[1])))
                    
    
        

        
with open(path1,'r') as data:
    lines = data.readlines()
    search_type = lines[0].strip()
    print (search_type)
    budget = lines[1].strip()
    start_state = lines[2].strip()
    destination_state = lines[3].strip()

    for i in range(4,len(lines)):
        graph.append(lines[i].strip())
    

    for branch in graph:
        chil = []
        branch = branch.replace(':','').strip()
        root = branch.split()[0]
        #root = branch[0]
        children = branch.split()[1:]
        #children = children.split(',')
        for child in children:
            child = child.split('-')
            child =  ((child[0].strip(),child[1].strip(',')))
            chil.append(child)
        graph_dict[root] = chil
    print (graph_dict)
    
    output = open('output.txt','w')
    if search_type=='BFS':
        result =  (BFS(graph_dict,start_state,destination_state,budget))
        if result is None:
            output.write("No Path")
        else:
            path = result[0][0]
            for i in range(1,len(result[0])):
                path = path +'-'+result[0][i]
            answer = path + ' '+str(result[1])
            output.write (answer)
        
                
        
    if search_type=='DFS':
        result =(DFS(graph_dict,start_state,destination_state,budget))
        #print (result)
        if result is None:
            output.write("No Path")
        else:
            path = result[0][0]
            for i in range(1,len(result[0])):
                path = path +'-'+result[0][i]
            answer = path + ' '+str(result[1])
            output.write (answer)
    if search_type=='UCS':
        result = (UCS(graph_dict,start_state,destination_state,budget))
        if result is None:
            output.write("No Path")
        else:
            path = result[0][0]
            for i in range(1,len(result[0])):
                path = path +'-'+result[0][i]
            answer = path + ' '+str(result[1])
            output.write (answer)
            
    output.close()
    
            
        
