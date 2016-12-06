from isa import CPU

class InvalidInstruction(Exception):
    pass

class ProgramTooLong(Exception):
    pass

class Instruction(object):

    def __init__(self, code, arg_count):
        self.code = code
        self.arg_count = arg_count

    def assemble(self, *args):
        if len(args) != self.arg_count:
            raise InvalidInstruction
        code = self.code
        for i, arg in enumerate(args, 1):
            code += (16 ** (self.arg_count - i)) * arg
        return code

class Assembler(object):

    arg_seperator = ' '
    arg_base = 16
    comment_prefix = '#'
    instruction_set = CPU.operations
    bitness = 16

    def __init__(self, fp):
        self.fp = fp
        self.build_instruction_map()
        super(Assembler, self).__init__()

    def build_instruction_map(self):
        imap = {
            instruction[2]: Instruction(*instruction[:2]) for instruction in self.instruction_set
        }
        self.instruction_map = imap

    def max_space(self):
        return 2 ** self.bitness

    def assemble(self, memory_size=None):
        max_memlength = memory_size or self.max_space()
        memory = []
        lines = self.fp.read().splitlines()
        for line in lines:
            if line.startswith(self.comment_prefix):
                continue
            parts = line.split(self.arg_seperator)
            if len(parts) == 1:
                try:
                    val = int(parts[0], self.arg_base)
                    memory.append(val)
                    continue
                except ValueError:
                    pass
            if parts[0] not in self.instruction_map:
                raise InvalidInstruction
            elif len(memory) >= max_memlength:
                raise ProgramTooLong
            else:
                instruction = self.instruction_map[parts[0]]
                parsed = [int(part, self.arg_base) for part in parts[1:]]
                memory.append(instruction.assemble(*parsed))
        while len(memory) < max_memlength:
            memory.append(0)
        return memory
