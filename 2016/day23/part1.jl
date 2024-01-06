## common regular expression patterns

LITERAL_EXP = "-?[0-9]+"
REGISTER_EXP = "[abcd]"
RVALUE_EXP = "$LITERAL_EXP|$REGISTER_EXP"

## common types

Optional{T} = Union{T, Nothing}

# a register or a literal
RValue = Union{Char, Int}

# a register
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

struct CpyInstruction
    src::RValue
    dst::RValue # for compatibility with toggled tgl
end

struct IncInstruction
    dst::RValue # for compatiblity with toggled tgl
end

struct DecInstruction
    dst::RValue # for compatiblity with toggled tgl
end

struct JnzInstruction
    cond::RValue
    offset::RValue
end

struct TglInstruction
    offset::RValue 
end 

Instruction = Union{
    CpyInstruction,
    IncInstruction,
    DecInstruction,
    JnzInstruction,
    TglInstruction,
}

#######################
# INSTRUCTION PARSERS #
#######################

CPY_EXP = Regex("cpy ($RVALUE_EXP) ($REGISTER_EXP)")

function parseCpy(text::AbstractString)::Optional{CpyInstruction}
    m = match(CPY_EXP, text)
    if m !== nothing
        src = parseRValue(m.captures[1])
        dst = m.captures[2][1]
        return CpyInstruction(src, dst)
    end
end


INC_EXP = Regex("inc ($REGISTER_EXP)")

function parseInc(text::AbstractString)::Optional{IncInstruction}
    m = match(INC_EXP, text)
    if m !== nothing
        dst = m.captures[1][1]
        return IncInstruction(dst)
    end
end


DEC_EXP = Regex("dec ($REGISTER_EXP)")

function parseDec(text::AbstractString)::Optional{DecInstruction}
    m = match(DEC_EXP, text)
    if m !== nothing
        dst = m.captures[1][1]
        return DecInstruction(dst)
    end
end


JNZ_EXP = Regex("jnz ($RVALUE_EXP) ($RVALUE_EXP)")

function parseJnz(text::AbstractString)::Optional{JnzInstruction}
    m = match(JNZ_EXP, text)
    if m !== nothing
        cond = parseRValue(m.captures[1])
        offset = parseRValue(m.captures[2])
        return JnzInstruction(cond, offset)
    end
end


TGL_EXP = Regex("tgl ($RVALUE_EXP)")

function parseTgl(text::AbstractString)::Optional{TglInstruction}
    m = match(TGL_EXP, text)
    if m !== nothing
        offset = parseRValue(m.captures[1])
        return TglInstruction(offset)
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
    instructions::Vector{Instruction}
    registers::Dict{Char, Int}
end

function valueOf(register::Char, state::State)::Int
    return state.registers[register]
end

function valueOf(literal::Int, _)::Int
    return literal
end

## instructions

function exec!(instruction::CpyInstruction, state::State)
    if isRegister(instruction.dst)
        state.registers[instruction.dst] = valueOf(instruction.src, state)
    end
    state.ic += 1
end

function exec!(instruction::IncInstruction, state::State)
    if isRegister(instruction.dst)
        state.registers[instruction.dst] += 1
    end
    state.ic += 1
end

function exec!(instruction::DecInstruction, state::State)
    if isRegister(instruction.dst)
        state.registers[instruction.dst] -= 1
    end
    state.ic += 1
end


function exec!(instruction::JnzInstruction, state::State)
    if valueOf(instruction.cond, state) != 0
        state.ic += valueOf(instruction.offset, state)
    else
        state.ic += 1
    end
end

function exec!(instruction::TglInstruction, state::State)
    function toggle(instruction::IncInstruction)::Instruction
        return DecInstruction(instruction.dst)
    end
    
    function toggle(instruction::DecInstruction)::Instruction
        return IncInstruction(instruction.dst)
    end
    
    function toggle(instruction::JnzInstruction)::Instruction
        return CpyInstruction(instruction.cond, instruction.offset)
    end
    
    function toggle(instruction::CpyInstruction)::Instruction
        return JnzInstruction(instruction.src, instruction.dst)
    end
    
    function toggle(instruction::TglInstruction)::Instruction
        return IncInstruction(instruction.offset)
    end

    targetAddress = state.ic + valueOf(instruction.offset, state)
    if 0 < targetAddress <= length(state.instructions)
        target = state.instructions[targetAddress]
        state.instructions[targetAddress] = toggle(target)
    end
    state.ic += 1
end

function step!(state::State)
    instruction = state.instructions[state.ic]
    exec!(instruction, state)
end

function run(lines::Vector{String})
    instructions = map(parseInstruction, lines)
    state = State(
        1, 
        instructions,
        Dict(
            'a' => 7,
            'b' => 0,
            'c' => 0,
            'd' => 0,
        ))

    while state.ic <= length(lines)
        step!(state)
    end

    return state.registers['a']
end

println(run(readlines()))