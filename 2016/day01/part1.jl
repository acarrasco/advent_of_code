movements = split(readline(), ", ")

distances = [0, 0, 0, 0]
direction = 1

for m in movements
    turn = if m[1] == 'R' 1 else -1 end
    distance_txt = chop(m, head=1, tail=0)
    distance = parse(Int64, distance_txt, base=10)
    global direction = mod(direction + turn, 4)
    distances[direction + 1] += distance
end

result = abs(distances[1] - distances[3]) + abs(distances[2] - distances[4])

println(result)