parse_int(x) = parse(Int, x)
parse_line(line) = map(parse_int, split(line))
parse_input(lines) = map(parse_line, lines)

function is_triangle(sides)
    a, b, c = sort(sides)
    return a + b > c
end

function count_valid_triangles(triangles)
    return sum(map(is_triangle, triangles))
end

triangles = parse_input(readlines())
result = count_valid_triangles(triangles)
println(result)