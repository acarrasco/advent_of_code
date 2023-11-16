

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
    repeatedSize = repeatedRegionSize * repsNumber
    return countSize(chop(compressed, head=nextOffset, tail=0), acc + sizeBeforeMarker + repeatedSize)
end

# println(countSize("ADVENT") == 6)
# println(countSize("A(2x2)BCD(2x2)EFG") == 11)
# println(countSize("A(1x5)BC") == 7)
# println(countSize("(3x3)XYZ") == 9)
# println(countSize("(6x1)(1x3)A") == 6)
# println(countSize("X(8x2)(3x3)ABCY") == 18)

println(countSize(join(readlines())))