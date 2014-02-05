Vending Machine Digital Machine
================================

Problem Description
--------------------

Emulate the operation of a vending maching on a limited 
user input-ouput (IO) digital system.  This vending 
machine is intended to work on a system with four discrete
input buttons and eight discrete output LEDs.

The vending machine will have four items with four different
costs:

    1. item 1 : 20 units
    2. item 2 : 100 units
    3. item 3 : 40 units
    4. item 4 : 55 units

The vending machine accepts four different coin types:

    1. coin 1 : 1 unit
    2. coin 2 : 5 units
    3. coin 3 : 10 units 
    4. coin 4 : 25 units

The vending maching is initially waiting for input, a 
user will select an item (1-4) by pressing one of the 
buttons.  The vending machine will then change state to
accept the coin inputs from the four input buttons.  The 
machine will display on the middle four leds which item 
as selected during the coin insertion (as soon as an item
is selected).

Once the correct amount for the item has been input the 
vending machine will dispence the item.  The machine indicates
it is dipencing by alternating the LEDs with the pattern:

    1 1 0  0  0  0  1 1  # for .5 seconds
    0 0 i4 i3 i2 i1 0 0  # for .5 seconds

When dispencing the above pattern will flash, the second
pattern indicates which item is dispenced by using the 
middle four LEDs.  The above pattern will flash three 
times (total of three seconds elapse).

The machine can be reset at any point by pressing more than
one button simultaneously - this will reset the machine back
to the waiting state.

If the wrong value is enter the machine will enter an error
state and display an error code on the LEDs (0xFF) or if
four seconds elapse before a button press during the coinage
insertion (emulated insertion with button press) the 
machine will enter the error state.  The error state can 
only be cleared by simultaneous button press.


Examples and State Diagrams
----------------------------
Example of a valid button sequence and the corresponding
LED codes (0 button indicates no button press and here 
I talk about buttons 1,2,3,4 not the possible encoding 
on a piece of hardware):

    button        led code              total coin
    -------        --------              ----------
    0              0x00  00_0000_00      0
    1              0x04  00_0001_00      0
    2              0x04  00_0001_00      5
    3              0x04  00_0001_00      15
    2              0xC3  11_0000_11      20  
   

Simplified ASMD:

    wait for item selection [waiting]
             |
       |item entered|
             |
      accept coin insertion [coinage]
                   |
         |coin insertion |--+
          |        |        |
        too much  timeout   |
        coin       |        |
         |         |        |
         \         /        |
            error           |
              |             |
           more than     |correct coin|
           one button       |
                            |
                         dispense item [dispense]
                            |
                            |
                         back to wait


More Sequences
--------------
This directory contains a collection of *valid* and *invalid*
sequences.  The files are simple comma-separated-value (csv) 
format:

    <button>, <led code>, <vend total>, <time ms>
