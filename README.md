# location-spending-time

This repo uses Google Maps Location History and provides how much time one might spent at specific locations such as home, work, and so on.


## Ingredients

- Google Maps Location History. If you enabled Google to keep track your every step (pun intended; Google Fit - step tracker, [wink wink nudge nudge](https://www.youtube.com/watch?v=SrDFGa0juCM)) in the past, you can download it easily [here](https://www.google.com/maps/timeline). As of today, you can click setting button located at bottom right corner. Click "Download copy of your all data" and choose "Location History" in JSON format. Download it. This is our past data.
- places.json. We will fill some locations by getting help from Google Maps. Format should be as follows:

```
{
  "home" : [32.429264, -112.165769],
  "work" : [36.421965, -112.090632] 
}
```

I have to prefer json since it is better not to provide location information carelessly (some irony here). 

## How it works?
- After you downloaded the data, move it the .json file to the same directory where the code is located, and change its name to data.json. 
- Edit your places.json according to the places that you want to learn how much time you spent at.
- Now we're ready to run jupyter notebook. You're in the same directory where the code is located and run this on your terminal: `jupyter notebook`.
- Hopefully the a web browser will automatically open. If not, copy the link you see in the terminal window to your web browser.
- Now you should see a notebook named `Location-Time-Analysis.ipynb`. Open it and run all the code.
- Done.


## Requirements
geopy==1.13.0
pandas=0.22.0
python>=3.6.0

## Author
Osman Baskaya (osmanbaskaya1@gmail.com)
