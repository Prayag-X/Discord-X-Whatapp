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

    for msg in data[1]:
        data[2].append(msg.split('\n')[-1])
        content.append(msg.split('\n')[-2])

    data[1]=content

    for i in range (len(data[2])-1,-1,-1):
        for j in range (0,i):
            if(data[2][j+1][-2:] == 'PM' and data[2][j][-2:] == 'AM'):
                try:
                    if(int(data[2][j+1][0:2])>6 and int(data[2][j][0:2])>=12 and int(data[2][j][0])<6):
                        data[1][j], data[1][j+1] = data[1][j+1], data[1][j]
                        data[2][j], data[2][j+1] = data[2][j+1], data[2][j]
                except:
                    data[1][j], data[1][j+1] = data[1][j+1], data[1][j]
                    data[2][j], data[2][j+1] = data[2][j+1], data[2][j]

            else:
                try:
                    d1=int(data[2][j+1][0:2])
                except:
                    d1=int(data[2][j+1][0])

                try:
                    d2=int(data[2][j][0:2])
                except:
                    d2=int(data[2][j][0])

                if(d2>d1):
                    data[1][j], data[1][j+1] = data[1][j+1], data[1][j]
                    data[2][j], data[2][j+1] = data[2][j+1], data[2][j]

    data[1]=data[1][-number:]
    data[2]=data[2][-number:]

    return data