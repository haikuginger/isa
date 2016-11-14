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


class CPU(InstructionSetMixin, object):

    operations = (
        (0x0000, 2, 'LDNX',),
        (0x0100, 2, 'LOAD',),
    )

    def __init__(self, memory=None):
        self.memory = [int(x, 16) for x in memory]
        self.registers = [int('0x0000', 16)] * 16
    
    @property
    def pc(self):
        return self.registers[0]

    def run(self):
        while self.pc < len(self.memory):
            opcode = self.load(self.pc)
            self.execute(opcode)
            self.print_registers()
            self.registers[0] += 1
    
    def execute(self, opcode):
        operation = self.get_operation(opcode)
        if operation:
            operation(opcode)

    def get_operation(self, opcode):
        for op in self.operations:
            shift = (4 - op[1]) * 4
            if op[0] >> shift == opcode >> shift:
                return getattr(self, op[2])

    def load(self, address):
        return self.memory[address]

    def print_registers(self):
        print(["0x%0.4X" % x for x in self.registers])

x = CPU(memory=['0001', '0003', '0112', 'FFFF'])
x.run()

