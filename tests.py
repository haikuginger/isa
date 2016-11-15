from unittest import TestCase
from isa import CPU

class TestCPU(TestCase):

    def test_memcp(self):
        stream = [
            0x0001, # LDNX to register 1
            0x0008,
            0x0002, # LDNX to register 2
            0x000A,
            0x0003, # LDNX to register 3
            0x0002,
            0x8132, # MEMCP 2 pages from 0x0008 to 0x000A
            0x0900,
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
                0x0900,
                0xDEAD,
                0xBEEF,
                0xDEAD,
                0xBEEF,
            ]
        )