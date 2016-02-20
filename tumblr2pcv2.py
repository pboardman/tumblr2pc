#!/usr/bin/env python

import argparse
import json
import os
import sys
import urllib

################################################################
# Arguments parsing and validation
################################################################
parser = argparse.ArgumentParser()

parser.add_argument("tumblr_name", help="name of the tumblr blog")
parser.add_argument("output", help="output location")
parser.add_argument("api_key", help="api key or file containing the api key")
parser.add_argument("-s", "--stop_after", help="how much post should be downloaded")
parser.add_argument("-o", "--original_post", action='store_true', help="Do not download reblogged content")
parser.add_argument("-t", "--text", action='store_true', help="Download only text posts")
parser.add_argument("-q", "--quote", action='store_true', help="Download only quote posts")
parser.add_argument("-l", "--link", action='store_true', help="Download only link posts")
parser.add_argument("-a", "--answer", action='store_true', help="Download only answer posts")
parser.add_argument("-v", "--video", action='store_true', help="Download only video posts using youtube-dl (experimental)")
parser.add_argument("-m", "--audio", action='store_true', help="Download only audio posts")
parser.add_argument("-p", "--photo", action='store_true', help="Download only photo posts")
parser.add_argument("-c", "--chat", action='store_true', help="Download only chat posts")
args = parser.parse_args()

# Setting download vars
blog_name = args.tumblr_name
output_dir = args.output

# Checking output directory
if not os.path.isdir(output_dir):
    print "Output Directory does not exist.."
    exit(1)
if output_dir.endswith('/'):
  output_dir = output_dir[:-1]

# Setting API key var
api_key = ""
if os.path.isfile(args.api_key):
  api_file = open(args.api_key,"r")
  api_key = api_file.readline().strip()
  api_file.close()
else:
  api_key = args.api_key

# Setting content type to download
types = {'text': False, 'quote': False, 'link': False, 'answer': False,
         'video': False, 'audio': False, 'photo': True, 'chat': False} # switch photo to false when arguments work

### TEMPORARILY DISABLED

#all_false=True
#for post_type in types:
  #if args.post_type:
    #types[post_type] = True
    #all_false=False

# If no type option is set download everything
#if all_false is True:
 # for post_type in types:
#    types[post_type] = True

################################################################
# get function for all types of posts
################################################################
def get_photo(api_json, directory): #pic_url, directory
  output = output_dir + '/' + directory + "/" #+ str(pic_url.split("/")[-1])

  # Create directory
  if not os.path.isdir(output):
      os.makedirs(output)
  # Get every image in the post
  for i in api_json["response"]["posts"]:
    for j in i["photos"]:
      filename = str(j["original_size"]["url"].split("/")[-1])
      urllib.urlretrieve(j["original_size"]["url"], output + filename)

def get_text(): #title, body, directory
  text_file = open(directory + "/text.txt", 'w')
  text_file.write(title + "\n\n")
  text_file.write(body)
  text_file.close()

def get_quote(): #quote, source, directory
  quote_file = open(directory + "/quote.txt", 'w')
  quote_file.write(quote + "\n")
  quote_file.write("- " + source)
  quote_file.close()

def get_link(): #url, directory
  url_file = open(directory + "/url.txt", 'w')
  url_file.write(url)
  quote_file.close()

def get_answer(): #???, directory
  print "Answer not implemented yet."

def get_video(): #url, directory
  #Use youtube-dl to get videos
  print "Video not implemented yet."

def get_audio(): # ???, directory
  print "Audio not implemented yet."

def get_chat(): # title, body, directory
  chat_file = open(directory + "/chat.txt", 'w')
  chat_file.write(title + "\n\n")
  chat_file.write(body)
  chat_file.close()

################################################################
# subs
################################################################
def get_max_post(URL):
  api_json = url_to_json(URL)
  return api_json["response"]["total_posts"]

def get_post_id(api_json):
  for i in api_json["response"]["posts"]:
    return str(i["id"])

def get_post_type(api_json):
  for i in api_json["response"]["posts"]:
    return i["type"]

def is_original(api_json): # maybe with the state variable
  # TODO
  return True

def url_to_json(URL):
  return json.loads(urllib.urlopen(URL).read())

################################################################
# Main
################################################################
def main():
  # Setting the max post to get
  base_url = "http://api.tumblr.com/v2/blog/"+ blog_name +"/posts?api_key="+ api_key + "&filter=text&limit=1&offset="
  max_post = get_max_post(base_url + "0")

  if args.stop_after:
    if args.stop_after < max_post:
      max_post = args.stop_after

  # Download loop
  for x in range(0, max_post):
    api_json = url_to_json(base_url + str(x))
    post_type = get_post_type(api_json)
    post_id = get_post_id(api_json)

    if args.original_post:
      if is_original(api_json) and types[post_type]:
        globals()["get_" + post_type](api_json, post_id)
    else:
      if types[post_type]:
        globals()["get_" + post_type](api_json, post_id)

main()
