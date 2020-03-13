import xml.etree.ElementTree as ET
import sys
import argparse
def parse_arguments():
    argparser=argparse.ArgumentParser(add_help=False)
    argparser.add_argument('--help', action="store_true")
    argparser.add_argument('--source', action="store")
    argparser.add_argument('--input', action="store")
    args=argparser.parse_args()
    if(len(sys.argv[1:])>2):
        print("Spatny pocet argumentu!\n")
        exit(11)
    return args
def parse_instruction(name):
    no_operands=[name.get('opcode').upper() == ("CREATEFRAME"),
                 name.get('opcode').upper() == ("POPFRAME"),
                 name.get('opcode').upper() == ("PUSHFRAME"),
                 name.get('opcode').upper() == ("RETURN"),
                 name.get('opcode').upper() == ("BREAK")]

    one_operand_var=[name.get('opcode').upper() == ("DEFVAR"),
                     name.get('opcode').upper() == ("POPS")]

    one_operand_symb=[name.get('opcode').upper() == ("PUSHS"),
                      name.get('opcode').upper() == ("WRITE"),
                      name.get('opcode').upper() == ("EXIT"),
                      name.get('opcode').upper() == ("DPRINT")]

    one_operand_label=[name.get('opcode').upper() == ("LABEL"),
                       name.get('opcode').upper() == ("JUMP"),
                       name.get('opcode').upper() == ("CALL"),]
    two_operand_read = [name.get('opcode').upper() == ("READ")]
    two_operand=[name.get('opcode').upper() == ("MOVE"),
                     name.get('opcode').upper() == ("INT2CHAR"),
                     name.get('opcode').upper() == ("STRLEN"),
                     name.get('opcode').upper() == ("TYPE"),
                     name.get('opcode').upper() == ("NOT"),]
    three_operand=[name.get('opcode').upper() == ("ADD"),
                     name.get('opcode').upper() == ("SUB"),
                     name.get('opcode').upper() == ("MUL"),
                     name.get('opcode').upper() == ("IDIV"),
                     name.get('opcode').upper() == ("LT"),
                     name.get('opcode').upper() == ("GT"),
                     name.get('opcode').upper() == ("EQ"),
                     name.get('opcode').upper() == ("AND"),
                     name.get('opcode').upper() == ("OR"),
                     name.get('opcode').upper() == ("STRI2INT"),
                     name.get('opcode').upper() == ("CONCAT"),
                     name.get('opcode').upper() == ("GETCHAR"),
                     name.get('opcode').upper() == ("SETCHAR"),]
    three_operand_label=[name.get('opcode').upper() == ("JUMPIFEQ"),
                         name.get('opcode').upper() == ("JUMPIFNEQ"),]
    if(any(no_operands)):

    elif(any(one_operand_var)):
        print("one operand_var\n")
    elif(any(one_operand_symb)):
        print("one operand_symb\n")
    elif(any(one_operand_label)):
        print("one operand label\n")
    elif(any(two_operand_read)):
        print("two read\n")
    elif (any(two_operand)):
        print("two\n")
    elif (any(three_operand)):
        print("three\n")
    elif (any(three_operand_label)):
        print("three label\n")
    else:
        print("Error unknown instruction\n")
        exit(11)


args=parse_arguments()
source=args.source
input=args.source
if(args.input == None and args.source == None):
    exit(11)
elif(args.input == None):
   input=""
   for line in sys.stdin:
       input+=line
elif(args.source == None):
    source=""
    for line in sys.stdin:
        source += line
if(args.source == None):
    tree=ET.fromstring(source)
    tree=ET.ElementTree(tree)
else:
    tree=ET.parse(source)
root=tree.getroot()
#1. syntaktická kontrola (základní kontrola možný argumentů a ukládání labelů pro 2. kontrolu
for name in root.findall('instruction'):
    #print(name.get('opcode') + " pozice: " + name.get('order'))
    parse_instruction(name)
