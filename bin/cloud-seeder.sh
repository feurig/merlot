#!/bin/bash -e
#-------------------------------------------------------------------------cloud-seeder.sh
# Set up cloud init source from /boot partition. 
# Stolen from
# https://gist.github.com/RichardBronosky/fa7d4db13bab3fbb8d9e0fff7ea88aa2#file-cloud-init-setup-sh
# with some adjustments.

set -x

# Get cloud-init
sudo apt update
sudo debconf-set-selections -v <<<"cloud-init cloud-init/datasources multiselect NoCloud, None" 2>/dev/null
sudo apt install -y cloud-init
#sudo debconf-set-selections -v <<<"cloud-init cloud-init/datasources multiselect NoCloud, None" 2>/dev/null; sudo dpkg-reconfigure cloud-init -f noninteractive 2>/dev/null;

# Prepare datasource
sudo tee /etc/cloud/cloud.cfg <<'YAML'
# The top level settings are used as module
# and system configuration.
datasource:
  NoCloud:
    seedfrom: /boot/

# A set of users which may be applied and/or used by various modules
# when a 'default' entry is found it will reference the 'default_user'
# from the distro configuration specified below
users:
   - default

# If this is set, 'root' will not be able to ssh in and they
# will get a message to login instead as the above $user (debian)
#disable_root: true

# This will cause the set+update hostname module to not operate (if true)
preserve_hostname: false

# Example datasource config
# datasource:
#    Ec2:
#      metadata_urls: [ 'blah.com' ]
#      timeout: 5 # (defaults to 50 seconds)
#      max_wait: 10 # (defaults to 120 seconds)

# The modules that run in the 'init' stage
cloud_init_modules:
 - migrator
 - bootcmd
 - write-files
 - mounts
 - rsyslog
 - users-groups
 #- ssh

# The modules that run in the 'config' stage
cloud_config_modules:
# Emit the cloud config ready event
# this can be used by upstart jobs for 'start on cloud-config'.
 - ssh-import-id
 - locale
 - set-passwords
 - ntp
 - timezone
 - runcmd

# The modules that run in the 'final' stage
cloud_final_modules:
 - package-update-upgrade-install
 - scripts-vendor
 - scripts-per-once
 - scripts-per-boot
 - scripts-per-instance
 - scripts-user
 - phone-home
 - final-message

# System and/or distro specific settings
# (not accessible to handlers/transforms)
system_info:
   # This will affect which distro class gets used
   distro: debian
   # Default user name + that default users groups (if added/used)
   default_user:
     name: feurig
     #lock_passwd: True
   # Other config here will be given to the distro class and/or path classes
   paths:
      cloud_dir: /var/lib/cloud/
      templates_dir: /etc/cloud/templates/
YAML

# Create meta-data
sudo tee /boot/meta-data <<'YAML'
instance-id: iid-raspberrypi-nocloud
YAML

