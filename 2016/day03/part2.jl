using DelimitedFiles

function parse_input(input)
   mat = readdlm(input, Int)
   size = length(mat)
   return reshape(mat, 3, Int(size // 3))
end

function is_triangle(sides)
    a, b, c = sort(sides)
    return a + b > c
end

count_valid_triangles(triangles) = sum(map(is_triangle, eachcol(triangles)))

triangles = parse_input(stdin)
result = count_valid_triangles(triangles)
println(result)