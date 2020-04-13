import os
import shutil 
import argparse, sys, json
import requests

with open(os.path.join("./Settings", "sdks.json")) as fh:
    valid_sdks = json.load(fh)


final = {}


for sdk in valid_sdks['names']:
    stripped = sdk.replace("-", "")

    final[sdk] = f"{stripped.upper()}TPModule"
    
valid_sdks['TPModuleNames'] = final

with open(os.path.join("./Settings", "sdks.json"), 'w') as fh:
    json.dump(valid_sdks, fh)