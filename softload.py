import os

def block_all():
    try:
        os.system("netsh advfirewall set allprofiles firewallpolicy blockinbound,blockoutbound")
    except:
        pass
