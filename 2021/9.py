from aocd import get_data
import yaml
import numpy as np
import copy


with open("config.yaml", "r") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

S = config["SESSION_COOKIES"]["HOME"]
day_nine = get_data(session=S, day=9, year=2021)

heightmap = np.array(([list(x) for x in day_nine.split('\n')]))

_map = []
for _input in heightmap:
    _map.append(list(map(int, _input)))

inputs = [
    '2199943210',
    '3987894921',
    '9856789892',
    '8767896789',
    '9899965678']
    
tst = []
for _input in inputs:
    tst.append(list(map(int, _input)))

def neighbuors(input_map: list, i, j):
    nghb = []
    
    # check to not cross bottom edge and append lower neighbour
    if i+1 < len(input_map):
        nghb.append(input_map[i+1][j])
    # check to not cross upper edge and append upper neighbour
    if i-1 >= 0:
        nghb.append(input_map[i-1][j])
    # check to not cross right edge and append right neighbour
    if j+1 < len(input_map[i]):
        nghb.append(input_map[i][j+1])
    # check to not cross left edge and append left neighbour
    if j-1 >= 0:
        nghb.append(input_map[i][j-1])
        
    return nghb
        
neighbuors(tst, 1, 1)

def lowest(input_map: list):
    result = 0
    
    # go through all points
    for i in range(len(input_map)):
        for j in range(len(input_map[i])):
            
            # check that the current point is the smallest of its neighbours
            if input_map[i][j] < min(neighbuors(input_map, i, j)):
                result += 1 + input_map[i][j]
                
    return result

lowest(tst)

print("The sum of the risk levels of all low points on heightmap equals:", lowest(_map))

# We will be grouping by counting the number neighbours that are not 9 or
# over the edge for example [2,1,3,4] suggest that we have 4 groups with 2,1,3,4 members respectively
groups = []
def count_gr(temp: list, i, j):
    # break the loop if index is over the edge or on point equal 9 or already visited, i.e. equal to -1
    if i < 0 or i >= len(temp) or j <0 or j >= len(temp[i]) or temp[i][j] == 9 or temp[i][j] == -1:
        return
    
    # mark current point as visited
    temp[i][j] = -1
    # add mark (+1) to the last point from group
    groups[len(groups)-1] += 1
    # check same above condition for ALL neighbours to count if there is more of none nines
    count_gr(temp, i+1, j)
    count_gr(temp, i-1, j)
    count_gr(temp, i, j+1)
    count_gr(temp, i, j-1)

temp = copy.deepcopy(tst)
# go through all points in matrix
for i in range(len(temp)):
    for j in range(len(temp[i])):
        groups.append(0)
        count_gr(temp, i, j)

temp
# multiple three largest groups members like dot product
np.prod(sorted([x for x in groups if x != 0], reverse=True)[:3])

groups = []
temp = copy.deepcopy(_map)
for i in range(len(temp)):
    for j in range(len(temp[i])):
        groups.append(0)
        count_gr(temp, i, j)
        
print("The sum of the risk levels of all low points on heightmap equals:",
      np.prod(sorted([x for x in groups if x != 0], reverse=True)[:3]))
