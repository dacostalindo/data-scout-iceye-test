This code aims to scrape all of the data from the given link provided. It creates a JSON file for every AreaCode and Code with available data. 

We could run periodically this using either a daemon or cronjob to ensure that any changes to the registered levels are update with our data pipelines. The data available on the website seems to date back only an hour/couple of minutes from time of our post request, thus, it seems prudent to store historical data in our cloud servers. 

I would store this data possibly in a data lake or other similar format, despite my relative unfamiliarity with the subject just mentioned. 