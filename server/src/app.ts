import * as bodyParser from "body-parser";
import * as express from "express";
import { Logger } from "./logger/logger";
import Routes from "./route/routes";
const path = require('path');
let multer  = require('multer');

class App {

    public express: express.Application;
    public logger: Logger;

    // array to hold users
    public users: any[];

    constructor() {
        this.express = express();
        this.middleware();
        this.routes();
        this.users = [];
        this.logger = new Logger();
    }

    // Configure Express middleware.
    private middleware(): void {
        this.express.use(bodyParser.json());
        this.express.use(bodyParser.urlencoded({ extended: true }));
        // this.express.use(express.static(process.cwd() + "/my-app/dist/"));
    }

    private routes(): void {

        this.express.get("/", (req, res, next) => {
            res.send("At the home!");
            // res.sendFile(process.cwd() + "/my-app/dist/index.html");
        });

        // user route
        this.express.use("/api", Routes);
        this.express.use((req, res, next) => {
            res.setHeader('Access-Control-Allow-Origin', '*');
            res.setHeader('Access-Control-Allow-Methods', 'GET, POST, DELETE, PUT, PATCH, OPTIONS');
            res.setHeader('Access-Control-Allow-Headers', 'Content-Type, api_key, Authorization'); 
            res.setHeader('Access-Control-Expose-Headers', 'Content-Range');
        }); 
        this.express.use(multer)
        // handle undefined routes
        this.express.use("*", (req, res, next) => {
            res.send("Make sure url is correct!");
        });
    }
}

export default new App().express;