"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.running = True
        self.ram = [0] * 256
        self.pc = 0
        self.reg = [0] * 8
        self.reg[7] = 0xF4
        self.sp = 7
        self.mar = None
        self.mdr = None
        self.fl = None
        self.im = None
        self.ist = None

        self.func_registry = {
            int(0b10000010): self.do_ldi,
            int(0b01000111): self.do_prn,
            int(0b10100010): self.do_mul,
            int(0b01000101): self.do_push,
            int(0b01000110): self.do_pop,
            int(0b00000001): self.do_hlt
        }

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

    def do_ldi(self):
        reg_addr = self.ram_read(self.pc + 1)
        value = self.ram_read(self.pc + 2)
        self.reg[reg_addr] = value
        self.pc += 3

    def do_prn(self):
        reg_addr = self.ram_read(self.pc + 1)
        print(self.reg[reg_addr])
        self.pc += 2

    def do_mul(self):
        op1 = self.reg[0]
        op2 = self.reg[1]
        product = (op1 * op2)
        self.reg[0] = product
        self.pc += 3

    def do_push(self):
        # Decrement stack pointer
        # print('self.reg:', self.reg)
        self.reg[self.sp] -= 1
        # Copy value from register into memory
        reg_addr = self.ram[self.pc+1]
        value = self.reg[reg_addr]  # This is what we want to push

        address = self.reg[self.sp]
        self.ram[address] = value

        self.pc += 2

    def do_pop(self):
        ram_addr = self.reg[self.sp]
        value = self.ram[ram_addr]

        # Find correct place in reg to put value with instructions at pc + 1
        reg_addr = self.ram[self.pc + 1]

        # Set correct reg address to new value
        self.reg[reg_addr] = value

        # Increment stack pointer
        self.reg[self.sp] += 1

        # Iterate pc
        self.pc += 2

    def do_hlt(self):
        self.running = False
        self.pc += 1

    def run(self):
        """Run the CPU."""
        while self.running:
            ir = self.ram[self.pc]  # Instruction register
            self.func_registry[ir]()

            if ir not in self.func_registry:
                print(f'Unknown instruction {ir} at address {self.pc}')
                sys.exit(1)


processor = CPU()

# Print 8
# processor.load(
#     "C:\\Users\\tyler\\Documents\\github\\Computer-Architecture\\ls8\\examples\\print8.ls8")
# processor.run()

# Multiply
# processor.load(
#     "C:\\Users\\tyler\\Documents\\github\\Computer-Architecture\\ls8\\examples\\mult.ls8")
# processor.run()

# Stack
processor.load(
    "C:\\Users\\tyler\\Documents\\github\\Computer-Architecture\\ls8\\examples\\stack.ls8")
processor.run()


# ORIGINAL INEFFICIENT IFELIF
# May need later:
# --------------------------------------------------------
# print(type(ir))
# print('IR', ir)
# print('Bin to Int', 0b10000010)
# self.func_registry[int(ir)].__call__
# relevant_func.__call__
# if ir == self.ldi:
#     reg_addr = self.ram_read(self.pc + 1)
#     value = self.ram_read(self.pc + 2)
#     self.reg[reg_addr] = value
#     self.pc += 3

# elif ir == self.prn:
#     reg_addr = self.ram_read(self.pc + 1)
#     print(self.reg[reg_addr])
#     self.pc += 2

# elif ir == self.mul:
#     op1 = self.reg[0]
#     op2 = self.reg[1]
#     product = (op1 * op2)
#     self.reg[0] = product
#     self.pc += 3

# elif ir == self.push:
#     # Decrement stack pointer
#     # print('self.reg:', self.reg)
#     self.reg[self.sp] -= 1
#     # Copy value from register into memory
#     reg_addr = self.ram[self.pc+1]
#     value = self.reg[reg_addr]  # This is what we want to push

#     address = self.reg[self.sp]
#     self.ram[address] = value

#     self.pc += 2

# elif ir == self.pop:
#     # Get value in ram at SP
#     ram_addr = self.reg[self.sp]
#     value = self.ram[ram_addr]

#     # Find correct place in reg to put value with instructions at pc + 1
#     reg_addr = self.ram[self.pc + 1]

#     # Set correct reg address to new value
#     self.reg[reg_addr] = value

#     # Increment stack pointer
#     self.reg[self.sp] += 1

#     # Iterate pc
#     self.pc += 2

# if ir == self.hlt:
#     running = False
#     self.pc += 1
