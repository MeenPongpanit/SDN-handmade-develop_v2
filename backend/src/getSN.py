from netmiko import ConnectHandler

class SSHError(Exception):
    pass

def getsn(device_ip, username = 'cisco', password = 'cisco'):
    """get SN unique identify of router"""
    device_par = {'device_type': 'cisco_ios',
                    'ip': device_ip,
                    'username': username,
                    'password': password,
                    }
    with ConnectHandler(**device_par) as ssh: 
        inventory_output = ssh.send_command('show inventory') #get inventory output
        outputList = inventory_output.splitlines() #split each line
        #print(inventory_output)
        for line in outputList: #find the line which have SN id
            if "SN" in line:
                inventory_SN_line = str(line).split()
                break
        #print(inventory_SN_line)
        for index in range(len(inventory_SN_line)): #find index of SN the next index will be SN id
            # print(inventory_SN_line[index])
            if "SN" in inventory_SN_line[index]:
                # print(inventory_SN_line[index + 1])
                return inventory_SN_line[index + 1]
        raise SSHError()
