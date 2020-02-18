import random as rd

#concept of a bot
class Bot:
    def __init__(self):
        self.__choices = ["right", "bottright", "bottleft", "left", "topleft", "topright"]
        self.__start = rd.choice(self.__choices)
        self.__port_labels = []
        self.__port_structure = {}


    def label_ports(self):
        port_labels = []
        for i in range(len(self.__choices)):
            if self.__start  == self.__choices[i]:
                circulate = self.__choices[0:i]
                port_labels = self.__choices[i:]
                for reverse_label in circulate:
                    port_labels.append(reverse_label)
        self.__port_labels = port_labels[0:]
        return

    def scan_ports(self):
        # Predefined occupied/unoccupied nodes for now
        # Actual value is result of this.node.check(keyword)
        occupied = {
            "right":    1,
            "bottright":1,
            "bottleft": 0,
            "left":     0,
            "topleft":  1,
            "topright": 0
        }
        print(occupied)
        port_structure = {
            "successors": ["", "", ""],
            "predecessors": ["", "", ""],
            "right":    {
                "region_origin":"",
                "empty_region":0,
                "occupied":0,
                "region_end":""
            },
            "bottright":{
                "region_origin":"",
                "empty_region":0,
                "occupied":0,
                "region_end":""
            },
            "bottleft": {
                "region_origin":"",
                "empty_region":0,
                "occupied":0,
                "region_end":""
            },
            "left":     {
                "region_origin":"",
                "empty_region":0,
                "occupied":0,
                "region_end":""
            },
            "topleft":  {
                "region_origin":"",
                "empty_region":0,
                "occupied":0,
                "region_end":""
            },
            "topright": {
                "region_origin":"",
                "empty_region":0,
                "occupied":0,
                "region_end":""
            }
        }
        # Check round all ports twice.
        # First pass
        region_origin = ""
        region_end = ""
        empty_region = 0
        agents = 0
        for j in range(len(self.__port_labels) + 1):
            i = j % len(self.__port_labels)
            if occupied[self.__port_labels[i]] == 1:
                port_structure[self.__port_labels[i]]["occupied"] = 1

                port_structure[self.__port_labels[i]]["region_origin"] = self.__port_labels[i]
                region_origin = self.__port_labels[i]

                port_structure[self.__port_labels[i]]["empty_region"] = 0

                if empty_region > 0:
                    print("empty region 0")
                    port_structure["successors"][agents] = self.__port_labels[i]
                    agents += 1
                    empty_region = 0

            else:
                port_structure[self.__port_labels[i]]["occupied"] = 0

                port_structure[self.__port_labels[i]]["region_origin"] = region_origin

                empty_region += 1
                port_structure[self.__port_labels[i]]["empty_region"] = empty_region

        agents = 0
        empty_region = 0

        self.__port_structure = port_structure
        return

    def status(self):
        print(b.__choices)
        print(b.__start)
        print(b.__port_labels)
        print(b.__port_structure)

b = Bot()
b.label_ports()
b.scan_ports()
b.status()
