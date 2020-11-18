# My data structure is having an instance variable for student name and a list of lists storing the class infomation
# Every inner list contains class name, units, and letter grade of one class

# description : this file contains the Record class. It checks whether it can read the data or the data can be stored in the data structure successfully
#               every Record object contains the information of class(es) that one student took before

class Record :
    
    
    # self._name, *rest = line......
    # * is packing
    
    def __init__(self, line) :
        
        infoList = line.strip().split(",")
        
        # check first, then do the work later (assigning instance variables)
        if (len(infoList) - 1) % 3 != 0 :
            raise ValueError("line: " + line + " is not valid.")
        
        self._studentName = infoList[0]
        self._classInfo = [ [ infoList[j + i*3]  for j in range(1, 4) ]   for i in range((len(infoList) - 1) // 3) ]
        
    def print1(self) :
        """ print the student name, print the class infomation in a formatted way """
        print(self._studentName)
        for tup in sorted(self._classInfo) :
            print("{0:9s} {1:1s} {2:4s} {3:2s}".format(tup[0],":", tup[1], tup[2]))
        print()
            
    def getName(self) :
        """ returns the student name """
        return self._studentName
    
    def hasGrade(self, letterGrade) :
        """ return a boolean value if the student got that certain letter grade """
        return any(elem[2] == letterGrade     for elem in self._classInfo)
