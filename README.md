# Mercury backend

The first step to get this running is to install the dependencies specified in `requirements.txt`. You may do so by executing `pip install -r requirements.txt` in a shell.

Next, execute `sh start_server.sh` in the shell to start the Flask server that processes image-generation requests.

If you are running this on a remote server, you also have to set up ngrok tunnelling. To do this, [install ngrok](https://ngrok.com/download), then execute `sh start_ngrok.sh` in a shell. You will then set the ngrok link you receive in the `HOST` constant in [`src/App.js`](https://github.com/mikeogezi/mercury-ui/blob/master/src/App.js) in the [Mercury UI](https://github.com/mikeogezi/mercury-ui). Note that since the ngrok link may change, you may also have to change the value of `HOST`, multiple times.