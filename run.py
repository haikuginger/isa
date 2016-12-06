import argparse

from isa import CPU
from assembler import Assembler 

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('--size', nargs='?', default=None, dest='max_size')
    args = parser.parse_args()
    with open(args.filename, 'r') as assembly_file:
        size = int(args.max_size) if args.max_size is not None else None
        assembled = Assembler(assembly_file).assemble(memory_size=size)
        cpu = CPU(memory=assembled)
        cpu.run()
        cpu.print_registers()
        cpu.print_memory()

if __name__ == '__main__':
    main()