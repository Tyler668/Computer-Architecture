"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.pc = 0
        # self.ir = 0
        self.reg = [0] * 8
        self.ldi = 0b10000010
        self.mul = 0b10100010
        self.prn = 0b01000111
        self.hlt = 0b00000001
        self.mar = None
        self.mdr = None
        self.fl = None
        self.im = None
        self.ist = None
        self.sp = None

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value

    def load(self, program_filename=''):
        """Load a program into memory."""

        address = 0

        with open(program_filename) as f:
            for line in f:
                line = line.split('#')
                line = line[0].strip()
                if line != '':
                    line = int(line, 2)
                    self.ram[address] = line
                    address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""

        running = True

        while running:
            ir = self.ram[self.pc]  # Instruction register

            if ir == self.ldi:
                reg_addr = self.ram_read(self.pc + 1)
                value = self.ram_read(self.pc + 2)
                self.reg[reg_addr] = value
                self.pc += 3

            elif ir == self.prn:
                reg_addr = self.ram_read(self.pc + 1)
                print(self.reg[reg_addr])
                self.pc += 2

            elif ir == self.hlt:
                running = False
                self.pc += 1

            elif ir == self.mul:
                op1 = self.reg[0]
                op2 = self.reg[1]
                product = (op1 * op2)
                self.reg[0] = product
                # print(product)
                self.pc += 3

            else:
                print(f'Unknown instruction {ir} at address {self.pc}')
                sys.exit(1)


processor = CPU()
# processor.load(
#     "C:\\Users\\tyler\\Documents\\github\\Computer-Architecture\\ls8\\examples\\print8.ls8")
processor.load(
    "C:\\Users\\tyler\\Documents\\github\\Computer-Architecture\\ls8\\examples\\mult.ls8")
processor.run()
