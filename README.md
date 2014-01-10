# Sheet Everywhere

Miracle Google spreadsheets into JSON so you can use them everywhere.

## Try It

You can try the reference implementation hosted on Heroku at:

> http://sheet-everywhere.herokuapp.com/

Use the key of the spreadsheet (found in the url) to miracle it into a JSON
resource like:

> http://sheet-everywhere.herokuapp.com/0AvtWFMTdBQSLdFI3Y2M0RnI5OTBMa2FydXNFelBDTUE/

And if you need a specific worksheet, add the `gid` as a get parameter:

> http://sheet-everywhere.herokuapp.com/0AvtWFMTdBQSLdFI3Y2M0RnI5OTBMa2FydXNFelBDTUE/?gid=1

The spreadsheet must be publicly accessible.


## Problem[?](http://cl.ly/BG7R/trollface.jpg)

### It's not working!
Sharing permissions must be at least "Anyone who has the link can view". If it still doesn't
show, make sure it's been published. To do that, navigate to File -> Publish to the web...,
and start publishing.

## Developing

Getting started:

```bash
pip install -r requirements.txt
```

See `Procfile` for example of how to run the webserver.

## Deploying to Heroku

Just push this to your Heroku app.

*Optional:* For a redis backed cache, install the [Redis To Go] addon:

```bash
heroku addons:add redistogo:nano
```

  [Redis To Go]: https://addons.heroku.com/redistogo
