from opentrons import protocol_api
import sys as sys

metadata = {
 'apiLevel': '2.13',
 'protocolName': 'distribute liquid media',
 'description': '''This protocol distributes liquid culture media to a set of 96 well plates.''',
    'author': 'DG Mets'
    }

def run(protocol: protocol_api.ProtocolContext):
 tips = protocol.load_labware('opentrons_96_tiprack_1000ul', 1)

 reservoir = protocol.load_labware('opentrons_10_tuberack_falcon_4x50ml_6x15ml_conical',2)
 radius=13.5
 max_vol=50
 reservoir_pos=['A4','B4','A5','B5']
 
 n_plates=9
 plate_dct={}
 for n in range(n_plates):
  plate_dct[str(n)]=protocol.load_labware('nest_96_wellplate_200ul_flat', n+3)
 pipette=protocol.load_instrument('p1000_single','left', tip_racks=[tips])
 pipette.pick_up_tip(tips['A1'])
 
 distribute_volume=200
 if len(reservoir_pos)*48*1000<96*n_plates*distribute_volume:
  print('not enough volume in reservoirs')
  sys.exit()
 
 current_well=0
 max_wells=96*n_plates
 while current_well != max_wells:
  for n in range(len(reservoir_pos)):
   source_loc = reservoir.wells(reservoir_pos[n])
   pipette.aspirate(1000,source_loc, rate = 1.0)
