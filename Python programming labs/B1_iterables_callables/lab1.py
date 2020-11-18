# description : this file creates a list of Record objects and record the class infomation for the classes each students have taken
#               after printing out all the infomation, print a menu for the user to click on  

from record import Record
import re

FILENAME = "lab1in_error.txt"

def getData() :
    """ open the input file, check whether the file can be opened or not, create a list of Record objects
        check whether each line in the input file is valid or not"""
    try :
        with open (FILENAME, "r") as infile :
            obList = [Record(line)    for line in infile    if line != ""]
            return obList
        
    except IOError:    # FileNotFoundError
        print(FILENAME, "not found")
        raise SystemExit
    except ValueError as e:
        print(e)
        raise SystemExit
        
def printAll(objectList) :
    """ print out all the infomation of Record objects """
    for ob in objectList :
        ob.print1()
    
def getChoice() :
    """ print out a menu, prompt the user to enter, repeat if the choice is not given """
    print("\n=========================\ns. search for one record\ng. grade count\nq. quit\n")
    answer = input("Enter your choice: ")
    while answer not in "sgq" or len(answer) != 1:        # answer.lower() not in "sgq"
        answer = input("Enter your choice: ")
    return answer
    
def userProcess(listOfObject) :
    """ keep looping if the user does not input q for quit, call the corresponding fuction related to the input
        prompt the user to enter a new choice again """
    dict1 = {"s" : search, "g" : countGrade}
    choice = getChoice()
    while choice != "q" :
        dict1[choice](listOfObject)
        choice = getChoice()
        
def search(obList) :
    """ sort all the Record objects by the students' last name, print out a student's record one at a time
        keep looping if the user inputs enter for next record, stop when it is the end of hte record """
    print("Printing one student record one at a time")
    gen = (ob   for ob in sorted(obList, key = lambda o : o.getName().split()[-1]))
    next(gen).print1()
    answer = input("\nPress Enter for next name, anything else to quit: ")
    while answer == "" :
        try :
            next(gen).print1()
            answer = input("\nPress Enter for next name, anything else to quit: ")
        except StopIteration :
            print("End of record")
            break
            
def countGrade(listObject) :
    """ prompt for letter grade to search, keep looping if the input is not a valid letter grade
        call the findGrade function """
    answer = input("Enter letter grade: ")
    while not re.search("^[ABCDF][+-]?$", answer):              # while not re.search("^([ABCD][+-]?|F)$", answer):
        print("Grade should be A-F with optional + and -")
        answer = input("Enter letter grade: ")
    
    findGrade(listObject, answer)
    
def check(fct) :
    """ it's a decorator, create a set which will contain the searched letter grades, check whether the letter grade has been searched
        determine whether the letter grade is stored in args or kwargs, add it to the set
        print out the set, call the fct function, return the reference"""
    set1 = set()
    def helper(*args, **kwargs) :
        if any(isinstance(elem, str) and elem in set1     for elem in args) or any(isinstance(kwargs[key], str) and kwargs[key] in set1    for key in kwargs) :  # in set
            print("already searched this grade")
        else :
            if any(isinstance(elem, str)   for elem in args ) :
                for elem in args :
                    if isinstance(elem, str) :
                        set1.add(elem)          
            else :
                for key in kwargs :
                    if isinstance(kwargs[key], str) :
                        set1.add(kwargs[key])
            print(set1)
            result = fct(*args, **kwargs)
            return result
    return helper
    
@check
def findGrade(listOfOb, letter) :
    """ go through the list of Record objects, count the number of how many students recieve the same grade
        print out the message saying how many students with the letter grade """
    count = 0
    for obj1 in listOfOb :
        if obj1.hasGrade(letter) == True:
            count += 1
    print(count, "student(s) with grade", letter)
        
def main() :
    """ assign a list of Record objects by calling getData function, call printAll function to print all the infomation
        call the userProcess function """
    studentRecordList = getData()
    printAll(studentRecordList)
    userProcess(studentRecordList)
        
main()