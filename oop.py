
# This is our parent class, we know it is not a child class because it doesn't inherit another class
class parent:

    # Each class has it's own built-in methods, a common one to override is the __init__, or instantiate method
    # Notice the methods allow you to pass variables the same way as normal functions, with the edition of self
    # Self represents the individual object of the class created at instantiation(You'll see this below)
    def __init__(self, foo):
        # It's good to remember that instantiating a class should not "do" things
        # This area should only be used to set up attributes
        # Now lets create some attributes for our object from the values passed to __init__ during creation

        # foo is a positional argument that is assigned to a specific variable
        self.foo = foo

        # Lastly we can create attributes that every instance of our class should have automatically
        self.lovespython = True

    # Methods should be passed self first, bringing all the attributes into its name space
    def foo_printer(self):
        """Prints self.foo and it's type"""
        print("\nHi I'm {}".format(self.foo))

    def bar_printer(self):
        print(self.foo + 'BAR!')

    # Methods can also be passed values to change an objects attribute, or to be used temporarily
    # They can also return any information in it's name space
    def foo_changer(self, newfoo, updatetxt):
        """Prints some text about the update, updates foo, then runs foo_printer()"""
        print(updatetxt)

        # updates the attribute
        self.foo = newfoo

        # Notice we don't have to put self in the (), it passes itself the information
        self.foo_printer()

        # Even though we didn't use this it was there to use
        return self.lovespython

    # Lastly this is possible to do without throwing an error but shouldn't be done without self
    # It is not part of the instance, and any call to it would have to be done through the class not the instance
    def dontdothis(something):
        print(something)

# Our child class will inherit all of the parents attributes, and can have it's own as well
class child(parent):
    # This time lets only ask for a name
    def __init__(self, name):
        # Here we call the __init__ of our parent with the params we want
        # By doing this every instance of this child will have the same attributes except name
        super().__init__('Bob')
        self.name = name

    # This class will have all the methods of the parent, plus its own
    def childmethod(self):
        print("\nI'm {}'s child {}".format(self.foo, self.name))
        print("I'm my own object!")
        print("But I can still use my parents methods")

        # You can call other class methods from inside of your method since the all belong to the instance
        self.bar_printer()

    # You can also override the parents methods, if you need them to do something else
    def foo_printer(self):
        print('\nFor the child object .foo_printer() now prints this instead.')
        print('But do I still love python? My.lovespthyon attribute still == {}'.format(self.lovespython))

# This creates an instance of the parent class object
instance = parent('bob')

# Now lets print off what methods we can use
print("The following are the methods available to the instance")
for method in instance.__dir__():
    # A method name starting with _ or __ are meant to be used inside the class only, normally you wouldn't use these
    # Also dir keeps the key names from vars so we want to sort those out for just methods
    if not method.startswith('_') and method not in vars(instance):
        print(method)

# Now that it is an object we can use the methods it contains
instance.bar_printer()
instance.foo_printer()
instance.foo_changer('Jane', 'Changing {} to Jane'.format(instance.foo))

# Note we could change the name back outside of the class by assigning straight to the instances attribute
instance.foo = 'Bob!'
instance.foo_printer()

# To show why you don't leave self out
try:
    instance.dontdothis('Ew')
# the instance automatically adds itself to the call, looking to the code like dontdothis(instance,'Ew')
except TypeError:
    print('Got 2 args instead of 1, FAIL!, Moving on')
# it can be used like this, but please don't, please..
parent.dontdothis('gross')


# Lets make an instance of a child
child_instance = child('Some kid')
# Run it's method
child_instance.childmethod()
# Run it's overriden parents method
child_instance.foo_printer()

# The very last thing to show is that you can have multiple of the same objects, with different attributes
different_child = child('Some other kid')

# These are both the same type of object
print('\nAre we the same type of object?')
print(type(different_child) == type(child_instance))

# But they have different attributes
print('\nDo you have the same names?')
print(different_child.name == child_instance.name)
