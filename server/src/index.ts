import * as http from "http";
import App from "./app";
import { Logger } from "./logger/logger";

const port: number = 3089;

App.set("port", port);
const server = http.createServer(App);
server.listen(port, () => {
    logger.info(`Example app listening at http://localhost:${port}`)
})
const logger = new Logger();
server.on("listening", function(): void {
    logger.info(`port: ${port}`)
    const addr: any= server.address();
    const bind = (typeof addr === "string") ? `pipe ${addr}` : `port ${addr.port}`;
    logger.info(`Listening on ${bind}`);
 });

module.exports = App;