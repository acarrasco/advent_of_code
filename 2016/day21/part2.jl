# symmetric
function swapPositions(text::Vector{Char}, x::Int, y::Int)::Vector{Char}
    function destIndex(i::Int)::Int
        if i == x+1
            return y+1
        elseif i == y+1
            return x+1
        else
            return i
        end
    end
    return [text[destIndex(i)] for i = 1:length(text)]
end

# symmetric
function swapLetters(text::Vector{Char}, x::Char, y::Char)::Vector{Char}
    function destChar(c::Char)
        if c == x
            return y
        elseif c == y
            return x
        else
            return c
        end
    end
    return [destChar(c) for c in text]
end

# change direction
function rotateLeftInv(text::Vector{Char}, x::Int)::Vector{Char}
    return circshift(text, x)
end

# change direction
function rotateRightInv(text::Vector{Char}, x::Int)::Vector{Char}
    return circshift(text, -x)
end

# reverse engineered by applying the direct rotation and checking the destination index
INVERSE_ROTATION =[7, -1, 2, -2, 1, -3, 0, -4,]

function rotateBasedOnCharInv(text::Vector{Char}, x::Char)::Vector{Char}
    idx = first(indexin(x, text))
    return circshift(text, INVERSE_ROTATION[idx])
end

# symmetric
function reversePositions(text::Vector{Char}, x::Int, y::Int)::Vector{Char}
    return [text[1:x]; reverse(text[x+1:y+1]); text[y+2:length(text)]]
end

# swap arguments
function moveInv(text::Vector{Char}, x::Int, y::Int)::Vector{Char}
    res = copy(text)
    deleteat!(res, y+1)
    insert!(res, x+1, text[y+1])
    return res
end

SWAP_POSITIONS = r"swap position ([0-9]+) with position ([0-9]+)"
SWAP_LETTERS = r"swap letter ([a-zA-Z]) with letter ([a-zA-Z])"
ROTATE_LEFT = r"rotate left ([0-9]+) steps?"
ROTATE_RIGHT = r"rotate right ([0-9]+) steps?"
ROTATE_BASED_ON_CHAR = r"rotate based on position of letter (([a-zA-Z]))"
REVERSE_POSITIONS = r"reverse positions ([0-9]+) through ([0-9]+)"
MOVE = r"move position ([0-9]+) to position ([0-9]+)"

function reverseCommand(command::AbstractString, text::Vector{Char})::Vector{Char}
    m = match(SWAP_POSITIONS, command)
    if m !== nothing
        x = parse(Int, m.captures[1])
        y = parse(Int, m.captures[2])
        return swapPositions(text, x, y)
    end

    m = match(SWAP_LETTERS, command)
    if m !== nothing
        x = m.captures[1][1]
        y = m.captures[2][1]
        return swapLetters(text, x, y)
    end

    m = match(ROTATE_LEFT, command)
    if m !== nothing
        x = parse(Int, m.captures[1])
        return rotateLeftInv(text, x)
    end

    m = match(ROTATE_RIGHT, command)
    if m !== nothing
        x = parse(Int, m.captures[1])
        return rotateRightInv(text, x)
    end

    m = match(ROTATE_BASED_ON_CHAR, command)
    if m !== nothing
        x = m.captures[1][1]
        return rotateBasedOnCharInv(text, x)
    end

    m = match(REVERSE_POSITIONS, command)
    if m !== nothing
        x = parse(Int, m.captures[1])
        y = parse(Int, m.captures[2])
        return reversePositions(text, x, y)
    end

    m = match(MOVE, command)
    if m !== nothing
        x = parse(Int, m.captures[1])
        y = parse(Int, m.captures[2])
        return moveInv(text, x, y)
    end

    return text
end

function solve(start::AbstractString, commands::Vector{String})::String
    text = [c for c in start]
    for command in reverse(commands)
        text = reverseCommand(command, text)
    end
    return join(text)
end

commands = readlines()
println(solve("fbgdceah", commands))