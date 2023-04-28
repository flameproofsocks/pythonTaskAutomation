# This program is meant to automate online tasks using python
# test
### Functionality
# Ability to record and replay mouse movements
    # replay text inputs
    # replay pauses and waits between actions
    # find html elements used in each actions for better versatility
    # output these to some re-usable script format (maybe txt)

# Ability to input texts on familiar prompts
# Ability to use AI (or something like it) to fill out unfamaliar prompts
# Ability to input text and numbers both one at a time and as a copy paste
    # to deal with different types of prompts
# Ability to read user user configurations and input data from a yml/json/
# ggggg


from pynput import mouse, keyboard
import keyboard as kb
import time
import pyperclip
import pyautogui


# Open output file for writing
outputFile = open("automationScripts/indeedAutomation/findNextIndeedJob.txt", "w")

# Initialize last click time to None
lastClickTime = None
isInKeyboardSequence = False
# Pressed: alt_l
# Pressed: f4

# Pressed: alt_l
# Pressed: tab
# ctrl v
# a
# c
# z
# f
# n
#
specialCharacterMap = {
    r"\x01": "Ctrl+A",
    r"\x03": "Ctrl+C",
    r"\x1a": "Ctrl+Z",
    r"\x06": "Ctrl+F",
    r"\x0e": "Ctrl+N",
    r"\x0e": "Ctrl+Shift+N"

}

def getLetterFromHex(hex):
    decimalValue = int(hex, 16)
    alphabet = 'abcdefghijklmnopqurtuvwxyz'
    letter = alphabet[decimalValue-1]
    return letter

# creates a
def createSpecialCharacter(previousCharacter, escapeCode):
    print("Escape character: " + escapeCode)
    if "alt" in previousCharacter:
        return "Alt+"+escapeCode

    escapeCode = escapeCode.replace("\'", "")
    escapeCode = escapeCode.replace("\\", "") # f
    letter = getLetterFromHex(escapeCode.split("x")[-1])
    if "ctrl" in previousCharacter:
        return "Ctrl+"+letter

# Function called when a mouse click is detected
def onClick(x, y, button, pressed):
    global lastClickTime
    global isInKeyboardSequence
    isInKeyboardSequence = False
    # Check if button is pressed


    buttonName = "Right"
    if button.name == "left":
        buttonName = "Left"

    if pressed:
        # Get current time in milliseconds
        currentTime = int(round(time.time() * 1000))
        # If last click time is not None, calculate time between clicks and write to file
        if lastClickTime is not None:
            timeBetweenClicks = currentTime - lastClickTime
            outputFile.write(f"Pause: {timeBetweenClicks}\n")
            outputFile.write(f"{buttonName} Clicked at: x={x}, y={y} \n")
        # Write clicked position to file if last click time is None
        else:
            outputFile.write(f"{buttonName} Clicked at: x={x}, y={y}\n")
        # Update last click time
        lastClickTime = currentTime


previousCharacter = ""
# Function called when a key is pressed
def onPress(key):
    global lastClickTime
    global isInKeyboardSequence
    global previousCharacter

    currentTime = int(round(time.time() * 1000))

    # Close the output file and return False if the escape key is pressed ff d d
    if key == keyboard.Key.esc:
        outputFile.write(f"EOF")
        outputFile.close()
        return False

    if "x16" in str(key): # test test test test performAction(key, value)
        outputFile.write(f"pasteStart{pyperclip.paste()}pasteEnd\n")
        isInKeyboardSequence = True
        lastClickTime = currentTime
        return

    if r"\x" in str(key):
        specialSequence = createSpecialCharacter(previousCharacter, str(key))
        if not isInKeyboardSequence: # f
            outputFile.write(f"Pause: {currentTime - lastClickTime}\n")
        outputFile.write(f"Combo: {specialSequence}\n")
        return

    # adding a way to detect alt+f4 and alt+tab by previous character being alt
    if "alt_" in previousCharacter:
        combo = ""
        if "tab" in str(key):
            combo = "Alt+Tab"
        if "f4" in str(key):
            combo = "Alt+f4"
        if combo != "":
            if not isInKeyboardSequence: # f
                outputFile.write(f"Pause: {currentTime - lastClickTime}\n")
            outputFile.write(f"Combo: {combo}\n")
            return

    keyText = str(key).replace("'", "")
    keyText = keyText.replace("Key.", "")

    try:
        # If key is a character, write the character to file
        if not isInKeyboardSequence:
            outputFile.write(f"Pause: {currentTime - lastClickTime}\n")
        outputFile.write(f"Pressed: {keyText}\n")
    except AttributeError:
        # If key is not a character, write the key to file ff
        if not isInKeyboardSequence:
            outputFile.write(f"Pause: {currentTime - lastClickTime}\n")
        outputFile.write(f"Pressed: {keyText}\n")


    isInKeyboardSequence = True
    lastClickTime = currentTime
    previousCharacter = keyText


# Function that starts tracking mouse and keyboard inputs
def trackInput():


    # Start mouse listener and keyboard listener
    with mouse.Listener(on_click=onClick) as mouseListener:
        with keyboard.Listener(on_press=onPress) as keyboardListener:
            # Wait for listeners to join
            mouseListener.join()
            keyboardListener.join()

trackInput()


# def takeInputs():
#     outputFile = input("Please specify what the output file should be called: ")
#
#
#
#     # run using our listener functions
#     with mouse.Listener(on_click=on_click) as listener:
#         with keyboard.Listener(on_press=on_press) as k_listener:
#             while ggggg