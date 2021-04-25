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
        ip = input("Enter the IP Address: ")
        f.write(ip)
else :
    with open(ipFile, "r") as f :
        ip = f.read()

bulb = yeelight.Bulb(ip)


#Opens the main window
def mainWindow() :
    sg.theme('LightGrey2')

    #Fallbacks in case the info cannot be retrived down below
    lastBrightness = 100
    lastPower = True

    #Retrives the state of the lightbulb
    try :
        lastPower = bulb.get_properties()["power"] == "on"
        lastBrightness = int(bulb.get_properties()["bright"])
    except :
        sg.popup_error("Could not retrive info", title = "Error")

    layout = [[sg.Text('Yeelight Control')],
                [sg.Radio('ON', "RADIO1", default=lastPower, enable_events=True), sg.Radio('OFF', "RADIO1", enable_events=True, default=not lastPower)],
                [sg.Slider(range=(1,100),default_value=lastBrightness, size=(20,15), orientation='horizontal', font=('Helvetica', 12))],
                [sg.Button('Set')] ]

    window = sg.Window('Yeelight', layout, no_titlebar = False, grab_anywhere = False, keep_on_top = False, margins = (8, 8), icon="icon.ico")
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel':
            break
        power = values[0]
        brightness = int(values[2])

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
        except :
            sg.popup_error('Something went wrong. Make sure the IP Address is correct and that LAN Control is turned on in the yeelight app.\nIf everything is set up correctly, you may also be getting rate limited, try again in a minute.', title="Error")
    window.close()

if __name__ == "__main__" :
    mainWindow()