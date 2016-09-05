#!/usr/bin/env python

import argparse
import json
import os
import sys
import urllib
import youtube_dl

################################################################
# Arguments parsing and validation
################################################################
parser = argparse.ArgumentParser()
parser.add_argument("TUMBLR_NAME",
                    help="name of the tumblr blog")
parser.add_argument("OUTPUT",
                    help="output location")
parser.add_argument("API_KEY",
                    help="api key or file containing the api key")
parser.add_argument("-s", "--stop-after",
                    help="how much post should be downloaded")
parser.add_argument("-o", "--original_post", action='store_true',
                    help="Do not download reblogged content")
parser.add_argument("-T", "--no-tags", action='store_true',
                    help="Do not download tags")
parser.add_argument("-L", "--likes", action='store_true',
                    help="Download liked posts from the blog")
parser.add_argument("-t", "--text", action='store_true',
                    help="Download only text posts")
parser.add_argument("-q", "--quote", action='store_true',
                    help="Download only quote posts")
parser.add_argument("-l", "--link", action='store_true',
                    help="Download only link posts")
parser.add_argument("-a", "--answer", action='store_true',
                    help="Download only answer posts")
parser.add_argument("-v", "--video", action='store_true',
                    help="Download only video posts using youtube-dl")
parser.add_argument("-m", "--audio", action='store_true',
                    help="Download only audio posts")
parser.add_argument("-p", "--photo", action='store_true',
                    help="Download only photo posts")
parser.add_argument("-c", "--chat", action='store_true',
                    help="Download only chat posts")
args = parser.parse_args()

# Setting download vars
blog_name = args.TUMBLR_NAME
output_dir = args.OUTPUT

# Checking output directory
if not os.path.isdir(output_dir):
        print("Output Directory does not exist..")
        exit(1)

# Creating directory to store this blog posts/likes
if args.likes:
    output_dir = output_dir + "/" + blog_name + "/likes"
else:
    output_dir = output_dir + "/" + blog_name + "/posts"
if not os.path.isdir(output_dir):
        os.makedirs(output_dir)


# Setting API key var
api_key = ""
if os.path.isfile(args.API_KEY):
    api_file = open(args.API_KEY, "r")
    api_key = api_file.readline().strip()
    api_file.close()
else:
    api_key = args.API_KEY

# Setting content type to download
types = {'text': False, 'quote': False, 'link': False, 'answer': False,
         'video': False, 'audio': False, 'photo': False, 'chat': False}

all_false = True
for post_type in types:
    if vars(args)[post_type]:
        types[post_type] = True
        all_false = False

# If no type option is set download everything
if all_false is True:
    for post_type in types:
        types[post_type] = True

################################################################
# Get function for all types of posts
################################################################


def get_photo(api_json, directory, likes_or_posts):
    # Get every image in the post
    for i in api_json["response"][likes_or_posts]:
        for j in i["photos"]:
            filename = str(j["original_size"]["url"].split("/")[-1])
            urllib.urlretrieve(j["original_size"]["url"],
                               directory + "/" + filename)


def get_text(api_json, directory, likes_or_posts):
    # Getting title and body
    for i in api_json["response"][likes_or_posts]:
            title = str(i["title"].encode("utf8"))
            body = str(i["body"].encode("utf8"))

    text_file = open(directory + "/text.txt", 'w')
    text_file.write(title + "\n\n")
    text_file.write(body)
    text_file.close()


def get_quote(api_json, directory, likes_or_posts):
    # Getting text and source
    for i in api_json["response"][likes_or_posts]:
            quote = str(i["text"].encode("utf8"))
            source = str(i["source"].encode("utf8"))

    quote_file = open(directory + "/quote.txt", 'w')
    quote_file.write(quote + "\n")
    quote_file.write("- " + source)
    quote_file.close()


def get_link(api_json, directory, likes_or_posts):
    # Getting text and source
    for i in api_json["response"][likes_or_posts]:
            url = str(i["url"].encode("utf8"))

    url_file = open(directory + "/link.txt", 'w')
    url_file.write(url)
    url_file.close()


def get_answer(api_json, directory, likes_or_posts):
    # Getting question and answer
    for i in api_json["response"][likes_or_posts]:
            question = str(i["question"].encode("utf8"))
            answer = str(i["answer"].encode("utf8"))

    url_file = open(directory + "/answer.txt", 'w')
    url_file.write("Question: " + question + "\n\n")
    url_file.write("Answer: " + answer)
    url_file.close()


