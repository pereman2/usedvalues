from typing import Dict, List
import json
import pdb
import copy

def is_container(obj) -> bool:
    return isinstance(obj, list) or isinstance(obj, dict)

class CheckUsedEntry:
    def __init__(self, obj):
        self.obj: Union[Dict, List] = obj
        if isinstance(obj, dict):
            self.used = {k:0 for k, _ in self.obj.items()}
            for k, v in self.obj.items():
                if is_container(v):
                    self.obj[k] = CheckUsedEntry(v)
        elif isinstance(obj, list):
            self.used = {i:0 for i in range(len(self.obj))}
            for i in range(len(self.obj)):
                v = self.obj[i]
                if is_container(v):
                    self.obj[i] = CheckUsedEntry(v)
        else:
            raise RuntimeError("Bad")

    def __getitem__(self, key):
        self.used[key] += 1
        return self.obj[key]

    def __setitem__(self, key, value):
        self.obj[key] = value

    def __len__(self):
        return len(self.obj)

    def __repr__(self):
        used = get_used_entries(self)
        return json.dumps(used, indent=2)

def pretty_entries(u: dict, acc_key: list=[]):
    res = {}
    for k, v in u.items():
        new_acc_k = copy.copy(acc_key)
        k = str(k)
        new_acc_k.append(k)
        k = '.'.join(new_acc_k)
        res[k] =  v['times']
        if isinstance(v['inner'], dict):
            res.update(pretty_entries(v['inner'], new_acc_k))
    return res



def get_used_entries(u: CheckUsedEntry):
    used = {}
    if isinstance(u.obj, dict):
        for k, v in u.obj.items():
            used[k] = {"times": u.used[k], "inner": get_used_entries(v) if isinstance(v, CheckUsedEntry) else None}
    elif isinstance(u.obj, list):
        for k in range(len(u.obj)):
            v = u.obj[k]
            used[k] = {"times": u.used[k], "inner": get_used_entries(v) if isinstance(v, CheckUsedEntry) else None}
            
    return used
    
def test():
    osd_map = {"osds": [{"name": "osd.1"}, {"name": "osd.2"}], "num": 2}
    osd_map = CheckUsedEntry(osd_map)
    used2 = osd_map["osds"][0]["name"]
    print(json.dumps(pretty_entries(get_used_entries(osd_map)), indent=2))
    print('-'*80)
    print(json.dumps(get_used_entries(osd_map), indent=2))


def main():
    test()

if __name__ == "__main__":
    main()
