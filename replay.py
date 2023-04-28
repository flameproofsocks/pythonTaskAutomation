import re
import pyautogui
import time
import pyperclip


# finds the first few lines and sees if they're variable names.
# if any line is a variable, it finds the key and value in this format:
# Var: KeyName: important data
# Var: OtherKeyName: important data blah blah
def readVariables(fileName):
    variableMap = {}
    with open(fileName, 'r') as file:
        lines = file.readlines()
        i = 0
        while i < len(lines):
            if lines[i].startswith("VarKey:"):
                key = lines[i].strip().replace("VarKey:", "").strip()
                i += 1
                if i < len(lines) and lines[i].startswith("VarValue:"):
                    value = lines[i].strip().replace("VarValue:", "").strip()
                    variableMap[key] = value
            i += 1
    return variableMap


# performs a combination of keys, I.E. "Ctrl+C"
# or Alt+f4
def performCombo(key1, key2):
    print("Performing combo: " + str(key1) + " - " + str(key2))
    pyautogui.keyDown(key1)
    pyautogui.press(key2)
    pyautogui.keyUp(key1)


# parses x and y coordinates for an input
def parseXY(input_string):
    x, y = input_string.split(", ")
    x = int(x.split("=")[1])
    y = int(y.split("=")[1])
    return x, y


# this gets passed an input (in the form of which action to take, a mouse, a pause, or a keyboard event
# then performs the task with the corresponding value
def performAction(action, value, variableMap):
    if "Pressed" in action:
        pyautogui.press(value)
    elif "Left Click" in action:
        pyautogui.leftClick(parseXY(value))
    elif "Right Click" in action:
        pyautogui.rightClick(parseXY(value))
    elif "Pause" in action:
        time.sleep(int(value)/1000) # convert ms to s
    elif "Combo" in action:
        performCombo(value.split("+")[0], value.split("+")[-1])
    elif "PasteVar" in action:
        pyperclip.copy(variableMap[value]) #paste the value
        print("Pasting variable")
        print(variableMap[value])
        pyautogui.keyDown("ctrl")
        pyautogui.press("v")
        pyautogui.keyUp("ctrl")
    elif "Paste" in action:
        pyperclip.copy(value) #paste the value
        pyautogui.keyDown("ctrl")
        pyautogui.press("v")
        pyautogui.keyUp("ctrl")
    else:#
        print("Action not found: " + str(action))

def replay(fileName = "", variableMap = {}):

    # grab the file name from the user
    if fileName == "":
        fileName = input("Please specify which file to replay: ")

    #grab any variables contained within the file
    if len(variableMap) == 0:
        variableMap = readVariables(fileName)


    #used to keep track of values to paste contained over multiple lines
    # these are delimted with "pasteStart" and "pasteEnd"
    pasteStarted = False
    pasteString = ""

    with open(fileName, "r") as inputFile:
        for line in inputFile:
            # Use regular expression to split line into key and value based on format of "Key: Value"
            if "EOF" in line:
                print("End of File Reached")
                return
#
            #handle pasting strings over multiple lines
            if 'pasteEnd' in line:
                pasteStarted = False
                lineData = line.split("pasteEnd")[0]
                if "pasteStart" in lineData:
                    lineData = lineData.split("asteStart")[-1]
                pasteString = pasteString + lineData
                performAction("Paste", pasteString, variableMap)
                continue

            if 'pasteStart' in line or pasteStarted:
                pasteStarted = True
                lineData = line.split("asteStart")[-1]
                pasteString = pasteString + lineData
                print("PASTING STRING BUILDER: " + pasteString)
                continue


            key = line.strip().split(": ")[0]
            value = line.strip().split(": ")[-1]

            if value == key:
                print("Error occurred")
                return

            print(f"Key: {key}, Value: {value}")
            performAction(key, value, variableMap)

# time.sleep(1)
# replay(r'automationScripts/downloadMJPins.txt')
#print(readVariables(r"automationScripts/uploadToTikTokYoutubeChannel.txt"))

