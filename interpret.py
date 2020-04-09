##NEED TO DO READ TYPE
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
Stack=[]
def escape_sequence(string):
    i=0
    if(string is None):
        return string
    for c in string:
        if(c == '\\'):
            if(string[i+1]=="0"):
                string=string[:i]+chr(int(string[i+2 : i+4]))+string[i+4:]
                i-=3
            else:
                string=string[:i]+chr(int(string[i+1 : i+4]))+string[i+4:]
                i-=3
        i+=1
    return string
def parse_arguments():
    argparser=argparse.ArgumentParser(add_help=False)
    argparser.add_argument('--help', action="store_true")
    argparser.add_argument('--source', action="store")
    argparser.add_argument('--input', action="store")
    args=argparser.parse_args()
    if(len(sys.argv[1:])>2):
        print("Spatny pocet argumentu!\n")
        sys.exit(11)
    return args
def check_constant(name, arg):
    type=name.find(arg).attrib['type']
    if(type == "bool"):
        if(name.find(arg).text !="true" and name.find(arg).text !="false"):
            exit(11)
    elif(type == "int"):
        if (name.find(arg).text == None):
            return
        try:
            value = int(name.find(arg).text)
        except ValueError:
            exit(11)
    elif(type=="var"):
        if(re.search('^[a-zA-Z\*_\-\$&\%!\?]', name.find(arg).text[3]) == None):
           exit(11)
    elif(type == "label"):
        if(re.search('^[a-zA-Z\*_\-\$&\%!\?]', name.find(arg).text[0]) == None):
            exit(11)
def parse_instruction(name):
    try:
        no_operands = [name.get('opcode').upper() == ("CREATEFRAME"),
                       name.get('opcode').upper() == ("POPFRAME"),
                       name.get('opcode').upper() == ("PUSHFRAME"),
                       name.get('opcode').upper() == ("RETURN"),
                       name.get('opcode').upper() == ("CLEARS"),
                       name.get('opcode').upper() == ("ADDS"),
                       name.get('opcode').upper() == ("SUBS"),
                       name.get('opcode').upper() == ("MULS"),
                       name.get('opcode').upper() == ("DIVS"),
                       name.get('opcode').upper() == ("IDIVS"),
                       name.get('opcode').upper() == ("LTS"),
                       name.get('opcode').upper() == ("GTS"),
                       name.get('opcode').upper() == ("EQS"),
                       name.get('opcode').upper() == ("ANDS"),
                       name.get('opcode').upper() == ("ORS"),
                       name.get('opcode').upper() == ("NOTS"),
                       name.get('opcode').upper() == ("INT2CHARS"),
                       name.get('opcode').upper() == ("STRI2INTS"),
                       name.get('opcode').upper() == ("BREAK")]

        one_operand_var = [name.get('opcode').upper() == ("DEFVAR"),
                           name.get('opcode').upper() == ("POPS")]

        one_operand_symb = [name.get('opcode').upper() == ("PUSHS"),
                            name.get('opcode').upper() == ("WRITE"),
                            name.get('opcode').upper() == ("EXIT"),
                            name.get('opcode').upper() == ("DPRINT")]

        one_operand_label = [name.get('opcode').upper() == ("LABEL"),
                         name.get('opcode').upper() == ("JUMP"),
                         name.get('opcode').upper() == ("CALL"),
                         name.get('opcode').upper() == ("JUMPIFEQS"),
                         name.get('opcode').upper() == ("JUMPIFNEQS"),]
        two_operand_read = [name.get('opcode').upper() == ("READ")]
        two_operand = [name.get('opcode').upper() == ("MOVE"),
                   name.get('opcode').upper() == ("INT2CHAR"),
                   name.get('opcode').upper() == ("STRLEN"),
                   name.get('opcode').upper() == ("TYPE"),
                   name.get('opcode').upper() == ("NOT"),
                   name.get('opcode').upper() == ("INT2FLOAT"),
                   name.get('opcode').upper() == ("FLOAT2INT"), ]
        three_operand = [name.get('opcode').upper() == ("ADD"),
                     name.get('opcode').upper() == ("SUB"),
                     name.get('opcode').upper() == ("MUL"),
                     name.get('opcode').upper() == ("IDIV"),
                     name.get('opcode').upper() == ("DIV"),
                     name.get('opcode').upper() == ("LT"),
                     name.get('opcode').upper() == ("GT"),
                     name.get('opcode').upper() == ("EQ"),
                     name.get('opcode').upper() == ("AND"),
                     name.get('opcode').upper() == ("OR"),
                     name.get('opcode').upper() == ("STRI2INT"),
                     name.get('opcode').upper() == ("CONCAT"),
                     name.get('opcode').upper() == ("GETCHAR"),
                     name.get('opcode').upper() == ("SETCHAR"), ]
        three_operand_label = [name.get('opcode').upper() == ("JUMPIFEQ"),
                           name.get('opcode').upper() == ("JUMPIFNEQ"), ]
    except:
        sys.exit(32)
    if(len(list(name)) == 1 or len(list(name)) == 2 or len(list(name)) == 3):
        try:
            constants_arg1=[name.find('arg1').attrib['type']=="string",
                    name.find('arg1').attrib['type']=="bool",
                    name.find('arg1').attrib['type']=="int",
                    name.find('arg1').attrib['type']=="nil",
                    name.find('arg1').attrib['type'] == "float"]
        except:
            sys.exit(32)
    if(len(list(name)) == 2 or len(list(name)) == 3):
        try:
            constants_arg2=[name.find('arg2').attrib['type']=="string",
                    name.find('arg2').attrib['type']=="bool",
                    name.find('arg2').attrib['type']=="int",
                    name.find('arg2').attrib['type']=="nil",
                    name.find('arg2').attrib['type'] == "float",
                    name.find('arg2').attrib['type'] == "type"]
        except:
            sys.exit(32)
    if(len(list(name)) == 3):
        try:
            constants_arg3=[name.find('arg3').attrib['type']=="string",
                    name.find('arg3').attrib['type']=="bool",
                    name.find('arg3').attrib['type']=="int",
                    name.find('arg3').attrib['type']=="nil",
                    name.find('arg3').attrib['type'] == "float"]
        except:
            sys.exit(32)
    if(any(no_operands)):
        if(len(list(name)) != 0):
            sys.exit(32)
    elif(any(one_operand_var)):
        if(len(list(name)) == 1):
            if(name.find('arg1').attrib['type'] =="var"):
              check_constant(name, 'arg1')
              return
        sys.exit(32)
    elif(any(one_operand_symb)):
        if(len(list(name)) == 1):
            if(name.find('arg1').attrib['type'] =="var" or any(constants_arg1)):
              check_constant(name, 'arg1')
              return
        sys.exit(32)
    elif(any(one_operand_label)):
        if(len(list(name)) == 1):
            if(name.find('arg1').attrib['type'] =="label"):
              check_constant(name, 'arg1')
              ### Zaznamenání labelu do slovníku
              if name.get('opcode').upper() == ("LABEL"):
                  if name.find('arg1').text in Labels:
                      sys.exit(52)
                  Labels[name.find('arg1').text]=int(name.get('order'))
              return
        sys.exit(32)
    elif(any(two_operand_read)):
        if(len(list(name)) == 2):
            if(name.find('arg1').attrib['type'] == "var"):
                check_constant(name, 'arg1')
                if(any(constants_arg2)):
                    check_constant(name, 'arg2')
                    return
        sys.exit(32)
    elif (any(two_operand)):
        if (len(list(name)) == 2):
            if (name.find('arg1').attrib['type'] == "var"):
                check_constant(name, 'arg1')
                if (any(constants_arg2) or name.find('arg2').attrib['type'] == "var"):
                    check_constant(name, 'arg2')
                    return
        sys.exit(32)
    elif (any(three_operand)):
       if (len(list(name)) == 3):
           if(name.find('arg1').attrib['type'] == "var"):
               check_constant(name, 'arg1')
               if (any(constants_arg2) or name.find('arg2').attrib['type'] == "var"):
                   check_constant(name, 'arg2')
                   if (any(constants_arg3) or name.find('arg3').attrib['type'] == "var"):
                       check_constant(name, 'arg3')
                       return
       sys.exit(32)
    elif (any(three_operand_label)):
        if(len(list(name)) == 3):
            if(name.find('arg1').attrib['type'] == "label"):
                if (re.search('^[a-zA-Z\*_\-\$&\%!\?]', name.find('arg1').text) == None):
                    sys.exit(52)
                if (any(constants_arg2) or name.find('arg2').attrib['type'] == "var"):
                    check_constant(name, 'arg2')
                if (any(constants_arg3) or name.find('arg3').attrib['type'] == "var"):
                    check_constant(name, 'arg3')
                    return
        sys.exit(32)
    else:
        sys.exit(32)
