import * as bodyParser from "body-parser";
import * as express from "express";
import { Logger } from "../logger/logger";
import * as fs from 'fs';


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

        this.express.post("/data/:type", (req: any, res: any, next) => {
            this.logger.info("testing data type: " + req.params.type);
            this.logger.info(req.files)
            this.logger.info(`${Object.keys(req.body)}`)
            res.status(200).send("url:::::::" );
            fs.readFile(req.body, function(err: any, data: any){
                if (err){
                    this.logger.console.error(err);
                    res.status(419).send(err)
                } else {
                    const jsondata: any = JSON.parse(data)
                    this.logger.info("data" + req.body);
                    res.status(200).send("url:::::::" );        
                }
            })
            // res.status(200).send("url:::::::" );  
        })
    }
}

export default new Routes().express;