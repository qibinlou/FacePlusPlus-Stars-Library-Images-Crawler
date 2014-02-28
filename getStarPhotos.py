#!/usr/bin/env python
# -*- coding: utf-8 -*-    
# file getStarPhotos.py 抓取facepp官网明星图片


"""getStarPhotos.py文档
@author: Leo Lou(qibinlou@gmail.com)
@version: 0.1.0
"""

import os
import urllib,urllib2
import sys  
from pprint import pprint
reload(sys)  
sys.setdefaultencoding('utf-8')  


# unify the star names like case '贝克·汉姆'' to '贝克 汉姆'
def unifyName(stars):
    for i in range(len(stars)):
        stars[i] = stars[i].replace('·', ' ')
    return stars

# read in the star list and remove the finished stars
def getStars(filename='stars.txt', donefilename='done.txt'):
    fin = open(filename,'r')
    findone = open(donefilename,'r')
    stars = fin.readlines()
    done = findone.readlines()
    fin.close()
    findone.close()
    for i in range(len(stars)):
        stars[i] = stars[i][:-1]
    for i in range(len(done)):
        done[i] = done[i][:-1]
    stars = list(set(unifyName(stars)))
    done = list(set(done))
    for s in done:
        if s in stars:
            stars.remove(s)
    return stars

# retrieve the star photos and save to local folder
def getStarImage(stars, path='/assets'):
    urlTemplate = 'http://www.faceplusplus.com.cn/assets/demo-img2/%s/%d.jpg'
    pathTemplate = os.getcwd() + path + '/%s/%s-%d.jpg' 
    print pathTemplate
    finishStars = []
    for s in stars:
        index = 1
        while index > 0:
            try:
                url = urlTemplate%(s,index)
                print url
                res = urllib2.urlopen(url)
            except Exception, e:
                # url error like 404 status when image does not exist
                print e
                break
            else:
                filepath = os.getcwd() + path + '/' + s  
                # create a new folder for a new star
                if index == 1 and os.path.exists(filepath) == False:
                    os.mkdir(filepath)
                filepath = pathTemplate%(s,s,index)
                # save the image to seperate folder 
                with open(filepath,'w') as img:
                    img.write(res.read())
                # increase the index to fetch more images of the same star until 404 error                    
                index += 1
        if index > 1:
            finishStars.append(s)
    return finishStars
            

# update the finished star list in order not to fetch their photos next time
def updateFinishStars(finishStars, donefilename='done.txt'):
    findone = open(donefilename,'r')
    done = findone.readlines()
    findone.close()
    for i in range(len(done)):
        done[i] = done[i][:-1]
    done += finishStars
    done = list(set(done))
    foutdone = open(donefilename,'w')
    for s in done:
        foutdone.write(s + '\n')
    foutdone.close()
                                

# main function
def main():
    stars = getStars('stars.txt', 'done.txt')
    finishStars = getStarImage(stars, '/assets')
    updateFinishStars(finishStars, 'done.txt')

if __name__ == '__main__':
    main()




