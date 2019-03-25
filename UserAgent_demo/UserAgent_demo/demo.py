
with open('user_agent.py', 'r') as f:
    for i in f:
        if len(i) > 50:
            
            print(i[i.find(': ')+2:].strip('\n'))


