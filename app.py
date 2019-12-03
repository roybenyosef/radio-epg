#!/usr/bin/env python3

from aws_cdk import core

from radio_epg.radio_epg_stack import RadioEpgStack


app = core.App()
RadioEpgStack(app, "radio-epg")

app.synth()
