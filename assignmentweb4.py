#Assignment 2 
#Abel Polycarpe
#CS 533

import random
import time
import threading
import sys
import json
import os 
import argparse
import getpass
import sys
import select
#if sys.platform.startswith('linux'):
    #import fcntl # used for the ability the interupt the quiz with the stop watch
if sys.platform.startswith('win'):
    import keyboard # used for the ability the interupt the quiz with the stop watch

from flask import Flask, render_template

app = Flask(__name__)




    

def get_questions_file(): # Gets the questions file and counts the questions
    
    global fileIn, fileName
    
    while  True:
        try: 
            if cmdStart == False:   
                fileName = input('Enter the question file FOLDER PATH and or NAME press enter for default (sample3.txt): ')
            
            if fileName == "": # no input
                fileName = "sample3.txt" # default to sample3 questions file
                print('The default file sample3.txt will be used')

            fileIn = open(fileName , "r") # try and read file
            break # Get out of while loop 
        except:
            print('Error finding or reading in the file ', fileName  )
            print('Please try again')
            if cmdStart == True:
                sys.exit() # exit completely if in cmd line mode

def count_questions():
    global numOfQuestions, fileIn
    numOfQuestions = 0 

    for line in fileIn: # read each line of the file 

        if line.strip() and not '*' in line: # remove all line breaks , comments and spaces 
            
            #print(line.strip())

            if '@Q' in line.strip():

                numOfQuestions = numOfQuestions + 1 #Count the number of questions for future use

def get_quiz_size():
    global inSetsize, numOfQuestions
    while True:
        try:    
            if cmdStart == False: 
                inSetsize = input('Please specificy the number of questions or press enter for the max amout: ') # convert set size input to numeric
            
            if inSetsize == "":
                inSetsize = numOfQuestions
                print('Using the max quiz size of ', inSetsize, 'questions.')

            if ((int(inSetsize) <= numOfQuestions) & (int(inSetsize) > 0)): 
                inSetsize = int(inSetsize)
                break
            else: 
                print('Quiz size number entered was 0 or greater than max of ',numOfQuestions, ', try again' )
                if cmdStart == True:
                    sys.exit() # exit completely if in cmd line mode
        except:
            print('Quiz size Input error try again' )
            if cmdStart == True:
                sys.exit() # exit completely if in cmd line mode

    print('Randomly selecting ' ,inSetsize , 'out of ' , numOfQuestions, 'questions availible')

