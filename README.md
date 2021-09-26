# PyCon TW Discord Screenshot Bot
The PyCon TW Discord Screenshot Bot will screenshot all track's YouTube streaming in a specific interval, then send these screenshots to assigned channel

### Install
`$ pip install -r requirements.txt`

Notice: Since some functionalities required in discord.py are only available from version 2.0, so please use

`$ pip install -U git+https://github.com/Rapptz/discord.py`

to install discord.py

- Several environment variables need to be set in .env file, included:
    - TOKEN
    - DEFAULT_INTERVAL (In minutes)
    - TRACK0_URL
    - TRACK1_URL
    - TRACK2_URL
    - TRACK3_URL