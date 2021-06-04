#Import modules, throw an error if they cannot be imported
try :
    import PySimpleGUI as sg
except :
    input("It seems like you did not install the PySimpleGUI module..\nPlease install PySimpleGUI")
    quit()

try :
    import yeelight
except :
    sg.popup_error("It seems like you did not install the yeelight module..\nPlease install yeelight", title="Fatal error")
    quit()

import os

#Location of a file that includes the IP Address of the yeelight lightbulb
ipFile = "yeelightIP.txt"

#Creates the file if it doesnt exist, if it does, sets the variable "ip" from the file
if not os.path.isfile(ipFile) :
    with open(ipFile, "w") as f :
        sg.theme('LightGrey2')
        layout = [  [sg.Text('Enter your yeelight device IP Address:')],
            [sg.InputText()],
            [sg.Button('Submit'), sg.Button('Cancel')] ]
        window = sg.Window('Yeelight', layout, no_titlebar = False, grab_anywhere = False, keep_on_top = False, margins = (8, 8), icon="icon.ico")
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'Cancel':
                quit()
            ip = values[0]
            f.write(ip)
            break
        window.close()

else :
    with open(ipFile, "r") as f :
        ip = f.read()

bulb = yeelight.Bulb(ip)

def mainWindow() :
    sg.theme('LightGrey2')

    #Fallbacks in case the info cannot be retrived down below
    lastBrightness = 100
    lastPower = True
    hasColor = False

    #Retrives the state of the lightbulb
    try :
        properties = bulb.get_properties()
        lastPower = properties["power"] == "on"
        lastBrightness = int(properties["bright"])
        #bulbType = str(bulb.bulb_type)
        bulbType = "disabled"
        hasColor = bulbType == "BulbType.Color"
        hasTemp = bulbType == "BulbType.WhiteTemp" or bulbType == "BulbType.Color"
        lastColor = lastColor = "#ffffff"
    except :
        sg.popup_error("Could not retrive info", title = "Error")
    
    if hasColor :
        colorRow = [sg.ColorChooserButton("Select color")]
    else :
        colorRow = []
    
    if hasTemp :
        tempRow = [sg.Button("Reset")] #Temp does not mean temporary
    else :
        tempRow = []

    layout = [[sg.Text('Yeelight Control')],
                [sg.Radio('ON', "RADIO1", default=lastPower, enable_events=True), sg.Radio('OFF', "RADIO1", enable_events=True, default=not lastPower)],
                colorRow,
                [sg.Slider(range=(1,100),default_value=lastBrightness, size=(20,15), orientation='horizontal', font=('Helvetica', 12))],
                tempRow,
                [sg.Button('Set')] ]

    window = sg.Window('Yeelight', layout, no_titlebar = False, grab_anywhere = False, keep_on_top = False, margins = (8, 8), icon="icon.ico")

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel':
            break
        power = values[0]
        brightness = int(values[2])
        if hasColor :
            color = values["Select color"]
        else :
            color = "#ffffff"

        if event == "Reset" : #Sets all values to fully bright white color
            color = lastColor
            brightness = 100
            power = True
            if hasTemp :
                bulb.set_color_temp(99999999)

        try :
            if not power == lastPower : #If the power state changed
                lastPower = power
                if power :
                    bulb.turn_on()
                else :
                    bulb.turn_off()
            if not brightness == lastBrightness and power : #If the brightness changed
                lastBrightness = brightness
                bulb.set_brightness(brightness)
            if not color == lastColor and power and hasColor : #If the color changes, and the bulb even has color
                if not len(color) == 0  :
                    lastColor = color
                else :
                    color = lastColor
                color = color.lstrip("#")
                rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4)) #Thanks @john1024 on StackOverflow, converts HEX to RGB
                if not rgb == (0, 0, 0) :
                    bulb.set_rgb(*rgb)
                else :
                    bulb.set_rgb(1, 1, 1)
        except :
            sg.popup_error('Something went wrong. Make sure the IP Address is correct and that LAN Control is turned on in the yeelight app.\nIf everything is set up correctly, you may also be getting rate limited, try again in a minute.', title="Error")
        
        if event == "Reset" : #Resets the whole window
            window.close()
            mainWindow()

    window.close()

if __name__ == "__main__" :
    mainWindow()