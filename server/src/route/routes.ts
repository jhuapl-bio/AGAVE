import * as bodyParser from "body-parser";
import * as express from "express";
import { Logger } from "../logger/logger";

class Routes {

    public express: express.Application;
    public logger: Logger;

    // array to hold users
    public users: any[];

    constructor() {
        this.express = express();
        this.middleware();
        this.routes();
        this.logger = new Logger();
    }

    // Configure Express middleware.
    private middleware(): void {
        this.express.use(bodyParser.json());
        this.express.use(bodyParser.urlencoded({ extended: false }));
    }

    private routes(): void {

        // request to get all the users
        this.express.get("/test", (req, res, next) => {
            this.logger.info("url test");
            res.status(200).send({status: 200, message: "Test complete" });
        });

        // request to get all the users by userName
        this.express.get("/users/:userName", (req, res, next) => {
            this.logger.info("url:::::" + req.url);
            const user = this.users.filter(function(user) {
                if (req.params.userName === user.userName) {
                    return user;
                }
            });
            res.json(user);
        });

        // req.body has object of type {firstName:"fnam1",lastName:"lnam1",userName:"username1"}
        this.express.post("/test/:url", (req: any, res: any, next) => {
            this.logger.info("url:::::::" + req.data);
            const data: any = JSON.parse(req.data)
            res.status(200).send("url:::::::" + data);
        });
    }
}

export default new Routes().express;