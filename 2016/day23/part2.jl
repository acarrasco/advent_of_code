## common regular expression patterns

LITERAL_EXP = "-?[0-9]+"
REGISTER_EXP = "[abcd]"
RVALUE_EXP = "$LITERAL_EXP|$REGISTER_EXP"

## common types

Optional{T} = Union{T, Nothing}

# a register reference or a literal
RValue = Union{Char, Int}

# a register reference
LValue = Char

function isRegister(_::Char)::Bool
    return true
end
function isRegister(_::Int)::Bool
    return false
end

######################
# INSTRUCTIONS TYPES #
######################

## native 
struct Cpy
    src::RValue
    dst::RValue # for compatibility with toggled jnz
end

struct Inc
    dst::RValue # for compatiblity with toggled tgl
end

struct Dec
    dst::RValue # for compatiblity with toggled tgl
end

struct Jnz
    cond::RValue
    offset::RValue
end

struct Tgl
    offset::RValue 
end

## optimized instructions 
struct Add
    val::LValue
    dst::LValue
end

struct Sub
    val::LValue
    dst::LValue
end

struct AddMul
    m1::LValue
    m2::LValue
    dst::LValue
end

struct SubMul
    m1::LValue
    m2::LValue
    dst::LValue
end

Instruction = Union{
    Cpy,
    Inc,
    Dec,
    Jnz,
    Tgl,
    # optimized insructions
    Add,
    Sub,
    AddMul,
    SubMul,
}

#######################
# INSTRUCTION PARSERS #
#######################

CPY_EXP = Regex("cpy ($RVALUE_EXP) ($REGISTER_EXP)")

function parseCpy(text::AbstractString)::Optional{Cpy}
    m = match(CPY_EXP, text)
    if m !== nothing
        src = parseRValue(m.captures[1])
        dst = m.captures[2][1]
        return Cpy(src, dst)
    end
end


INC_EXP = Regex("inc ($REGISTER_EXP)")

function parseInc(text::AbstractString)::Optional{Inc}
    m = match(INC_EXP, text)
    if m !== nothing
        dst = m.captures[1][1]
        return Inc(dst)
    end
end


DEC_EXP = Regex("dec ($REGISTER_EXP)")

function parseDec(text::AbstractString)::Optional{Dec}
    m = match(DEC_EXP, text)
    if m !== nothing
        dst = m.captures[1][1]
        return Dec(dst)
    end
end


JNZ_EXP = Regex("jnz ($RVALUE_EXP) ($RVALUE_EXP)")

function parseJnz(text::AbstractString)::Optional{Jnz}
    m = match(JNZ_EXP, text)
    if m !== nothing
        cond = parseRValue(m.captures[1])
        offset = parseRValue(m.captures[2])
        return Jnz(cond, offset)
    end
end


TGL_EXP = Regex("tgl ($RVALUE_EXP)")

function parseTgl(text::AbstractString)::Optional{Tgl}
    m = match(TGL_EXP, text)
    if m !== nothing
        offset = parseRValue(m.captures[1])
        return Tgl(offset)
    end
end


function parseRValue(repr::AbstractString)::RValue
    if length(repr) == 1 && repr[1] in "abcd"
        return repr[1]
    else
        return parse(Int, repr)
    end
end


function parseInstruction(text::AbstractString)::Instruction
    for f in (parseCpy, parseDec, parseInc, parseJnz, parseTgl)
        instruction = f(text)
        if instruction !== nothing
            return instruction
        end
    end
    error("Invalid instruction <$text>") 
end

#########################
# INSTRUCTION EXECUTION #
#########################

## common
mutable struct State
    ic::Int
    registers::Dict{Char, Int}
    instructions::Vector{Instruction}
    optimized::Dict{Int, Instruction} # this is an overlay of Add and AddMul instructions 
end

function valueOf(register::Char, state::State)::Int
    return state.registers[register]
end

function valueOf(literal::Int, _)::Int
    return literal
end

## instructions

function exec!(instruction::Cpy, state::State)
    if isRegister(instruction.dst)
        state.registers[instruction.dst] = valueOf(instruction.src, state)
    end
    state.ic += 1
end

function exec!(instruction::Inc, state::State)
    if isRegister(instruction.dst)
        state.registers[instruction.dst] += 1
    end
    state.ic += 1
end

function exec!(instruction::Dec, state::State)
    if isRegister(instruction.dst)
        state.registers[instruction.dst] -= 1
    end
    state.ic += 1
end

function exec!(instruction::Jnz, state::State)
    if valueOf(instruction.cond, state) != 0
        state.ic += valueOf(instruction.offset, state)
    else
        state.ic += 1
    end
end

function exec!(instruction::Tgl, state::State)
    function toggle(instruction::Inc)::Instruction
        return Dec(instruction.dst)
    end
    
    function toggle(instruction::Dec)::Instruction
        return Inc(instruction.dst)
    end
    
    function toggle(instruction::Jnz)::Instruction
        return Cpy(instruction.cond, instruction.offset)
    end
    
    function toggle(instruction::Cpy)::Instruction
        return Jnz(instruction.src, instruction.dst)
    end
    
    function toggle(instruction::Tgl)::Instruction
        return Inc(instruction.offset)
    end

    targetAddress = state.ic + valueOf(instruction.offset, state)
    if 0 < targetAddress <= length(state.instructions)
        target = state.instructions[targetAddress]
        state.instructions[targetAddress] = toggle(target)
    end
    # the previously optimized code might be invalid.
    # we could be a bit smarter and check if it is necessary, but whatevs
    state.optimized = optimize(state.instructions)
    state.ic += 1