def start_quiz():

    global questionsAskedCount, displayquest, saveanswer, displaychoice, linetracker, choicenum, numofcorrect, numOfQuestions, ranQuestionnum, starttime, quizActive
    #start of quiz

    print( "-------------------------------------------" )
    print('Get ready , The Quiz start Now!')
    if timeLimit > 0:
        print('Time limit: ', timeLimit, ' second(s)' )
    print( "-------------------------------------------" )
    print( " " )
    time.sleep(2) 
    starttime = time.time() #start the time now
    

    while  (questionsAskedCount < inSetsize) & (quizActive == True): # loop until we ask the requested amout of questions or the stop watch changes quizActive to false
        fileIn.seek(0) # read the specific file again
        Questnumhold = 0

        ranQuestionnum = random.randint(1,numOfQuestions)

        if ranQuestionnum not in questionnumlist:
            questionnumlist.append(ranQuestionnum)
        else:
            continue #try again


        for line in fileIn: # read each line of the file 

            if line.strip() and not '*' in line: # remove all line breaks , comments and spaces 
                
                #print(line.strip())

                if (displayquest == True) & ('@A' not in line.strip()):
                    print(line.strip())

                if (displayquest == True) & ('@A' in line.strip()):
                    displayquest = False
                    saveanswer = True
                    
                if (saveanswer == True) & ('@A' not in line.strip()):   
                    if (linetracker == 0):  # save only once 
                        questanswer = int(line.strip())
                    displaychoice = True
                    linetracker = linetracker + 1
                    
                
                if (displaychoice == True) and (linetracker == 2) & ('@E' not in line.strip()): # need to go to the second line after getting the answer
                    saveanswer = False
                    #displaychoice = False
                    choicenum = choicenum + 1
                    print(choicenum , ') ', line.strip())
                    
                
                if (displaychoice == True) & ('@E' in line.strip()):
                    linetracker = 0
                    displaychoice = False
                    while quizActive == True: 
                        try:   
                            
                            if sys.platform.startswith('Linux'):
                                print ("Select answer: " , end='', flush=True)
                                #fcntl.fcntl(sys.stdin, fcntl.F_SETFL, os.O_NONBLOCK) # std is now in non blocking mode which lets the while loop cycle and allows the timer to interupt
                                while True:
                                    # Check if there's input available on stdin
                                    if quizActive == False:
                                        break
                                    if (sys.stdin in select.select([sys.stdin], [], [], 0)[0]): # std in is now not in blocking mode which wont freeze the thread 
                                        # Read the input character
                                        useranswerinput = sys.stdin.read(1).strip()
                                        if useranswerinput != '':
                                            useranswerinput = int(useranswerinput)
                                            break     
                                #fcntl.fcntl(sys.stdin, fcntl.F_SETFL, 0) # std in is now in blocking mode which freezes the thread 
                            
                               
                            else: 
                                 useranswerinput = int(input("Select answer: ")) # the stopwatch can force an enter key press and allow the while loop to check the quizActive status
                
                            
                            if  (useranswerinput > 0) & (useranswerinput <= choicenum):
                                #if sys.platform.startswith('linux'):
                                    #fcntl.fcntl(sys.stdin, fcntl.F_SETFL, 0) # std in is now in blocking mode which freezes the thread 
                                break
                            else:
                                #if sys.platform.startswith('linux'):
                                    #fcntl.fcntl(sys.stdin, fcntl.F_SETFL, 0) # std in is now in blocking mode which freezes the thread 
                                if quizActive == True:
                                    print('Selection is out of range, try again')
                                useranswerinput = 0 # force and valid integer in case of stop watch interuption
                        except:
                            if quizActive == True:
                                print('invalid input, try again')
                            useranswerinput = 0 # force and valid integer in case of stop watch interuption
                    if questanswer == useranswerinput:
                        numofcorrect = numofcorrect + 1
                        if quizActive == True:
                            print( "Correct!" )
                            print( "------------------------------------" )
                        
                    else:
                        if quizActive == True:
                            print( "Incorrect answer" )
                            print( "------------------------------------" )
                        
                    choicenum = 0
                    break


                
                    

                if '@Q' in line.strip():

                    Questnumhold = Questnumhold + 1 # index through questions

                    if Questnumhold == ranQuestionnum: # if the index in equal to the random number choosen , then display the question
                        questionsAskedCount = questionsAskedCount + 1 # add to the question asked count

                        displayquest = True
    
    if quizActive == True: # the user finished the quiz in time or no time limit was specified
        quizActive = False # we are done with the quiz , this could happen before the stopwatch routine changes this variable 


def print_results():
    global starttime, questionsAskedCount, percentcorrect

    print('The Quiz has ended!! ')
    print(' ')
    print('----------- Session Summary ---------------')
    print('number of questions in the quiz: ', inSetsize)
    if timeLimit > 0:
        print('number of questions actually asked before time expired: ' ,questionsAskedCount )
    print('number of correct questions : ' , numofcorrect)
    percentcorrect = int((numofcorrect / inSetsize) * 100)
    print ('percentage of correct answers : ',  percentcorrect, '%')
    elapsedtime = int(time.time() - starttime)
    print ('elapsed time : ',  (elapsedtime ) , ' seconds') 
    print( "------------------------------------" )

def logfilesetup():
    global logfile, logfilefolder, logfilein
    if os.path.exists(logfilefolder):
        #print('log folder found')
        if os.path.exists(logfilefolder + '/' + logfile):
            pass
            #print('log file found')
        else:
            logfilein = open(logfilefolder + '/' + logfile , "a")
            
    else:
        os.mkdir(logfilefolder) # Make folder
        logfilein = open(logfilefolder + '/' + logfile , "a") # make log file


