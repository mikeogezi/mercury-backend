# Mercury backend

To get this running, open up a shell and execute `sh start_server.sh`. This starts the Flask server that processes image-generation requests.

If you are running this on a host server, you also have to set up ngrok tunnelling. To do that, [install ngrok](https://ngrok.com/download), then execute `sh start_ngrok.sh` in a shell. You will then set the ngrok link you receive in the `HOST` constant in [`src/App.js`](https://github.com/mikeogezi/mercury-ui/blob/master/src/App.js) in [Mercury UI](https://github.com/mikeogezi/mercury-ui). Note that since the ngrok link may change, you may have to change the value of `HOST` multiple times.