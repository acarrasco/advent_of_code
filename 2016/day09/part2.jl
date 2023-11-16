

MARKER_EXP = r"\([0-9]+x[0-9]+\)"
function countSize(compressed::AbstractString, acc::Int=0)::Int
    # println("compressed=$compressed, acc=$acc")
    m = match(MARKER_EXP, compressed)
    if m === nothing
        return acc + length(compressed)
    end
    sizeBeforeMarker = m.offset - 1
    repsLength, repsNumber = (parse(Int, x) for x in split(chop(m.match, head=1, tail=1), "x"))
    repeatedRegionSize = min(repsLength, length(compressed) - length(m.match) - sizeBeforeMarker)
    nextOffset = repeatedRegionSize + length(m.match) + sizeBeforeMarker
    repeatedOffset = m.offset + length(m.match)
    repeatedRegion = compressed[repeatedOffset:repeatedOffset + repeatedRegionSize - 1]
    repeatedSize = countSize(repeatedRegion) * repsNumber
    # println("repeatedRegion=$repeatedRegion repeatedSize=$repeatedSize")
    return countSize(chop(compressed, head=nextOffset, tail=0), acc + sizeBeforeMarker + repeatedSize)
end

# println(countSize("ADVENT") == 6)
# println(countSize("A(2x2)BCD(2x2)EFG") == 11)
# println(countSize("A(1x5)BC") == 7)
# println(countSize("(3x3)XYZ") == 9)
# println(countSize("(27x12)(20x12)(13x14)(7x10)(1x12)A") == 241920)
# println(countSize("X(8x2)(3x3)ABCY") == 20)
# println(countSize("(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN") == 445)

println(countSize(join(readlines())))