import xml.etree.ElementTree as ET
import sys
import argparse
import re
import copy
FrameStack=[]
Temporary_frame={"defined" : "no"}
Global_frame={}
Labels={}
Stack_call=[]
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
                    name.find('arg1').attrib['type']=="nil",
                    name.find('arg1').attrib['type'] == "float",]
    if(len(list(name)) == 2 or len(list(name)) == 3):
        constants_arg2=[name.find('arg2').attrib['type']=="string",
                    name.find('arg2').attrib['type']=="bool",
                    name.find('arg2').attrib['type']=="int",
                    name.find('arg2').attrib['type']=="nil",
                    name.find('arg1').attrib['type'] == "float",]
    if(len(list(name)) == 3):
        constants_arg3=[name.find('arg3').attrib['type']=="string",
                    name.find('arg3').attrib['type']=="bool",
                    name.find('arg3').attrib['type']=="int",
                    name.find('arg3').attrib['type']=="nil,",
                    name.find('arg1').attrib['type'] == "float",]
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
                  Labels[name.find('arg1').text]=int(name.get('order'))
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
def sematic_check(root, instruction_number):
    global Temporary_frame
    global FrameStack
    shcontinue= False
    for name in root.findall('instruction'):

        shcontinue=False
        while instruction_number != int(name.get('order')):
            if(instruction_number > int(name.get('order'))):
                shcontinue=True
                break
            shcontinue=False
            break
        if(shcontinue == True):
            continue
        three_operand = [name.get('opcode').upper() == ("ADD"),
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
                         name.get('opcode').upper() == ("SETCHAR"), ]
        print(name.get('opcode') + " pozice: " + name.get('order'))
        if (name.get('opcode').upper() == "CREATEFRAME"):
           Temporary_frame.clear()
           Temporary_frame["defined"]="yes"
        if (name.get('opcode').upper() == "PUSHFRAME"):
           if (Temporary_frame["defined"] == "no"):
                exit(55)
           FrameStack.append(copy.deepcopy(Temporary_frame))
           Temporary_frame.clear()
           Temporary_frame["defined"]="no"
        if(name.get('opcode').upper() == "RETURN"):
            if(len(Stack_call) == 0):
                exit(56)
            instruction_number=Stack_call.pop()
            instruction_number+=1
            sematic_check(root, instruction_number)
            break
        if (name.get('opcode').upper() == "POPFRAME"):
           if (len(FrameStack) == 0):
              exit(55)
           Temporary_frame=FrameStack.pop()

        if (name.get('opcode').upper() == "DEFVAR"):
           if(name.find('arg1').text[:2] == "GF"):
              if(name.find('arg1').text[3:] in Global_frame):
                  exit(55)
              Global_frame[name.find('arg1').text[3:]] = ""
           elif(name.find('arg1').text[:2] == "LF"):
              if(len(FrameStack) == 0):
                  exit(55)
              if (name.find('arg1').text[3:] in FrameStack[0]):
                  exit(55)
              FrameStack[0][name.find('arg1').text[3:]] = ""
           elif(name.find('arg1').text[:2] == "TF"):
             if (name.find('arg1').text[3:] in Temporary_frame):
                 exit(55)
             Temporary_frame[name.find('arg1').text[3:]] = ""
           else:
             exit(55)
        if (name.get('opcode').upper() == "JUMP"):
            try:
                instruction_number=Labels[name.find('arg1').text]
            except:
                exit(55)
            instruction_number+=1
            sematic_check(root, instruction_number)
            break
        if (name.get('opcode').upper() == "CALL"):
            try:
                instruction_number=Labels[name.find('arg1').text]
            except:
                exit(55)
            instruction_number+=1
            Stack_call.append(int(name.get('order')))
            sematic_check(root, instruction_number)
            break
        if (name.get('opcode').upper() == "WRITE"):
            if(name.find('arg1').attrib['type']=="var"):
                if (name.find('arg1').text[:2] == "GF"):
                    if (name.find('arg1').text[3:] in Global_frame):
                        pass
                    else:
                        exit(55)
                    print(Global_frame[name.find('arg1').text[3:]][0])
                elif (name.find('arg1').text[:2] == "LF"):
                    if (len(FrameStack) == 0):
                        exit(55)
                    if (name.find('arg1').text[3:] in FrameStack[0]):
                        pass
                    else:
                        exit(55)
                    print(FrameStack[0][name.find('arg1').text[3:]][0])
                elif (name.find('arg1').text[:2] == "TF"):
                    if (name.find('arg1').text[3:] in Temporary_frame):
                        pass
                    else:
                        exit(55)
                    print(Temporary_frame[name.find('arg1').text[3:]][0])
                else:
                    exit(55)
            if(name.find('arg1').attrib['type']=="string"):
                print(name.find('arg1').text, end='')
            elif(name.find('arg1').attrib['type']=="int"):
                print(name.find('arg1').text, end='')
            elif(name.find('arg1').attrib['type']=="nil"):
                print(name.find('arg1').text, end='')
            elif(name.find('arg1').attrib['type']=="float"):
                print(name.find('arg1').text, end='')
              ### třeba dodělat
        if (name.get('opcode').upper() == "EXIT"):
            if(name.find('arg1').attrib['type'] == "var"):


                try:
                    exit_code=int(name.find('arg1').text[4:])
                except:
                       exit(57)
                if( exit_code in range(0,49)):
                    exit(exit_code)
                else:
                    exit(57)
        if(name.get('opcode').upper() == "MOVE"):
           if(name.find('arg2').attrib['type'] == "var"):
               if (name.find('arg2').text[:2] == "GF"):
                   if (name.find('arg2').text[3:] in Global_frame):
                       pass
                   else:
                       exit(55)
                   moved=Global_frame[name.find('arg1').text[3:]][0]
               elif (name.find('arg2').text[:2] == "LF"):
                   if (len(FrameStack) == 0):
                       exit(55)
                   if (name.find('arg2').text[3:] in FrameStack[0]):
                       pass
                   else:
                       exit(55)
                   moved=FrameStack[0][name.find('arg1').text[3:]][0]
               elif (name.find('arg2').text[:2] == "TF"):
                   if (name.find('arg2').text[3:] in Temporary_frame):
                       pass
                   else:
                       exit(55)
                   moved=Temporary_frame[name.find('arg1').text[3:]][0]
               else:
                   exit(55)
           if (name.find('arg2').attrib['type'] == "string"):
               moved=name.find('arg2').text
           elif (name.find('arg2').attrib['type'] == "int"):
               moved=name.find('arg2').text
           elif (name.find('arg2').attrib['type'] == "nil"):
               moved=name.find('arg2').text
           elif (name.find('arg2').attrib['type'] == "float"):
               moved=name.find('arg2').text
           if(name.find('arg1').attrib['type'] == "var"):
               if (name.find('arg1').text[:2] == "GF"):
                   if (name.find('arg1').text[3:] in Global_frame):
                       pass
                   else:
                       exit(55)
                   Global_frame[name.find('arg1').text[3:]]=(moved, name.find('arg2').attrib['type'])
               elif (name.find('arg1').text[:2] == "LF"):
                   if (len(FrameStack) == 0):
                       exit(55)
                   if (name.find('arg1').text[3:] in FrameStack[0]):
                       pass
                   else:
                       exit(55)
                   FrameStack[0][name.find('arg1').text[3:]]=(moved, name.find('arg2').attrib['type'])
               elif (name.find('arg1').text[:2] == "TF"):
                   if (name.find('arg1').text[3:] in Temporary_frame):
                       pass
                   else:
                       exit(55)
                   Temporary_frame[name.find('arg1').text[3:]]=(moved,name.find('arg2').attrib['type'])
               else:
                   exit(55)
           else:
               exit(55)
        if (any(three_operand)):
            if(name.get('opcode').upper() == "ADD"):
                if(name.find('arg2').attrib['type'] == "var"):
                   if (name.find('arg2').text[:2] == "GF"):
                        if (name.find('arg2').text[3:] in Global_frame):
                            pass
                        else:
                            exit(55)
                        first_value = Global_frame[name.find('arg2').text[3:]][0]
                   elif (name.find('arg2').text[:2] == "LF"):
                        if (len(FrameStack) == 0):
                            exit(55)
                        if (name.find('arg2').text[3:] in FrameStack[0]):
                            pass
                        else:
                            exit(55)
                        first_value = FrameStack[0][name.find('arg2').text[3:]][0]
                   elif (name.find('arg2').text[:2] == "TF"):
                        if (name.find('arg2').text[3:] in Temporary_frame):
                            pass
                        else:
                            exit(55)
                        first_value = Temporary_frame[name.find('arg2').text[3:]][0]
                if(name.find('arg3').attrib['type'] == "var"):
                      if (name.find('arg3').text[:2] == "GF"):
                          if (name.find('arg3').text[3:] in Global_frame):
                              if(Global_frame[name.find('arg3').text[3:]][1] != "int"):
                                  exit(55)
                          else:
                              exit(55)
                          second_value = Global_frame[name.find('arg3').text[3:]][0]
                      elif (name.find('arg3').text[:2] == "LF"):
                          if (len(FrameStack) == 0):
                              exit(55)
                          if (name.find('arg3').text[3:] in FrameStack[0]):
                              if (FrameStack[0][name.find('arg3').text[3:]][1] != "int"):
                                  exit(55)
                          else:
                              exit(55)
                          second_value = FrameStack[0][name.find('arg3').text[3:]][0]
                      elif (name.find('arg3').text[:2] == "TF"):
                          if (name.find('arg3').text[3:] in Temporary_frame):
                              if (Temporary_frame[name.find('arg3').text[3:]][1] != "int"):
                                  exit(55)
                          else:
                              exit(55)
                          second_value = Temporary_frame[name.find('arg3').text[3:]][0]
                if(name.find('arg3').attrib['type'] == "var")
                ###### Tady pokračovat!
                else:
                 exit(54)

                try:
                  first_value = int(name.find('arg2').text)
                  second_value = int(name.find('arg3').text)
                except:
                  exit(54)
            elif(name.get('opcode').upper() == "SUB"):
                if(name.find('arg2').attrib['type'] == "int" and name.find('arg3').attrib['type'] == "int"):
                 try:
                    first_value=int(name.find('arg2').text)
                    second_value=int(name.find('arg3').text)
                 except:
                    exit(54)
                 result=first_value-second_value
                else:
                 exit(54)
            elif (name.get('opcode').upper() == "MUL"):
                if(name.find('arg2').attrib['type'] == "int" and name.find('arg3').attrib['type'] == "int"):
                 try:
                    first_value=int(name.find('arg2').text)
                    second_value=int(name.find('arg3').text)
                 except:
                    exit(54)
                 result=first_value*second_value
                else:
                 exit(54)
            elif (name.get('opcode').upper() == "IDIV"):
                if(name.find('arg2').attrib['type'] == "int" and name.find('arg3').attrib['type'] == "int"):
                 try:
                    first_value=int(name.find('arg2').text)
                    second_value=int(name.find('arg3').text)
                 except:
                    exit(54)
                 result=first_value//second_value
                else:
                 exit(54)
            if(name.get('opcode').upper() == "LT"):
                first_type=type(name.find('arg2').text)
                second_type=type(name.find('arg3').text)
                if (name.find('arg2').attrib['type'] == "nil"):
                    exit(54)
                if(name.find('arg2').attrib['type'] == "bool"):
                    pass
                if(first_type != second_type):
                    exit(55)
                if(first_type == int):
                    result=int(name.find('arg2').text) < int(name.find('arg3').text)
                if(first_type == str):
                    result=name.find('arg2').text < name.find('arg3').text
            if (name.find('arg1').text[:2] == "GF"):
                if (name.find('arg1').text[3:] in Global_frame):
                    pass
                else:
                    exit(55)
                Global_frame[name.find('arg1').text[3:]] = first_value
            elif (name.find('arg1').text[:2] == "LF"):
                if (len(FrameStack) == 0):
                    exit(55)
                if (name.find('arg1').text[3:] in FrameStack[0]):
                    pass
                else:
                    exit(55)
                FrameStack[0][name.find('arg1').text[3:]] = moved
            elif (name.find('arg1').text[:2] == "TF"):
                if (name.find('arg1').text[3:] in Temporary_frame):
                    pass
                else:
                    exit(55)
                Temporary_frame[name.find('arg1').text[3:]] = moved
            else:
                exit(55)



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
    parse_instruction(name)
#2. Běh sematicka kontrola a interpretace
sematic_check(root, 1)