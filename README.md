
# arcadia-opentrons
## purpose
This repository contains code (protocols, STL CAD files, etc...) developed at Arcadia for using the Opentrons liquid handling robots.

## resources
- opentrons [github](https://github.com/Opentrons)
- example 3d printed accessories (STL files) for opentrons(https://blog.opentrons.com/opentrons-3d-printing-directory/)
- opentrons protocols(https://protocols.opentrons.com/)
- Tutorial for the python API(https://docs.opentrons.com/v2/writing.html)
- Establishing an SSH connection to the robots(https://support.opentrons.com/s/article/Connecting-to-your-OT-2-with-SSH)
- Arcadia opentrons github(https://github.com/Arcadia-Science/arcadia-opentrons)

## Downloading and installing the opentrons app
To use the opentrons robot you will need to download and install the opentrons app.  
This is available for Mac, Windows, and Linux and is available here:
https://opentrons.com/ot-app/
After downloading you will need to follow the OS specific installation instructions available here:
https://support.opentrons.com/s/article/Get-started-Download-and-install-the-Opentrons-App

## Installing the opentrons python API
- If you haven't already, install conda. You can find installation instructions [here](https://training.arcadiascience.com/arcadia-users-group/20221017-conda/lesson/#installing-conda).
- Create a conda environment to install opentrons: `conda create -n opentrons -c conda-forge opentrons`
- Activate the conda environment: `conda activate opentrons`
