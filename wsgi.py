# -*- coding: utf-8 -*-
from core.startup import create_app

# ============ NOTE ============
# Change the configuration name if needed
app = create_app(name=__name__, config_name='production')
# ==============================

