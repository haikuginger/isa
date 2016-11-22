from unittest import TestCase
from isa import CPU

class TestCPU(TestCase):

    def test_memcp(self):
        """
        Test that we can block-copy data from a location in memory
        to another location in memory.
        """
        stream = [
            0x0001, # LDNX to register 1
            0x0008,
            0x0002, # LDNX to register 2
            0x000A,
            0x0003, # LDNX to register 3
            0x0002,
            0x8132, # MEMCP 2 pages from 0x0008 to 0x000A
            0x0900, # HALT
            0xDEAD,
            0xBEEF,
            0x0000,
            0x0000,
        ]
        cpu = CPU(memory=stream)
        cpu.run()
        self.assertEqual(
            cpu.memory,
            [
                0x0001, # LDNX to register 1
                0x0008,
                0x0002, # LDNX to register 2
                0x000A,
                0x0003, # LDNX to register 3
                0x0002,
                0x8132, # MEMCP 2 pages from 0x0008 to 0x000A
                0x0900, # HALT
                0xDEAD,
                0xBEEF,
                0xDEAD,
                0xBEEF,
            ]
        )
        self.assertEqual(
            cpu.registers,
            [8, 8, 10, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        )

    def test_halt(self):
        """
        Test that instructions past a certain point are not executed
        """
        stream = [
            0x0900, # HALT
            0x0001, # LDNX that we definitely shouldn't reach
            0xFFFF,
        ]
        cpu = CPU(memory=stream)
        cpu.run()
        self.assertEqual(cpu.memory, stream)
        self.assertEqual(
            cpu.registers,
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        )

    def test_ldnx(self):
        stream = [
            0x0001, # LDNX to R1
            0xFFFF,
            0x0900, # HALT
        ]
        cpu = CPU(memory=stream)
        cpu.run()
        self.assertEqual(cpu.memory, stream)
        self.assertEqual(
            cpu.registers,
            [3, 0xFFFF, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        )

    def test_dmpnx(self):
        stream = [
            0x0001, # LDNX to register 1
            0x0006, # Memory location of 0x0900
            0x0112, # LOAD contents of *R1 to R2
            0x0202, # DMPNX register 2
            0x0000, # Placeholder that will jump to PC=0 if executed
            0x0000,
            0x0900,
        ]
        cpu = CPU(memory=stream)
        cpu.run()
        self.assertEqual(
            cpu.memory,
            [
                0x0001,
                0x0006,
                0x0112,
                0x0202,
                0x0900,
                0x0000,
                0x0900,
            ]
        )
        self.assertEqual(
            cpu.registers,
            [0x0005, 0x0006, 0x0900, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        )

    def test_load(self):
        stream = [
            0x0001, # LDNX to R1
            0x0004, # Address of target memory to load
            0x0112, # LOAD contents at *R1 to R2
            0x0900, # HALT
            0xBEEF,
        ]
        cpu = CPU(memory=stream)
        cpu.run()
        self.assertEqual(cpu.memory, stream)
        self.assertEqual(
            cpu.registers,
            [0x0004, 0x0004, 0xBEEF, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        )

    def test_dump(self):
        stream = [
            0x0001, # LDNX to R1
            0xDEAD, # Placeholder memory
            0x0002, # LDNX to R2
            0x0006, # Address to dump to
            0x0312, # DUMP contents of R1 to *R2
            0x0900, # HALT
            0x0000,
        ]
        cpu = CPU(memory=stream)
        cpu.run()
        self.assertEqual(
            cpu.memory,
            [
                0x0001, # LDNX to R1
                0xDEAD, # Placeholder memory
                0x0002, # LDNX to R2
                0x0006, # Address to dump to
                0x0312, # DUMP contents of R1 to *R2
                0x0900, # HALT
                0xDEAD,
            ]
        )
        self.assertEqual(
            cpu.registers,
            [0x0006, 0xDEAD, 0x0006, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        )
