import json
import subprocess
import os
import keyboard
from pathlib import Path
import threading

version = "v0.0.1"

srcPath = Path(__file__).parent

f = open(srcPath / "snippets.json")
snippetsDict = json.loads(f.read())

f = open(srcPath / "temp.py", "r")
template = f.read()

binding = {}

endCode = "if stopKey != \"\": keyboard.wait(stopKey)"

def runCode(code):
    # print("Here!\n")
    # f = open(srcPath / "temp.file.py", "w")
    # f.write(code)
    # f.close()
    # subprocess.run(["python", srcPath / "temp.file.py"])
    print(code)
    exec(code)
    # os.remove(srcPath / "temp.file.py")

def runSnippet(*args):
    # print(args)
    # code = "".join(args)
    code = args[0]
    code = template + "\n" + f"hotkeyId = {args[1]}" + "\n" + code + "\n" + endCode
    t = threading.Thread(target=runCode, args=(code,))
    t.run()
    # runCode(code)

def initSnippetByName(name):
    snippetFileName = snippetsDict[name]["name"]
    snippetHotKey = snippetsDict[name]["hotkey"]
    f = open(srcPath / name / snippetFileName, "r")
    snippetFile = f.read()
    # for key, value in snippetHotKey.items():
    #     binding[key] = [snippetFile, value]
    binding[snippetHotKey] = [snippetFile, 0]

hotkeys = []

def registerAll():
    for key in snippetsDict:
        initSnippetByName(key)
    
    for key, value in binding.items():
        # print(type(value))
        hotkey = keyboard.add_hotkey(key, callback=runSnippet, args=(value))
        hotkeys.append(hotkey)

def clear():
    global hotkeys
    for i in hotkeys:
        keyboard.remove_hotkey(i)
    hotkeys = []

def reloadOnNewCommandLine():
    global srcPath
    f = open(srcPath / "snippets.json")
    global snippetsDict
    res = f.read()
    print(res)
    snippetsDict = json.loads(res)
    clear()
    registerAll()

def loadSnippet(file, hotkey):
    f = open(file)
    jsonFile = json.loads(f.read())
    name = list(jsonFile.keys())[0]
    # print(type(snippetsDict[self.name.get()]))
    snippetsDict[name] = {}
    snippetsDict[name]["hotkey"] = hotkey
    snippetsDict[name]["description"] = jsonFile[name]["description"]
    snippetsDict[name]["name"] = jsonFile[name]["name"]
    snippetsDict[name]["usage"] = jsonFile[name]["usage"]
    f = open(srcPath / "snippets.json", "w")
    f.write(json.dumps(snippetsDict))
    f.close()
    reloadOnNewCommandLine()

icon = """
   _____       _                  _   
  / ____|     (_)                | |  
 | (___  _ __  _ _ __  _ __   ___| |_ 
  \___ \| '_ \| | '_ \| '_ \ / _ \ __|
  ____) | | | | | |_) | |_) |  __/ |_ 
 |_____/|_| |_|_| .__/| .__/ \___|\__|
                | |   | |             
                |_|   |_|             
"""

usage = """
commands:
  help                      get help
  load   file hotkey        load a snippet, file should refer to a file that's a json
  run    name               run a snippet by it's name
  rebind name hotkey        rebind a snippet's hotkey
  delete name               delete a snippet
  exit                      exit snippet
"""

def repl():
    while True:
        command = input(">>> ")
        commandLex = command.split()
        if commandLex[0] == "help":
            print(usage)
        if commandLex[0] == "exit":
            return
        if commandLex[0] == "load":
            if len(commandLex) < 3:
                print("Wrong Command: Too few arguments, expect 3, get ", len(commandLex) - 1)
                continue
            loadSnippet(commandLex[1], commandLex[2])

if __name__ == "__main__":
    print(icon)
    print("version: ", version, " - https://github.com/SnippetDeveloper/Snippet")
    print("Automate boring things with python!")
    registerAll()
    repl()