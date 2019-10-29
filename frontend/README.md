Made using [Create-React-App](https://github.com/facebook/create-react-app).

# Installing `npm`

* [Follow this link](https://tecadmin.net/install-latest-nodejs-npm-on-ubuntu/) to install `npm`. You can use the latest release. `npm -v` gives Emily 6.12.0
* Run `npm install`

# Running in dev
1. Run the flask app from the root folder `./start.sh run` (`./start.sh init-db` if you haven't already)
2. `npm start` from this `frontend/` folder to run the app in the development mode.
3. Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

Dependencies:
- bootstrap
- react-bootstrap

# Building for prod 

run `npm run build` to compile react files
run `serve -l 80 -s build` to run the webserver on [http://localhost:80](http://localhost:80) 
