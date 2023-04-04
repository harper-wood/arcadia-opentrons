# Introduction to opentrons

This tutorial will help you to access and program our OT-2 Opentrons liquid handling robots. The OT-2 is very flexible with both a low-ish level [python API](https://docs.opentrons.com/v2/) as well as a graphical programming interface called the ‘Protocol Designer’; both are available [here](https://opentrons.com/protocols/).  There is also a [very large code base](https://protocols.opentrons.com/) with many developed protocols. A set of getting started tutorials is available [here](https://support.opentrons.com/s/ot2-get-started).

---
## 0.0 Installing software

### Installing the Opentrons app

To access and program the Opentrons instruments using protocols written with the 'Protocol Designer' or written with python you will need the Opentrons app. The app is available for Mac, Windows, and Linux and you can download it [here](https://opentrons.com/ot-app/).
Once downloaded, you will need to follow the OS specific instructions available [here](https://support.opentrons.com/s/article/Get-started-Download-and-install-the-Opentrons-App).

### Installing Python and the opntrons Python API

Basic programming of the opentrons is available using the 'Protocol Designer' but, for more complex programming, the Python API is extremely helpful. Furthermore, if you are familiar with Python even simple tasks are easier to develop using the Python API.
The API consists of two components, a Python library for developing softwre that will interface with the Opentrons hardware and a simulator that will allow you to evaluate your programs prior to uploading them to the machines.

To install the Opentrons Python API you will need to do the following:
- If you haven’t already, install python3.  A tutorial for this is available [here](https://realpython.com/installing-python/).
- If you haven’t already, install pip.  A tutorial for this is available [here](https://pip.pypa.io/en/stable/installation/).
- Open a command line and type: ‘pip3 install opentrons’

---
## 0.1 Acessing and prgramming our OT-2 robots

Once the Opentrons app is installed, you should be able to access our robots.
- Connect to the Arcadia wifi or wired network.
- Run the opentrons app.
- Select ‘Devices’ from the left panel, you should now find both robots.

COMPLETE THIS FOR RUNNING UPLOADED PROTOCOLS AND CALIBRATING THE MACHINES

---
## 0.2 The Opentrons deck and attachments

COMPLETE THIS

---
## 1.0 Anatomy of an Opentrons protocol

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
#distribute diluent
p300.transfer(100, reservoir['A1'], plate.wells())
```
Here, we are asking the robot to use the 'p300' object to 'transfer' 100ul from reservoir position A1 to all of the wells in the 'plate'.
This is kind of a lot packed into a small amount of code, but it takes advantage of many aspects of the API that make programming the opentrons relatively easy.
Because we defined 'p300' as 'p300_single_gen2' the robot knows that the 'p300' object has a 'attribute' called 'transfer' and that 'transfer' requires a series of inputs: first, how much to transfer(100ul); second, where to transfer from(reservoir['A1']); third, where to transfer to (plate.wells()).
