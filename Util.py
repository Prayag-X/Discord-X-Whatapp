def util1(inp,a):
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
    return sender_msg