import xml.etree.ElementTree as ET
import os
import sys
import copy
sys.setrecursionlimit(1000000)

RES = []


class PlaceOrTrans:

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


# 解析pnml文件
def xml_to_list(path):
    tree = ET.parse(path)
    iter_place = tree.iter(tag="place")  # dom树中住所对象的列表
    iter_trans = tree.iter(tag="transition")  # dom树中变迁对象的列表
    iter_arc = tree.iter(tag="arc")  # dom树中弧对象的列表
    # print(type(iter_place))
    places = [PlaceOrTrans(place[1][0].text, place.attrib['id']) for place in iter_place]
    transitions = [PlaceOrTrans(trans[1][0].text, trans.attrib['id']) for trans in iter_trans]
    arcs = [Arc(arc.attrib['source'], arc.attrib['target']) for arc in iter_arc]
    return places, transitions, arcs


def get_log_of_model(model_file, log_file):
    places, transitions, arcs = xml_to_list(model_file)
    places_id_index = {}  # 住所的id和索引的字典映射
    transitions_id_index = {}  # 变迁的id和索引的字典映射
    for i in range(len(places)):
        places_id_index.update({places[i].get_id():i})
    for i in range(len(transitions)):
        transitions_id_index.update({transitions[i].get_id():i})
    # print(places_id_index)
    # print(transitions_id_index)
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
    # for p in places:
    #     print(p.get_name())
    #     print(p.get_input())
    #     print(p.get_output())
    # for t in transitions:
    #     print(t.get_name())
    #     print(t.get_input())
    #     print(t.get_output())
    # 初始状态
    init_state = [1 if p.get_input() == [] else 0 for p in places]
    # 结束状态
    end_state = [1 if p.get_output() == [] else 0 for p in places]
    # 执行过的状态与执行后达该状态的变迁的字典映射
    state_trans = {i:[] for i in range(len(places))}
    get_path(init_state,end_state, places, transitions,transitions_id_index, [],[init_state],state_trans)
    count = 0
    for p in RES:
        print(p)
        count += 1
    print("总数：", count)
    log(log_file,RES)


def log(file_name, res):
    with open(file_name,'w',encoding='utf-8') as f:
        f.write(str(len(res)))
        f.write('\n')
        for r in res:
            f.write(" ".join(r))
            f.write('\n')


# 当前状态，结束状态，住所列表，变迁列表，变迁的id和索引的字典映射，某一次遍历的路径，已经执行过的状态，执行过的状态与执行后达该状态的变迁的字典映射
def get_path(state, end_state, places,transitions,transitions_id_index, path, exe_state, state_trans):
    if state == end_state:
        RES.append(path)
    else:
        enable_trans = {}
        for s in range(len(state)):
            if state[s] >= 1:
                for t_id in places[s].get_output():
                    # 对于可达变迁的输入place的状态-1
                    after_place = [state[i] - 1 if places[i].get_id() in transitions[transitions_id_index[t_id]].get_input() else state[i] for i in range(len(state))]
                    # print(after_place)
                    if -1 not in after_place:
                        # 对于可达变迁的输出place状态+1，构建变迁id和状态的映射字典
                        enable_trans[t_id] = [after_place[i] + 1 if places[i].get_id() in transitions[transitions_id_index[t_id]].get_output() else after_place[i] for i in range(len(state))]
                # print(enable_trans)
        for t_id, cur_state in enable_trans.items():
            cur_index = exe_state.index(state)
            if cur_state not in exe_state:
                path_next = path+[transitions[transitions_id_index[t_id]].get_name()]
                exe_state_next = exe_state+[cur_state]
                # 记录当前状态已经执行了哪些变迁
                state_trans_next = copy.deepcopy(state_trans)
                state_trans_next[cur_index].append(t_id)
                get_path(cur_state,end_state, places,transitions,transitions_id_index,path_next, exe_state_next, state_trans_next)
            elif t_id not in state_trans[cur_index] or len(enable_trans) == 1:
                path_next = path+[transitions[transitions_id_index[t_id]].get_name()]
                exe_state_next = exe_state
                # 记录当前状态已经执行了哪些变迁
                state_trans_next = copy.deepcopy(state_trans)
                state_trans_next[cur_index].append(t_id)
                get_path(cur_state, end_state, places, transitions, transitions_id_index, path_next,
                         exe_state_next, state_trans_next)


if __name__ == '__main__':
    get_log_of_model("test_cases/Model1.xml","log_model1.txt")
