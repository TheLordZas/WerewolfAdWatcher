import sys

from ppadb.client import Client
from time import sleep
from PIL import Image
import numpy
from time import time
import datetime
from os import system


class noLog:
    def addLog(self, message):
        return 'NOLOG'


class Logs:
    def __init__(self):
        self.day = str(datetime.datetime.now())[:10]

    def addLog(self, message):
        self.hour = str(datetime.datetime.now())[11:19]
        with open('logs/' + self.day, 'a') as l:
            l.write(self.hour + '\t' + message + '\n')


class Screen:
    def __init__(self, passDevice, log):
        self.device = passDevice

    def screenshot(self):
        self.image = self.device.screencap()
        with open('screen.png', 'wb') as f:
            f.write(self.image)

        self.image = Image.open('screen.png')
        self.image = numpy.array(self.image, dtype=numpy.uint8)

    def checkScreen(self):
        self.screenshot()  # We capture the screen
        # We check the screen in which we are
        # print(self.image[418, 298])   # For debug

        # Check if there is no coin sign to exit
        default = 'UNKNOWN'
        if (93 < self.image[25, 25, 0] < 97
                and 197 < self.image[25, 25, 1] < 201
                and 231 < self.image[25, 25, 2] < 235):
            print('Screen: Entered Werewolf')
            log.addLog('Screen: Entered Werewolf')
            return 'FINISH'

        if (93 < self.image[220, 50, 0] < 110
                and 197 < self.image[220, 50, 1] < 220
                and 231 < self.image[220, 50, 2]):
            print('Screen: Entered Werewolf')
            log.addLog('Screen: Entered Werewolf')
            return 'WEREWOLF'

        if (115 < self.image[920, 600, 0] < 135
                and 28 < self.image[920, 600, 1] < 40
                and 24 < self.image[920, 600, 2] < 32):
            print('Screen: roulette')
            log.addLog('Screen: roulette')
            return 'ROULETTE'

        if (45 < self.image[418, 298, 0] < 58  # If roulette gets bugged
                and 48 < self.image[418, 298, 1] < 60
                and 52 < self.image[418, 298, 2] < 64):
            print('Screen: bugged roulette')
            log.addLog('Screen:  bugged roulette')
            return 'BROULETTE'

        if (52 < self.image[1100, 860, 0] < 72
                and 120 < self.image[1100, 860, 1] < 140
                and 210 < self.image[1100, 860, 2]):
            print('Screen: Confirm close video (Google)')
            log.addLog('Screen: Confirm close video (Google)')
            return 'CLOSE'

        if (48 < self.image[445, 440, 0] < 76
                and 111 < self.image[445, 440, 1] < 140
                and 210 < self.image[445, 440, 2] < 252):
            print('Screen: Confirm close video (Google)')
            log.addLog('Screen: Confirm close video (Google)')
            return 'CLOSE'

        if (95 < self.image[300, 500, 0] < 105
                and 230 < self.image[300, 500, 1]
                and self.image[300, 500, 2] < 15):
            print('Screen: Home')
            log.addLog('Screen: Home')
            return 'HOME'

        if (self.image[300, 500, 0] == 0
                and self.image[300, 500, 1] == 90
                and self.image[300, 500, 2] == 239):
            print('Screen: Home')
            log.addLog('Screen: Home')
            return 'EXIT'
        return default

    def checkButton(self):  # Returns the point of the button
        self.screenshot()
        self.count = 0  # 0: no ha empezado a contar, 1: está contando, 2: bloquea cuenta
        self.a = []
        # We sweep from y = 750 to y = 450
        for i in range(500):
            if self.image[1900 - i, 605, 0] > 230 and self.image[1900 - i, 605, 1] > 200 and self.image[
                1900 - i, 605, 1] > 200:
                if self.count == 0 or self.count == 1:
                    self.a.append(1900 - i)
                    self.count = 1
            else:
                if self.count == 1:
                    self.count = 2
        if self.a:
            return 605, int((self.a[0] + self.a[len(self.a) - 1]) / 2 )
        else:
            return -1, -1

    def checkButtonUpsideDown(self):  # Returns the point of the button
        self.screenshot()
        self.count = 0  # 0: no ha empezado a contar, 1: está contando, 2: bloquea cuenta
        self.a = []
        # We sweep from y = 750 to y = 450
        for i in range(400):
            if self.image[1400 + i, 605, 0] > 230 and self.image[1400 + i, 605, 1] > 200 and self.image[
                1400 + i, 605, 1] > 200:
                if self.count == 0 or self.count == 1:
                    self.a.append(1400 + i)
                    self.count = 1
            else:
                if self.count == 1:
                    self.count = 2
        if self.a:
            return 605, int((self.a[0] + self.a[len(self.a) - 1]) / 2)
        else:
            return -1, -1


def restartShell(device, myScreen, log):
    if myScreen.checkScreen() != 'HOME':
        device.shell('input keyevent KEYCODE_HOME')
    while myScreen.checkScreen() != 'HOME':
        pass
    device.shell('am force-stop com.werewolfapps.online')
    device.shell("su -c 'killall com.werewolfapps.online'")
    print('Werewolf stopped')
    log.addLog('Werewolf stopped')


