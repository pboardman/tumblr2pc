# tumblr2pc

tumblr2pc automatically downloads every posts of a tumblr blog.

## Usage

To use tumblr2pc.py you need to obtain a tumblr API key, for info on getting an API key check the section below.

Then run the script like this:

```./tumblr2pc.py blog.tumblr.com /output/location api_key```

## Getting an API key

To get an API key you first need to register an "application" on Tumblr [Here](https://www.tumblr.com/oauth/apps).

Then, use your "application" info to get your API key [Here](https://api.tumblr.com/console/calls/user/info).

## Requirements
- youtube-dl

Installing requirements:
- ```pip install youtube-dl```


## Notes

Downloading audio and answer post is not implemented yet.


## TODO
- implement audio post download
- implement answer post download
- loading bar ( [===   ]50% )
- Download likes
