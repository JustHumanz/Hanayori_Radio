## Hanayori API

### youtube_crawler
https://api.justhumanz.me/hanayori/live/{parameters}

if Authentication request  
user : kano  
pass : kano2525

#### how to use
This api just have 3 parameters  
[now](https://api.justhumanz.me/hanayori/live/now) it's mean show data who's live stream right now  
[upcome](https://api.justhumanz.me/hanayori/live/upcome) show data schedule live  
[last](https://api.justhumanz.me/hanayori/live/last) show all hanayori schedule live in past

and for [last](https://api.justhumanz.me/hanayori/live/last) parameters you can filter with member name,like [kano](https://api.justhumanz.me/hanayori/live/last/kano) or [parerun](https://api.justhumanz.me/hanayori/live/last/parerun)

### twitter scraper
https://api.justhumanz.me/hanayori/twitter/{member}/{limit}  

this api will scraper all tweet with hashtag hanayori member fanart (#鹿乃art,#ひとなーと,#はなまるお絵かき,#ののののえ)

#### how to use
the parameter just hanayori member name and limitation,by default the limitation is 10 tweet   
*update* add all parameter

##### example
```https://api.justhumanz.me/hanayori/twitter/kano```  just 10 tweet  
```https://api.justhumanz.me/hanayori/twitter/kano/100``` 100 tweet will appear

### deployment
For dependency you need firestore and mux

