#!/bin/python

python read_live_data.py level1ShMktData | python format_sh_tick_to_1min_bar.py sh | python send_to_nats.py