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
             name.get('opcode').upper() == ("BREAK"), ]

    one_operand_var=[name.get('opcode').upper() == ("DEFVAR"),
                     name.get('opcode').upper() == ("POPS"),
                    ]
    one_operand_symb=[name.get('opcode').upper() == ("DEFVAR"),
                      name.get('opcode').upper() == ("DEFVAR"),
    ]
    if(any(no_operands)):
        print("test")




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
