#WRITTEN BY GPT4 USE WITH CAUTION
from opentrons import protocol_api

metadata = {
    'protocolName': 'Multi-Plate Dispensing',
    'author': 'Your Name',
    'description': 'Script to pick up 200uL from a deep well plate and dispense into 3 different plates',
    'apiLevel': '2.10'
}

def run(protocol: protocol_api.ProtocolContext):

    # labware
    tiprack = protocol.load_labware('opentrons_96_tiprack_300ul', '1')
    source_plate = protocol.load_labware('nest_96_wellplate_2ml_deep', '2')  # changed to 96 deep well plate
    destination_plates = [protocol.load_labware('corning_96_wellplate_360ul_flat', slot)
                          for slot in ['3', '4', '5']]

    # pipettes
    left_pipette = protocol.load_instrument('p300_multi', 'left', tip_racks=[tiprack])

    # protocol
    for i in range(12):  # for each column
        left_pipette.pick_up_tip()
        for plate in destination_plates:

            # mix the liquid in the source well before aspirating
            left_pipette.mix(3, 200, source_plate.columns()[i][0])

            # pick up 200uL from source plate
            left_pipette.aspirate(200, source_plate.columns()[i][0])

            # dispense 200uL into the destination plate
            left_pipette.dispense(200, plate.columns()[i][0])

        left_pipette.drop_tip()
        