def write_log_results():
    
    newuserdata = {}
    global logfilefolder, logfilein, filepath, username, percentcorrect
    global osSlashes
    #username = "Bob"
    #try:
    print('Quiz result have been logged for ', username)
    logfile = "quizlog.json" 
    logfilefolder = "logs"
    filepath = logfilefolder + osSlashes + logfile
    if (os.path.getsize(filepath) == 0): # if its empty just write
        with open(logfilefolder + osSlashes + logfile, 'r') as file:
            #newuserdata = {}
            attemptslog = {"attempts": []}
            newlog = [
                {
                    'quiz_number' : 1,
                    'quiz_file_used': fileName,
                    'asked_questions': questionsAskedCount,
                    'user_score': percentcorrect
                }
            ]
            
            attemptslog['attempts'] = newlog # into attempts
            newuserdata[username] = attemptslog #into the user
            writetojson(newuserdata)
            #print('Results for user were logged')
    else:             # file ise not empty 
        with open(filepath, 'r') as file:
            user_quiz_data = json.load(file) #load file 
            if username in user_quiz_data: # Search for user 
                print('User ', username , ' found in logs file') # Found the user !!
                #currentuserdata = user_quiz_data.get(username)
                attemptsdata = user_quiz_data.setdefault(username, {}).get('attempts', []) # get all the attempts
                
                maxquiznumber = max(attempt.get("quiz_number", 0) for attempt in attemptsdata) # get the max number
                maxquiznumber = maxquiznumber + 1 # increment

                newlog = {
                    'quiz_number' : maxquiznumber,
                    'quiz_file_used': fileName,
                    'asked_questions': questionsAskedCount,
                    'user_score': percentcorrect
                }
                attemptsdata.append(newlog) # add the newest attempt into the list 
                writetojson(user_quiz_data) # write back the updated dated over writting the old
                print("    new quiz attempt was logged ")

            else: # file not empty but user not found 

                attemptslog = {"attempts": []}
                newlog = [
                    {
                        'quiz_number' : 1,
                        'quiz_file_used': fileName,
                        'asked_questions': questionsAskedCount,
                        'user_score': percentcorrect
                    }
                ]
            
                attemptslog['attempts'] = newlog # into attempts
                user_quiz_data[username] = attemptslog #add new user
                
                #usersdata.append(newuserdata) # add the new user, and its attempts list of quiz dictionaries
                writetojson(user_quiz_data) # wite it all back overwriting the old data
               

    
    
            
def writetojson(data):
    with open(filepath, 'w') as file:
        json.dump(data, file, indent=4)


            
    #except:
        #print('error opening log file')


def get_time_limit():
    global timeLimit
    while True:
        try:
            if cmdStart == False:
                timeLimit = input("Please specifiy a time limit for the quiz in seconds or press enter for no time limit: ")
            if (timeLimit == ""):
                raise
                #timeLimit = 0 # force integer
                #break # Get out of while loop
            elif (int(timeLimit) > 0) :
                timeLimit = int(timeLimit) # force int
                break # Get out of while loop
            else:
                print('A negative or 0 time limit is invalid, please try again')
                if cmdStart == True:
                    sys.exit() # exit completely if in cmd line mode
        except:
            print('The time limit entered was invalid, please try again')
            if cmdStart == True:
                sys.exit() # exit completely if in cmd line mode

def stop_watch():
    global starttime, timeLimit, quizActive

    
    time.sleep(2) # to match with the quiz start
    if timeLimit > 0:
        #print('Quiz time limit is set to ', timeLimit, ' second(s)' )
        endTime = time.time() + timeLimit 
        while quizActive == True: # continues to check time while quiz is being taken 
            if time.time() >= endTime:
                quizActive = False  
                if sys.platform.startswith('win'):
                    keyboard.press_and_release('enter') # submit whatever answer was already enter , or a blank. This allows a forced termination 
                #os.system("echo -ne '\n'")

                print('') #empty print statement to move to the next line 
                print(' ')
                print('Times up!! Sorry the time limit of ', timeLimit, ' second(s) has passed. ' )
                
            else:
                time.sleep(1)       
    else:
        return # stop watch not needed, end thread 


