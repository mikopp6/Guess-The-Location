import http from "../http-common"
import IGame from "../types/Game"
const getAll = () => {
    return http.get<Array<IGame>>("/statistics/")
}
// const get = (id: any) => {
//   return http.get<ILocation>(`/locations/${id}`);
// };
// const create = (data: ILocation) => {
//   return http.post<ILocation>("/locations", data);
// };
const update = (url: string, player_name: string, score: number, timestamp: string, game_type: number) => {
    url = url.replace("/api", "")
    const data = {
        "player_name": player_name,
        "score": score,
        "timestamp": timestamp,
        "game_type": game_type
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
const GameService = {
    getAll,
    // get,
    // create,
    update,
    remove,
    // removeAll,
    // findByTitle,
}
export default GameService