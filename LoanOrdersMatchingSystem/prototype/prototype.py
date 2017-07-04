import json, time
BORROWERS_FILE = "borrowers.json"
PROPERTIES = ["Name", "City", "Purpose", "Income.GrossAnnual"]
SEP = "-"

class Loader(object):
    def __init__(self):
        self.DATA_DICT = {}
        self.NAME_DICT = {}
        self.CITY_DICT = {}
        self.PURPOSE_DICT = {}
        self.INCOME_DICT = {}
        
class Tree(object):
    def __init__(self):
        self.expression_type = None
        self.left_operand = None
        self.right_operand = None

def convert_into_json(json_obj, order_id, _loader, prefix=""):
    for prop, val_obj in json_obj.iteritems():
        if prefix == "":
            prefix_new = prop
        else:
            prefix_new = prefix + "." + prop            
        if type(val_obj) is dict:
            convert_into_json(val_obj, order_id, _loader, prefix=prefix_new)
        else:
            print prefix_new, ": ", val_obj
            if prefix_new not in _loader.DATA_DICT:
                _loader.DATA_DICT[prefix_new] = {}
            if val_obj not in _loader.DATA_DICT[prefix_new]:
                _loader.DATA_DICT[prefix_new][val_obj] = []
            _loader.DATA_DICT[prefix_new][val_obj].append(order_id)
        
def load_data(_loader):
    try:
        with open(BORROWERS_FILE) as fp:
            data = json.load(fp)
        for order in data["orders"]:
            properties = order["OrderProperties"]                        
            print "\n"
            print "Id: ", order["Id"]
            convert_into_json(properties, order["Id"], _loader)
        print "\n********Loaded the below objects**********\n"
        for key, val in _loader.DATA_DICT.iteritems():
            print "%s : %s" % (key, val)            
        print "********************************************\n"
    except Exception, e:
        print "Error", e
        raise e
        
def generate_expression_tree(predicate):
    node = Tree()
    node.expression_type = predicate["ExpressionType"]
    if predicate["ExpressionType"] in ["Or", "And"]:
        node.left_operand = generate_expression_tree(predicate["LeftOperand"])
        node.right_operand = generate_expression_tree(predicate["RightOperand"])
    elif predicate["ExpressionType"] in ["Equals", "GreaterThan", "LessThan"]:
        node.left_operand = predicate["LeftOperand"]["Value"]
        node.right_operand = predicate["RightOperand"]["Value"]
    elif predicate["ExpressionType"] == "Not":
        node.left_operand = generate_expression_tree(predicate["Child"])
    return node
    
def union_sets(set1, set2):
    return set1.union(set2)
    
def intersection_sets(set1, set2):
    return set1.intersection(set2)
    
def evaluate(root, _loader):
    result_list = list()    
    if root.expression_type == "Equals":
        if root.left_operand not in _loader.DATA_DICT:
            return result_list
        if root.right_operand in _loader.DATA_DICT[root.left_operand]:
            result_list = _loader.DATA_DICT[root.left_operand][root.right_operand]
    elif root.expression_type == "GreaterThan":
        if root.left_operand not in _loader.DATA_DICT:
            return result_list
        values_dict = _loader.DATA_DICT[root.left_operand]
        for key in values_dict.iterkeys():
            if key > root.right_operand:
                result_list.extend(values_dict[key])
    elif root.expression_type == "LessThan":
        if root.left_operand not in _loader.DATA_DICT:
            return result_list
        values_dict = _loader.DATA_DICT[root.left_operand]
        for key in values_dict.iterkeys():
            if key < root.right_operand:
                result_list.extend(values_dict[key])
    elif root.expression_type == "Or":
        result_list = union_sets(evaluate(root.left_operand, _loader), evaluate(root.right_operand, _loader))
    elif root.expression_type == "And":
        result_list = intersection_sets(evaluate(root.left_operand, _loader), evaluate(root.right_operand, _loader))
    return set(result_list)
    
        
def match_lender_order(_loader, lender_order):
    result = set()
    print "\n"
    for predicate in lender_order["Predicates"]:
        root = generate_expression_tree(predicate)
        res =  evaluate(root, _loader)
        print "Results of predicate" , predicate, ":"
        print res, "\n"
        if len(result) > 1:
            result = result.intersection(res)
        else:
            result = res
    return result

lender_order = {
	"Id": 1,
	"Predicates": [
            {
                "ExpressionType": "Or",
                "LeftOperand": {
                    "LeftOperand": {"Value":"Purpose"},
                    "RightOperand": {"Value":"Car"},
                    "ExpressionType": "Equals"
                },
                "RightOperand": {
                    "LeftOperand": {"Value":"Purpose"},
                    "RightOperand": {"Value":"House"},
                    "ExpressionType": "Equals"
                }
            },
            {
                "LeftOperand": {"Value":"Income.GrossAnnual"},
                "RightOperand": {"Value":50000},
                "ExpressionType": "GreaterThan"
            },
            {
                "LeftOperand": {"Value":"City"},
                "RightOperand": {"Value":"Sydney"},
                "ExpressionType": "Equals"
            }
        ]
    }

start_time = time.time()
print "Placing the below lender order: \n", lender_order
_loader = Loader()
load_data(_loader)
result = match_lender_order(_loader, lender_order)
print "Final Result:\n", result
end_time = time.time()
print "Total time taken: ", end_time - start_time, "sec"