def mainMenu():
    global menuInput, lastuserinput, logfilein, logResults
    global firstStart, testmenuInput, logfile, logfilefolder, username, fileIn

    while True:
        try:
            if firstStart == False:
                lastuserinput = (input("Type \"done\" to end the program or \"menu\" to return back to the MODES MENU: ")).lower().strip()
                
                if lastuserinput == "done":
                    break # can exit in try except bloc
                elif lastuserinput == "menu":
                    firstStart == False
                    break
                else:
                    print('invalid input, try again')
            else:
                firstStart = False
                break # go to next menu 
            
        except:
            print('invalid input, try again')
    
    if lastuserinput == "done":
        sys.exit()

    while True:
        try:
            menuInput = int(input('Enter (1) for the Classroom quiz mode or Enter (2) for normal quiz mode: '))
            if menuInput == 1 or menuInput == 2:
                break
        except:
            print( 'Invalid input try again')
    
    if menuInput == 1: 
        print('Class Test Mode Menu choosen') # Proceed below 
    elif menuInput == 2:
        print('normal test mode choosen')
        return
    
    
    userrole = login()
    
    # CLASS TEST MENU #


    # find logs folder and quizlog.json file , or make 1 or bother
    
    logfile = "quizlog.json" 
    logfilefolder = "logs"
    if os.path.exists(logfilefolder):
        #print('log folder found')
        if os.path.exists(logfilefolder + '/' + logfile):
            pass
            #print('log file found')
        else:
            logfilein = open(logfilefolder + '/' + logfile , "a")
            
    else:
        os.mkdir(logfilefolder) # Make folder
        logfilein = open(logfilefolder + '/' + logfile , "a") # make log file

    while True: # menu loop 
        global testmenuInput, inSetsize, filepath
        class_test_menu(userrole)

        if (testmenuInput == 1):
            get_questions_file()
            count_questions() # upadate count
            inSetsize = numOfQuestions #update max default
        elif (testmenuInput == 2):
            get_quiz_size()
        elif (testmenuInput == 3):
            get_time_limit()
        elif (testmenuInput == 4): # view results
            filepath = logfilefolder + osSlashes + logfile
            if (os.path.getsize(filepath) == 0): 
                print('No quiz records avilible, file is empty ') # file was empty
                input('press enter to return to the menu')
                
            else:
                with open(filepath, 'r') as file:
                    user_quiz_data = json.load(file) #load file 
                    
                    if (userrole == 1): #teacher print
                        #studentnameslist = user_quiz_data.setdefault(username, [])
                        for student in user_quiz_data:
                            printstudentdata(student,user_quiz_data,userrole)
                        print('Printing completed, No more student records in this file ')
                        input('Press enter to the menu ')
                    elif (userrole == 2): # current student print
                        if username in user_quiz_data:
                            print('----- Printing quiz records ------')
                            printstudentdata(username,user_quiz_data,userrole)
                        else:
                            print('No quiz records for ', username) # user wasnt found 
                            input('press enter to return to the menu')

        elif (testmenuInput == 5): 
            if os.path.exists(fileName): # file exists
                if userrole == 1: # student mode 
                    print('Options saved ! ')
                    userrole = login(2) # log in 
                fileIn = open(fileName , "r") # try and read file
                break # return control back to main for the start of the quiz
            else:
                print('The default file sample3.txt was not found ')
                print('specify another file or place the sample3.txt file in the programs directory ')
                input('Press enter to return to the main menu')
                # this will loop back to the main menu
        
            

        elif (testmenuInput == 6): 
            sys.exit() # bye bye
        
def  printstudentdata(username,user_quiz_data,userrole):

    print(' ')
    print('Student: >>> ',  username, ' <<<')
    print('----------------------------')
    attemptsdata = user_quiz_data.setdefault(username, {}).get('attempts', []) # get all the attempts
    for attempt in attemptsdata:
        print('Quiz attempt number: ', attempt.get("quiz_number"))
        print('-----       File used: ', attempt.get("quiz_file_used"))
        print('----- Questions Asked: ', attempt.get("asked_questions"))
        print('-----           Grade: ', attempt.get("user_score"), '%')
        print('----------------------------')
        print('')
    
    if (userrole == 1):
        input('For the next student press enter')

    elif (userrole == 2): 
        if cmdStart == False:
            input(' Printing complete, Press enter to return to the menu')
        else:
            print(' --- Printing complete ---')


