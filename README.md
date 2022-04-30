pyoverlander

Collect location data from the "Overland GPS TRacker" app  and put it in a sqlite file.
https://github.com/aaronpk/Overland-iOS

Run the app:
main.py takes 2 inputs:
	STDIN: The very first line will be the TOKEN, all other stdin is ignored
	1 argument: location of the db file

While running, it will always listen on localhost on port 8080 (submit a PR if you don't like it)
	(I'd recommend a config table in the DB and pull the listen information from that table)

```shell
echo "MYTOKEN" | python3 main.py mydata.db
```

In production, you probably don't want to use echo, you can cat a special private file, or use your password manager to export the token to stdout and pipe it in, whatever you want.

exposed via nginx in /etc/nixos/configuration.nix like this:
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


url: https://example.com/overland/

URL for overland app:
    https://example.com/overland/submit?token=happy

    or for auto setup(should work):
    overland://setup?url=https%3A%2F%2Fexample.come%2Foverland%2Fsubmit&token=happy&device_id=ziephone

Interesting Queries:
    select timestamp,x,y,json_extract(properties,"$.battery_level") from locations;

Docs/urls
 * bottle docs: https://bottlepy.org/docs/0.12/
 * Overland iOS App: https://github.com/aaronpk/Overland-iOS#api
 * Sqlite:
    * json docs: https://sqlite.org/json1.html
