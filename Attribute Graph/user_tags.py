
'''
Got all tags the user had tagged
'''

import traceback
import pickle

user_tag = r"D:\2016\Datasets\Attributed Graph Dataset\Delicious Bookmarks\hetrec2011-delicious-2k\user_taggedbookmarks-timestamps.dat"

tags = set()
user_tags = {}

def getUserTags(userTagFile, user_tags):
    flag = True # indicate header line
    with open(user_tag) as f:
        for line in f:
            if flag:
                flag = False
                continue
            data = line.split("\t")
            try:
                user_tags.setdefault(data[0], set()).add(data[2])
                tags.add(int(data[2]))
            except Exception as e:
                print data[2]

getUserTags(user_tag, user_tags)
print len(user_tags)
print len(tags)
print user_tags["8"]
print len(user_tags["8"])

outputFile = r"D:\2016\Datasets\Attributed Graph Dataset\Delicious Bookmarks\hetrec2011-delicious-2k\user_tags.pkl"
output = open(outputFile, 'wb')
pickle.dump(user_tags, output)
output.close()