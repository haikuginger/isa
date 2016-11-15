def split_opcode(fn):
    def inner(self, opcode):
        stringified = "%0.4X" % opcode
        thing = [int(x, 16) for x in stringified]
        fn(self, *thing)
    return inner

class InstructionSetMixin(object):
        
    @split_opcode
    def LDNX(self, *args):
        dest = args[3]
        addr = self.pc + 1
        data = self.memory[addr]
        self.registers[dest] = data
        self.registers[0] += 1

    @split_opcode
    def LOAD(self, *args):
        src = args[2]
        dest = args[3]
        src_addr = self.registers[src]
        data = self.memory[src_addr]
        self.registers[dest] = data

    @split_opcode
    def DMPNX(self, *args):
        src = args[3]
        data = self.registers[src]
        self.memory[self.pc + 1] = data

    @split_opcode
    def DUMP(self, *args):
        src = args[2]
        dest = self.registers[args[3]]
        self.memory[dest] = self.registers[src]

    @split_opcode
    def MEMCP(self, *args):
        srcaddr = self.registers[args[1]]
        length = self.registers[args[2]]
        destaddr = self.registers[args[3]]
        for i in range(length):
            self.memory[destaddr + i] = self.memory[srcaddr + i]

    @split_opcode
    def HALT(self, *args):
        self.halted = True


class CPU(InstructionSetMixin, object):

    operations = (
        (0x0000, 2, 'LDNX',),
        (0x0100, 2, 'LOAD',),
        (0x0200, 2, 'DMPNX',),
        (0x0300, 2, 'DUMP',),
        (0x8000, 3, 'MEMCP',),
        (0x0900, 2, 'HALT',),
    )

    def __init__(self, memory=None, registers=None):
        self.memory = memory
        self.registers = [0x0000] * 16
    
    @property
    def pc(self):
        return self.registers[0]

    def run(self):
        self.halted = False
        while self.pc < len(self.memory) and not self.halted:
            opcode = self.load(self.pc)
            self.execute(opcode)!
            self.registers[0] += 1
    
    def execute(self, opcode):
        operation = self.get_operation(opcode)
        if operation:
            operation(opcode)

    def get_operation(self, opcode):
        for op in self.operations:
            shift = op[1] * 4
            if op[0] >> shift == opcode >> shift:
                return getattr(self, op[2])

    def load(self, address):
        return self.memory[address]

    def print_registers(self):
        print(["0x%0.4X" % x for x in self.registers])

