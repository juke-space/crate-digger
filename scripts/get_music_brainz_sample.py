from typing import List
from random import sample
from copy import deepcopy
from time import sleep
import requests as re
import json
import pathlib


BASE_URL = "https://musicbrainz.org/ws/2/"

HEADERS = {
    "User-Agent": "Juke Space/0.1.0 (https://github.com/kosmic-link)"
}

AREAS = ["Connecticut", "Vermont", "Massachusetts"]
COUNTRY = "United States"
LIMIT = 100
session = re.Session()
session.headers.update(HEADERS)

def _build_path_params(params: List[str]) -> str:
    # set const. path params
    params.append("fmt=json")
    params.append(f"limit={LIMIT}")
    return "?" + "&".join(params)

def _build_search_url(entity: str, field: str, value: str):
    path_params = [f"query={field}:{value}"]
    return BASE_URL + "/".join([entity, _build_path_params(path_params)])

def _build_browse_url(entity: str, entity_link: str, entity_id: str, path_params: List[str]):
    path_params.insert(0, f"{entity_link}={entity_id}")
    return BASE_URL + entity + _build_path_params(path_params)


if __name__ == "__main__":
    artist_data = {area: {} for area in AREAS}
    for area in AREAS:
        print(f"Getting Artists for {area}...")
        search_url = _build_search_url("area", "area", area)
        response = session.get(search_url)
        response_body = response.json()
        if response.status_code != 200:
            raise Exception(f"Error with request: {response_body}")
        area_results = response_body["areas"]
        print(f"Number of Area Results: {len(area_results)}")
        for area in area_results:
            if area["relation-list"][0]["relations"][0]["area"]["name"] != COUNTRY:
                continue
            area_id = area["id"]
            path_params = ["inc=genres+artist-rels", "offset=0"]
            browse_url = _build_browse_url("artist", "area", area_id, deepcopy(path_params))
            browse_response = session.get(browse_url)
            browse_response_body = browse_response.json()
            if browse_response.status_code != 200:
                raise Exception(f"Error with request: {browse_response_body}")
            response_bodies = [browse_response_body]
            total_artists = browse_response_body["artist-count"]
            print(f"Total number of artists: {total_artists}")
            random_offset_limit = total_artists  // LIMIT
            starting_offsets = sample(range(1, random_offset_limit), min(10, random_offset_limit - 1))
            for starting_offset in starting_offsets:
                path_params[-1] = f"offset={starting_offset*LIMIT}"
                print(starting_offset)
                browse_url = _build_browse_url("artist", "area", area_id, deepcopy(path_params))
                browse_response = session.get(browse_url)
                try:
                    browse_response_body = browse_response.json()
                except re.exceptions.JSONDecodeError:
                    print(browse_url)
                if browse_response.status_code != 200:
                    raise Exception(f"Error with request: {browse_response.text}")
                response_bodies.append(browse_response_body)
                sleep(0.75)
            artist_data[area["name"]] = response_bodies
    data_path = pathlib.Path("data", "artist_sample.json")
    data_path.parent.mkdir(parents=True, exist_ok=True)
    with open(data_path, "w") as f:
        json.dump(artist_data, f, indent=4, ensure_ascii=True)