#### pomocná funkce na zpracování hodnot pro aritmetické fce
def find_value(arg, name):
    value=[]
    if (name.find(arg).attrib['type'] == "var"):
        if (name.find(arg).text[:2] == "GF"):
            if (name.find(arg).text[3:] in Global_frame):
                if(len(Global_frame[name.find(arg).text[3:]]) == 0):
                    sys.exit(56)
                if (Global_frame[name.find(arg).text[3:]][1] != "int" and Global_frame[name.find(arg).text[3:]][1] != "float"):
                    exit(55)
            else:
                sys.exit(54)
            value.append(Global_frame[name.find(arg).text[3:]][0])
            value.append(Global_frame[name.find(arg).text[3:]][1])
        elif (name.find(arg).text[:2] == "LF"):
            if (len(FrameStack) == 0):
                sys.exit(55)
            frame=FrameStack.pop()
            FrameStack.append(frame)
            if (name.find(arg).text[3:] in frame):
                if(len(frame[name.find(arg).text[3:]]) == 0):
                    sys.exit(56)
                if (frame[name.find(arg).text[3:]][1] != "int" and frame[name.find(arg).text[3:]][1] != "float"):
                    sys.exit(55)
            else:
                sys.exit(54)
            value.append(frame[name.find(arg).text[3:]][0])
            value.append(frame[name.find(arg).text[3:]][1])
        elif (name.find(arg).text[:2] == "TF"):
            if (Temporary_frame['defined'] == "no"):
                sys.exit(55)
            if (name.find(arg).text[3:] in Temporary_frame):
                if(len(Temporary_frame[name.find(arg).text[3:]]) == 0):
                    sys.exit(56)
                if (Temporary_frame[name.find(arg).text[3:]][1] != "int" and Temporary_frame[name.find(arg).text[3:]][1] != "float"):
                    sys.exit(55)
            else:
                sys.exit(54)
            value.append(Temporary_frame[name.find(arg).text[3:]][0])
            value.append(Temporary_frame[name.find(arg).text[3:]][1])
    elif(name.find(arg).attrib['type'] == "int"):
        try:
            value.append(int(name.find(arg).text))
            value.append("int")
        except:
            sys.exit(57)
    elif(name.find(arg).attrib['type'] == "float"):
        try:
            value.append(value[0])
            value.append("float")
        except:
            try:
                try:
                    value.append(float.fromhex(name.find(arg).text))
                except:
                    value.append(float(name.find(arg).text))
                value.append("float")
            except:
                sys.exit(57)
    else:
        sys.exit(53)
    return value

