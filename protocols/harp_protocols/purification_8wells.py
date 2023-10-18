from opentrons import protocol_api

# metadata
metadata = {
    'protocolName': 'Purification',
    'author': 'Atanas, Harper',
    'description': 'e. coli chem comp cells purification in 96 well block',
    'apiLevel': '2.13'
}

# protocol run function
def run(protocol: protocol_api.ProtocolContext):

    # Load a magnetic module GEN1 in deck slot 3.
    magnetic_module = protocol.load_module('magnetic module', location='3')

    # labware
    plate1 = magnetic_module.load_labware('nest_96_wellplate_2ml_deep')
    plate2 = protocol.load_labware('nest_96_wellplate_200ul_flat', location='6')
    plate3 = protocol.load_labware('nest_12_reservoir_15ml', location='2')
    # column1 is resuspension/washing buffer, column2 is lysis reagent, column3 is beads, 
    # column4 is elution buffer, column 12 is for waste
    # may need another 12-well reservoir in deck slot 1 for waste when scaling up to 96 samples

    #tiprack20 = protocol.load_labware('opentrons_96_tiprack_20ul', location='5')
    tiprack300 = [protocol.load_labware('opentrons_96_tiprack_300ul', location) for location in ['4','5']]
    # may need more tips across the remaining deck slots 6,7,8,9,10,11 for scaling up to 96 samples
    
    # pipettes
    #left_pipette = protocol.load_instrument(
    #     'p20_single_gen2', mount='left', tip_racks=[tiprack20])
    right_pipette = protocol.load_instrument(
         'p300_multi_gen2', mount='right', tip_racks=tiprack300)


    # commands
    # Step 5 in the Notion protocol – resuspend cells in buffer in the 2ml block 
    right_pipette.transfer(200, plate3.columns_by_name()['1'], plate1.columns_by_name()['4'], mix_after=(10,180), aspirate_speed=400,
    dispense_speed=600)

    # Step 6 in the Notion protocol – add lysis reagent, then mix
    right_pipette.transfer(50, plate3.columns_by_name()['2'], plate1.columns_by_name()['4'], mix_after=(10,200), aspirate_speed=300,
    dispense_speed=500)

    # Step 7 in the Notion protocol – mix and add beads to lysate -> it's really important to make sure beads are mixed well!!!
    #below we are changing dispense height to hopefully mix beads better
    right_pipette.well_bottom_clearance.aspirate = 1
    right_pipette.well_bottom_clearance.dispense = 20
    right_pipette.pick_up_tip()
    right_pipette.transfer(280, plate3.columns_by_name()['3'], plate3.columns_by_name()['3'], new_tip='never')
    right_pipette.transfer(280, plate3.columns_by_name()['3'], plate3.columns_by_name()['3'], new_tip='never')
    right_pipette.transfer(280, plate3.columns_by_name()['3'], plate3.columns_by_name()['3'], new_tip='never')
    right_pipette.transfer(280, plate3.columns_by_name()['3'], plate3.columns_by_name()['3'], new_tip='never')
    right_pipette.transfer(280, plate3.columns_by_name()['3'], plate3.columns_by_name()['3'], new_tip='never')
    right_pipette.transfer(280, plate3.columns_by_name()['3'], plate3.columns_by_name()['3'], new_tip='never')
    right_pipette.transfer(280, plate3.columns_by_name()['3'], plate3.columns_by_name()['3'], new_tip='never')
    right_pipette.transfer(280, plate3.columns_by_name()['3'], plate3.columns_by_name()['3'], new_tip='never')
    right_pipette.transfer(280, plate3.columns_by_name()['3'], plate3.columns_by_name()['3'], new_tip='never')
    right_pipette.transfer(280, plate3.columns_by_name()['3'], plate3.columns_by_name()['3'], new_tip='never')
    right_pipette.transfer(200, plate3.columns_by_name()['3'], plate1.columns_by_name()['4'], new_tip='never', mix_after=(10,280))
    right_pipette.drop_tip()

    # Step 8 in the Notion protocol – incubate with beads 5min
    protocol.delay(minutes=10)

    right_pipette.well_bottom_clearance.dispense = 1

    magnetic_module.engage()
    protocol.delay(minutes=4)

    # Step 9 in the Notion protocol – engage magnet and save supernatant to analyze later on gel
    right_pipette.well_bottom_clearance.aspirate = 5 #needs height editing. picked up too many beads and then nothing on waste
    
    right_pipette.transfer(200, plate1.columns_by_name()['4'], plate2.columns_by_name()['1'], new_tip='once')
    #right_pipette.transfer(220, plate1.columns_by_name()['4'], plate3.columns_by_name()['12'])
    magnetic_module.disengage()
    
    right_pipette.well_bottom_clearance.aspirate = 1

    # 9.1 washing and removing supernatant
    right_pipette.transfer(200, plate3.columns_by_name()['1'], plate1.columns_by_name()['4'], mix_after=(10,200))
    magnetic_module.engage()
    protocol.delay(minutes=4)
    right_pipette.transfer(200, plate1.columns_by_name()['4'], plate3.columns_by_name()['12'])
    magnetic_module.disengage()

    # 9.2 washing and removing supernatant
    right_pipette.transfer(200, plate3.columns_by_name()['1'], plate1.columns_by_name()['4'], mix_after=(10,200))
    magnetic_module.engage()
    protocol.delay(minutes=4)
    right_pipette.transfer(200, plate1.columns_by_name()['4'], plate3.columns_by_name()['12'])
    magnetic_module.disengage()

    # 9.3 washing and removing supernatant
    right_pipette.transfer(200, plate3.columns_by_name()['1'], plate1.columns_by_name()['4'], mix_after=(10,200))
    magnetic_module.engage()
    protocol.delay(minutes=4)
    right_pipette.transfer(200, plate1.columns_by_name()['4'], plate3.columns_by_name()['12'])
    magnetic_module.disengage()

    # Step 10 in the Notion protocol – elution
    right_pipette.transfer(200, plate3.columns_by_name()['4'], plate1.columns_by_name()['4'], mix_after=(10,200))
    magnetic_module.engage()
    protocol.delay(minutes=4)
    right_pipette.transfer(200, plate1.columns_by_name()['4'], plate2.columns_by_name()['2'])
    magnetic_module.disengage()
