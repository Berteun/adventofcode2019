from collections import defaultdict 
orbits = defaultdict(list)

dist = {
    0 : ["COM"]
}

f = open("input_day06.txt")
#f = open("example.txt")
for l in f:
    center, orbit = l.strip().split(')')
    orbits[center].append(orbit)

d = 0
while d in dist and dist[d]:
    centers = dist[d]
    dist[d + 1] = []
    for c in centers:
        for o in orbits[c]:
            dist[d + 1].append(o)
    d += 1

print(sum(d * len(dist[d]) for d in dist))