def get_value_comparasion(name):
    arg='arg2'
    i=0
    return_value=[]
    while i<2:
     value = []
     if (name.find(arg).attrib['type'] == "var"):
        if (name.find(arg).text[:2] == "GF"):
            if (name.find(arg).text[3:] in Global_frame):
                if(len(Global_frame[name.find(arg).text[3:]]) == 0):
                    sys.exit(56)
                if (Global_frame[name.find(arg).text[3:]][1] != "int" and
                    Global_frame[name.find(arg).text[3:]][1] != "string" and
                    Global_frame[name.find(arg).text[3:]][1] != "bool" and
                    Global_frame[name.find(arg).text[3:]][1] != "nil" and
                    Global_frame[name.find(arg).text[3:]][1] != "float" and
                    Global_frame[name.find(arg).text[3:]][1] != "type"):
                    sys.exit(53)
            else:
                sys.exit(54)
            value.append(Global_frame[name.find(arg).text[3:]][0])
            value.append(Global_frame[name.find(arg).text[3:]][1])
        elif (name.find(arg).text[:2] == "LF"):
            if (len(FrameStack) == 0):
                exit(55)
            frame=FrameStack.pop()
            FrameStack.append(frame)
            if (name.find(arg).text[3:] in frame):
                if(len(frame[name.find(arg).text[3:]]) == 0):
                    sys.exit(56)
                if (frame[name.find(arg).text[3:]][1] != "int" and
                    frame[name.find(arg).text[3:]][1] != "string" and
                    frame[name.find(arg).text[3:]][1] != "bool" and
                    frame[name.find(arg).text[3:]][1] != "nil" and
                    frame[name.find(arg).text[3:]][1] != "float" and
                    frame[name.find(arg).text[3:]][1] != "type"):
                    sys.exit(53)
            else:
                sys.exit(54)
            value.append(frame[name.find(arg).text[3:]][0])
            value.append(frame[name.find(arg).text[3:]][1])
        elif (name.find(arg).text[:2] == "TF"):
            if(Temporary_frame['defined'] =="no"):
                sys.exit(55)
            if (name.find(arg).text[3:] in Temporary_frame):
                if(len(Temporary_frame[name.find(arg).text[3:]]) == 0):
                    sys.exit(56)
                if (Temporary_frame[name.find(arg).text[3:]][1] != "int" and
                    Temporary_frame[name.find(arg).text[3:]][1] != "string" and
                    Temporary_frame[name.find(arg).text[3:]][1] != "int" and
                    Temporary_frame[name.find(arg).text[3:]][1] != "nil" and
                    Temporary_frame[name.find(arg).text[3:]][1] != "float" and
                    Temporary_frame[name.find(arg).text[3:]][1] != "type"):
                    sys.exit(53)
            else:
                sys.exit(54)
            value.append(Temporary_frame[name.find(arg).text[3:]][0])
            value.append(Temporary_frame[name.find(arg).text[3:]][1])
        else:
            sys.exit(55)
     elif(name.find(arg).attrib['type']=="string",
          name.find(arg).attrib['type']=="bool",
          name.find(arg).attrib['type']=="int",
          name.find(arg).attrib['type'] == "float"):
        if(name.find(arg).attrib['type']=="int"):
           value.append(int(name.find(arg).text))
        elif(name.find(arg).attrib['type']== "string"):
            value.append(escape_sequence(name.find(arg).text))
        elif(name.find(arg).attrib['type']=="float"):
            float_num=name.find(arg).text
            try:
                int(float_num)
                value.append(float(float_num))
            except:
                value.append(float.fromhex(float_num))
        elif(name.find(arg).attrib['type']=="bool"):
           if (name.find(arg).text =="false"):
              value.append("false")
           else:
               value.append("true")
        else:
           value.append(name.find(arg).text)
        value.append(name.find(arg).attrib['type'])
     else:
         sys.exit(53)
     i+=1
     arg='arg3'
     return_value.append(value)
    return return_value

def get_variable_value(name, arg):
    if (name.find(arg).text[:2] == "GF"):
        if (name.find(arg).text[3:] in Global_frame):
            pass
        else:
            sys.exit(54)
        try:
            return_value = Global_frame[name.find(arg).text[3:]]
        except:
            sys.exit(56)
    elif (name.find(arg).text[:2] == "LF"):
        if (len(FrameStack) == 0):
            sys.exit(55)
        frame=FrameStack.pop()
        FrameStack.append(frame)
        if (name.find(arg).text[3:] in frame):
            pass
        else:
            sys.exit(54)
        try:
            return_value=frame[name.find(arg).text[3:]]
        except:
            sys.exit(56)
    elif (name.find(arg).text[:2] == "TF"):
        if(Temporary_frame["defined"] == "no"):
            exit(55)
        if (name.find(arg).text[3:] in Temporary_frame):
            pass
        else:
            sys.exit(54)
        try:
            return_value= Temporary_frame[name.find(arg).text[3:]]
        except:
            sys.exit(56)
    return return_value
