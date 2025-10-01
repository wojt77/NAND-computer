#NAND gate using python not logical operator. 
# The NAND-gate is the fundamental building block for all further logic gates/chips in this file
def NAND(a, b):
    return not (a and b)

def NOT(a):
    return NAND(a, a)

def AND(a, b):
    return NOT(NAND(a, b))

def OR(a, b):
    return NOT(AND(NOT(a), NOT(b)))

def XOR(a, b):
    return OR(AND(NOT(a), b), AND(a, NOT(b)))

def mux(a, b, sel):
    return OR(AND(a, NOT(sel)), AND(b, sel))

def dmux(inp, sel):
    a = AND(inp, NOT(sel))
    b = AND(inp, sel)
    return a, b

def NOT16(inp):
    output = [False]*len(inp)
    for i, pin in enumerate(inp):
        output[i] = NOT(pin)
    return(output)

def AND16(inp_a,inp_b):
    output = [False]*len(inp_b)
    for i in range(0,len(inp_b)):
        output[i] = AND(inp_a[i],inp_b[i])
    return(output)

def OR16(inp_a,inp_b):
    output = [False]*len(inp_b)
    for i in range(0,len(inp_b)):
        output[i] = OR(inp_a[i],inp_b[i])
    return(output)

def MUX16(inp_a,inp_b,sel):
    output = [False]*len(inp_b)
    for i in range(0,len(inp_b)):
        output[i] = mux(inp_a[i],inp_b[i],sel)
    return(output)

def OR8Way(inp):
    or0_1 = OR(inp[0], inp[1])
    or2_3 = OR(inp[2], inp[3])
    or4_5 = OR(inp[4], inp[5])
    or6_7 = OR(inp[6], inp[7])

    or01_23 = OR(or0_1, or2_3)
    or45_67 = OR(or4_5, or6_7)

    output = OR(or01_23, or45_67)
    return(output)

def MUX4way16(a, b, c, d, sel):
    
    top  = MUX16(a, c, sel[0])  
    bot  = MUX16(b, d, sel[0])  
    
    out = MUX16(top, bot, sel[1])
    return out

def MUX8way16(a, b, c, d, e, f, g, h, sel):
    or0_4 = MUX16(a, e, sel[0])  
    or1_5 = MUX16(b, f, sel[0]) 
    or2_6 = MUX16(c, g, sel[0])  
    or3_7 = MUX16(d, h, sel[0])  

    top = MUX16(or0_4, or1_5, sel[1])
    bottom = MUX16(or2_6, or3_7, sel[1])

    output = MUX16(top, bottom, sel[2])
    return output

def DMUX4way(inp, sel):

    nsel0 = NOT(sel[0])
    nsel1 = NOT(sel[1])
    
    top0 = AND(inp, nsel0)  
    top1 = AND(inp, sel[0]) 

    a = AND(top0, nsel1)  
    b = AND(top0, sel[1])  
    c = AND(top1, nsel1)  
    d = AND(top1, sel[1])  

    return a, b, c, d

def DMUX8way(inp, sel):
    nsel0 = NOT(sel[0])
    nsel1 = NOT(sel[1])
    nsel2 = NOT(sel[2])

    top0 = AND(inp, nsel0)
    top1 = AND(inp, sel[0])

    top0_0 = AND(top0, nsel1)
    top0_1 = AND(top0, sel[1])
    top1_0 = AND(top1, nsel1)
    top1_1 = AND(top1, sel[1])

    a = AND(top0_0, nsel2)
    b = AND(top0_0, sel[2])
    c = AND(top0_1, nsel2)
    d = AND(top0_1, sel[2])
    e = AND(top1_0, nsel2)
    f = AND(top1_0, sel[2])
    g = AND(top1_1, nsel2)
    h = AND(top1_1, sel[2])

    return a, b, c, d, e, f, g, h


def HalfAdder(a, b):
    sum = XOR(a,b)
    carry = AND(a,b)
    return sum,carry

def FullAdder(a, b, c):
    par_sum, carry1 = HalfAdder(a, b)
    sum, carry2 = HalfAdder(par_sum, c)
    carry = OR(carry1, carry2)

    return sum, carry

def Add16(inp_a,inp_b):
    output = [False]*len(inp_b)
    output[0], carry = HalfAdder(inp_a[0],inp_b[0])
    for i in range(1,len(inp_b)):
        output[i], carry = FullAdder(inp_a[i],inp_b[i],carry)
    return(output)

def Inc16(inp):
    one = [False] * 16
    one[0] = True
    output = Add16(inp,one)
    return output


#arithmetic logic unit of CPU, based on HACK-computer in:
#The Elements of Computing Systems: Building a Modern Computer from First Principles.
def ALU(x, y, zx, nx, zy, ny, f, no):
    x1 = MUX16(x, [False]*16, zx)
    notx1 = NOT16(x1)
    x2 = MUX16(x1, notx1, nx)

    y1 = MUX16(y, [False]*16, zy)
    noty1 = NOT16(y1)
    y2 = MUX16(y1, noty1, ny)

    xAdd16y = Add16(x2, y2)
    xAnd16y = AND16(x2, y2)

    preout = MUX16(xAnd16y, xAdd16y, f)
    notpreout = NOT16(preout)
    out = MUX16(preout, notpreout, no)

    zr0 = OR8Way(out[0:8])
    zr1 = OR8Way(out[8:16])
    zr2 = OR(zr0, zr1)
    zr = NOT(zr2)

    ng = out[15]

    return out, zr, ng


