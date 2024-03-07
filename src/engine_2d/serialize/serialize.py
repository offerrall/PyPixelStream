from typing import TYPE_CHECKING
from json import dump, load
from os.path import exists

from ..sources import get_source_type_list
from ..filters import get_filters_list

if TYPE_CHECKING:
    from ..filter import Filter
    from ..source import Source
    from ..scene import Scene

def save_scene_to_file(scene_name: str,
                       scene_internal_id: str,
                       scene_order: int,
                       sources: list,
                       filters: list,
                       path_to_save: str) -> None:
    """Save the scene as a json file compatible with dict_to_source() and dict_to_filter() functions"""
    filters = [filter_to_dict(filter) for filter in filters]
    
    scene_dict = {"name": scene_name,
                    "internal_id": scene_internal_id,
                    "order": scene_order,
                    "filters": filters,
                    "sources": [source_to_dict(source) for source in sources]}

    path_to_file = f"{path_to_save}/{scene_internal_id}.json"
    with open(path_to_file, 'w') as file:
        dump(scene_dict, file, indent=4)

def load_scene_from_file(scene_name: str, path_to_save: str) -> dict:
    """Load and return the sources from a json file compatible with dict_to_source() and dict_to_filter() functions"""
    path_to_file = f"{path_to_save}/{scene_name}.json"
    if not exists(path_to_file):
        raise FileNotFoundError(f"File '{scene_name}.json' not found")
    
    with open(path_to_file, 'r') as file:
        scene_data = load(file)

    scene_dict = {"name": scene_data["name"],
                    "internal_id": scene_data["internal_id"],
                    "order": scene_data["order"],
                    "filters": [],
                    "sources": []}

    for filter_dict in scene_data["filters"]:
        filter = dict_to_filter(filter_dict)
        scene_dict["filters"].append(filter)
    
    for source_dict in scene_data["sources"]:
        source = dict_to_source(source_dict)
        scene_dict["sources"].append(source)
    
    return scene_dict

def filter_to_dict(filter_obj: 'Filter') -> dict:
    """Return a dictionary with the filter properties"""
    filter_type = filter_obj.__class__.__name__
    properties_internal = ['visible']
    return {
        "type": filter_type,
        "name": filter_obj.name,
        "order": filter_obj.order,
        "is_visible": filter_obj.is_visible,
        "properties": {key: value for key, value in filter_obj.properties.items() if key not in properties_internal}
    }

def source_to_dict(source: 'Source') -> dict:
    """Return a dictionary with the source properties"""
    filters_list = [filter_to_dict(f) for f in source.filters.filters]
    properties_internal = ['width', 'height', 'position', 'visible', 'selectable', 'selected']

    return {
        "type": source.__class__.__name__,
        "name": source.name,
        "order": source.order,
        "width": source.width,
        "height": source.height,
        "x": source.x,
        "y": source.y,
        "is_visible": source.is_visible,
        "is_selectable": source.is_selectable,
        "filters": filters_list,
        "properties": {key: value for key, value in source.properties.items() if key not in properties_internal}
    }

def dict_to_filter(filter_dict: dict) -> 'Filter':
    """Return a filter object from a dictionary"""
    filter_type = filter_dict["type"]
    basic_dict = {"order": filter_dict["order"],
                  "name": filter_dict["name"]}
    
    for key, value in filter_dict["properties"].items():
        basic_dict[key] = value
    
    filter_list = get_filters_list()

    for key, value in filter_list.items():
        invalids_properties = []
        if value.__name__ == filter_type:
            # while is necessary because some properties are not required
            while True:
                try:
                    basic_dict = {key: value for key, value in basic_dict.items() if key not in invalids_properties}
                    filter: 'Filter' = value(**basic_dict)
                    break
                except TypeError as e:
                    formated = str(e).split(" ")[-1].replace("'", "") # get the property name from the error message
                    invalids_properties.append(formated)
    
    filter.set_visible(filter_dict["is_visible"])
    return filter


def dict_to_source(source_dict: dict) -> 'Source':
    """Return a source object from a dictionary"""
    source_type = source_dict["type"]
    basic_dict = {"order": source_dict["order"],
                  "name": source_dict["name"],
                  "width": source_dict["width"],
                  "height": source_dict["height"]}
    
    for key, value in source_dict["properties"].items():
        basic_dict[key] = value
    
    source_list = get_source_type_list()

    for key, value in source_list.items():
        
        invalids_properties = []
        if value.__name__ == source_type:
            # while is necessary because some properties are not necessary for some sources
            while True:
                try:
                    basic_dict = {key: value for key, value in basic_dict.items() if key not in invalids_properties}
                    source: 'Source' = value(**basic_dict)
                    break
                except TypeError as e:
                    formated = str(e).split(" ")[-1].replace("'", "") # get the property name from the error message
                    invalids_properties.append(formated) 

    for filter_dict in source_dict["filters"]:
        filter = dict_to_filter(filter_dict)
        source.filters.add(filter)

    source.set_position((source_dict["x"], source_dict["y"]))    
    source.set_visible(source_dict["is_visible"])
    source.set_selectable(source_dict["is_selectable"])

    return source