def class_test_menu(userrole):
    global testmenuInput, logResults, timeLimit , username
    logResults = True
    if (userrole == 1): # teacher
        print(' ')
        print(' ')
        print(' ')
        print('-------------------------------logged in as: Teacher')
        print('-------- Class Test Menu -------')
        print('---------------------------------| ------------')
        #if user == 'admin':
        print('1) Change Question file          | ', fileName)
        print('2) Change Quiz size              | ', inSetsize )
        
        if (timeLimit == 0):
            print('3) Change Time Limit options     | No time limit')
        else:
            print('3) Change Time Limit options     | Time limit is: ', timeLimit, ' Seconds'   )
        
        print('4) View all test results ' )
        
        print('5) --> Save options & Start quiz <-- ')

        print('6) Exit Program')

        print(' ')
    elif userrole == 2:
        #studedntname = input('Enter you student name: ')

        print(' ')
        print(' ')
        print(' ')
        print('-------------------------------logged in as: ', username)
        print('-------- Class Test Menu -------')
        print('---------------------------------| ------------')
        #if user == 'admin':
        print('Questions file       | ', fileName)
        print('Quiz size            | ', inSetsize )
        
        if (timeLimit == 0):
            print('Time limit           | No time limit')
        else:
            print('Time limit           |', timeLimit, ' Seconds'   )
        
        print('1) View all test results for: ', username )
        
        print('2) --> Start quiz <-- ')

        print('3) Exit Program')

        print(' ')
    
    
    while True:
        try:
            testmenuInput = int(input("select an option from the menu: ")) #needs loop 
            if (userrole == 1): # teacher    
                if (testmenuInput > 0) & (testmenuInput <= 6):
                    break # go to options controle
                else:
                    print( 'Invalid input try again')
            elif (userrole == 2): # sutent has limited options
                if (testmenuInput > 0) & (testmenuInput <= 3):
                     testmenuInput = testmenuInput + 3 # fix the offest (4 , 5 or 6)
                     break # go to options controler
                else:
                    print( 'Invalid input try again')

        except:
            print( 'Invalid input try again')


def defaultParms():
    global fileIn, fileName, inSetsize, numOfQuestions, timeLimit , username, logfilefolder, logfile, osSlashes
    
    logfile = "quizlog.json" 
    logfilefolder = "logs"
    logfilesetup() # always set up the log file for printing
    fileName = "sample3.txt" # default to sample3 questions file
    numOfQuestions = 5
    inSetsize = 5
    timeLimit = 0

    if len(sys.argv) > 1: # Parms might get over written 
        username = args.name.lower()

        if args.mode.lower() == 'results':
            filepath = logfilefolder + osSlashes + logfile
            
            
            if (os.path.getsize(filepath) > 0) & (os.path.exists(logfilefolder)): # file exists and is not empty 
                with open(filepath, 'r') as file:
                    user_quiz_data = json.load(file) #load file
                    if username in user_quiz_data:
                        print('----- Printing quiz records ------')
                        userrole = 2 # student by default
                        printstudentdata(username,user_quiz_data,userrole)
                    else:
                        print('No quiz records for ', username) # user wasnt found 
            else: 
                print('No quiz records for ', username)

            sys.exit() # all done after printing results


        if args.file is not None: # check if the optional argument was passed
            fileName = args.file
        else:
            fileName = '' # lets display a message

        get_questions_file() # will completely exit with theres an issue 
        count_questions()  # get the number of questions dynamically 
        
        if args.size is not None: # check if the optional argument was passed
            inSetsize = args.size
        get_quiz_size()

        if args.time is not None: # check if the optional argument was passed
            timeLimit = args.time
            get_time_limit()

        




