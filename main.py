import xml.etree.ElementTree as ET
import os
import sys

res = []
path = []


class PlaceOrTrans:
    # type = 0

    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.input = []
        self.output = []

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

    def get_input(self):
        return self.input

    def set_input(self,id):
        self.input.append(id)

    def get_output(self):
        return self.output

    def set_output(self,id):
        self.output.append(id)

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
    places = [PlaceOrTrans(place[1][0].text, place.attrib['id']) for place in iter_place]
    transitions = [PlaceOrTrans(trans[1][0].text, trans.attrib['id']) for trans in iter_trans]
    # for p in places:
    #     p.set_type(0)
    # for t in transitions:
    #     t.set_type(1)
    # places.extend(transitions)
    arcs = [Arc(arc.attrib['source'], arc.attrib['target']) for arc in iter_arc]
    return places, transitions, arcs


def get_log_of_model(model_file, logfile):
    places, transitions, arcs = xml_to_list(model_file)
    # graph = [[0 for _ in range(num_places)] for _ in range(num_places)]
    places_id_index = {}
    transitions_id_index = {}
    for i in range(len(places)):
        places_id_index.update({places[i].get_id():i})
    for i in range(len(transitions)):
        transitions_id_index.update({transitions[i].get_id():i})
    print(places_id_index)
    print(transitions_id_index)
    for arc in arcs:
        source = arc.get_source()  # 获取弧的源节点id
        target = arc.get_target()  # 获取弧的目标节点id
        # 源节点是place，目标节点是transition
        if source in places_id_index.keys() and target in transitions_id_index.keys():
            places[places_id_index[source]].set_output(target)
            transitions[transitions_id_index[target]].set_input(source)
        # 源节点是transition，目标节点是place
        elif source in transitions_id_index.keys() and target in places_id_index.keys():
            places[places_id_index[target]].set_input(source)
            transitions[transitions_id_index[source]].set_output(target)
    for p in places:
        print(p.get_name())
        print(p.get_input())
        print(p.get_output())
    for t in transitions:
        print(t.get_name())
        print(t.get_input())
        print(t.get_output())
    # 初始状态
    init_state = [1 if p.get_input() == [] else 0 for p in places]
    # 结束状态
    end_state = [1 if p.get_output() == [] else 0 for p in places]
    print(init_state)
    print(end_state)
    get_path(init_state,[],[init_state],[])
    # pathes = get_path(graph,num_places)
    # print(pathes)
    # res_string = []
    # tuple_string = ""
    # for i in pathes:
    #     for j in i:
    #         # print(j)
    #         tuple_string += (name_dic[j]+" ")
    #         # print(name_dic[j])
    #     res_string.append(tuple_string)
    #     tuple_string = ""
    # for r in res_string:
        # print(r)



def get_path(state, path, exe_state, output_state):
    visited = [0 for _ in range(num_places)]
    source = 0
    target = 0
    for i in range(num_places):
        flag = True
        for j in range(num_places):
            if graph[j][i]:
                flag = False
                break
        if flag:
            source = i
            break
    for i in range(num_places):
        flag = True
        for j in range(num_places):
            if graph[i][j]:
                flag = False
                break
        if flag:
            target = i
            break
    path.append(source)
    visited[source] += 1
    dfs(graph, visited, target)
    return res

def dfs(graph, visited, target):
    cur = path[-1]
    if cur == target:
        res.append(path)
        path.pop(-1)
        visited[cur] -= 1
        return
    for i in range(len(graph)):
        if graph[cur][i]:
            if visited[i] < 2:
                path.append(i)
                visited[i] += 1
                dfs(graph, visited, target)
    path.pop(-1)
    visited[cur] -= 1
    return







if __name__ == '__main__':
    get_log_of_model("test_cases/Model1.pnml","log.txt")