def save_variable_value(name, arg, value):
    if (name.find(arg).text[:2] == "GF"):
        if (name.find(arg).text[3:] in Global_frame):
            pass
        else:
            sys.exit(54)
        try:
            Global_frame[name.find(arg).text[3:]] = value
        except:
            sys.exit(56)
    elif (name.find(arg).text[:2] == "LF"):
        if (len(FrameStack) == 0):
            sys.exit(55)
        frame=FrameStack.pop()
        if (name.find(arg).text[3:] in frame):
            pass
        else:
            sys.exit(54)
        try:
            frame[name.find(arg).text[3:]] = value
        except:
            sys.exit(56)
        FrameStack.append(frame)
    elif (name.find(arg).text[:2] == "TF"):
        if(Temporary_frame["defined"] == "no"):
            exit(55)
        if (name.find(arg).text[3:] in Temporary_frame):
            pass
        else:
            sys.exit(54)
        try:
            Temporary_frame[name.find(arg).text[3:]] = value
        except:
            sys.exit(56)
    else:
        sys.exit(55)
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
                         name.get('opcode').upper() == ("DIV"),
                         name.get('opcode').upper() == ("LT"),
                         name.get('opcode').upper() == ("GT"),
                         name.get('opcode').upper() == ("EQ"),
                         name.get('opcode').upper() == ("AND"),
                         name.get('opcode').upper() == ("OR"),
                         name.get('opcode').upper() == ("NOT"),
                         name.get('opcode').upper() == ("STRI2INT"),
                         name.get('opcode').upper() == ("CONCAT"),
                         name.get('opcode').upper() == ("GETCHAR"),
                         name.get('opcode').upper() == ("SETCHAR"), ]
        if (name.get('opcode').upper() == "CREATEFRAME"):
            Temporary_frame.clear()
            Temporary_frame["defined"]="yes"
        if (name.get('opcode').upper() == "PUSHFRAME"):
            if (Temporary_frame["defined"] == "no"):
                sys.exit(55)
            FrameStack.append(copy.deepcopy(Temporary_frame))
            Temporary_frame.clear()
            Temporary_frame["defined"]="no"
        if (name.get('opcode').upper() == "CLEARS"):
            Stack.clear()
        if (name.get('opcode').upper() == "ADDS"):
            try:
                value2=Stack.pop()
                value1=Stack.pop()
            except:
                exit(56)
            first_value = value1[0]
            second_value = value2[0]
            if (value1[1] != value2[1]):
                sys.exit(53)
            if (value1[1] != "int" and value1[1] != "float"):
                sys.exit(53)
            if (value1[1] == "int" and value2[1] == "int"):
                type = "int"
                try:
                    first_value=int(first_value)
                    second_value=int(second_value)
                except:
                    sys.exit(53)
            if (value1[1] == "float" or value2[1] == "float"):
                type = "float"
                try:
                    first_value=float.fromhex(first_value)
                    second_value=float.fromhex(second_value)
                except:
                    pass
                try:
                    first_value=float(first_value)
                    second_value=float(second_value)
                except:
                    sys.exit(53)
            result = first_value + second_value
            Stack.append((result, type))
        if(name.get('opcode').upper() == "SUBS"):
            try:
                value2=Stack.pop()
                value1=Stack.pop()
            except:
                exit(56)
            first_value=value1[0]
            second_value=value2[0]
            if(value1[1] != value2[1]):
                sys.exit(53)
            if(value1[1] != "int" and value1[1] != "float"):
                sys.exit(53)
            if (value1[1] == "int" and value2[1] == "int"):
                type = "int"
                try:
                    first_value = int(first_value)
                    second_value = int(second_value)
                except:
                    sys.exit(53)
            if (value1[1] == "float" or value2[1] == "float"):
                type = "float"
                try:
                    first_value = float.fromhex(first_value)
                    second_value = float.fromhex(second_value)
                except:
                    pass
                try:
                    first_value = float(first_value)
                    second_value = float(second_value)
                except:
                    sys.exit(53)
            result = first_value - second_value
            Stack.append((result, type))
        if (name.get('opcode').upper() == "MULS"):
            try:
                value2=Stack.pop()
                value1=Stack.pop()
            except:
                exit(56)
            first_value=value1[0]
            second_value=value2[0]
            if(value1[1] != value2[1]):
                sys.exit(53)
            if(value1[1] != "int" and value1[1] != "float"):
                sys.exit(53)
            if (value1[1] == "int" and value2[1] == "int"):
                type = "int"
                try:
                    first_value=int(first_value)
                    second_value=int(second_value)
                except:
                    sys.exit(53)
            if (value1[1] == "float" or value2[1] == "float"):
                type = "float"
                try:
                    first_value=float.fromhex(first_value)
                    second_value=float.fromhex(second_value)
                except:
                    pass
                try:
                    first_value=float(first_value)
                    second_value=float(second_value)
                except:
                    sys.exit(53)
            result = first_value * second_value
            Stack.append((result, type))
        if (name.get('opcode').upper() == "IDIVS"):
            try:
                value2=Stack.pop()
                value1=Stack.pop()
            except:
                exit(56)
            first_value=value1[0]
            second_value=value2[0]
            if(value1[1] != value2[1]):
                sys.exit(53)
            if(value1[1] != "int"):
                sys.exit(53)
            if(second_value == 0):
                sys.exit(57)
            try:
                first_value=int(first_value)
                second_value=int(second_value)
            except:
                sys.exit(53)
            result=first_value//second_value
            type="int"
            Stack.append((result, type))
        if (name.get('opcode').upper() == "DIVS"):
            try:
                value2=Stack.pop()
                value1=Stack.pop()
            except:
                exit(56)
            first_value=value1[0]
            second_value=value2[0]
            if(second_value == 0):
                sys.exit(57)
            if (value1[1] != value2[1]):
                sys.exit(53)
            if(value1[1] != "int" and value1[1] != "float"):
                sys.exit(53)
            if (value1[1] == "int" and value2[1] == "int"):
                type = "int"
                try:
                    first_value = int(first_value)
                    second_value = int(second_value)
                except:
                    sys.exit(53)
            if (value1[1] == "float" or value2[1] == "float"):
                type = "float"
                try:
                    first_value = float.fromhex(first_value)
                    second_value = float.fromhex(second_value)
                except:
                    pass
                try:
                    first_value = float(first_value)
                    second_value = float(second_value)
                except:
                    sys.exit(53)
            result = first_value / second_value
            Stack.append((result, type))
        if(name.get('opcode').upper() == "LTS"):
            values=[]
            try:
                arg2=Stack.pop()
                arg1=Stack.pop()
                values.append(arg1)
                values.append(arg2)
            except:
                sys.exit(56)
            if(values[0][1] == "nil" or values[1][1]=="nil"):
                sys.exit(53)
            if(values[0][1] != values[1][1]):
                sys.exit(53)
            result=values[0][0] < values[1][0]
            if(result == True):
                result="true"
            else:
                result="false"
            type = "bool"
            Stack.append((result, type))
        if (name.get('opcode').upper() == "GTS"):
            values=[]
            try:
                arg2=Stack.pop()
                arg1=Stack.pop()
                values.append(arg1)
                values.append(arg2)
            except:
                sys.exit(56)
            if (values[0][1] == "nil" or values[1][1] == "nil"):
                sys.exit(53)
            if (values[0][1] != values[1][1]):
                sys.exit(53)
            result = values[0][0] > values[1][0]
            if(result == True):
                result="true"
            else:
                result="false"
            type = "bool"
            Stack.append((result, type))
        if (name.get('opcode').upper() == "EQS"):
            values=[]
            try:
                values.append(Stack.pop())
                values.append(Stack.pop())
            except:
                sys.exit(56)
            if (values[0][1] != "nil" and values[1][1] != "nil"):
                if (values[0][1] != values[1][1]):
                    sys.exit(53)
            result = values[0][0] == values[1][0]
            if(result == True):
                result="true"
            else:
                result="false"
            type = "bool"
            Stack.append((result, type))
        if(name.get('opcode').upper() == "ANDS"):
            values=[]
            try:
                arg2=Stack.pop()
                arg1=Stack.pop()
                values.append(arg1)
                values.append(arg2)
            except:
                sys.exit(56)
            if(values[0][1] != "bool" or values[1][1] !="bool"):
                sys.exit(53)
            if(values[0][0]=="true" and values[1][0]=="true"):
                result="true"
                type="bool"
            else:
                result="false"
                type="bool"
            Stack.append((result, type))
        if(name.get('opcode').upper() == "ORS"):
            values=[]
            try:
                arg2=Stack.pop()
                arg1=Stack.pop()
                values.append(arg1)
                values.append(arg2)
            except:
                sys.exit(56)
            if(values[0][1] != "bool" or values[1][1] !="bool"):
                sys.exit(53)
            if(values[0][0] == "true" or values[1][0] == "true"):
                result="true"
                type="bool"
            else:
                result="false"
                type="bool"
            Stack.append((result, type))
        if(name.get('opcode').upper() == "NOTS"):
            try:
                value=Stack.pop()
            except:
                sys.exit(56)
            if(value[1] == "bool"):
                if(value[0] == "false"):
                    result="true"
                    type="bool"
                else:
                    result="false"
                    type="bool"
            else:
                sys.exit(53)
            Stack.append((result, type))
        if(name.get('opcode').upper() == "STRI2INTS"):
             values = []
             try:
                 arg2 = Stack.pop()
                 arg1 = Stack.pop()
                 values.append(arg1)
                 values.append(arg2)
             except:
                 sys.exit(56)
             if(values[0][1] != "string"):
                 sys.exit(53)
             if(values[1][1] != "int"):
                 sys.exit(53)
             try:
                 result=values[0][0][int(values[1][0])]
                 try:
                    result=ord(result)
                 except:
                    sys.exit(58)
                 type="int"
             except:
                 sys.exit(58)
             Stack.append((result, type))
        if (name.get('opcode').upper() == "INT2CHARS"):
            try:
                integer=Stack.pop()
            except:
                sys.exit(56)
            if (integer[1] != "int"):
                sys.exit(53)
            try:
                integer = chr(integer[0])
            except:
                sys.exit(58)
            Stack.append((integer, "string"))
        if (name.get('opcode').upper() == "JUMPIFEQS" or name.get('opcode').upper() == "JUMPIFNEQS"):
            values = []
            try:
                arg2=Stack.pop()
                arg1=Stack.pop()
                values.append(arg1)
                values.append(arg2)
            except:
                sys.exit(56)
            if (values[0][1] == values[1][1] or (values[0][0] == "nil" or values[1][0] == "nil")):
                if (values[0][0] == values[1][0] and name.get('opcode').upper() == "JUMPIFEQS"):
                    try:
                        instruction_number = Labels[name.find('arg1').text]
                    except:
                        sys.exit(52)
                    instruction_number += 1
                    sematic_check(root, instruction_number)
                    break
                if (values[0][0] != values[1][0] and name.get('opcode').upper() == "JUMPIFNEQS"):
                    try:
                        instruction_number = Labels[name.find('arg1').text]
                    except:
                        sys.exit(52)
                    instruction_number += 1
                    sematic_check(root, instruction_number)
                    break
            else:
                sys.exit(53)

        if(name.get('opcode').upper() == "RETURN"):
            if(len(Stack_call) == 0):
                sys.exit(52)
            instruction_number=Stack_call.pop()
            instruction_number+=1
            sematic_check(root, instruction_number)
            break
        if (name.get('opcode').upper() == "POPFRAME"):
            if (len(FrameStack) == 0):
                sys.exit(55)
            Temporary_frame=FrameStack.pop()

        if (name.get('opcode').upper() == "DEFVAR"):
            if(name.find('arg1').text[:2] == "GF"):
                if(name.find('arg1').text[3:] in Global_frame):
                    sys.exit(52)
                Global_frame[name.find('arg1').text[3:]] = ""
            elif(name.find('arg1').text[:2] == "LF"):
                if(len(FrameStack) == 0):
                    sys.exit(55)
                value=FrameStack.pop()
                if (name.find('arg1').text[3:] in value):
                    sys.exit(52)
                value[name.find('arg1').text[3:]] = ""
                FrameStack.append(value)
            elif(name.find('arg1').text[:2] == "TF"):
                if (Temporary_frame["defined"] == "no"):
                    exit(55)
                if (name.find('arg1').text[3:] in Temporary_frame):
                    sys.exit(52)
                Temporary_frame[name.find('arg1').text[3:]] = ""
            else:
                sys.exit(55)
        if (name.get('opcode').upper() == "JUMP"):
            try:
                instruction_number=Labels[name.find('arg1').text]
            except:
                sys.exit(52)
            instruction_number+=1
            sematic_check(root, instruction_number)
            break
        if (name.get('opcode').upper() == "CALL"):
            try:
                instruction_number=Labels[name.find('arg1').text]
            except:
                sys.exit(52)
            instruction_number+=1
            Stack_call.append(int(name.get('order')))
            sematic_check(root, instruction_number)
            break

        if (name.get('opcode').upper() == "PUSHS"):
            if(name.find('arg1').attrib['type'] == "var"):
                push_value=get_variable_value(name, 'arg1')
            else:
                push_value=name.find('arg1').text
                if(name.find('arg1').attrib['type'] == "float"):
                    try:
                        push_value=(float.fromhex(push_value))
                    except:
                        push_value=(float(push_value))
                if(name.find('arg1').attrib['type'] == "int"):
                    try:
                        push_value=int(push_value)
                    except:
                        exit(53)
                if(name.find('arg1').attrib['type'] == "string"):
                    push_value=(escape_sequence(name.find('arg1').text), name.find('arg1').attrib['type'])
                else:
                    push_value=(push_value, name.find('arg1').attrib['type'])
            Stack.append(push_value)
        if (name.get('opcode').upper() == "POPS"):
            if (name.find('arg1').attrib['type'] == "var"):
                try:
                    save_value = Stack.pop()
                except:
                    sys.exit(56)
                save_variable_value(name, "arg1", save_value)
            else:
                sys.exit(53)
        if (name.get('opcode').upper() == "INT2CHAR"):
            if (name.find('arg2').attrib['type'] == "var"):
                integer = get_variable_value(name, 'arg2')
                if (integer[1] != "int"):
                    sys.exit(53)
                try:
                    integer = chr(integer[0])
                except:
                    sys.exit(58)
            else:
                if (name.find('arg2').attrib['type'] != "int"):
                    sys.exit(53)
                try:
                    integer = chr(int(name.find('arg2').text))
                except:
                    sys.exit(57)
            save_variable_value(name, "arg1", (integer, "string"))
        if (name.get('opcode').upper() == "WRITE"):
            if(name.find('arg1').attrib['type']=="var"):
                if (name.find('arg1').text[:2] == "GF"):
                    if (name.find('arg1').text[3:] in Global_frame):
                        pass
                    else:
                        sys.exit(54)
                    if(Global_frame[name.find('arg1').text[3:]][1]== "nil"):
                        print("", end='')
                    else:
                        if(Global_frame[name.find('arg1').text[3:]][1] == "float"):
                            print(float.hex(Global_frame[name.find('arg1').text[3:]][0]), end='')
                        else:
                            print(Global_frame[name.find('arg1').text[3:]][0], end='')
                elif (name.find('arg1').text[:2] == "LF"):
                    if (len(FrameStack) == 0):
                        exit(55)
                    value=FrameStack.pop()
                    FrameStack.append(value)
                    if (name.find('arg1').text[3:] in value):
                        pass
                    else:
                        sys.exit(54)
                    if(value[name.find('arg1').text[3:]][1]== "nil"):
                        print("", end='')
                    else:
                        if(value[name.find('arg1').text[3:]][1] == "float"):
                            print(float.hex(value[name.find('arg1').text[3:]][0]), end='')
                        else:
                            print(value[name.find('arg1').text[3:]][0], end='')
                elif (name.find('arg1').text[:2] == "TF"):
                    if (name.find('arg1').text[3:] in Temporary_frame):
                        pass
                    else:
                        sys.exit(54)
                    if(Temporary_frame[name.find('arg1').text[3:]][1]== "nil"):
                        print("", end='')
                    else:
                        if(Temporary_frame[name.find('arg1').text[3:]][1] == "float"):
                            print(float.hex(Temporary_frame[name.find('arg1').text[3:]][0]), end='')
                        else:
                            print(Temporary_frame[name.find('arg1').text[3:]][0], end='')
                else:
                    sys.exit(54)
            if(name.find('arg1').attrib['type']=="string"):
                value=escape_sequence(name.find('arg1').text)
                print(value, end='')
            elif(name.find('arg1').attrib['type']=="int"):
                print(name.find('arg1').text, end='')
            elif(name.find('arg1').attrib['type']=="nil"):
                print("", end='')
            elif(name.find('arg1').attrib['type']=="float"):
                try:
                    float_value=float.fromhex(name.find('arg1').text)
                except:
                    float_value=float(name.find('arg1').text)
                print(float.hex(float_value), end='')
        if (name.get('opcode').upper() == "EXIT"):
            if(name.find('arg1').attrib['type'] == "var"):
                exit_code=get_variable_value(name, "arg1")
                if(exit_code=None):
                    sys.exit(56)
                try:
                    exit_code=int(exit_code);
                except:
                    sys.exit(53)
            else:
                try:
                    exit_code=int(name.find('arg1').text)
                except:
                    sys.exit(53)

            if( exit_code in range(0,49)):
                sys.exit(exit_code)
            else:
                sys.exit(57)
        if(name.get('opcode').upper() == "STRLEN"):
            if (name.find('arg2').attrib['type'] == "var"):
                string_len=get_variable_value(name, 'arg2')
                if (string_len[1] != "string" and string_len[1] != "nil"):
                    sys.exit(58)
                string_len=string_len[0]
            elif (name.find('arg2').attrib['type'] == "string"):
                string_len=escape_sequence(name.find('arg1').text)
            elif (name.find('arg2').attrib['type'] == "nil"):
                string_len=name.find('arg2').text
            else:
                sys.exit(58)
            string_len=len(string_len)
            string_len=(string_len, "int")
            save_variable_value(name, "arg1", string_len)
        if(name.get('opcode').upper() == "TYPE"):
            if (name.find('arg2').attrib['type'] == "var"):
                type=get_variable_value(name, 'arg2')
                if(type==""):
                    type=""
                else:
                    type=type[1]
            else:
                type=name.find('arg2').attrib['type']
            save_variable_value(name, "arg1", (type, "type"))
        if(name.get('opcode').upper() == "INT2CHAR"):
            if (name.find('arg2').attrib['type'] == "var"):
                integer=get_variable_value(name, 'arg2')
                if(integer[1] != "int"):
                    sys.exit(53)
                try:
                    integer=chr(integer[0])
                except:
                    sys.exit(58)
            else:
                if(name.find('arg2').attrib['type'] != "int"):
                    sys.exit(53)
                try:
                    integer=chr(int(name.find('arg2').text))
                except:
                    sys.exit(57)
            save_variable_value(name, "arg1", (integer, "string"))
        if(name.get('opcode').upper() == "FLOAT2INT"):
            if (name.find('arg2').attrib['type'] == "var"):
                floatpoint=get_variable_value(name, 'arg2')
                try:
                    floatpoint[1]
                except:
                    sys.exit(56)
                try:
                    integer = int(floatpoint[0])
                except:
                    sys.exit(53)
                if (floatpoint[1] != "float"):
                    sys.exit(53)
            else:
                if(name.find('arg2').attrib['type'] != "float"):
                    sys.exit(53)
                try:
                    int(name.find('arg2').text)
                except:
                    floatpoint=float.fromhex(name.find('arg2').text)
                try:
                    integer=int(floatpoint)
                except:
                    sys.exit(57)
            save_variable_value(name, "arg1", (integer, "int"))
        if(name.get('opcode').upper() == "INT2FLOAT"):
            if (name.find('arg2').attrib['type'] == "var"):
                integer=get_variable_value(name, 'arg2')
                try:
                    integer[1]
                except:
                    sys.exit(56)
                try:
                    floatpoint = float(integer[0])
                except:
                    sys.exit(53)
                if (integer[1] != "int"):
                    sys.exit(53)
            else:
                if(name.find('arg2').attrib['type'] != "float"):
                    sys.exit(53)
                try:
                    floatpoint=float(int(name.find('arg2').text))
                except:
                    sys.exit(57)
            save_variable_value(name, "arg1", (floatpoint, "float"))
        if(name.get('opcode').upper() == "READ"):
            try:
                input_value= input()
                if (name.find('arg2').text == "string"):
                    input_value=escape_sequence(input_value)
                    input_value = (input_value, "string")
                elif (name.find('arg2').text == "int"):
                    input_value = (input_value, "int")
                elif (name.find('arg2').text == "float"):
                    try:
                        input_value=float.fromhex(input_value)
                    except:
                        input_value=float(input_value)
                    input_value = (input_value, "float")
                elif (name.find('arg2').text == "bool"):
                    if (input_value.upper() == "TRUE"):
                        input_value = "true"
                    else:
                        input_value = "false"
                    input_value = (input_value, "bool")
                else:
                    input_value = "nil"
                    input_value = (input_value, "nil")
            except EOFError:
                input_value=("nil", "nil")
            save_variable_value(name, "arg1", input_value)
        if(name.get('opcode').upper() == "MOVE"):
            if(name.find('arg2').attrib['type'] == "var"):
                moved=get_variable_value(name, "arg2")
                type=moved[1]
                moved=moved[0]
            if (name.find('arg2').attrib['type'] == "string"):
                moved=name.find('arg2').text
                moved=escape_sequence(moved)
                type=name.find('arg2').attrib['type']
            elif (name.find('arg2').attrib['type'] == "int"):
                try:
                    moved=int(name.find('arg2').text)
                    type=name.find('arg2').attrib['type']
                except:
                    sys.exit(53)
            elif (name.find('arg2').attrib['type'] == "nil"):
                moved=name.find('arg2').text
                type=name.find('arg2').attrib['type']
            elif (name.find('arg2').attrib['type'] == "float"):
                try:
                    int(name.find('arg2').text)
                    moved=float(name.find('arg2').text)
                    type=name.find('arg2').attrib['type']
                except:
                    moved=float.fromhex(name.find('arg2').text)
                    type=name.find('arg2').attrib['type']
            elif(name.find('arg2').attrib['type'] == "bool"):
                if(name.find('arg2').text == "true"):
                    moved="true"
                    type="bool"
                elif(name.find('arg2').text == "false"):
                    moved="false"
                    type="bool"
                else:
                    sys.exit(53)
            if(name.find('arg1').attrib['type'] == "var"):
                save_variable_value(name, "arg1", (moved, type))
            else:
                sys.exit(53)
        if (any(three_operand)):
            if(name.get('opcode').upper() == "ADD"):
                value1=find_value('arg2', name)
                value2=find_value('arg3', name)
                first_value=value1[0]
                second_value=value2[0]
                if(value1[1] != value2[1]):
                    sys.exit(53)
                if(value1[1] != "int" and value1[1] != "float"):
                    sys.exit(53)
                result=first_value+second_value
                if(value1[1] == "int" and value2[1] == "int"):
                    type="int"
                if(value1[1] == "float" or value2[1] == "float"):
                    type="float"
            elif(name.get('opcode').upper() == "SUB"):
                value1=find_value('arg2', name)
                value2=find_value('arg3', name)
                first_value=value1[0]
                second_value=value2[0]
                if(value1[1] != value2[1]):
                    sys.exit(53)
                if(value1[1] != "int" and value1[1] != "float"):
                    sys.exit(53)
                result=first_value-second_value
                if(value1[1] == "int" and value2[1] == "int"):
                    type="int"
                if(value1[1] == "float" or value2[1] == "float"):
                    type="float"
            elif (name.get('opcode').upper() == "MUL"):
                value1=find_value('arg2', name)
                value2=find_value('arg3', name)
                first_value=value1[0]
                second_value=value2[0]
                if(value1[1] != value2[1]):
                    sys.exit(53)
                if(value1[1] != "int" and value1[1] != "float"):
                    sys.exit(53)
                result=first_value*second_value
                if(value1[1] == "int" and value2[1] == "int"):
                    type="int"
                if(value1[1] == "float" or value2[1] == "float"):
                    type="float"
            elif (name.get('opcode').upper() == "IDIV"):
                value1=find_value('arg2', name)
                value2=find_value('arg3', name)
                first_value=value1[0]
                second_value=value2[0]
                if(value1[1] != value2[1]):
                    sys.exit(53)
                if(value1[1] != "int"):
                    sys.exit(53)
                if(second_value == 0):
                    sys.exit(57)
                result=first_value//second_value
                type="int"
            elif (name.get('opcode').upper() == "DIV"):
                value1=find_value('arg2', name)
                value2=find_value('arg3', name)
                first_value=value1[0]
                second_value=value2[0]
                if(second_value == 0):
                    sys.exit(57)
                if (value1[1] != value2[1]):
                    sys.exit(53)
                if(value1[1] != "int" and value1[1] != "float"):
                    sys.exit(53)
                result=first_value/second_value
                if(value1[1] == "int" and value2[1] == "int"):
                    type="int"
                if(value1[1] == "float" or value2[1] == "float"):
                    type="float"
            elif(name.get('opcode').upper() == "LT"):
                values=get_value_comparasion(name)
                if(values[0][1] == "nil" or values[1][1]=="nil"):
                    sys.exit(53)
                if(values[0][1] != values[1][1]):
                    sys.exit(53)
                result=values[0][0] < values[1][0]
                if(result == True):
                    result="true"
                else:
                    result="false"
                type = "bool"
            elif (name.get('opcode').upper() == "GT"):
                values = get_value_comparasion(name)
                if (values[0][1] == "nil" or values[1][1] == "nil"):
                    sys.exit(53)
                if (values[0][1] != values[1][1]):
                    sys.exit(53)
                result = values[0][0] > values[1][0]
                if(result == True):
                    result="true"
                else:
                    result="false"
                type = "bool"
            elif (name.get('opcode').upper() == "EQ"):
                values = get_value_comparasion(name)
                if (values[0][1] != "nil" and values[1][1] != "nil"):
                    if (values[0][1] != values[1][1]):
                        sys.exit(53)
                result = values[0][0] == values[1][0]
                if(result == True):
                    result="true"
                else:
                    result="false"
                type = "bool"
            elif(name.get('opcode').upper() == "AND"):
                values= get_value_comparasion(name)
                if(values[0][1] != "bool" or values[1][1] !="bool"):
                    sys.exit(53)
                if(values[0][0] == "true" and values[1][0] == "true"):
                    result="true"
                    type="bool"
                else:
                    result="false"
                    type="bool"
            elif(name.get('opcode').upper() == "OR"):
                values= get_value_comparasion(name)
                if(values[0][1] != "bool" or values[1][1] !="bool"):
                    sys.exit(53)
                if(values[0][0] == "true" or values[1][0] == "true"):
                    result="false"
                    type="bool"
                else:
                    result="true"
                    type="bool"
            elif(name.get('opcode').upper() == "NOT"):
                if(name.find('arg2').attrib['type'] == "bool"):
                    if(name.find('arg2').text == "false"):
                        result="true"
                        type="bool"
                    else:
                        result="false"
                        type="bool"
                elif(name.find('arg2').attrib['type'] == "var"):
                    if (name.find('arg2').text[:2] == "GF"):
                        if (name.find('arg2').text[3:] in Global_frame):
                            pass
                        else:
                            sys.exit(54)
                        result=Global_frame[name.find('arg1').text[3:]]
                    elif (name.find('arg2').text[:2] == "LF"):
                        if (len(FrameStack) == 0):
                            sys.exit(55)
                        value=FrameStack.pop()
                        FrameStack.append(value)
                        if (name.find('arg2').text[3:] in value):
                            pass
                        else:
                            sys.exit(54)
                        result = value[name.find('arg1').text[3:]]
                    elif (name.find('arg1').text[:2] == "TF"):
                        if (name.find('arg1').text[3:] in Temporary_frame):
                            pass
                        else:
                            sys.exit(54)
                        result= Temporary_frame[name.find('arg1').text[3:]]
                    else:
                        sys.exit(54)
                    if(result[1] != "bool"):
                        sys.exit(53)
                    if(result[0] == "true"):
                        result="false"
                        type="bool"
                    else:
                        result="true"
                        type= "bool"
            elif(name.get('opcode').upper() == "STRI2INT"):
                values=get_value_comparasion(name)
                if(values[0][1] != "string"):
                    sys.exit(53)
                if(values[1][1] != "int"):
                    sys.exit(53)
                try:
                    result=values[0][0][int(values[1][0])]
                    result=ord(result)
                    type="int"
                except:
                    sys.exit(58)
            elif(name.get('opcode').upper() == "CONCAT"):
                values=get_value_comparasion(name)
                if(values[0][1] != "string" or values[1][1] != "string"):
                    sys.exit(53)
                if(values[0][0] == None):
                    result=values[1][0]
                elif(values[1][0]== None):
                    result=values[0][0]
                else:
                    result=values[0][0]+values[1][0]
                type="string"
            elif(name.get('opcode').upper() == "GETCHAR"):
                values=get_value_comparasion(name)
                if(values[0][1] != "string"):
                    sys.exit(53)
                try:
                    position= int(values[1][0])
                except:
                    sys.exit(53)
                string=values[0][0]
                try:
                    result=string[position]
                    type="string"
                except:
                    sys.exit(58)
            elif(name.get('opcode').upper() == "SETCHAR"):
                values=get_value_comparasion(name)
                if(values[1][1] != "string"):
                    sys.exit(53)
                if(values[1][0] == ""):
                    sys.exit(58)
                try:
                    position= int(values[0][0])
                except:
                    sys.exit(53)
                if (name.find('arg1').text[:2] == "GF"):
                    if (name.find('arg1').text[3:] in Global_frame):
                        pass
                    else:
                        sys.exit(54)
                    string=Global_frame[name.find('arg1').text[3:]]
                elif (name.find('arg1').text[:2] == "LF"):
                    if (len(FrameStack) == 0):
                        sys.exit(55)
                    value=FrameStack.pop()
                    FrameStack.append(value)
                    if (name.find('arg1').text[3:] in value):
                        pass
                    else:
                        sys.exit(54)
                    string=value[name.find('arg1').text[3:]]
                elif (name.find('arg1').text[:2] == "TF"):
                    if (name.find('arg1').text[3:] in Temporary_frame):
                        pass
                    else:
                        sys.exit(54)
                    string=Temporary_frame[name.find('arg1').text[3:]]
                else:
                    exit(55)
                string=string[0]
                string=list(string)
                try:
                    string[position]=values[1][0]
                except:
                    sys.exit(58)
                result=''.join(string)
                type="string"

            else:
                sys.exit(32)
            if (name.find('arg1').attrib['type'] == "var"):
                save_variable_value(name, "arg1", (result, type))
        if(name.get('opcode').upper() == "JUMPIFEQ" or name.get('opcode').upper() == "JUMPIFNEQ"):
            values=get_value_comparasion(name)
            if(values[0][1] == values[1][1] or (values[0][0] == "nil" or values[1][0] == "nil")):
                if(values[0][0] == values[1][0] and name.get('opcode').upper() == "JUMPIFEQ"):
                    try:
                        instruction_number = Labels[name.find('arg1').text]
                    except:
                        sys.exit(52)
                    instruction_number += 1
                    sematic_check(root, instruction_number)
                    break
                if(values[0][0] != values[1][0] and name.get('opcode').upper() == "JUMPIFNEQ"):
                    try:
                        instruction_number = Labels[name.find('arg1').text]
                    except:
                        sys.exit(52)
                    instruction_number += 1
                    sematic_check(root, instruction_number)
                    break
            else:
                sys.exit(32)




