# pyoverlander

Collect location data from the "Overland GPS Tracker" app  and put it in a sqlite file.
Requires python3, no other dependencies(uses bottle, included).

https://github.com/aaronpk/Overland-iOS

Run the app:
main.py takes 2 inputs:
 * STDIN: The very first line will be the TOKEN, all other stdin is ignored
 * 1 argument: location of the db file

While running, it will always listen on localhost on port 8080 (submit a PR if you don't like it)
	(I'd recommend a config table in the DB and pull the listen information from that table)
## DB setup

Create the necessary tables:
```shell
./main.py newdb mydata.db
sqlite3 mydata.db 
insert into tokens (token,email,valid,device_id,extra,note) VALUES ('mytoken','me@example.com',1,'myphone','{}','token for my iphone');
.quit
```

A decent way to generate a token:
```shell
# generate a ~ 64 character token, the arguably sane max
python3 -c 'import secrets;print(secrets.token_urlsafe(48))'
```

# Run the application:
```shell
python3 main.py mydata.db
```

This code requires bottle.py, you can just shove the file in the same dir or you can install it via pip or whatever.

you also probably want to proxy the HTTP via a HTTPS proxy, I do it via nginx in /etc/nixos/configuration.nix like this:
```nix
        virtualHosts."example.com" = {
                addSSL = true;
                useACMEHost = "example.com";
                root = "/var/www/www.example.com";
                locations."/overland/" = {
                        proxyPass = "http://localhost:8080";
                };
        };
```
or for non nix, passing through a proxy is your problem :) Though I accept pull requests to add more.

NOTE: right now it's hardcoded to /overland/, so be sure to include that in the requests. (PR's accepted)


url: https://example.com/overland/

URL for overland app:
    https://example.com/overland/submit?token=happy

    or for auto setup(should work):
    overland://setup?url=https%3A%2F%2Fexample.come%2Foverland%2Fsubmit&token=happy&device_id=myphone

Interesting Queries:
    select timestamp,lat,long,json_extract(properties,"$.battery_level") from locations;

Docs/urls
 * bottle docs: https://bottlepy.org/docs/0.12/
 * Overland iOS App: https://github.com/aaronpk/Overland-iOS#api
 * Sqlite:
    * json docs: https://sqlite.org/json1.html
