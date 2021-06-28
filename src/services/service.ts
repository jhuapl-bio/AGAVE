import api from "@/services/api"
export default class Service {
    public init(){
        api.get('/api/test')
        .then(response=> (console.log(response)))
    }
    public getData(formData: any){
        api.post('/api/data/json', formData, {
            headers: {
                "Content-Type": `multipart/form-data;`,
        },
        })
        .then(response=> (console.log(response)))
    }
}