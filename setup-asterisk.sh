#!/bin/bash

# Asterisk Setup Script
# This script helps configure Asterisk for SIP trunking

echo "=== Asterisk Setup Script ==="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    print_error "Please run this script as root (use sudo)"
    exit 1
fi

print_status "Starting Asterisk configuration..."

# Backup existing configurations
print_status "Backing up existing configurations..."
cp /etc/asterisk/pjsip.conf /etc/asterisk/pjsip.conf.backup.$(date +%Y%m%d_%H%M%S)
cp /etc/asterisk/extensions.conf /etc/asterisk/extensions.conf.backup.$(date +%Y%m%d_%H%M%S)
cp /etc/asterisk/manager.conf /etc/asterisk/manager.conf.backup.$(date +%Y%m%d_%H%M%S)

# Configure Manager Interface (AMI)
print_status "Configuring Asterisk Manager Interface..."
cat > /etc/asterisk/manager.conf << 'EOF'
[general]
enabled = yes
port = 5038
bindaddr = 0.0.0.0

[admin]
secret = password
deny=0.0.0.0/0
permit=127.0.0.1/255.255.255.0
permit=10.0.0.0/255.0.0.0
permit=172.16.0.0/255.240.0.0
permit=192.168.0.0/255.255.0.0
read = all
write = all
EOF

# Configure PJSIP (you'll need to update with your provider details)
print_status "Configuring PJSIP..."
cat > /etc/asterisk/pjsip.conf << 'EOF'
[global]
type=global
debug=yes

[system]
type=system
timer_t1=500
timer_b=32000
disable_tcp_switch=yes

[transport-udp]
type=transport
protocol=udp
bind=0.0.0.0:5060
local_net=10.0.0.0/8
local_net=172.16.0.0/12
local_net=192.168.0.0/16

; SIP Trunk Configuration (REPLACE WITH YOUR PROVIDER DETAILS)
[trunk]
type=endpoint
context=incoming
disallow=all
allow=ulaw
allow=alaw
allow=g729
outbound_auth=auth_trunk
aors=trunk
direct_media=no
force_rport=yes
rewrite_contact=yes
rtp_symmetric=yes
force_avp=yes
ice_support=yes
use_ptime=yes
media_use_received_transport=yes
rtp_timeout=60
rtp_timeout_hold=600
rtp_keepalive=15

[auth_trunk]
type=auth
auth_type=userpass
username=YOUR_USERNAME
password=YOUR_PASSWORD

[trunk]
type=aor
contact=sip:YOUR_PROVIDER_IP:5060
qualify_frequency=60
qualify_timeout=3.0
default_expiration=3600
maximum_expiration=7200
minimum_expiration=60

[trunk]
type=identify
endpoint=trunk
match=YOUR_PROVIDER_IP
EOF

# Configure Extensions
print_status "Configuring Extensions..."
cat > /etc/asterisk/extensions.conf << 'EOF'
[general]
static=yes
writeprotect=no
clearglobalvars=no

[globals]

[incoming]
; Handle incoming calls from SIP trunk
exten => _X.,1,Answer()
 same => n,Wait(1)
 same => n,Playback(hello-world)
 same => n,Wait(1)
 same => n,SayDigits(${CALLERID(num)})
 same => n,Wait(1)
 same => n,Playback(demo-abouttotry)
 same => n,Wait(1)
 same => n,Hangup()

; Handle specific number patterns
exten => 4807868280,1,Answer()
 same => n,Wait(1)
 same => n,Playback(hello-world)
 same => n,Wait(1)
 same => n,Playback(demo-congrats)
 same => n,Wait(1)
 same => n,Hangup()

[internal]
; Internal extensions for testing
exten => 1000,1,Answer()
 same => n,Wait(1)
 same => n,Playback(hello-world)
 same => n,Wait(1)
 same => n,Hangup()

exten => 1001,1,Answer()
 same => n,Wait(1)
 same => n,Playback(demo-congrats)
 same => n,Wait(1)
 same => n,Hangup()

; Outbound dialing (if needed)
exten => _9NXXXXXX,1,Set(CALLERID(num)=${CALLERID(num)})
 same => n,Dial(SIP/trunk/${EXTEN:1})
 same => n,Hangup()

exten => _91NXXNXXXXXX,1,Set(CALLERID(num)=${CALLERID(num)})
 same => n,Dial(SIP/trunk/${EXTEN:1})
 same => n,Hangup()

[default]
; Default context for unhandled calls
exten => s,1,Answer()
 same => n,Wait(1)
 same => n,Playback(invalid)
 same => n,Wait(1)
 same => n,Hangup()
EOF

# Set proper permissions
print_status "Setting permissions..."
chown asterisk:asterisk /etc/asterisk/pjsip.conf
chown asterisk:asterisk /etc/asterisk/extensions.conf
chown asterisk:asterisk /etc/asterisk/manager.conf

# Reload Asterisk configuration
print_status "Reloading Asterisk configuration..."
asterisk -rx "core reload"

# Test configuration
print_status "Testing configuration..."
asterisk -rx "pjsip show endpoints"
asterisk -rx "dialplan show"

print_status "Configuration complete!"
print_warning "IMPORTANT: You need to update /etc/asterisk/pjsip.conf with your SIP trunk provider details:"
print_warning "1. Replace YOUR_USERNAME with your SIP trunk username"
print_warning "2. Replace YOUR_PASSWORD with your SIP trunk password"
print_warning "3. Replace YOUR_PROVIDER_IP with your SIP trunk provider's IP address"
print_warning "4. Update the match parameter with your provider's IP"

print_status "To test the configuration:"
print_status "1. Update pjsip.conf with your provider details"
print_status "2. Run: asterisk -rx 'core reload'"
print_status "3. Run: asterisk -rx 'pjsip show endpoints'"
print_status "4. Make a test call to your number"

echo ""
print_status "Setup complete! Remember to configure your SIP trunk provider details." 