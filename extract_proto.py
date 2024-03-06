import re
import os

import argparse
proto_types = ['BOOL', 'BYTES', 'DOUBLE', 'ENUM', 'Enum', 'FIXED32', 'FIXED64', 'FLOAT', 'SFIXED32', 'SFIXED64', 'SINT32', 'SINT64', 'STRING', 'UINT32', 'UINT64', "INT32", "INT64"]

convert_dict = dict(zip([item.lower() for item in proto_types], proto_types))
#print(convert_dict)

def proto_to_dict(proto_path):
    f = open(proto_path)
    t = ''.join(f.readlines())
    regex = r"[a-z0-9]* [_a-zA-Z]* = [0-9]*[0-9]"
    tmp = re.findall(regex, t)
    res = {}
    for item in tmp:
        things = item.split(' ')
        res.update({things[-1]: (things[0], things[1])})
    return res

def proto_to_python_message_declaration_file(proto_path, your_path="./messages/"):
    os.makedirs(your_path, exist_ok=True)
    filename=proto_path.split('/')[-1][:-6] + ".py"
    lines = ["import proto", "\n", f"class MessageSchema(proto.Message):\n"]
    dicti = proto_to_dict(proto_path)
    for number in dicti.keys():
        lines.append(f"    {dicti[number][1]} = proto.Field(proto.{convert_dict[dicti[number][0]]}, number={number})\n")

    f = open(your_path + filename, "w")
        
    f.writelines(lines)
#    print(*lines,sep="\n")


def isMessage(s):
    regex = r"message [a-zA-Z]*"
    return len(re.findall(regex,s)) > 0

def isAttr(s):
    regex = r"[a-zA-Z0-9]* [_a-zA-Z]* = [0-9]*[0-9]"
    return len(re.findall(regex,s)) > 0


def nestedObjectParser(proto_path, your_path="./messages/"):
    if not os.path.exists(your_path):
        os.mkdir(your_path)
    import pprint
    f = open(proto_path)
    accepted_lines = []
    lines = f.readlines()
    line_info = {}
    varRegex = r"[a-zA-Z0-9]* [_a-zA-Z]* = [0-9]*[0-9]"
    messRegex = r"message [a-zA-Z]*"
    for i in range(len(lines)):
        stripped = lines[i].lstrip()
        if not (stripped.startswith("package") and stripped.startswith("syntax")) and (isAttr(stripped) or isMessage(stripped)):
            accepted_lines.append(lines[i])

    #print(accepted_lines[10:50])
    messages = {}
    attributes = {}
    for line in accepted_lines:
        if isMessage(line): # if a message -> define a new one with those lines
            level = getLayers(line)
            name = line.lstrip().split(' ')[1]
            messages.update({name: level})
        else:
            level = getLayers(line)
            attributes.update({line: level-1})

    #print(messages)
    #print("\n\n\n\n\n")
    #print(attributes)
    name = None
    mapping = {}
    for line in accepted_lines:
        if isMessage(line):
            name = line.lstrip().split(' ')[1]
        elif isAttr(line):
            tmp = re.findall(varRegex, line)[0].split(' ')
            if name in mapping.keys():
                mapping[name].append((tmp[1], tmp[0], tmp[3])) # Name, type, number
            else:
                mapping[name] = [(tmp[1], tmp[0], tmp[3])]


    #print(tmp)
    pprint.pprint(mapping)
    pyfile_lines = ["import proto\n"]
    for mess in list(mapping.keys())[::-1]:
        pyfile_lines.append("\n\n")
        pyfile_lines.append(f"class {mess}(proto.Message):\n")
        for attr in mapping[mess]:
            if attr[1] in convert_dict.keys():
                tmptype = "proto." + convert_dict[attr[1]]
            else:
                tmptype = attr[1]
            pyfile_lines.append(f"    {attr[0]} = proto.Field({tmptype}, number={attr[2]})\n")
    


    filename=proto_path.split('/')[-1][:-6] + ".py"
    f = open(your_path + filename, "w")
        
    f.writelines(pyfile_lines)



            #break
            #if name in mapping:
            #else:

            


    





    

    
def getLayers(s):
    if not s.startswith("  "):
        return 0
    return 1 + getLayers(s[2:])
    

def decode_utf8(obj):
    print(type(obj))
    if isinstance(obj, bytes):
        return obj.decode("utf-8")
    if isinstance(obj, list):
        res = []
        for item in obj:
            res.append(decode_utf8(item))
        return res
    if isinstance(obj, dict):
        for key, value in obj.items():
            obj.update({key: decode_utf8(value)})
        return obj
    return obj

if __name__ == "__main__":
    for name in os.listdir('./protos/'):
        #proto_to_python_message_declaration_file("./protos/" + name)
        nestedObjectParser("./protos/" + name)
        #break
