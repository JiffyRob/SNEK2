# SNEK 2
## The Super NPC / Event Koordinator 2

This is a programming language I wrote for cutscene management with pygame (though it could be used for other things).
It has no dependencies save for the python standard library.

It uses `asyncio` under the hood so that commands can take multiple frames to run without stopping the game.
[Cool book that helped me a lot](https://craftinginterpreters.com)

Here's an example of how to run a script with it:
```py
import asyncio
from SNEK2 import SNEKProgram, SNEKCallback, AsyncSNEKCallback

def my_callback():
    return "3 cuz why not"

async def sleep_for(some_argument):
    await asyncio.sleep(some_argument)

script = """
print f"This is your callback's result: {my_callback()}";
print "Finishing in three seconds.";
sleep_for(3);
"""

def main():
    program = SNEKProgram(script, {
        "my_callback": SNEKCallback(my_callback, 0),  # second arg is how many arguments to take.  No kwd or variable length args.
        "sleep_for": AsyncSNEKCallback(sleep_for, 1),
    })
    # blocks
    program.run()
    # or you can do this inside an asyncio coroutine
    # runs the program as a coroutine
    # asyncio.create_task(program.run_async())
```

Here's a rough documentation page for how to use the language itself:
```
# <- this is a comment
# makes a new variable a and sets it to 0
# everything is a float in SNEK
a = 0;

# print statements take one argument
print a;
print("you can also write them like this");

# strings 
string = "this is a string";
# there are some backslash escapes as well
print "\n";  # prints a newline
print "\\n";  # prints "\n"
print "\\";  # prints "\"

# format strings work sorta like python.
# all strings can be multi-line
fstring = f"a is equal to:
one less than {a + 1}.";
print fstring;

# there is a bool type as well
falsey = false;
truey = true;
# and nil
nilly = nil;

print falsey;
print truey;
print nil;

# blocks
{
    b = 10;  # b is only defined in this scope
    a = 4;  # a is changed in global scope because it is already defined
}
# builtin functions
my_boolean = bool(randint(0, 1));  # truthiness works like python's
my_string = str(4);  # note this will be "4.0"
print(upper("abc"));  # also lower() and title()

# arithmetic is a thing
math_answer = 4 * (4 + 2) / 3 - 7;
other_answer = 5 + -2;

print math_answer;
print other_answer;

# if statements (multi-line)
if my_boolean {
    # creates a new scope
    print("My random is true");
} else {
    print("My random is false");
}

# if statements (one-line)
if truey then print "truey is true";  # works in enclosing scope
else print "truey is false";

# switch case can have arbitrary expressions
# both for switch and for case
switch !my_boolean{
    # case statements (one-line)
    case true do print "my random is not true";
    # case statements (multi-line)
    case !true {
        print "my random is not false";
    }
}

# while loops are a thing too
num = 0;
# multi-line
while num < 10 {
    num += 1;
    print f"My num is {num}";
}
# single-line
while randint(0, 10) do print "one liners!";
```