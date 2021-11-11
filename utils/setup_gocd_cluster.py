#!/usr/bin/env python
from gomatic import *

configurator = GoCdConfigurator(HostRestClient("127.0.0.1:8153"))
configurator.save_updated_config(save_config_locally=True, dry_run=True)
