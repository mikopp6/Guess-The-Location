import http from "../http-common"
import ILocation from "../types/Location"
const getAll = () => {
    return http.get<Array<ILocation>>("/locations/")
}
// const get = (id: any) => {
//   return http.get<ILocation>(`/locations/${id}`);
// };
// const create = (data: ILocation) => {
//   return http.post<ILocation>("/locations", data);
// };
const update = (url: string, image_path: string, country_name: string, town_name: string, person_id: number) => {
    url = url.replace("/api", "")
    const data = {
        "image_path": image_path,
        "country_name": country_name,
        "town_name": town_name,
        "person_id": person_id,
    }
    return http.put<string>(url, data)
}

const remove = (url: string) => {
    url = url.replace("/api", "")
    return http.delete<string>(url)
}
// const removeAll = () => {
//   return http.delete<any>(`/locations`);
// };
// const findByTitle = (title: string) => {
//   return http.get<Array<ILocation>>(`/locations?title=${title}`);
// };
const LocationService = {
    getAll,
    // get,
    // create,
    update,
    remove,
    // removeAll,
    // findByTitle,
}
export default LocationService