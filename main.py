import xml.etree.ElementTree as ET
import os
import sys


class Place:
    type = 0

    def __init__(self, name, id):
        self.name = name
        self.id = id

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_id(self):
        return self.id

    def set_id(self, id):
        self.id = id

    def get_type(self):
        return self.type

    def set_type(self, type):
        self.type = type


class Arc:
    def __init__(self, source, target):
        self.source = source
        self.target = target

    def get_source(self):
        return self.source

    def set_source(self, source):
        self.source = source

    def get_target(self):
        return self.target

    def set_target(self, target):
        self.target = target


def xml_to_list(path):
    tree = ET.parse(path)
    root = tree.getroot()

    print(root.tag)
    print(root.attrib)
    iter_place = tree.iter(tag="place")
    iter_trans = tree.iter(tag="transition")
    iter_arc = tree.iter(tag="arc")
    print(type(iter_place))
    places = [Place(place[1][0].text, place.attrib['id']) for place in iter_place]
    transitions = [Place(trans[1][0].text, trans.attrib['id']) for trans in iter_trans]
    for p in places:
        p.set_type(0)
    for t in transitions:
        t.set_type(1)
    places.extend(transitions)
    arcs = [Arc(arc.attrib['source'], arc.attrib['target']) for arc in iter_arc]
    return places, arcs

def get_log_of_model(model_file, logfile):
    places, arcs = xml_to_list(model_file)
    num_places = len(places)
    graph = [[0 for _ in range(num_places)] for _ in range(num_places)]
    id_dic = {}
    name_dic = {}
    for i in range(num_places):
        id_dic.update({places[i].get_id():i})
        if places[i].get_type() == 1:
            name_dic.update({i:places[i].get_name()})
    print(id_dic)
    print(name_dic)
    for arc in arcs:
        i = id_dic[arc.get_source()]
        j = id_dic[arc.get_target()]
        graph[i][j] = 1
    print(graph)




if __name__ == '__main__':
    get_log_of_model("test_cases/Model1.pnml","log.txt")