def get_video(api_json, directory, likes_or_posts):
    # Change dir so youtube-dl download the video at the right place
    current_dir = os.getcwd()
    os.chdir(directory)

    # Print \r to remove the loading bar before yt-dl output
    print("\r",)

    for i in api_json["response"][likes_or_posts]:
            if 'permalink_url' in i:
                with youtube_dl.YoutubeDL() as ydl:
                    ydl.download([i["permalink_url"]])

    os.chdir(current_dir)


def get_audio(api_json, directory, likes_or_posts):
    print("\rAudio not implemented yet.")


def get_chat(api_json, directory, likes_or_posts):
    for i in api_json["response"][likes_or_posts]:
            title = str(i["title"].encode("utf8"))
            body = str(i["body"].encode("utf8"))

    chat_file = open(directory + "/chat.txt", 'w')
    chat_file.write(title + "\n\n")
    chat_file.write(body)
    chat_file.close()

################################################################
# subs
################################################################


def get_max_post(URL, is_likes):
    api_json = url_to_json(URL)
    if is_likes:
        return api_json["response"]["liked_count"]
    else:
        return api_json["response"]["total_posts"]


def get_post_id(api_json, likes_or_posts):
    for i in api_json["response"][likes_or_posts]:
        return str(i["id"])


def get_post_type(api_json, likes_or_posts):
    for i in api_json["response"][likes_or_posts]:
        return i["type"]


def get_tags(api_json, directory, likes_or_posts):
    for i in api_json["response"][likes_or_posts]:
        tags = i["tags"]

    chat_file = open(directory + "/tags.txt", 'w')
    for tag in tags:
        chat_file.write("{0}\n".format(tag.encode("utf8")))
    chat_file.close()


def is_original(api_json, likes_or_posts):
    for i in api_json["response"][likes_or_posts]:
            if "reblogged_from_id" in i:
                return False
            else:
                return True


def url_to_json(URL):
    return json.loads(urllib.urlopen(URL).read())

################################################################
# Main
################################################################


def main():
    # Checking if we are downloading likes or post
    likes_or_posts = ""
    base_url = ""
    if args.likes:
        likes_or_posts = "liked_posts"
        base_url = "http://api.tumblr.com/v2/blog/" + blog_name +\
                   "/likes?api_key=" + api_key +\
                   "&filter=text&reblog_info=true&limit=1&offset="
    else:
        likes_or_posts = "posts"
        base_url = "http://api.tumblr.com/v2/blog/" + blog_name +\
                   "/posts?api_key=" + api_key +\
                   "&filter=text&reblog_info=true&limit=1&offset="

    # Checking how much posts/likes to downloads
    max_post = get_max_post(base_url + "0", args.likes)
    if args.stop_after:
        if args.stop_after < max_post:
            max_post = args.stop_after

    # Download loop
    for x in range(0, max_post):
        api_json = url_to_json(base_url + str(x))
        post_type = get_post_type(api_json, likes_or_posts)
        post_id = get_post_id(api_json, likes_or_posts)
        directory = output_dir + '/' + post_id + "/"

        # Posts are only downloaded if their directory does not exist
        # to prevent redownloading them.

        if args.original_post:
            if is_original(api_json, likes_or_posts) and types[post_type]:
                    if not os.path.isdir(directory):
                        os.makedirs(directory)
                        try:
                            globals()["get_" + post_type](api_json,
                                                          directory,
                                                          likes_or_posts)
                            if not args.no_tags:
                                get_tags(api_json, directory, likes_or_posts)
                        except:
                            print("Error downloading {0}".format(post_id))
                            pass
        else:
            if types[post_type]:
                if not os.path.isdir(directory):
                    os.makedirs(directory)
                    try:
                        globals()["get_" + post_type](api_json,
                                                      directory,
                                                      likes_or_posts)
                        if not args.no_tags:
                            get_tags(api_json, directory, likes_or_posts)
                    except:
                        print("Error downloading {0}".format(post_id))
                        pass

        # Code for percentage printing
        percentage = int(float(x) / float(max_post) * 100)
        sys.stdout.write("\r[" + '#'*(percentage/10) +
              ' '*(10 - percentage/10) + "]" + str(percentage) + "%")

        sys.stdout.flush()

    sys.stdout.write("\r[##########]100%")
    sys.stdout.flush()
    print("Done!")

main()
