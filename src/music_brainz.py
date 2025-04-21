from copy import deepcopy
from random import sample
from time import sleep
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, Any, List
from crate_server.models.artist_query import ArtistQuery
import requests as re
from area import Area, AreaType

BASE_URL = "https://musicbrainz.org/ws/2/"

HEADERS = {
    "User-Agent": "Juke Space/0.1.0 (https://github.com/juke-space)"
}
REQUEST_LIMIT = 100
RESULT_TYPE_MAP = {
    "City": AreaType.MUNICIPALITY,
    "Municipality": AreaType.MUNICIPALITY,
    "Subdivision": AreaType.STATE_PROVINCE,
    "Country": AreaType.COUNTRY
}

def get_artists_by_location(query: ArtistQuery, limit: int = None) -> List[Dict[str, Any]]:
    area = Area(municipality=query.municipality, state_province=query.state_province, country=query.country)
    search_url = _build_search_url("area", "area", area.name)
    session = re.Session()
    session.headers.update(HEADERS)
    artist_data = []
    response = session.get(search_url)
    response_body = response.json()
    if response.status_code != 200:
        raise Exception(f"Error with request: {response_body}")
    area_results = response_body["areas"]

    area_index = 0
    matches_to_find = area.type.value
    match_found = _validate_area(area_results[area_index], area, matches_to_find)
    while not match_found:
        area_index += 1
        match_found = _validate_area(area_results[area_index], area, matches_to_find)

    area_match = area_results[area_index]
    area_id = area_match["id"]
    path_params = ["inc=genres+artist-rels+url-rels", "offset=0"]
    browse_url = _build_browse_url("artist", "area", area_id, deepcopy(path_params))
    browse_response = session.get(browse_url)
    browse_response_body = browse_response.json()
    if browse_response.status_code != 200:
        raise Exception(f"Error with request: {browse_response_body}")

    artist_data.append[browse_response_body]
    if not limit:
        limit = browse_response_body["artist-count"]
    random_offset_limit = limit // REQUEST_LIMIT
    starting_offsets = sample(range(1, random_offset_limit), min(10, random_offset_limit - 1))
    for starting_offset in starting_offsets: # Not threaded to respect API limits
        path_params[-1] = f"offset={starting_offset*REQUEST_LIMIT}"
        browse_url = _build_browse_url("artist", "area", area_id, deepcopy(path_params))
        browse_response = session.get(browse_url)
        browse_response_body = browse_response.json()
        if browse_response.status_code != 200:
            raise Exception(f"Error with request: {browse_response.text}")
        artist_data.append(browse_response_body)
        sleep(0.75) # TODO: Buffer should be made a parameter
        break

    if not artist_data:
        raise ValueError(f"No results found for {area}")
    return artist_data


def parse_artist_from_area(artists: Dict[str, Dict[str, Any]]):
    # will want to multi-thread the processing of each result
    with ThreadPoolExecutor() as pool:
        results = pool.map(_parse_artist_from_area, artists)


def _build_path_params(params: List[str]) -> str:
    # set const. path params
    params.append("fmt=json")
    params.append(f"limit={REQUEST_LIMIT}")
    return "?" + "&".join(params)


def _build_search_url(entity: str, field: str, value: str):
    path_params = [f"query={field}:{value}"]
    return BASE_URL + "/".join([entity, _build_path_params(path_params)])


def _validate_area(result: Dict[str, Any], area: Area, matches_left: int): # TODO: Add a parameter that says where or not all levels have been found. (start with the number to find and decrement)
    result_area_type = RESULT_TYPE_MAP[result["type"]]
    if result_area_type == area.type and \
        area.type == AreaType.COUNTRY and \
            matches_left == AreaType.COUNTRY.value and \
                result["name"].lower() == area.country.lower(): # TODO: Use fuzzy matching, like levenshtein distance
        return True
    elif result_area_type == area.type and \
        area.type == AreaType.STATE_PROVINCE and \
            matches_left == AreaType.STATE_PROVINCE.value and \
                result["name"].lower() == area.state_province.lower():
        matches_left -= 1
        _validate_area(result["rels"], Area(country=area.country), matches_left)
    elif result_area_type == area.type and \
        area.type == AreaType.MUNICIPALITY and \
            matches_left == AreaType.MUNICIPALITY.value and \
                result["name"].lower() == area.municipality.lower():
        # TODO: if the result area type is not something in the map, just move up the chain.
        matches_left -= 1
        _validate_area(result["relation_list"][0]["relations"], Area(state_province=area.state_province, country=area.country), matches_left)
    else:
        return False


def _build_browse_url(entity: str, entity_link: str, entity_id: str, path_params: List[str]):
    path_params.insert(0, f"{entity_link}={entity_id}")
    return BASE_URL + entity + _build_path_params(path_params)


def _parse_artist_from_area(artist: Dict[str, Any]):
    # need to parse out the artist data, genre data, artist_genre combinations, and most easily the raw music brainz data.
    print(artist)
    pass
