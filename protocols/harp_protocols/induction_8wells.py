from opentrons import protocol_api

# metadata
metadata = {
    'protocolName': 'Induction',
    'author': 'Atanas, Harper',
    'description': 'e. coli induction in  96 well block',
    'apiLevel': '2.13'
}

# protocol run function
def run(protocol: protocol_api.ProtocolContext):

    # Load a Temperature Module GEN1 in deck slot 3. We are not using it for this protocol but it always lives in slot 3.
    temperature_module = protocol.load_module('temperature module', location='3')

    # labware
    plate1 = protocol.load_labware('nest_96_wellplate_2ml_deep', location='6')
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
     # LB: calcuate total volume of LB needed, load maximum 30mL into each falcon tube
     # antibiotic: 10uL per well of plate 2 column 3 for each well you wish to induce from plate 1
     # IPTG: only add after the OD has reached 0.6-0.8. Do not leave sitting out.


 # commands:

    # Step 4 in the Notion protocol - distributing LB
    left_pipette.well_bottom_clearance.aspirate = 15
    left_pipette.transfer(990, tube_holder.wells_by_name()['A1'], plate1.columns_by_name()['3'])
    left_pipette.transfer(990, tube_holder.wells_by_name()['A1'], plate1.columns_by_name()['4'])
    # the below command tells the robot to aspirate from closer to bottom of tube as liquid level decreases
    left_pipette.well_bottom_clearance.aspirate = 1
    left_pipette.transfer(990, tube_holder.wells_by_name()['A1'], plate1.columns_by_name()['5'])

    # Step 5 in the Notion protocol  - distributing cells to LB
    right_pipette.transfer(10, plate1.columns_by_name()['2'], plate1.columns_by_name()['3'], mix_before=(10,20), mix_after=(4,20))
    right_pipette.transfer(10, plate1.columns_by_name()['2'], plate1.columns_by_name()['4'], mix_before=(10,20), mix_after=(4,20))
    right_pipette.transfer(10, plate1.columns_by_name()['2'], plate1.columns_by_name()['5'], mix_before=(10,20), mix_after=(4,20))

    # Step 6 in the Notion protocol - distributing antibiotic to the dilutions
    right_pipette.transfer(1.2, plate2.columns_by_name()['3'], plate1.columns_by_name()['3'], mix_after=(4,20))
    right_pipette.transfer(1.2, plate2.columns_by_name()['3'], plate1.columns_by_name()['4'], mix_after=(4,20))
    right_pipette.transfer(1.2, plate2.columns_by_name()['3'], plate1.columns_by_name()['5'], mix_after=(4,20))

    # Step 7/8/9 in the Notion protocol - pause to grow, check OD, take preinduction sample
    protocol.pause()

    # Step 10 in the Notion protocol - adding IPTG to induce
    right_pipette.transfer(1, plate2.columns_by_name()['4'], plate1.columns_by_name()['4'], mix_after=(4,20))
    right_pipette.transfer(1, plate2.columns_by_name()['4'], plate1.columns_by_name()['5'], mix_after=(4,20))
