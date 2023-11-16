BOT = Val(:bot)
OUTPUT = Val(:output)

DestinationType = Union{typeof(BOT), typeof(OUTPUT)}
Destination = Pair{DestinationType, Int}

struct DistributionCommand
    src::Int
    low::Destination
    high::Destination
end

struct InputCommand
    value::Int
    to::Int
end

Command = Union{DistributionCommand, InputCommand}

destinationExp = "(bot|output) ([0-9]+)"
distributionExp = Regex("bot ([0-9]+) gives low to $destinationExp and high to $destinationExp")
inputExp = r"value ([0-9]+) goes to bot ([0-9]+)"

CommandsBuffer = Dict{Int, Vector{Command}}

ChipPair = Union{Pair{Missing, Missing}, Pair{Int, Missing}, Pair{Int, Int}}

HeldChips = Dict{Int, ChipPair}

function parseDestination(destType::AbstractString, destNumber::AbstractString)::Destination
    if destType == "bot"
        return BOT => parse(Int, destNumber)
    elseif destType == "output"
        return OUTPUT => parse(Int, destNumber)
    else
        error("Invalid destination type <$destType>")
    end
end

function parseDistribution(line::AbstractString)::Union{Command, Missing}
    m = match(distributionExp, line)
    if m !== nothing
        src = parse(Int, m.captures[1])
        low = parseDestination(m.captures[2], m.captures[3])
        high = parseDestination(m.captures[4], m.captures[5])
        return DistributionCommand(src, low, high)
    end
    return missing
end

function parseInput(line::AbstractString)::Union{Command, Missing}
    m = match(inputExp, line)
    if m !== nothing
        value = parse(Int, m.captures[1])
        to = parse(Int, m.captures[2])
        return InputCommand(value, to)
    end
    return missing
end

function parseCommand(line::AbstractString)::Command
    return coalesce(parseDistribution(line),  parseInput(line))
end

addToPair(pair::Pair{Missing, Missing}, chip::Int)::ChipPair = chip => missing
addToPair(pair::Pair{Int, Missing}, chip::Int)::ChipPair = if pair.first < chip pair.first => chip else chip => pair.first end

function executeCommand(command::DistributionCommand, commandsBuffer::CommandsBuffer, heldChips::HeldChips, condition)
    src = command.src
    chips = get(heldChips, src, missing => missing)
    if chips.first !== missing && chips.second !== missing
        if condition(chips.first, chips.second)
            return command.src
        end
        heldChips[src] = missing => missing
        if command.low.first === BOT
            res = executeCommand(InputCommand(chips.first, command.low.second), commandsBuffer, heldChips, condition)
            if res !== nothing
                return res
            end
        end
        if command.high.first === BOT
            res = executeCommand(InputCommand(chips.second, command.high.second), commandsBuffer, heldChips, condition)
            if res !== nothing
                return res
            end
        end
    else
        push!(get!(commandsBuffer, src, []), command)
    end
    return nothing
end

function executeCommand(command::InputCommand, commandsBuffer::CommandsBuffer, heldChips::HeldChips, condition)
    chips = get(heldChips, command.to, missing => missing)
    withAddedChip = addToPair(chips, command.value)
    heldChips[command.to] = withAddedChip

    if withAddedChip.first !== missing && withAddedChip.second !== missing
        commands = get(commandsBuffer, command.to, [])
        if length(commands) > 0
            return executeCommand(popfirst!(commands), commandsBuffer, heldChips, condition)
        end
    end
    return nothing
end

function check(x, y)
    return x == 17 && y == 61
end

function executePlan(commands::AbstractArray{Command}, condition)
    commandsBuffer = CommandsBuffer()
    heldChips = HeldChips()

    for command in commands
        res = executeCommand(command, commandsBuffer, heldChips, condition)
        if res !== nothing
            return res
        end
    end
end


commands::Vector{Command} = map(parseCommand, readlines())
println(executePlan(commands, check))