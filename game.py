import pygame
import pyautogui
import webbrowser
import math
import speech_recognition as sr
from playsound import playsound

# # Define some colors.
BLACK = pygame.Color('black')
WHITE = pygame.Color('white')

pyautogui.FAILSAFE = False

# This is a simple class that will help us print to the screen.
# It has nothing to do with the joysticks, just outputting the
# information.
class TextPrint(object):
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 20)

    def tprint(self, screen, textString):
        textBitmap = self.font.render(textString, True, BLACK)
        screen.blit(textBitmap, (self.x, self.y))
        self.y += self.line_height

    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 15

    def indent(self):
        self.x += 10

    def unindent(self):
        self.x -= 10


pygame.init()

# Set the width and height of the screen (width, height).
screen = pygame.display.set_mode((400, 600))

pygame.display.set_caption("gamepad")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates.
clock = pygame.time.Clock()

# Initialize the joysticks.
pygame.joystick.init()

# Get ready to print.
textPrint = TextPrint()

# -------- Main Program Loop -----------
while not done:
    #
    # EVENT PROCESSING STEP
    #
    # Possible joystick actions: JOYAXISMOTION, JOYBALLMOTION, JOYBUTTONDOWN,
    # JOYBUTTONUP, JOYHATMOTION
    for event in pygame.event.get(): # User did something.
        if event.type == pygame.QUIT: # If user clicked close.
            done = True # Flag that we are done so we exit this loop.
        elif event.type == pygame.JOYBUTTONDOWN:
            print("Joystick button pressed.")
        elif event.type == pygame.JOYBUTTONUP:
            print("Joystick button released.")

    #
    # DRAWING STEP
    #
    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(WHITE)
    textPrint.reset()

    # Get count of joysticks.
    joystick_count = pygame.joystick.get_count()

    textPrint.tprint(screen, "Number of joysticks: {}".format(joystick_count))
    textPrint.indent()

    # For each joystick:
    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()

        textPrint.tprint(screen, "Joystick {}".format(i))
        textPrint.indent()

        # Get the name from the OS for the controller/joystick.
        name = joystick.get_name()
        textPrint.tprint(screen, "Joystick name: {}".format(name))

        # Usually axis run in pairs, up/down for one, and left/right for
        # the other.
        axes = joystick.get_numaxes()
        textPrint.tprint(screen, "Number of axes: {}".format(axes))
        textPrint.indent()

        for i in range(axes):
            axis = joystick.get_axis(i)
            textPrint.tprint(screen, "Axis {} value: {:>6.3f}".format(i, axis))
            xx=0
            yy=0
            if i==0:
                xx=axis*1366
                pyautogui.moveRel(xx/10,0,duration=1)
            elif i==1:
                yy=axis*768
                pyautogui.moveRel(0,yy/10,duration=1)
            elif i==3 and axis < 0:
                pyautogui.hscroll((2))
            elif i==3 and axis > 0:
                pyautogui.hscroll(-(2))
            elif i==4 and axis < 0:
                pyautogui.scroll((2))
            elif i==4 and axis > 0:
                pyautogui.scroll(-(2))
            elif i==2 and (axis!=-1 and axis!=0):
                pyautogui.hotkey('ctrl','tab')
                print("aaaa")
            elif i==5 and (axis!=-1 and axis!=0):
                pyautogui.hotkey('ctrl','shift','tab')
            
        textPrint.unindent()

        buttons = joystick.get_numbuttons()
        textPrint.tprint(screen, "Number of buttons: {}".format(buttons))
        textPrint.indent()

        for i in range(buttons):
            button = joystick.get_button(i)
            textPrint.tprint(screen,
                             "Button {:>2} value: {}".format(i, button))
            if i==8 and button==1:
                webbrowser.open("https://google.com/",2)
            elif i==4 and button==1:
                pyautogui.click()
            elif i==5 and button==1:
                pyautogui.click(button="right")
            elif i==7 and button==1:
                playsound("files/abc.mp3")
                r = sr.Recognizer()
                with sr.Microphone() as source:
                    print("Say something!")
                    audio = r.listen(source)
                try:
                    pyautogui.write(r.recognize_sphinx(audio))
                    # print("Sphinx thinks you said " + )
                except sr.UnknownValueError:
                    print("Sphinx could not understand audio")
                except sr.RequestError as e:
                    print("Sphinx error; {0}".format(e))
        textPrint.unindent()

        hats = joystick.get_numhats()
        textPrint.tprint(screen, "Number of hats: {}".format(hats))
        textPrint.indent()

        # Hat position. All or nothing for direction, not a float like
        # get_axis(). Position is a tuple of int values (x, y).
        for i in range(hats):
            hat = joystick.get_hat(i)
            textPrint.tprint(screen, "Hat {} value: {}".format(i, str(hat)))
        textPrint.unindent()

        textPrint.unindent()

    #
    # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
    #

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # Limit to 20 frames per second.
    clock.tick(20)

# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()
