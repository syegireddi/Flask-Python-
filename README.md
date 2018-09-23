# Data Engineer Task

For this assignement you have to process one file and enrich it with data provided by an API, in order to provide high level aggregate info.

The goal is to see how you implement the missing parts of the API, and how you deal with file processing and data structures manipulation.


## Description

### API

There two endpoints that need to be implemented, one that searches for the user_status on a given date,
and another one that returns a city based on IP provided.


`/user_status/<user_id>?date=2017-10-10T10:00:00`
On this endpoint, please provide an implementation that searches the records and based on the date, returns the correct user status at that time.
In case there's no status available for a given date, simply return non-paying.
The valid statuses that should be provided are: paying, canceled or non-paying.

`/ip_city/10.0.0.0`
On this endpoint, please provide an implementation that searched the IP ranges provided, and based on the IP, returns the correct city.
In case IP range is not within any of the provided cities, **unknown** should be provided.

### File Processing

Here you need to read the file provided, `transactions.json`, and enrich it with the data provided by the API.
The output of the script should provide an aggregate containing the sum of `product_price`, grouped by user_status and city.

## Setup
There's a simple API which you'll need, to install it simply use pip.
To run the API, simply run the api.py file.

```
pip install -r requirements.txt
python api.py
```




### Delivery
Please provide a zip or tar file containing the complete implementation.