from collections import defaultdict 
orbits = defaultdict(list)

dist = {
    0 : ["COM"]
}


parent = {} 

f = open("input_day06.txt")
#f = open("example2.txt")
for l in f:
    center, orbit = l.strip().split(')')
    parent[orbit] = center
    orbits[center].append(orbit)

d = 0
while d in dist and dist[d]:
    centers = dist[d]
    dist[d + 1] = []
    for c in centers:
        for o in orbits[c]:
            dist[d + 1].append(o)
    d += 1
    
path = ["YOU"]
while path[-1] in parent:
    path.append(parent[path[-1]])

path.reverse()

spath = ["SAN"]
while spath[-1] in parent:
    spath.append(parent[spath[-1]])

spath.reverse()

prefix = 0
while path[prefix] == spath[prefix]:
    print(path[prefix], spath[prefix])
    prefix += 1

print(len(spath) - prefix + len(path) - prefix - 2)
