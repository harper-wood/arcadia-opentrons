# Accessing Opentrons robots

Created: November 28, 2022 11:54 AM
Created By: David Mets
Last edited By: David Mets
Last edited time: April 3, 2023 5:04 PM
Project: ABPP in Protists, Cheese Micro Communities, Comparative Cytoskeleton, Genome Assemblies, HTP Biology of Protists, Microbial Community Manipulators, Phage Discovery, Spatial Transcriptomics, Trove
Status: In Progress 🙌
Tags: Fluid handler, Lab automation, Opentrons
Team: Cell biology, Lab Ops, Microbiology, Neuro
Type: How-to

## Context

We have two [OT-2](https://opentrons.com/ot-2/?utm_source=google&utm_campaign=Branded&utm_term=opentrons%20ot%202&utm_medium=cpc&hsa_tgt=kwd-549863988937&hsa_cam=881433800&hsa_acc=2303351826&hsa_kw=opentrons%20ot%202&hsa_mt=e&hsa_src=g&hsa_grp=55045114298&hsa_ad=305456799804&hsa_ver=3&hsa_net=adwords&gclid=Cj0KCQiA1ZGcBhCoARIsAGQ0kkr7GDKkYxWL16_0clCUDiSApJtCua_kb-KFSfV8YSiaMSNLJRof_vYaAtOzEALw_wcB) liquid handling robots.  These may be useful for various lab tasks such as: pouring 96 well solid media plates, distributing and pooling liquid cultures, high-throughput sequencing library preparation, high-throughput protein purification etc…  The OT-2 is very flexible with both a low-ish level [python API](https://docs.opentrons.com/v2/) as well as a graphical programming interface called the ‘Protocol Designer’; both are available [here](https://opentrons.com/protocols/).  There is also a [very large code base](https://protocols.opentrons.com/) with many developed protocols. A set of getting started tutorials is available [here](https://support.opentrons.com/s/ot2-get-started).

### **Other resources**

- opentrons [github](https://github.com/Opentrons)
- [example 3d printed accessories (STL files) for opentrons](https://blog.opentrons.com/opentrons-3d-printing-directory/)
- [opentrons protocols](https://protocols.opentrons.com/)
- [Tutorial for the python API](https://docs.opentrons.com/v2/writing.html)
- [Establishing an SSH connection to the robots](https://support.opentrons.com/s/article/Connecting-to-your-OT-2-with-SSH)
- [Arcadia opentrons github](https://github.com/Arcadia-Science/arcadia-opentrons)

## Downloading and installing the opentrons app

To use the opentrons robot you will need to download and install the opentrons app.  This is available for Mac, Windows, and Linux and is available [here](https://opentrons.com/ot-app/).  After downloading you will need to follow the OS specific installation instructions available [here](https://support.opentrons.com/s/article/Get-started-Download-and-install-the-Opentrons-App).  

## Installing the opentrons python API

- If you haven’t already, install python3.  A tutorial for this is available [here](https://realpython.com/installing-python/).
- If you haven’t already, install pip.  A tutorial for this is available [here](https://pip.pypa.io/en/stable/installation/).
- Open a command line and type: ‘pip3 install opentrons’

## Accessing our OT-2 robots

- Connect to the Arcadia wifi or wired network.
- Run the opentrons app.
- Select ‘Devices’ from the left panel, you should now find both robots.