#!/usr/bin/env python3
"""NetworkOps Batch 4 — add 70 topics to reach 150."""
import json
from pathlib import Path
TOPICS_DIR = Path(__file__).parent.parent / "data" / "topics"

def t(id,dom,ph,name,diff,what,why,how,when,concepts,config,ts,rel,tags):
    return {"id":id,"domain":dom,"phase":ph,"name":name,"difficulty":diff,
            "theory":{"what":what,"why":why,"how":how,"when":when,
            "key_concepts":concepts,"configuration":config,
            "troubleshooting":ts},"related_topics":rel,"tags":tags}

# 14 more NOC topics
noc=[
