data=''
for i in range(100000000):
    data+='THIS IS A TEST '
    if i%5==0:
        data+='\n'


with open('longFileTest.txt', 'w') as f:
    f.write(data)
f.close()