def initWerewolf(device, log):
    print('Entering werewolf')
    log.addLog('Entering werewolf')
    device.shell('input touchscreen swipe 106 302 106 302 100')


def enterRoulette():  # Enter roulette
    device.shell('input touchscreen swipe 28 29  28 29 100')
    print('Entering roulette')
    log.addLog('Entering roulette')


def clickWatchVideo(myScreen, thisattempts):  # Click Watch Video
    print('Clicking Watch Video')
    upsidedown = thisattempts % 2
    if upsidedown == 1:
        x, y = myScreen.checkButtonUpsideDown()
    else:
        x, y = myScreen.checkButton()
    if y > 0:
        z = y
        y = y - 5 * thisattempts
        z = z + 5 * thisattempts
        device.shell('input touchscreen swipe {0} {1} {0} {1} 100'.format(x, y))
        device.shell('input touchscreen swipe {0} {1} {0} {1} 100'.format(x, z))
    else:
        return


def panicClick(attempts):
    x = attempts*70 + 1150
    device.shell('input touchscreen swipe 605 {0} 605 {0} 100'.format(x))

def exitAd():
    # Press X
    # Left
    device.shell('input touchscreen swipe 70 65  70 65 100')
    # Right
    device.shell('input touchscreen swipe 1130 65 1130 65 100')
    sleep(3)  ### Changed



def AdWatcher(videoWatched, device, log):  # Watch ad
    laststate = 'NONE'
    closeCounter = 0  # Reset counter to handle errors
    attempts = 0
    firstTry = 0
    timer = 20
    while 1:
        print(laststate)
        state = myScreen.checkScreen()
        if state == 'HOME':
            closeCounter = 0
            if laststate != 'HOME':
                timer = time()
            if time() - timer > 20:
                quit()
            initWerewolf(device, log)
            laststate = 'HOME'

        if state == 'WEREWOLF':
            closeCounter = 0
            attempts = 0
            if laststate != 'WEREWOLF':
                timer = time()
            if time() - timer > 20:
                print('Nothing else to do')
                quit()
            enterRoulette()
            laststate = 'WEREWOLF'

        if state == 'ROULETTE':
            closeCounter = 0
            if attempts < 15:
                if videoWatched:
                    clickWatchVideo(myScreen, attempts)
                    attempts += 1
                    videoWatched = 0
                else:
                    clickWatchVideo(myScreen, attempts)
                    attempts += 1
            else:
                if attempts < 30:
                    panicClick(attempts-20)
                    attempts += 1
                else:
                    restartShell(device, myScreen, log)
                    AdWatcher(0, device, log)
            laststate = 'ROULETTE'

        if state == 'BROULETTE':
            closeCounter = 0
            if attempts < 10:
                if videoWatched:
                    clickWatchVideo(myScreen, 0)
                    attempts += 1
                    videoWatched = 0
                else:
                    clickWatchVideo(myScreen, 0)
                    attempts += 1
            else:
                if attempts < 20:
                    if videoWatched:
                        clickWatchVideo(myScreen, attempts)
                        attempts += 1
                        videoWatched = 0
                    else:
                        clickWatchVideo(myScreen, attempts)
                        attempts += 1
                else:
                    if attempts < 35:
                        panicClick(attempts-20)
                        attempts += 1
                    else:
                        restartShell(device, myScreen, log)
                        AdWatcher(0, device, log)
            laststate = 'ROULETTE'

        if state == 'CLOSE':
            if closeCounter < 5:
                device.shell('input touchscreen swipe 830 1060 830 1060 100')
                closeCounter += 1
            else:
                restartShell(device, myScreen, log)
                AdWatcher(0, device, log)
            laststate = 'CLOSE'

        if state == 'UNKNOWN':
            attempts = 0
            if laststate != 'UNKNOWN':
                timer = time()
            if time() - timer > 60:
                restartShell(device, myScreen, log)
                AdWatcher(0, device, log)
            laststate = 'UNKNOWN'
            if not videoWatched:
                beginVideo = time()
                print('Watching video')
                videoWatched = 1
            else:
                if time() - beginVideo > 15:
                    exitAd()
                    beginVideo = time()


####### BEGIN #######

# Check parameters
if len(sys.argv) > 1:
    if sys.argv[1] == '-l':
        print('Logless')
        log = noLog()  # We create a new logfile
    else:
        print('Parámetro incorrecto. Logless: -l')
        quit()
else:
    log = Logs()


adb = Client(host='127.0.0.1', port=5037)
devices = adb.devices()

# Check connection
if len(devices) > 0:
    print('Connected to 192.168.1.165')
    log.addLog('Connected to 192.168.1.165')
else:
    print('Could not connect to 192.168.1.165')
    log.addLog('Could not connect to 192.168.1.165')
    log.addLog('Disconnecting...')
    exit()

device = devices[0]

# Block rotation
device.shell('content insert --uri content://settings/system --bind name:s:accelerometer_rotation --bind value:i:0')
print('Blocked rotation')
log.addLog('Blocked rotation')

myScreen = Screen(device, log)

# Restart game
print('Restarting...')
log.addLog('Restarting shell')
restartShell(device, myScreen, log)

# Begin AdWatcher
videoWatched = 0
AdWatcher(videoWatched, device, log)