args=parse_arguments()
source=args.source
input_args=args.source
if(args.help):
    if(args.source != None or args.input != None):
        sys.exit(10)
    print("Napoveda k programu - program se spousti pomoci:\n python3.8 --source=$source_file --input=$input_file")
    sys.exit(0)
if(args.input == None and args.source == None):
    exit(11)
elif(args.source == None):
    source=""
    for line in sys.stdin:
        source += line
if(args.source == None):
    tree=ET.fromstring(source)
    tree=ET.ElementTree(tree)
else:
    try:
        tree=ET.parse(source)
    except:
        sys.exit(31)
if (args.input != None):
    try:
        sys.stdin=open(args.input, 'r')
    except:
        sys.exit(11)
root=tree.getroot()
if(root.tag != "program"):
    sys.exit(32)
if(root.get('language').upper() != "IPPCODE20"):
    sys.exit(32)
#1. syntaktická kontrola (základní kontrola možný argumentů a ukládání labelů pro 2. kontrolu
current_order=-1
while(1):
    current_order = -1
    insert=False
    for name in root.findall('instruction'):
        try:
            if (int(name.get('order')) == current_order):
                exit(32)
            if (int(name.get('order')) < current_order and current_order != -1):
                root.remove(name)
                for tmp_next in root.findall('instruction'):
                    if (int(name.get('order')) == int(tmp_next.get('order'))):
                        exit(32)
                    if (int(name.get('order')) < int(tmp_next.get('order'))):
                        next = int(tmp_next.get('order'))
                        break
                old_code = -1
                for tmp_name in root.findall('instruction'):
                    if (int(name.get('order')) == old_code):
                        sys.exit(32)
                    if (int(name.get('order')) > old_code and int(name.get('order')) < next):
                        if (old_code == -1):
                            root.insert(0, name)
                            insert=True
                        else:
                            tmp_name.addnext(name)
                            insert=True
                        break
                    old_code = int(tmp_name.get('order'))
            if(insert == True):
                break
            if (int(name.get('order')) < 1):
                sys.exit(32)
            current_order = int(name.get('order'))
        except:
            sys.exit(32)
    old_value=-1
    for name in root.findall('instruction'):
        if(old_value < int(name.get('order'))):
            order=True
        else:
            order=False
            break
        old_value=int(name.get('order'))
    if(order==True):
        break
for child in root:
    if(child.tag != "instruction"):
        sys.exit(32)
for name in root.findall('instruction'):
    parse_instruction(name)
#2. Běh sematicka kontrola a interpretace
sematic_check(root, 1)