def login(userrole = 0):
    global username
    if userrole == 0:
        print( '1) Login as Teacher 2) Login as student')
        while True:
            try:
                userrole = int(input(' select an option: '))
                if userrole == 1 or userrole == 2:
                    break # valid input
                    
                else:
                    print('invalid input , try again ')
                    
            except:
                print('invalid iput , try again ')

    if userrole == 1:
        while True:
            try:
                password = int(getpass.getpass(' enter the provided Teacher password (it will not show when entered): '))
                if password == 12345:
                    break # correct password
                    
                else:
                    print('invalid password , try again ')
                    
            except:
                print('invalid password , try again ')
    elif userrole == 2:
        while True:
            try:
                username = input('Enter student name: ').lower().strip()
                if username != "":
                    break
                else:
                    print('invalid input, try again')
            except:
                print('invalid input, try again')

    return userrole
        


# ---------- MAIN LINE -----------#
def main(): 

    global numOfQuestions , setSize, displaytext, displayquest,saveanswer, Questnumhold,displaychoice, questionnumlist, choicenum,percentcorrect,numofcorrect,questionsAskedCount,linetracker,starttime,inSetsize, timeLimit, quizActive,menuInput,firstStart, lastuserinput
    global logResults, osSlashes
    
    firstStart = True # only do this once 
    quizActive = True
   # if sys.platform.startswith('linux'):
    # print("Quiz program is Running on Linux")
    # osSlashes = '/'

    if sys.platform.startswith('win'):
     print("Quiz program is Running on Windows")
     osSlashes = '\\'


    defaultParms()
    
   

    while True:
        #numOfQuestions = 0
        setSize = 0 
        displaytext = False
        displayquest = False
        saveanswer = False
        #inSetsize = 0
        Questnumhold = 0
        displaychoice = False
        questionnumlist = []
        choicenum = 0
        percentcorrect = 0
        numofcorrect = 0
        questionsAskedCount = 0
        linetracker = 0
        #timeLimit = 0
        #quizActive = True
        menuInput = 0
        logResults = False
        lastuserinput = ''

        if len(sys.argv) <= 1: # No parms were passed 
            mainMenu()
        else:
            menuInput = 1 # class test mode 



        if menuInput == 2: # nomal mode 
            get_questions_file()
            count_questions()
            get_quiz_size()
            get_time_limit()
            
        if timeLimit > 0: # if there is a time limit , we run a stop watch in parallel with the quiz
            thread1 = threading.Thread(target=stop_watch)
            thread2 = threading.Thread(target=start_quiz)

            thread1.start()
            thread2.start()

            thread1.join() #  join the stop watch , if the user completes the quiz , the quiz status is updated and the stopwatch ends 
            thread2.join() 

        else:
            start_quiz()

        print_results()
        
        if (logResults == True or len(sys.argv) > 1): # log results when class mode is choosen in the menu or when the test is started by the cmd line
            write_log_results()
            #logResults = False

        if len(sys.argv) > 1: # command line parms were passed so do not loop back , bye bye 
            sys.exit()

def check_mode(mode):
    if (mode.lower() == 'quiz') or (mode.lower() == 'results') :
        pass
    else:
        raise argparse.ArgumentTypeError(f"'{mode}' is not 'quiz' or 'results'")
    return mode


@app.route('/') #call the function below when the app starts
def hello():
    name = 'World'
    return render_template('/index.html', name=name)

if __name__ == "__main__": # start program at the main function 
   
   app.run(debug=True)

   parser = argparse.ArgumentParser(description="Run the Quiz program or view results from the command line")
   parser.add_argument("--mode", help="Specify the programs mode (quiz or results)", required=True, type=check_mode)
   parser.add_argument("--name", help="Specify the students name", required=True)
   
   parser.add_argument("--file", help="Specify the quiz file to be used")
   parser.add_argument("--size", help="Specify the number of questions to be asked", type=int )
   parser.add_argument("--time", help="Specify a time limit in seconds", type=int )

   if len(sys.argv) > 1:
    cmdStart = True # command line start
    args = parser.parse_args()
   else:
       cmdStart = False
             
   
   main()





