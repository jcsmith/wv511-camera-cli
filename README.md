# wv511-camera-cli

A command line interface to list traffic cameras and the associated RTRSP URL.

This is useful to avoid using the website at wv411.org and avoid using flash player.

## Usage
Execute the command:

`python3 wv411-camera-cli.py`

To list the description and RTSP URL.

You can then use a player which supports RTSP to play the stream.  For example using ffmpeg:

`ffplay $URL`

## Installation
`pip3 install -r requirements.txt`

