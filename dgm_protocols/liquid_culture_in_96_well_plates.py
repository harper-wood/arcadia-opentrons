from opentrons import protocol_api
import sys as sys
import math as math

metadata = {
 'apiLevel': '2.13',
 'protocolName': 'distribute liquid media',
 'description': '''This protocol distributes liquid culture media to a set of 96 well plates.''',
    'author': 'DG Mets'
    }

def run(protocol: protocol_api.ProtocolContext):
 # function to calculate initial heights for 50ml conical
 def calc_initial_50(vol):
  dh = -(56.4 - vol)*1000/(math.pi*(13.4**2)) - 14
  return dh 

 def height_track_50(pos, vol):
  nonlocal res_heights

  dh = vol/(math.pi*(13.4**2))
  if res_heights[pos] - dh < -116:
   heights[pos] = -116
  else:
   res_heights[pos] -= dh

 res_initial=calc_initial_50(50.0)

 tips = protocol.load_labware('opentrons_96_tiprack_1000ul', 1)

 reservoir = protocol.load_labware('opentrons_6_tuberack_falcon_50ml_conical',2)
 radius=13.5
 max_vol=50
 reservoir_pos=['A1','A2','A3','B1','B2','B3']
  
 res_heights={}
 for x in reservoir_pos:
  res_heights[x]=res_initial

 n_plates=9
 plate_dct={}
 for n in range(n_plates):
  plate_dct[n]=protocol.load_labware('nest_96_wellplate_200ul_flat', n+3)
 pipette=protocol.load_instrument('p1000_single','left', tip_racks=[tips])
 pipette.pick_up_tip(tips['A1'])
 
 distribute_volume=100
 if len(reservoir_pos)*48*1000<96*n_plates*distribute_volume:
  print('not enough volume in reservoirs')
  sys.exit()
 
 #row_dct={0:'A',1:'B',2:'C',3:'D',4:'E',5:'F',6:'G',7:'H'}
 rows=['A','B','C','D','E','F','G','H']
 well_dct={}
 curr_well=0
 for r in rows:
  for n in range(1,13):
   well_dct[curr_well]=r+str(n)
   curr_well+=1

 absolute_well=0
 current_well=0
 max_wells=(96*n_plates)-1
 #max_wells=10
 current_plate=0
 complete=False
 while absolute_well != max_wells:
  for n in range(len(reservoir_pos)):
   source_loc = reservoir[reservoir_pos[n]]
   for m in range(max_vol-1):
    height=res_heights[reservoir_pos[n]]
    pipette.aspirate(1000,source_loc.top(height), rate = 1.0)
    protocol.delay(seconds=1)
    height_track_50(reservoir_pos[n],1000.0)
    for z in range(int(1000/distribute_volume)):
     pipette.dispense(100, plate_dct[current_plate][well_dct[current_well]])
     current_well+=1
     absolute_well+=1
     if current_well>95:
      current_well=0
      current_plate+=1
     if current_plate==n_plates:
      complete=True
      break
    if complete==True: 
     break
   if complete==True:
    break
  if complete==True:
   break
  
 pipette.drop_tip()


