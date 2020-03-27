# """CPU functionality."""

import sys

class CPU:
    """Main CPU class."""
    def __init__(self):
        self.ram = [None] * 256
        self.reg = [None] * 8
        self.pc = 0
        self.SP = 7
        self.Flags = {
            'E': 0,
            'L': 0,
            'G':0
            
        }
        self.functions = {
            # 164: self.MOD,
            # 172: self.SHL,
            # 173: self.SHR,
            # 171: self.XOR,
            # 105: self.NOT,
            # 170: self.OR,
            # 168: self.AND,
            84: self.JMP,
            86: self.JNE,
            85: self.JEQ,
            167: self.CMP,
            130 : self.LDI,
            71 : self.PRN,
            162: self.MUL,
            69: self.PUSH,
            70: self.POP,
            80: self.CALL,
            17: self.RET,
            160: self.ADD,
            1: self.HLT
        }
    def HLT(self):
        exit()
  
    def ram_read(self, address):
        return self.ram[address]
    
    def ram_write(self, address, value):
        self.ram[address] = value

    def binary_convert_hex(self, binary):
        string=str(binary)
        binary_string=string[0:9]
        decimal_rep= int(binary_string, 2)
        hex_string = hex(decimal_rep)
        return hex_string[2:4]

    def binary_convert_dec(self, binary):
        string=str(binary)
        binary_string=string[0:9]
        decimal_rep= int(binary_string, 2)
        return decimal_rep

    def LDI(self):
        self.pc += 1
        setReg = self.binary_convert_dec(self.ram_read(self.pc))
        self.pc +=1
        self.reg[setReg] = self.binary_convert_dec(self.ram_read(self.pc))
        self.pc +=1

    def PRN(self):
        self.pc +=1
        print(self.reg[self.binary_convert_dec(self.ram_read(self.pc))])
        self.pc +=1
    
    def ADD(self):
        regOne = self.pc + 1
        regTwo = self.pc + 2
        self.reg[self.binary_convert_dec(self.ram_read(regOne))] = self.reg[self.binary_convert_dec(self.ram_read(regOne))] + self.reg[self.binary_convert_dec(self.ram_read(regTwo))]
        self.pc += 3
       
    def MUL(self):
        self.pc +=1
        setReg = self.binary_convert_dec(self.ram_read(self.pc))
        self.pc +=1
        setSecondReg = self.binary_convert_dec(self.ram_read(self.pc))
        self.reg[setReg] = self.reg[setReg] * self.reg[setSecondReg]
        self.pc += 1

    def PUSH(self):
        self.SP -= 1
        self.pc +=1
        self.ram[self.SP] = self.reg[self.binary_convert_dec(self.ram_read(self.pc))]
        self.pc += 1

    def POP(self):
        self.pc +=1
        self.reg[self.binary_convert_dec(self.ram_read(self.pc))] = self.ram[self.SP]
        self.SP += 1
        self.pc += 1
        
    def CALL(self):
        self.pc +=1
        self.SP -=1
        self.ram[self.SP] = self.pc
        self.pc = self.reg[self.binary_convert_dec(self.ram_read(self.pc))]

    def RET(self):
        self.pc = self.ram[self.SP] + 1
        self.SP +=1

    def CMP(self):
        regOne = self.pc + 1
        regTwo = self.pc + 2
       
        if self.reg[self.binary_convert_dec(self.ram_read(regOne))] == self.reg[self.binary_convert_dec(self.ram_read(regTwo))]:
            self.Flags['E'] = 1
        else:
            self.Flags['E'] = 0

        if self.reg[self.binary_convert_dec(self.ram_read(regOne))] < self.reg[self.binary_convert_dec(self.ram_read(regTwo))]:
            self.Flags['L'] = 1
        else:
            self.Flags['L'] = 0
    
        if self.reg[self.binary_convert_dec(self.ram_read(regOne))] > self.reg[self.binary_convert_dec(self.ram_read(regTwo))]:
            self.Flags['G'] = 1
        else:
            self.Flags['G'] = 0
        self.pc += 3

    def JEQ(self):
        regOne = self.pc + 1
        if self.Flags['E'] == 1:
            self.pc = self.reg[self.binary_convert_dec(self.ram_read(regOne))] 
        else:
            self.pc += 2
       
    def JNE(self):
        
        regOne = self.pc + 1
        if self.Flags['E'] == 0:
            self.pc = self.reg[self.binary_convert_dec(self.ram_read(regOne))]
        else:
            self.pc += 2
    def JMP(self):
        regOne = self.pc + 1
        self.pc = self.reg[self.binary_convert_dec(self.ram_read(regOne))]
    

    def load(self, filename):
        """Load a program into memory."""

        address = 0

        try:
            with open(filename) as f:
                for line in f:
                    comment_split = line.split("#")
                    num = comment_split[0].strip()
                    if num == "":
                        continue
    
                    instruction = int(num)
                    self.ram[address] = instruction
                    address += 1
        except FileNotFoundError:
            print("File not found")
            sys.exit(2)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
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
        while running == True:
            self.functions[self.binary_convert_dec(self.ram_read(self.pc))]()
    



cpu = CPU()

cpu.load(sys.argv[1])

cpu.run()




                 
        
