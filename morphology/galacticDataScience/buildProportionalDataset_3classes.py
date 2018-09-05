import sys
import pandas as pd

# read input lists
ls_E  = pd.read_csv(sys.argv[1], header=None, names=['fileId'])
ls_S  = pd.read_csv(sys.argv[2], header=None, names=['fileId'])
ls_SB = pd.read_csv(sys.argv[3], header=None, names=['fileId'])

print len(ls_E)
print len(ls_S)
print len(ls_SB)

# get proportions
sample_E  =  ls_E.sample(100)  #  2000
sample_S  =  ls_S.sample(8000)  #  8000
sample_SB = ls_SB.sample(10000) # 10000

E_path  = '/DL_data/GZ2/k10/imgs/3classes/E/'
S_path  = '/DL_data/GZ2/k10/imgs/3classes/S_/'
SB_path = '/DL_data/GZ2/k10/imgs/3classes/SB_/'

sample_E['fileId']  = E_path  +  sample_E['fileId'].astype(str) + ' 0'
sample_S['fileId']  = S_path  +  sample_S['fileId'].astype(str) + ' 2'
sample_SB['fileId'] = SB_path + sample_SB['fileId'].astype(str) + ' 1'

print 'E:'
print len(sample_E)
print sample_E.head(n=5)
print ''

print 'S:'
print len(sample_S)
print sample_S.head(n=5)
print ''

print 'SB:'
print len(sample_SB)
print sample_SB.head(n=5)
print ''

# concatenate dfs into 1 df and print to file
# final = E + SB_ + S_
# whole = sample_E.append([sample_SB, sample_S])
# print 'whole'
# print len(whole)
# print whole
# print ''
# whole.to_csv(sys.argv[4], index=False, header=None)

# training = 80%; val = 10%; test = 10%
train_E  =  sample_E.sample(frac=0.8,random_state=200)
train_S  =  sample_S.sample(frac=0.8,random_state=200)
train_SB = sample_SB.sample(frac=0.8,random_state=200)

# print 'train_E'
# print len(train_E)
# print train_E
# print ''

# print 'train_S'
# print len(train_S)
# print train_S
# print ''

# print 'train_SB'
# print len(train_SB)
# print train_SB
# print ''

validation_E  =  sample_E.drop(train_E.index).sample(frac=0.5,random_state=200)
validation_S  =  sample_S.drop(train_S.index).sample(frac=0.5,random_state=200)
validation_SB = sample_SB.drop(train_SB.index).sample(frac=0.5,random_state=200)

# print 'validation_E'
# print len(validation_E)
# print validation_E
# print ''

# print 'validation_S'
# print len(validation_S)
# print validation_S
# print ''

# print 'validation_SB'
# print len(validation_SB)
# print validation_SB
# print ''

test_E  =  sample_E.drop(train_E.index).drop(validation_E.index)
test_S  =  sample_S.drop(train_S.index).drop(validation_S.index)
test_SB = sample_SB.drop(train_SB.index).drop(validation_SB.index)

# print 'test_E'
# print len(test_E)
# print test_E
# print ''

# print 'test_S'
# print len(test_S)
# print test_S
# print ''

# print 'test_SB'
# print len(test_SB)
# print test_SB
# print ''

# VERIFY!!!

train = train_E.append([train_SB, train_S])
print 'train'
print len(train)
print train
print ''
train.to_csv(sys.argv[4], index=False, header=None)

validation = validation_E.append([validation_SB, validation_S])
print 'validation'
print len(validation)
print validation
print ''
validation.to_csv(sys.argv[5], index=False, header=None)

test = test_E.append([test_SB, test_S])
print 'test'
print len(test)
print test
print ''
test.to_csv(sys.argv[6], index=False, header=None)