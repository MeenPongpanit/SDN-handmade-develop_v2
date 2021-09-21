from netmiko import ConnectHandler

def getsn():
    """get SN unique identify of router"""
    inventory_output = ssh.send_command('show inventory') #get inventory output
    outputList = inventory_output.splitlines() #split each line
    #print(inventory_output)
    for line in outputList: #find the line which have SN id
        if "SN" in line:
            inventory_SN_line = str(line).split()
            break
    #print(inventory_SN_line)
    for index in range(len(inventory_SN_line)): #find index of SN the next index will be SN id
        print(inventory_SN_line[index])
        if "SN" in inventory_SN_line[index]:
            print(inventory_SN_line[index + 1])
            return inventory_SN_line[index + 1]
    return "NO_SnID_Found"
            

username = 'cisco'
password = 'cisco'

device_ip = '10.50.34.43'
device_par = {'device_type': 'cisco_ios',
                'ip': device_ip,
                'username': username,
                'password': password,
                }

with ConnectHandler(**device_par) as ssh:
    getsn()
