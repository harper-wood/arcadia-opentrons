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

So, lets look at the code:

'''

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
'''
