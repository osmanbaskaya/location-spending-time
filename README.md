# location-spending-time

This repo uses Google Maps Location History and provides how much time one might spent at specific locations such as home, work, and so on.


## Ingredients

- Google Maps Location History. If you enabled location history in the past, you can download it easily [here](https://www.google.com/maps/timeline). As of today, you can click setting button located at bottom right corner. Click "Download copy of your all data" and choose "Location History" in JSON format. Download it. This is our past data.
- places.json. We will fill some locations by getting help from Google Maps. Format should be as follows:

```
{
  "home" : [32.429264, -112.165769],
  "work" : [36.421965, -112.090632] 
}
```

I have to prefer json since it is better not to provide location information carelessly (some irony here). 

## How it works?


## Requirements
It is tested on Python 3.6

## Author
Osman Baskaya (osmanbaskaya1@gmail.com)