# Create user-data
sudo tee /boot/user-data <<'YAML'
#cloud-config
users:
    - name: feurig
    passwd: "$y$j9T$tQ8RNmITXWZKZR087zQAp1$b/qa0h8rPsuDCDRojd9y5nPRcWb3hOfQVsvVsDDzugD"
    gecos: Donald Delmar Davis
    ssh-authorized-keys:
        - ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDCNy/mrQ8eTWAAVZ7CMvUKm1FW6+OFzEFz6VPICa232AlIqm/VbIYUG3MuS5CS7yLK/+vqPo365GfgirMBXTVA07B1+DrWG4qsZrZexWrTM7VHjKf8JgNQVufZqBpJXAloNaOmjlnTERVtiSV/1bzqdkPetba0K9T0gkCwvXLgedjsOvCusunpxl7hcxEXWORZrn+UiFs03+Xpp9njrb3BDT5SFD4xCHFP3y/3v+ScvcTe6iQ3MWO915h2ZOVmNzam3+S2XlHGZrFLS1jnHqWzn1IUMUgDnVkB6nuRLDNJ3en/P9stkGIv4MQJKu9uWtGl3xwG8/EhCCblyd/ZfH7seE5QqAUem9uTGHY2vBAwi4s6O6hNdk/c4IjANkzw0R//n6QN2GK/hGd3xWZRGCWQLhfQIKwrlZyZH+dj6YK55n3GFzg7EP4vfyWbNogdhvZLMdhm/Lo8LQYXZWRWd93Rp3+sB2nqvcToiawG8GK1eVNHcYuTNg+gPjbxlxLBr1s= root@utah
        - ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDCr3NJ4Pyb3lwgPXerxeMHhhdq4+XZTgMBG/oikbeexiKr8o8U0lZs046Avf1bQO/IOJNpyzebPGQlz7pV5VDkIehtkGSIq5YI5IoOKfhK8K0wGP8mNYqEwAHsbWG3KntLM63X+hUy4t7ng+o5KtBVyWmc9hJg6eo8EDjJTnOhQMmcVqmrXQ0yR6DRGc6SarULHPQLKljmE3k1sCNLzORGFVV0mqhblmvCwONGEDQOHEg9AW/f56OVppwnDqdsmrtns+iE36A5Ib4FTuFe/XvJPCIqP3w1kvFuH99TourUt6YdtGAXQShI5gnMQg+GbuH16SaPBxCleE1AuVytmSMv5y2L/zLSnfSuJ9eAL1Shmf5Hy7z14uOHQWlCN0nQNVbF2ehumUG7eR0wnQhnwoYHiRqXqRO/FR1mCGfvv42yTDlgm8/SKRzgZcIgIFiZAoujQQzVHrBcb1PSZTFdHjp1Qbeew2DTPnOA4QNIWFD6Yg70MXJ8illickfQEaL2nvU= feurig@costello
        - ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAINOPzj8x1N0dxgQkZTIw4PYxuCwCY9+HXm1n3DNMNfEd root@guthrie
        - ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDQiVOR+1dZzYeNwqbDs3w9rug2odA9nqdbiijZmUWE8LsOO/iyo+AoyFZSbq9/Qiis8nRcVCDngZ0NqYrAcY6XRLByfxS3cwkVnh8C+WMda7wJ09hWKwwOXfWyFjJ3bs3CBpmLQ4umrpRfpbr198bJ7BOzHGf9ttPRaFUxExO6PCdA2SwJ0sjCDzIY03iM4xVcE0K3zQmHI1Fy2Ep3jRLCZ6v7jbwAJs71kR80gF53QKTaSXaP/VLCCh2KdE4g+kv0L9+1r5bQWVkOyAkW85whSlfqDx7dx2mM2kfiLKNkHyUDoG/ckxva+i6LRN4UpB4TDFNe+C0NWHPT5YCJapdjkwfFi/49mjzEjDCg991oLHgHJypoRehL1DrMt+kSHkltUtXxoEvnAJpMad4xB9ZDvZPNXREmB71qFggY5lAhwsxzdI7Ytrx9r+4DmK3O8JmJ1EZW0yPJ1FPMaDG/k5cN095TRC3IabzxetmyTdittAoWHh3birTWYHkKbi6cal0= root@Eddie.lan
        - ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDMv8iznfGVmdp8iNzi7xIyiVreQq23sqzdQt5Oiif7yuXWHy5ejvug1cKCWWrFfe4W9qmY01oxrZm6t5QZTnIBcScvdixwa9nRvDVY7QW6/I8blQI6OXfwW2d8DvP85pdgUIKxQzYScaNlNkm5mME7sop16eN7D7o8dwCovwr8mOvkPZM65Vbtrn0xRek118gDoHS1yFqSwNKV3hvlXOqSqoWeHmnMnm7Nx3wS75Rdo97fyWguZJc3GObvzTaqmC3JqnDHtuGKwu2hbiRODId0/TbZ9lFohTa5AnwpsQkjBvJuZwCaIRku/c4DG8sP5nwGV2bBbBLh8zDalQUm52RSfAAQ9FCSzt1xdZ64NPml/Rnrg16hLVOpUGemNgso5ACSQd6wgqzVT/S66zLpN+f425vCNC+mBIXVmvfMxwzh9XyOkL1W9p+KOEPAIO1Owj1uVJvnojbp1EMmcy1wp2zeA2LexoBGi2iFhLLbLysRgkFWxXyWvUETf0DlM5GEGMc= feurig@nedelko.local
        - ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDMYKq9b1+utFxip1dsujTRqpG3maSwDHfyDoYduHRs9ntq3NS80yRZYbvSgdlUACbTFM84tXPi76reN5DIvQf4pqlBsfQoBAf0iVs+yeh2a7b+fMzIfV5jEYvvTnlf914TtPI706XVOzmcX4OWgViwSNmMMHSBER33/V+oSylhaXALJOSPkd1QEfwiXlcERsYt1To8dclbI/fOfX6LZA0PHWT58hXXmJIQOqWnG9Zsv5gUO8rsq2dy+QHUDHxdX/0fOUQTVaMIzkdUOu4viHZSlKEKEcLDg3fag0qaNaK3LgwCCtPkuDU9y0SN+B8sviTBnqjLNh1GYMi9F9orFGvKfyWd3e8JVeP7RXmS2JgQYC61Y9Dz0v3AW8lUYP6ASvpGFPlg2ql6yklz+GBLhN4dc/bRrBfoElF+GHo954OeMOTwFlWMTy6X7SCk6ZDpVILYnKfExbaOlVNSHHaN2Aq0Lr98N3r5kHtt4hPCm6kXNashHtUyhI7qIPecPK8xXhE= feurig@amyl.lan
    groups: sudo,root,wheel
    shell: /bin/bash
