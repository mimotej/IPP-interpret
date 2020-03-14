import xml.etree.ElementTree as ET
import sys
import argparse
import re

FrameStack=[]
Labels={}
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
def check_constant(name, arg):
    type=name.find(arg).attrib['type']
    if(type == "bool"):
        if(name.find(arg).text !="true" and name.find('arg1').text !="false"):
            exit(11)
    elif(type == "int"):
        try:
            value = int(name.find(arg).text)
        except ValueError:
            exit(11)
    elif(type=="var"):
        if(re.search('^[a-zA-Z\*_\-\$&\%!\?]', name.find(arg).text[3]) == None):
           exit(11)
    elif(type=="string"):
       if(name.find(arg).text.find('\\') != -1):
            if (re.search('[\\\\][0-9][0-9][0-9]', name.find(arg).text) != None):
                exit(11)
    elif(type == "label"):
        if(re.search('^[a-zA-Z\*_\-\$&\%!\?]', name.find(arg).text[3]) == None):
            exit(11)
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
    if(len(list(name)) == 1 or len(list(name)) == 2 or len(list(name)) == 3):
        constants_arg1=[name.find('arg1').attrib['type']=="string",
                    name.find('arg1').attrib['type']=="bool",
                    name.find('arg1').attrib['type']=="int",
                    name.find('arg1').attrib['type']=="nil",]
    if(len(list(name)) == 2 or len(list(name)) == 3):
        constants_arg2=[name.find('arg2').attrib['type']=="string",
                    name.find('arg2').attrib['type']=="bool",
                    name.find('arg2').attrib['type']=="int",
                    name.find('arg2').attrib['type']=="nil",]
    if(len(list(name)) == 3):
        constants_arg3=[name.find('arg3').attrib['type']=="string",
                    name.find('arg3').attrib['type']=="bool",
                    name.find('arg3').attrib['type']=="int",
                    name.find('arg3').attrib['type']=="nil,"]
    if(any(no_operands)):
        if(len(list(name)) != 0):
            exit(55)
    elif(any(one_operand_var)):
        if(len(list(name)) == 1):
            if(name.find('arg1').attrib['type'] =="var"):
              check_constant(name, 'arg1')
              return
        print("error")
    elif(any(one_operand_symb)):
        if(len(list(name)) == 1):
            if(name.find('arg1').attrib['type'] =="var" or any(constants_arg1)):
              check_constant(name, 'arg1')
              return
        print("error")
    elif(any(one_operand_label)):
        if(len(list(name)) == 1):
            if(name.find('arg1').attrib['type'] =="label"):
              check_constant(name, 'arg1')
              ### Zaznamenání labelu do slovníku
              if name.get('opcode').upper() == ("LABEL"):
                  if name.find('arg1').text in Labels:
                      exit(11)
                  Labels[name.find('arg1').text]=name.get('order')
              return
        print("error")
    elif(any(two_operand_read)):
        if(len(list(name)) == 2):
            if(name.find('arg1').attrib['type'] == "var"):
                check_constant(name, 'arg1')
                if(any(constants_arg2)):
                    check_constant(name, 'arg2')
                    return
    elif (any(two_operand)):
        if (len(list(name)) == 2):
            if (name.find('arg1').attrib['type'] == "var"):
                check_constant(name, 'arg1')
                if (any(constants_arg2) or name.find('arg2').attrib['type'] == "var"):
                    check_constant(name, 'arg2')
                    return
        exit(11)
    elif (any(three_operand)):
       if (len(list(name)) == 3):
           if(name.find('arg1').attrib['type'] == "var"):
               check_constant(name, 'arg1')
               if (any(constants_arg2) or name.find('arg2').attrib['type'] == "var"):
                   check_constant(name, 'arg2')
                   if (any(constants_arg3) or name.find('arg3').attrib['type'] == "var"):
                       check_constant(name, 'arg3')
                       return
       exit(11)
    elif (any(three_operand_label)):
        if(len(list(name)) == 3):
            if(name.find('arg1').attrib['type'] == "label"):
                if (re.search('^[a-zA-Z\*_\-\$&\%!\?]', name.find('arg1').text[3]) == None):
                    exit(11)
                if (any(constants_arg2) or name.find('arg2').attrib['type'] == "var"):
                    check_constant(name, 'arg2')
                if (any(constants_arg3) or name.find('arg3').attrib['type'] == "var"):
                    check_constant(name, 'arg3')
                    return
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
if(root.get('language').upper() != "IPPCODE20"):
    exit(11)
#1. syntaktická kontrola (základní kontrola možný argumentů a ukládání labelů pro 2. kontrolu
for name in root.findall('instruction'):
    print(name.get('opcode') + " pozice: " + name.get('order'))
    parse_instruction(name)
    print(Labels)