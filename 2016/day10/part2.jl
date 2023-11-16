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

function executeCommand(command::DistributionCommand, commandsBuffer::CommandsBuffer, heldChips::HeldChips, outputs)
    src = command.src
    chips = get(heldChips, src, missing => missing)
    if chips.first !== missing && chips.second !== missing
        heldChips[src] = missing => missing
        if command.low.first === BOT
            executeCommand(InputCommand(chips.first, command.low.second), commandsBuffer, heldChips, outputs)
        else
            outputs[command.low.second] = chips.first
        end

        if command.high.first === BOT
            executeCommand(InputCommand(chips.second, command.high.second), commandsBuffer, heldChips, outputs)
        else
            outputs[command.high.second] = chips.second
        end
    else
        push!(get!(commandsBuffer, src, []), command)
    end
end

function executeCommand(command::InputCommand, commandsBuffer::CommandsBuffer, heldChips::HeldChips, outputs)
    chips = get(heldChips, command.to, missing => missing)
    withAddedChip = addToPair(chips, command.value)
    heldChips[command.to] = withAddedChip

    if withAddedChip.first !== missing && withAddedChip.second !== missing
        commands = get(commandsBuffer, command.to, [])
        if length(commands) > 0
            executeCommand(popfirst!(commands), commandsBuffer, heldChips, outputs)
        end
    end
end

function executePlan(commands::AbstractArray{Command})
    commandsBuffer = CommandsBuffer()
    heldChips = HeldChips()
    outputs = Dict{Int, Int}()

    for command in commands
        executeCommand(command, commandsBuffer, heldChips, outputs)
    end
    return outputs[0] * outputs[1] * outputs[2]
end


commands::Vector{Command} = map(parseCommand, readlines())
println(executePlan(commands))