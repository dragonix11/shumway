#!/usr/bin/env python
import sys,os.path,os,getopt,time,subprocess,re,argparse
from dis import disassemble

class Base:
    asc = None
    avm = None
    
    def __init__(self):
        self.setEnvironmentVariables();
        pass
    
    def setEnvironmentVariables(self):
        if 'ASC' in os.environ:
            self.asc = os.environ['ASC'].strip();
        else:
            print "Environment variable ASC is not defined, set it to asc.jar"
        
        if not self.asc:
            sys.exit();

    def runAsc(self, file, createSwf = False):
        args = ["java", "-jar", self.asc, file]
        subprocess.call(args)
        if createSwf:
            args = ["java", "-jar", self.asc, "-swf", "cls,1,1", file]
            subprocess.call(args)

    def runAvm(self, file, execute = True, quiet = False, disassemble = False):
        args = ["js", "avm.js"];
        if disassemble:
            args.append("-d")
        if quiet:
            args.append("-q")
        if execute:
            args.append("-x")
        args.append(file)
        subprocess.call(args)
            
class Command(Base):
    name = ""
    
    def __init__(self, name):
        Base.__init__(self)
        self.name = name
    
    
class Asc(Command):
    def __init__(self):
        Command.__init__(self, "asc")
        
    def __repr__(self):
        return self.name
    
    def execute(self, args):
        parser = argparse.ArgumentParser(description='Compiles an ActionScript source file to .abc or .swf using the asc.jar compiler.')
        parser.add_argument('src', help="source .as file")
        parser.add_argument('-swf', action='store_true', help='optionally package compiled file in a .swf file')
        args = parser.parse_args(args)
        print "Compiling %s" % args.src
        self.runAsc(args.src, args.swf)

class Avm(Command):
    def __init__(self):
        Command.__init__(self, "avm")
        
    def __repr__(self):
        return self.name
    
    def execute(self, args):
        parser = argparse.ArgumentParser(description='Runs an .abc file using Shumway AVM')
        parser.add_argument('src', help="source .abc file")
        args = parser.parse_args(args)
        print "Running %s" % args.src
        self.runAvm(args.src)

class Dis(Command):
    def __init__(self):
        Command.__init__(self, "dis")
        
    def __repr__(self):
        return self.name
    
    def execute(self, args):
        parser = argparse.ArgumentParser(description='Disassembles an .abc file ')
        parser.add_argument('src', help="source .abc file")
        args = parser.parse_args(args)
        print "Disassembling %s" % args.src
        self.runAvm(args.src, execute = False, disassemble = True)
                
commands = {}
for command in [Asc(), Avm(), Dis()]:
    commands[str(command)] = command;

parser = argparse.ArgumentParser()
parser.add_argument('command', help=",".join(commands.keys()))
args = parser.parse_args(sys.argv[1:2])

if (not args.command in commands):
    print "Invalid command: %s" % args.command
    parser.print_help()

command = commands[args.command];
command.execute(sys.argv[2:])