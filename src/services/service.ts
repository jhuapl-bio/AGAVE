import api from "@/services/api"
export default class Service {
    public init(){
        api.get('/api/test')
        .then(response=> (console.log(response)))
    }
}