apt_update: true
apt_upgrade: true
packages:
    - nano
    - openssh-server
    - less
    - git
    - python3-pip
    - htop 
    - curl
    - net-tools
    - prometheus-node-exporter
ssh_authorized_keys:
    - ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDMYKq9b1+utFxip1dsujTRqpG3maSwDHfyDoYduHRs9ntq3NS80yRZYbvSgdlUACbTFM84tXPi76reN5DIvQf4pqlBsfQoBAf0iVs+yeh2a7b+fMzIfV5jEYvvTnlf914TtPI706XVOzmcX4OWgViwSNmMMHSBER33/V+oSylhaXALJOSPkd1QEfwiXlcERsYt1To8dclbI/fOfX6LZA0PHWT58hXXmJIQOqWnG9Zsv5gUO8rsq2dy+QHUDHxdX/0fOUQTVaMIzkdUOu4viHZSlKEKEcLDg3fag0qaNaK3LgwCCtPkuDU9y0SN+B8sviTBnqjLNh1GYMi9F9orFGvKfyWd3e8JVeP7RXmS2JgQYC61Y9Dz0v3AW8lUYP6ASvpGFPlg2ql6yklz+GBLhN4dc/bRrBfoElF+GHo954OeMOTwFlWMTy6X7SCk6ZDpVILYnKfExbaOlVNSHHaN2Aq0Lr98N3r5kHtt4hPCm6kXNashHtUyhI7qIPecPK8xXhE= feurig@amyl.lan
write_files:
    - path: /etc/resolv.conf.static
    permissions: '0644'
    owner: root:root
    content: |
        nameserver 192.168.128.1
        nameserver 198.202.31.141
        search suspectdevices.com fromhell.com vpn
    - path: /usr/local/bin/update.sh
    permissions: '0774'
    owner: root:root
    content: |
        #!/bin/bash
        # update.sh for debian/rocky/pihole  (copyleft) don@suspecdevices.com
        echo --------------------- begin updating `uname -n` ----------------------
        if [ -x "$(command -v apt-get)" ]; then
        apt-get update
        apt-get -y dist-upgrade
        apt-get -y autoremove
        fi
        if  [ -x "$(command -v pihole)" ]; then
        echo update pihole.
        pihole -up
        fi
        if  [ -x "$(command -v dnf)" ]; then
        echo dnf upgrade.
        dnf -y upgrade
        fi
        echo ========================== done ==============================
runcmd:
    - sed -i "s/^127.0.0.1/#127.0.0.1/" /etc/hosts
    - echo 127.0.0.1 `hostname` localhost >>/etc/hosts
    - passwd feurig -u
    - mv /etc/resolv.conf /etc/resolv.conf.foobarred
    - ln -s /etc/resolv.conf.static /etc/resolv.conf
    #- apt-get install -y openssh-server nano less
power_state:
    mode: reboot
    message: See You Soon...
    condition: true

YAML

# Initialize cloud-init
sudo cloud-init init --local

# Create a script to run per boot
sudo tee /var/lib/cloud/scripts/per-boot/00_run-parts.sh <<'BASH'
#!/bin/bash

# Prevent *.sh from returning itself if there are no matches
shopt -s nullglob

# Run every per-once script
run-parts --regex '.*\.sh$' /boot/per-once

# Rename every per-once script
for f in /boot/per-once/*.sh; do
    mv $f $(dirname $f)/$(basename $f .sh).$(date +%F@%H.%M.%S)
done

# Run every per-boot script
run-parts --regex '.*\.sh$' /boot/per-boot
BASH
sudo chmod +x /var/lib/cloud/scripts/per-boot/00_run-parts.sh

# Create sample per-boot and per-once scripts
sudo mkdir -p /boot/{per-boot,per-once}
sudo tee /boot/per-boot/01_get_ready.sh \
         /boot/per-boot/02_do_it.sh \
         /boot/per-once/01_prepare.sh \
         /boot/per-once/02_install_stuff.sh <<'BASH'
#!/bin/bash

date="$(date +"%x %X")"
script_path="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
script_name="$(basename ${BASH_SOURCE[0]} .sh)"
log_name="$(basename $script_path)"

echo "$date - $script_name" >> /home/pi/${log_name}.out
BASH

echo "Cloud-Init setup is complete."
# vim: et sw=4 ts=4 sts=4 syntax=sh