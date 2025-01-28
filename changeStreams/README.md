# MongoDB Change Stream examples

In order to run the demo you need to have a MongoDB running with a database called `DEMO`, containing two collections named `EBalance` and  `EBalanceHistory` (you can modify this in the code as needed).
The sample code will listen to changes in the `EBalance` collection and saves changes made on documents there into the `EBalanceHistory` collection. Feel free to modify and explore the ChangeStream functionality of MongoDB.

**Getting started:**
- Install NPM packages: `npm install`
- Copy `.env.sample`, change the name to `.env` and update your cluster login information
- run the script: `node documentHistoryCollection.js` -> This will start a changeStream listener waiting for changes on the `EBalance` collection. You can use a debugger if you want to get closer look to what happens to a change event.