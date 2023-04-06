# Introduction to opentrons

This tutorial will help you to access and program our OT-2 Opentrons liquid handling robots. The OT-2 is very flexible with both a low-ish level [python API](https://docs.opentrons.com/v2/) as well as a graphical programming interface called the ‘Protocol Designer’; both are available [here](https://opentrons.com/protocols/). There is also a [very large code base](https://protocols.opentrons.com/) with many developed protocols. A set of getting started tutorials is available [here](https://support.opentrons.com/s/ot2-get-started).

---
## 0.0 Installing software

### Installing the Opentrons app

To access and program the Opentrons instruments using protocols written with the 'Protocol Designer' or written with python you will need the Opentrons app. The app is available for Mac, Windows, and Linux and you can download it [here](https://opentrons.com/ot-app/).
Once downloaded, you will need to follow the OS specific instructions available [here](https://support.opentrons.com/s/article/Get-started-Download-and-install-the-Opentrons-App).

### Installing Python and the opntrons Python API

Basic programming of the opentrons is available using the 'Protocol Designer' but, for more complex programming, the Python API is extremely helpful. Furthermore, if you are familiar with Python even simple tasks are easier to develop using the Python API.
The API consists of two components, a Python library for developing software that will interface with the Opentrons hardware and a simulator that will allow you to evaluate your programs prior to uploading them to the machines.

To install the Opentrons Python API you will need to do the following:
- If you haven’t already, install python3.  A tutorial for this is available [here](https://realpython.com/installing-python/).
- If you haven’t already, install pip.  A tutorial for this is available [here](https://pip.pypa.io/en/stable/installation/).
- Open a command line and type: ‘pip3 install opentrons’

---
## 0.1 Interfacing with our OT-2 robots

Once the Opentrons app is installed, you should be able to access our robots.
- Connect to the Arcadia wifi or wired network.
- Run the opentrons app.
- Select ‘Devices’ from the left panel, you should now find both robots.

---
## 1.0 The Opentrons hardware

Opentrons hardware we have available:
- 2 O2-t robots
- 3 GEN1 temperature modules (temp range 4-95 C)
- 3 GEN1 magnetic modules
- 1 GEN1 polymerase chain reaction module


---
## 2.0 The Opentrons software

Within the Opentrons software there are three tabs on the left: Protocols, Labware, Devices

- Protocols
This button provides a list of the protocols that have been imported to your Opentrons software. At the upper left you can use the 'import' button to import a new protocol. After selecting an individual protocol, you can 'examine' that protocol or run a protocol from this dialog.

- Labware
This provides a list of available 'labware.' Each piece of labware that can be placed on the deck must has a formatting file that indicates its dimensions, well number etc...  You can create these files for custom labware, but this is beyond the scope of this training. As with the 'Protocols' dialoge, you can import new 'Labware' files by selecting 'Import' at the upper left.

- Devices
Here you should find a list of the available devices.  From this dialoge you can select a device and run a protocol on a particular device.  You can also recalibrate the devices after changing one of the pipettes.  You can also control the modules manually.  You may want to control a module manually if, for example, you need to pre-head a temperature block prior to running your protocol.

---
## 3.0 Anatomy of an Opentrons protocol

We are going to start by going through an example protocol which was developed by Opentrons for training.
This protocol is for generating serial dilutions on a 96 well plate.
The github repository for this example is availbale [here](https://github.com/Opentrons/opentrons/blob/edge/api/docs/v2/example_protocols/dilution_tutorial.py)
and a full walkthrough of the example is available [here](https://docs.opentrons.com/v2/tutorial.html#tutorial)

### Everything
Lets look at the code for this protocol:

```python
from opentrons import protocol_api

metadata = {
    'apiLevel': '2.13',
    'protocolName': 'Serial Dilution Tutorial',
    'description': '''This protocol is the outcome of following the
                   Python Protocol API Tutorial located at
                   https://docs.opentrons.com/v2/tutorial.html. It takes a
                   solution and progressively dilutes it by transferring it
                   stepwise across a plate.''',
    'author': 'New API User'
    }

def run(protocol: protocol_api.ProtocolContext):
	tiprack = protocol.load_labware('opentrons_96_tiprack_300ul', 1)
	reservoir = protocol.load_labware('nest_12_reservoir_15ml', 2)
	plate = protocol.load_labware('nest_96_wellplate_200ul_flat', 3)
	p300 = protocol.load_instrument('p300_single_gen2', 'left', tip_racks=[tiprack])

	# distribute diluent
	p300.transfer(100, reservoir['A1'], plate.wells())

	# loop through each row
	for i in range(8):

		# save the destination row to a variable
		row = plate.rows()[i]

		# transfer solution to first well in column
		p300.transfer(100, reservoir['A2'], row[0], mix_after=(3, 50))

		# dilute the sample down the row
		p300.transfer(100, row[:11], row[1:], mix_after=(3, 50))
```

This protocol contains three main sections:

### Imported packages
```python
from opentrons import protocol_api
```
Here, we import any of the 'packages' that we might need access to in order to execute our program. In different settings, this might have different things (e.g. math, os, sys, sklearn, etc...), but, for this protocol we only need the opentrons API.

### Second, the Metadata and 'context'
```python
metadata = {
    'apiLevel': '2.13',
    'protocolName': 'Serial Dilution Tutorial',
    'description': '''This protocol is the outcome of following the
                   Python Protocol API Tutorial located at
                   https://docs.opentrons.com/v2/tutorial.html. It takes a
                   solution and progressively dilutes it by transferring it
                   stepwise across a plate.''',
    'author': 'New API User'
    }
```
This is a mandatory section for any Opentrons protocol and it must contain, at a minimum, the information provided above. Most critical is the API level which tells the robot which version of the firmware it should be using to interpret your protocol.

### Third: The 'run' function
```python
def run(protocol: protocol_api.ProtocolContext):
        tiprack = protocol.load_labware('opentrons_96_tiprack_300ul', 1)
        reservoir = protocol.load_labware('nest_12_reservoir_15ml', 2)
        plate = protocol.load_labware('nest_96_wellplate_200ul_flat', 3)
        p300 = protocol.load_instrument('p300_single_gen2', 'left', tip_racks=[tiprack])

        # distribute diluent
        p300.transfer(100, reservoir['A1'], plate.wells())

        # loop through each row
        for i in range(8):

                # save the destination row to a variable
                row = plate.rows()[i]

                # transfer solution to first well in column
                p300.transfer(100, reservoir['A2'], row[0], mix_after=(3, 50))

                # dilute the sample down the row
                p300.transfer(100, row[:11], row[1:], mix_after=(3, 50))    
```
This section contains the meat of what you would like the robot to do.  It must be defined as a function ('def') and it must be called 'run'.

Lets walk though this section line by line.

```python
def run(protocol: protocol_api.ProtocolContext):
```
This line tells the robot 'There is a function, it is called 'run.' That function is a 'protocol' and it has a 'context' called 'ProtocolContext.'
It is a little esoteric, but this is the function that the robot will actually execute.  The 'context' is a bunch of information, including the metadata you defined earlier and the hardware configuration (which you haven't told it but it knows) for the robot.


#### Hardware
The next block defines most of the 'hardware' available to the robot:
```python
	tiprack = protocol.load_labware('opentrons_96_tiprack_300ul', 1)
        reservoir = protocol.load_labware('nest_12_reservoir_15ml', 2)
        plate = protocol.load_labware('nest_96_wellplate_200ul_flat', 3)
        p300 = protocol.load_instrument('p300_single_gen2', 'left', tip_racks=[tiprack]) 
```

The first three lines define objects that are in specific locations on the deck and defines handles for those objects.
```python
tiprack = protocol.load_labware('opentrons_96_tiprack_300ul', 1)
```
Tells the robot there is a 96 tip rack of 300ul tips available at deck position 1 and that object is called 'tiprack.'
```python
reservoir = protocol.load_labware('nest_12_reservoir_15ml', 2)
```
Tells the robot that there is a 12 slot (15ml per slot) reservoir at deck position 2 and that object is called 'reservoir.'
```python
plate = protocol.load_labware('nest_96_wellplate_200ul_flat', 3)
```
Tells the robot that there is a 200ul 96 well plate at position 3 on the deck and that object is called 'plate.'
```python
p300 = protocol.load_instrument('p300_single_gen2', 'left', tip_racks=[tiprack]) 
```
Tells the robot that there is a single channel p300 available on the 'left' position of the gantry arm, that its default tip source is 'tiprack' and that that object is called 'p300.'

So that defines all of the resources we wan the robot to have access to during the protocol: the place to get tips is 'tiprack,' the place to get liquid is 'reservoir,' the place to put liquid is 'plate,' the pipetteman the robot will be using is 'p300.'


#### Actions using that hardware
The next portion of the code defines what we want the robot to do with these tools.
We will walk through this section in some detail to be sure we know what is going on at every step.

Lets look at the next few lines:
```python
p300.transfer(100, reservoir['A1'], plate.wells())
```
Here, we are asking the robot to use the 'p300' object to 'transfer' 100ul from reservoir position A1 to all of the wells in the 'plate'.
This is kind of a lot packed into a small amount of code, but it takes advantage of many aspects of the API that make programming the opentrons relatively easy and is worth walking through in some detail.

Lets be a bit pedantic and break it down a little further:
```python
p300.transfer(100
```
Because we defined 'p300' as 'p300_single_gen2' the robot knows that the 'p300' object has a 'attribute' called 'transfer' and that 'transfer' requires a series of inputs. First: how much to transfer (100ul), second: where to transfer from (reservoir['A1']), third: where to transfer to (plate.wells()).

```python
reservoir['A1']
```
Because we defined 'reservoir' as 'nest_12_reservoir_15ml' the robot knows that the 'reservoir' object has a position 'A1'

```python
plate.wells()
```
Because we defined 'plate' as nest_96_wellplate_200ul_flat' the robot knows that the 'plate' object has an atribute called 'wells()' which can be iterated over.  Furthermore, it knows that it should iterate over all of the wells if any one well isn't specified.


This next chunk of code takes advantage of a few other features of the API to iterate through specific rows in the plate.
```python
# loop through each row
for i in range(8):

	# save the destination row to a variable
	row = plate.rows()[i]

	# transfer solution to first well in column
        p300.transfer(100, reservoir['A2'], row[0], mix_after=(3, 50))

        # dilute the sample down the row
        p300.transfer(100, row[:11], row[1:], mix_after=(3, 50))    
```

More pedantry:
```python
for i in range(8):
```
This starts a 'for' loop where, for each value in the range 0-7 we will define a variable i to be that value then execute the subsequent code.

For each execution of the loop we do each of the following:
First:
```python 
	row = plate.rows()[i]
```
This defines a variable 'row' to be a specific row object from the plate.  On the second iteration of the loop, the variable `i` will equal 1 (python starts counting at 0).  This line will define the variable `row` as row B of our 96 well plate.

Second:
```python 
        p300.transfer(100, reservoir['A2'], row[0], mix_after=(3, 50))
```
This line uses the p300 to transfer 100ul from position A2 in the reservoir to position [0] (column 1 on the 96 well plate) in the current row.  After dispensing the liquid, the sample is mixed 3 times with a stroke of 50ul.

Third:
```python 
        p300.transfer(100, row[:11], row[1:], mix_after=(3, 50))
```
This line dilutes the sample that was just moved down the current row.  It uses the p300 to transfer 100ul from each position in the row (up to position 11), to the next position in the row.  After each transfer it mixes 3 times with a stroke of 50ul.
This line could be a little confusing.  Embedded in this function is a loop. The loop is defined here: `row[:11], row[1:]`.  This notation provides a list of wells to the `transfer` function. `row[:11]` = `[row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10]]` and 'row[1:]' is a similar list starting with 1 and ending at the end of the row.  If you provide transfer with a list of locations in this format, it will move through both lists at the same time.  So, the first move it will do is from `row[0]` to `row[1]` then `row[1]` to `row[2]` and so on.

And, thats it!that is a protocol that will move a sample to be diluted into the first row of a 96 well plate and then conduct serial dilutions on each transfered sample.


### 3.1 Changes
To provide some intuition about how to change a protocol to suit your needs, we will make some small changes to this protocol.
Here it is again:

```python
from opentrons import protocol_api

metadata = {
    'apiLevel': '2.13',
    'protocolName': 'Serial Dilution Tutorial',
    'description': '''This protocol is the outcome of following the
                   Python Protocol API Tutorial located at
                   https://docs.opentrons.com/v2/tutorial.html. It takes a
                   solution and progressively dilutes it by transferring it
                   stepwise across a plate.''',
    'author': 'New API User'
    }

def run(protocol: protocol_api.ProtocolContext):
        tiprack = protocol.load_labware('opentrons_96_tiprack_300ul', 1)
        reservoir = protocol.load_labware('nest_12_reservoir_15ml', 2)
        plate = protocol.load_labware('nest_96_wellplate_200ul_flat', 3)
        p300 = protocol.load_instrument('p300_single_gen2', 'left', tip_racks=[tiprack])

        # distribute diluent
        p300.transfer(100, reservoir['A1'], plate.wells())

        # loop through each row
        for i in range(8):

                # save the destination row to a variable
                row = plate.rows()[i]

                # transfer solution to first well in column
                p300.transfer(100, reservoir['A2'], row[0], mix_after=(3, 50))

                # dilute the sample down the row
                p300.transfer(100, row[:11], row[1:], mix_after=(3, 50))
```

Lets say we want to do something simple like only do dilutions in the first 4 rows not all 8. To do this we make 2 changes.  First, we only put diluent in the first 8 lanes. Second, we change the number of iterations in the loop. 
Here is the new code:
```python
from opentrons import protocol_api

metadata = {
    'apiLevel': '2.13',
    'protocolName': 'Serial Dilution Tutorial',
    'description': '''This protocol is the outcome of following the
                   Python Protocol API Tutorial located at
                   https://docs.opentrons.com/v2/tutorial.html. It takes a
                   solution and progressively dilutes it by transferring it
                   stepwise across a plate.''',
    'author': 'New API User'
    }

def run(protocol: protocol_api.ProtocolContext):
        tiprack = protocol.load_labware('opentrons_96_tiprack_300ul', 1)
        reservoir = protocol.load_labware('nest_12_reservoir_15ml', 2)
        plate = protocol.load_labware('nest_96_wellplate_200ul_flat', 3)
        p300 = protocol.load_instrument('p300_single_gen2', 'left', tip_racks=[tiprack])

        # distribute diluent
        p300.transfer(100, reservoir['A1'], plate.rows()[:4])

        # loop through each row
        for i in range(4):

                # save the destination row to a variable
                row = plate.rows()[i]

                # transfer solution to first well in column
                p300.transfer(100, reservoir['A2'], row[0], mix_after=(3, 50))

                # dilute the sample down the row
                p300.transfer(100, row[:11], row[1:], mix_after=(3, 50))
```

OK, something a little more complicated
After running our titration, we want to wait 30min for our reaction to run then add another reagent to the wells.  To do this we need to load a module called 'time' which is part of the core python package. Then add a line that causes the system to pause, then add another transfer function.
Here is the new code:

```python
from opentrons import protocol_api
import time as tm

metadata = {
    'apiLevel': '2.13',
    'protocolName': 'Serial Dilution Tutorial',
    'description': '''This protocol is the outcome of following the
                   Python Protocol API Tutorial located at
                   https://docs.opentrons.com/v2/tutorial.html. It takes a
                   solution and progressively dilutes it by transferring it
                   stepwise across a plate.''',
    'author': 'New API User'
    }

def run(protocol: protocol_api.ProtocolContext):
        tiprack = protocol.load_labware('opentrons_96_tiprack_300ul', 1)
        reservoir = protocol.load_labware('nest_12_reservoir_15ml', 2)
        plate = protocol.load_labware('nest_96_wellplate_200ul_flat', 3)
        p300 = protocol.load_instrument('p300_single_gen2', 'left', tip_racks=[tiprack])

        # distribute diluent
        p300.transfer(100, reservoir['A1'], plate.wells())

        # loop through each row
        for i in range(8):

                # save the destination row to a variable
                row = plate.rows()[i]

                # transfer solution to first well in column
                p300.transfer(100, reservoir['A2'], row[0], mix_after=(3, 50))

                # dilute the sample down the row
                p300.transfer(100, row[:11], row[1:], mix_after=(3, 50))

        tm.sleep(30*60) #sleep expects time in seconds.  30*60 will sleep for 30 min.

        p300.transfer(20, reservoir['A3'], plate.wells(), mix_after=(3,50))
```
