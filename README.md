# tumblr2pc

tumblr2pc automatically downloads every posts/likes of a tumblr blog.

## Usage

To use tumblr2pc.py you need to obtain a tumblr API key. For info on getting an API key check the section below.

Then run the script like this:

```./tumblr2pc.py blog_name /output/location api_key```

The api_key argument can be a file containing the api key or the key directly.

## Getting an API key

To get an API key you first need to register an "application" on Tumblr [Here](https://www.tumblr.com/oauth/apps).

Then, use your "application" info to get your API key [Here](https://api.tumblr.com/console/calls/user/info).

## Requirements
- youtube-dl

Installing requirements:
- ```pip install youtube-dl```


## Notes

Downloading audio posts is not implemented yet.


## TODO
- implement audio post download
