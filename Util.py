def driver_location():
    driver_loc=""
    loc=(__file__).split('\\')
    for i in loc[0:len(loc)-1]:
        driver_loc+=i+'/'
    return (driver_loc+'chromedriver.exe')

def sender_msg(inp,a):
    sender_bool=True
    sender_msg = ""
    for i in range(a, len(inp)):
        if(inp[i][0] == '<' and inp[i][-1] == '>'):
            sender_msg += inp[i][1:len(inp[i])-1]+"|||"
        elif(inp[i][0] == '<'):
            sender_msg += inp[i][1:]+" "
        elif(inp[i][-1] == '>'):
            sender_msg += inp[i][0:len(inp[i])-1]+"|||"
        elif(sender_bool):
            sender_msg += inp[i]+" "
    return sender_msg.split('|||')

def filter(data, number):
    content=[]
    data[1]=list(set(data[1]))
    # data[1]=data[::-1]
    # data[1]=data[0:number]
    for msg in data[1]:
        data[2].append(msg.split('\\n')[-1])
        content.append(msg.split('\\n')[-2])

    data[1]=content

    for i in range (0,len(data[2])-1):
        for j in range (i+1,len(data[2])):
            if(data[2][i][-2:0] == 'PM' and data[2][j][-2:0] == 'AM'):
                try:
                    if(int(data[2][i][0:2])>6 and int(data[2][j][0:2])>=12 and int(data[2][j][0])<6):
                        pass
                except:
                    pass
