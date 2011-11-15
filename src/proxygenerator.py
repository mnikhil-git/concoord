import inspect, types
import os

INDENT = '\t'
get_class = lambda x: globals()[x]

def get_functions_of_obj(classobj):
    templist = dir(classobj)
    dirlist = []
    for temp in templist:
        if isinstance(classobj.__dict__[temp], types.FunctionType):
            dirlist.append(temp)
    return dirlist

def get_arguments_of_func(function):
    args, _, _, values = inspect.getargspec(function)
    return args

def create_file(classobj, clientobjfile):
    try:
        os.mkdir("clientsrc")
    except:
        pass
    f = open("clientsrc/"+os.path.basename(clientobjfile.name), 'w')
    objectfuncs = get_functions_of_obj(classobj)
    f.write("#automatically generated by the proxygenerator\n")
    f.write("from clientproxy import *\n\n")
    f.write("class "+classobj.__name__+"():\n")
    for func in objectfuncs:
        f.write(INDENT + "def " + func + "(")
        f.write(", ".join(get_arguments_of_func(getattr(classobj, func))) + "):\n")
        f.write(INDENT + INDENT + "invoke_command(")
        f.write("self, \"" + func + "\"")
        f.write(", ".join(['']+get_arguments_of_func(getattr(classobj, func))[1:]) + ")\n\n")
    f.close()
    return f

def createproxyfromname(classname):
    moduleobject = get_class(classname)
    classobject = getattr(moduleobject, objectname.capitalize())
    return create_file(classobject)

def getobjectfromname(classname):
    moduleobject = get_class(classname)
    return getattr(moduleobject, classname)

def main():
    abspath = os.path.abspath("bank.py")
    objectfile = open(abspath, "r")
    objectfile.close()
    
    moduleobject = __import__('bank', globals(), locals(), [], -1)
    classobject = getattr(moduleobject, "Bank")
    create_file(classobject, objectfile)

if __name__=='__main__':
    main()