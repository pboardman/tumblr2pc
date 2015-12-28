#!/usr/bin/env python

import argparse
import urllib
import sys
import xml.etree.ElementTree as ET

# argument parser
parser = argparse.ArgumentParser()

parser.add_argument("tumblr_URL", help="URL of the tumblr blog")
parser.add_argument("output", help="output location")
parser.add_argument("-l", "--limit", help="how much post should be downloaded")
args = parser.parse_args()

URL = args.tumblr_URL.replace("http://","")
output_dir = args.output

if output_dir.endswith('/'):
  output_dir = output_dir[:-1]

if args.limit:
  img_limit = int(args.limit)
else:
  img_limit = -1

def get_picture(pic_url):
  output = output_dir+'/'+ str(pic_url.split("/")[-1])
  urllib.urlretrieve(pic_url, output)

def max_post():
  # getting max post number
  xml_str = urllib.urlopen("http://"+ URL + "/api/read?type=photo&num=1&start=" + '0').read()
  root = ET.fromstring(xml_str)

  for child in root:
      if child.tag == 'posts':
        max_post_nb = child.get('total')
        break

  return max_post_nb

def main():
  print "Downloading.."

  max_post_nb = int(max_post())
  img_nb=0

  while 1:

    xml_str = urllib.urlopen("http://" + URL + "/api/read?type=photo&num=1&start=" + str(img_nb)).read()
    root = ET.fromstring(xml_str)

    # checking if there is more than one picture in the post
    photoset=False
    for neighbor in root.iter('photoset'):
      photoset = True

    # getting the picture
    if not photoset:
      for photo_url in root.findall('posts/post/photo-url'):
        if photo_url.get('max-width') == '1280':
          get_picture(photo_url.text)
    else:
      for photo_url in root.findall('posts/post/photoset/photo/photo-url'):
        if photo_url.get('max-width') == '1280':
          get_picture(photo_url.text)

    img_nb+=1

    # printing progress
    if args.limit:
      current_percentage = int(float(img_nb) / float(img_limit) * 100)
    else:
      current_percentage = int(float(img_nb) / float(max_post_nb) * 100)


    print '\r[{0}{1}] {2}%'.format('#'*(current_percentage/10),' '*(10 - current_percentage/10) , current_percentage),
    sys.stdout.flush()

    # stop when all post have been checked
    if img_nb == max_post_nb or img_nb == img_limit:
      print "\nDone!"
      break


main()
