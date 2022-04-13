import http from "../http-common";
import IGame from "../types/Game";
const getAll = () => {
  return http.get<Array<IGame>>("/statistics/");
};
// const get = (id: any) => {
//   return http.get<ILocation>(`/locations/${id}`);
// };
// const create = (data: ILocation) => {
//   return http.post<ILocation>("/locations", data);
// };
// const update = (id: any, data: ILocation) => {
//   return http.put<any>(`/locations/${id}`, data);
// };
const remove = (url: string) => {
  url = url.replace("/api", "")
  console.log(url)
  return http.delete<string>(url);
};
// const removeAll = () => {
//   return http.delete<any>(`/locations`);
// };
// const findByTitle = (title: string) => {
//   return http.get<Array<ILocation>>(`/locations?title=${title}`);
// };
const GameService = {
  getAll,
  // get,
  // create,
  // update,
  remove,
  // removeAll,
  // findByTitle,
};
export default GameService;