# """CPU functionality."""

import sys

class CPU:
    """Main CPU class."""
    def __init__(self):
        self.ram = [None] * 256
        self.reg = [None] * 8
        self.pc = 0
        self.SP = 7
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
       
        


    # def JUMP():



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
        IR = self.ram_read(self.pc)
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)
        while running == True:
            if self.binary_convert_hex(self.ram_read(self.pc)) == "82":
               self.LDI()
            if self.binary_convert_hex(self.ram_read(self.pc)) == "47":
                self.PRN()
            if self.binary_convert_dec(self.ram_read(self.pc)) == 162:
                self.MUL()
            if self.binary_convert_dec(self.ram_read(self.pc)) == 69:
                self.PUSH()
            if self.binary_convert_dec(self.ram_read(self.pc)) == 70:
                self.POP()
            if  self.binary_convert_dec(self.ram_read(self.pc)) == 80:
                self.CALL()
            if self.binary_convert_dec(self.ram_read(self.pc)) == 17:
                self.RET()
            if self.binary_convert_dec(self.ram_read(self.pc)) == 160:
                self.ADD()
            if self.binary_convert_dec(self.ram_read(self.pc)) == 1:
                self.HLT()




cpu = CPU()

cpu.load(sys.argv[1])

cpu.run()




                 
        
