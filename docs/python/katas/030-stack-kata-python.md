# Stack Kata in Python

A stack is a linear data structure that follows the principle of Last In First Out (LIFO). This means the last element inserted inside the stack is removed first.

You can think of the stack data structure as the pile of plates on top of another or a deck of cards where you can only push to the top or take from the top.

In programming terms, putting an item on top of the stack is called **push** and removing an item is called **pop**.

## Test Driven Development approach (TDD)

#### Red, Green, Refactor
  - Add a test
  - Run all tests and see if the new one fails - Red
  - Write the minimum amount of code to pass the failing test -
  - Run tests - Green
  - Refactor code - Blue
  - Repeat

#### TDD Golden Rule
Do not write any production code until you have a failing test that requires it

#### Arrange, Act, Assert
- Arrange : Setup everything needed for the testing code Data initialization / mocks
- Act : Invoke the code under test / behavior
- Assert : Specify the pass criteria for the test

## Steps:
- A newly created stack should be empty
- if a element is pushed to an empty stack the size is one
- After push, stack should NOT be empty
- After push and pop, stack should be empty
- After two pushes and one pop, stack should not be empty
- After pushing X to stack, pop should return X
- After pushing X, then Y to stack, pop should return Y, then X
- Popping an empty stack should throw an Underflow exception

For an explanation on the stack based calculator see: https://orkhanhuseyn.medium.com/what-are-stack-based-calculators-cf2dbe249264

## Steps:
- Read the expression from left to right
- If current element is a value (e.g. Integer) push it to the stack
- If current element is an operator, pop last two operands from stack, apply operator and push the result back to the stack

## Steps:
- the calculator stack should accept only numbers
- the string with the sum to calculate should only contain numbers and arithmetic operators '+','-' and '*' seperated by spaces
- given a string in RPN (Reverse Polish Notation) the calculator should calculate the outcome of the sum.
- given a string that is not correct RPN the calculator should return an error.
- the string with the sum to calculate can also contain the '/' operator
