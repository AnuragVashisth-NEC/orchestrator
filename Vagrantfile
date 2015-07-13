#
# Copyright 2015 Telefonica Investigacion y Desarrollo, S.A.U
#
# This file is part of Orchestrator.
#
# Orchestrator is free software: you can redistribute it and/or
# modify it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Orchestrator is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero
# General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Orchestrator. If not, see http://www.gnu.org/licenses/.
#
# For those usages not covered by this license please contact with
# iot-support at tid dot es
#
# Author: IoT Platform Team

# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  # For a complete reference, please see the online documentation at vagrantup.com.
  
  # Cent OS 6.5 base image
  config.vm.box = "chef/centos-6.5"
  
  # This script will be run at startup
  config.vm.provision :shell, path: "scripts/bootstrap/centos65.sh"
  
  # Network configuration
  config.vm.network "forwarded_port", host: 8184, guest: 8084 # Orchestrator port


end