end

# optimized instructions:
# they set the temporary registers to 0 and skip unoptimized instructions

function exec!(instruction::Add, state::State)
    state.registers[instruction.dst] += abs(valueOf(instruction.val, state))
    state.registers[instruction.val] = 0
    state.ic += 3
end

function exec!(instruction::Sub, state::State)
    state.registers[instruction.dst] -= abs(valueOf(instruction.val, state))
    state.registers[instruction.val] = 0
    state.ic += 3
end

function exec!(instruction::AddMul, state::State)
    m1 = abs(valueOf(instruction.m1, state))
    m2 = abs(valueOf(instruction.m2, state))
    state.registers[instruction.dst] += m1 * m2
    state.registers[instruction.m1] = 0
    state.registers[instruction.m2] = 0
    state.ic += 5 # we are overlaying after the cpy, so we still jump after the jnz
end

function exec!(instruction::SubMul, state::State)
    m1 = abs(valueOf(instruction.m1, state))
    m2 = abs(valueOf(instruction.m2, state))
    state.registers[instruction.dst] -= m1 * m2
    state.registers[instruction.m1] = 0
    state.registers[instruction.m2] = 0
    state.ic += 5 # we are overlaying after the cpy, so we still jump after the jnz
end

function printState(state::State)
    reg = join(("$r=$(state.registers[r])" for r in "abcd"), ", ")
    println("ic: $(state.ic) ins:$(state.instructions[state.ic]) reg:$reg")
end

function onlyOrNothing(seq)
    try return only(seq)
    catch end
end

function optimizeAdditive(segment::Vector{Instruction})::Optional{Add}
    a, b, j = segment
    dstMutIns = onlyOrNothing(i for i in (a, b) if i.dst != j.cond)
    counterMutInt = onlyOrNothing(i for i in (a, b) if i.dst == j.cond)
    if typeof(dstMutIns) == Inc
        Op = Add
    elseif typeof(dstMutIns) == Dec
        Op = Sub
    else
        return
    end
    # we trust the counter mutation instruction will go in the right direction
    # if we wanted to check it we should add that info to the instruction and
    # fail at runtime if the the mutation for the counter is Inc and counter is >= 0
    # or if the mutation of the counter is Dec and the counter is <= 0
    return Op(counterMutInt.dst, dstMutIns.dst)
end

function optimizeMultiplicative(segment::Vector{Instruction})::Optional{AddMul}
    a, b, c, d, e, j = segment
    additiveInstruction = onlyOrNothing(i for i in (a, b, c, d, e) if typeof(i) in (Add, Sub))
    if typeof(additiveInstruction) == Add
        Op = AddMul
    elseif typeof(additiveInstruction) == Sub
        Op = SubMul
    else
        return
    end
    if typeof(a) !== Cpy
        return
    end
    dst = additiveInstruction.dst
    m1 = j.cond
    m2 = additiveInstruction.val
    return Op(m1, m2, dst)
end

function optimizeInstruction!(
    instruction::Jnz,
    idx::Int,
    instructions::Vector{Instruction},
    optimized::Dict{Int, Instruction})

    offset = instruction.offset
    if offset == -2
        # add an addition to the overlay if necessary
        opt = optimizeAdditive(instructions[idx+offset:idx])
        if opt !== nothing
            optimized[idx+offset] = opt
        end
    elseif offset == -5
        overlaid = Vector{Instruction}()
        for i = idx+offset:idx
            push!(overlaid, get(optimized, i, instructions[i]))
        end
        opt = optimizeMultiplicative(overlaid)
        if opt !== nothing
            # we overlay the instruction after the cpy
            optimized[idx+offset+1] = opt
        end
    end
end

function optimizeInstruction!(
    _,
    idx::Int,
    instructions::Vector{Instruction},
    optimized::Dict{Int, Instruction})
    # instructions other than JNZ are not optimized
end

function optimize(instructions::Vector{Instruction})::Dict{Int, Instruction}
    optimized = Dict{Int, Instruction}()
    for (i, ins) in enumerate(instructions)
        optimizeInstruction!(ins, i, instructions, optimized)
    end
    return optimized
end

function step!(state::State)
    # printState(state)
    instruction = get(state.optimized, state.ic, state.instructions[state.ic])
    exec!(instruction, state)
end

function run(lines::Vector{String}, input::Int)
    instructions::Vector{Instruction} = map(parseInstruction, lines)
    state = State(
        1, 
        Dict(
            'a' => input,
            'b' => 0,
            'c' => 0,
            'd' => 0,
        ),
        instructions,
        optimize(instructions),
    )

    while state.ic <= length(lines)
        step!(state)
    end

    return state.registers['a']
end
lines = readlines()
println(run(lines, 12))