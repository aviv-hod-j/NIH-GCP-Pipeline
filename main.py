# def main():
#     print("All Good Babe")

# # this boolean expression will be True when python is running the file directly and it is not imported.
# if __name__ == '__main__':
#     main()
######################################################################################################
    
# OOP

# lesson 1:
# class object = a blueprint for creating instances
# instance object = a uniqe instance 
# method = a function associated with a class
# attrabute


class Employee:

# self = instance, first,last,pay = arguments
# the function takes the instance (object) as the first argument
    def __init__(self, first, last, pay):
        self.first = first
        self.last = last
        self.pay = pay
        self.email = first + '.' + last + '@.company.com'

    #the instance is the only thing we'll need in order to get the full name here
    #the instence is given to the func automatically
    def fullname(self):
        return '{} {}'.format(self.first , self.last)
    

emp_1 = Employee('Aviv','Hod',33000)

#the next 2 following lines perform the same action in the background:
# print(Employee.fullname(emp_1))
# print(emp_1.fullname())

#an instance is given to the func automatically so we don't need to add parenthasis with it
#works different on the backgound
print(emp_1.fullname())





