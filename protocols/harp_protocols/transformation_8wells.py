from opentrons import protocol_api

# metadata
metadata = {
    'protocolName': 'e. Coli Transformation on the Opentrons: 8 Wells in a 96 Well Block',
    'author': 'Atanas, Harper',
    'description': 'e. coli chem comp cells transformation in 96 well block',
    'apiLevel': '2.13'
}


#to follow along with the protocol in Notion, search for "Automated E. coli Transformation on the Opentrons" which lives in the Protocol section of Harper's ELN



# protocol run function
def run(protocol: protocol_api.ProtocolContext):

# telling the opentrons where everything is located:

    # Load a Temperature Module GEN1 in deck slot 3.
    temperature_module = protocol.load_module('temperature module', location='3')

    # labware
    plate1 = temperature_module.load_labware('nest_96_wellplate_2ml_deep')
    plate2 = protocol.load_labware('nest_96_wellplate_100ul_pcr_full_skirt', location='1')
    
    tiprack1000 = protocol.load_labware('opentrons_96_tiprack_1000ul', location='5')
    tiprack20 = protocol.load_labware('opentrons_96_tiprack_20ul', location='4')

    # pipettes
    left_pipette = protocol.load_instrument(
         'p1000_single_gen2', mount='left', tip_racks=[tiprack1000])
    right_pipette = protocol.load_instrument(
         'p20_multi_gen2', mount='right', tip_racks=[tiprack20])

    # Arcadia's custom falcon tube holder
    tube_holder = protocol.load_labware('opentrons_6_tuberack_falcon_50ml_conical', location='2')

# setup:
    # cells: calculate total volume of cells needed, then make sure there is ~200ul extra in the 50ml falcon tube
    # LB: calculate total volume of LB needed, then make sure there is ~200ul extra in the 50ml falcon tube
    # plasmids: calculate total volume of plasmids needed, then make sure there is ~2ul extra in each well
    # antibiotic: aliquot 4uL of antibiotic per well you wish to transform (more than is needed for below command)

# commands:
    # Step 5 in the Notion protocol - cells to block
    left_pipette.distribute(50, tube_holder.wells_by_name()['A1'], plate1.columns_by_name()['2'])
    
    # Step 6 in the Notion protocol - plasmids to cells in block
    right_pipette.transfer(2, plate2.columns_by_name()['1'], plate1.columns_by_name()['2'], mix_after=(4,15))

    # Step 7 in the Notion protocol - heat shocking
    temperature_module.set_temperature(celsius=45)
    protocol.delay(seconds=40)
    temperature_module.set_temperature(celsius=4)
    protocol.delay(minutes=3)
    temperature_module.deactivate()

    # Step 8 in the Notion protocol - transfer LB for recovery   
    # change the height from which liquid is dispensed above the bottom of the well
    # this is necessary for the transferring of 900ul into many wells using the same P1000 tip
    left_pipette.well_bottom_clearance.dispense = 30
    left_pipette.transfer(900, tube_holder.wells_by_name()['A2'], plate1.columns_by_name()['2'])


    # Step 9 in the Notion protocol - ause for incubation, incubate at 37C, shake at 280rpm
    protocol.pause()

    # Step 10 in the Notion protocol - transfer antibiotic only after recovery of the transformed cells at 37C shaking for 1hr
    # change the height from which liquid is dispensed above the bottom of the well
    # this is to avoid submerging the entire P20 tip into 900ul of liquid
    right_pipette.well_bottom_clearance.dispense = 10
    right_pipette.transfer(1.5, plate2.columns_by_name()['2'], plate1.columns_by_name()['2'])
