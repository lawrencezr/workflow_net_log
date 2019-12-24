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


def xml_to_dic(path):
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
    arcs = [Place(arc[1][0].text, arc.attrib['id']) for arc in iter_arc]


if __name__ == '__main__':
    xml_to_dic("test_cases/Model1.pnml")
