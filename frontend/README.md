Made using [Create-React-App](https://github.com/facebook/create-react-app).

This folder contains the files for rendering the front-end for the application.

# Setup

## Installing `npm`

* [Follow this link](https://tecadmin.net/install-latest-nodejs-npm-on-ubuntu/) to install `npm` (and `node`). You can use the latest release. 
	* A recent installation of `npm` and `node` should suffice.
	* It has been tested that `npm` 6.12.0 and `node` 12.13.0 works.
* Run `npm install` from this folder `./frontend/`.

## Dependencies:
- bootstrap
- react-bootstrap

# Running in developmet

1. Run the flask app from the root folder `./start.sh run` (`./start.sh init-db` if you haven't already)
2. `npm start` from this `frontend/` folder to run the app in the development mode.
3. Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

# Building for production

1. run `npm run build` to compile react files
2. run `serve -l 80 -s build` to run the webserver on [http://localhost:80](http://localhost:80) 
