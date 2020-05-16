import pickle as pkl
file=pkl.load(open('user_info.dat','rb'))
for each in file:
    print('-------------------')
    print(each)
    print(file[each])
    print('-------------------')