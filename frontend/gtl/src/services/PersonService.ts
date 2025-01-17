import http from "../http-common"
import IPerson from "../types/Person"
const getAll = () => {
    return http.get<Array<IPerson>>("/persons/")
}
// const get = (id: any) => {
//   return http.get<ILocation>(`/locations/${id}`);
// };
// const create = (data: ILocation) => {
//   return http.post<ILocation>("/locations", data);
// };
// const update = (id: any, data: ILocation) => {
//   return http.put<any>(`/locations/${id}`, data);
// };
// const remove = (id: any) => {
//   return http.delete<any>(`/locations/${id}`);
// };
// const removeAll = () => {
//   return http.delete<any>(`/locations`);
// };
// const findByTitle = (title: string) => {
//   return http.get<Array<ILocation>>(`/locations?title=${title}`);
// };
const PersonService = {
    getAll,
    // get,
    // create,
    // update,
    // remove,
    // removeAll,
    // findByTitle,
}
export default PersonService