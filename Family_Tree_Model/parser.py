

class InputParser:

    pattern_map = {
        "king" : ("king", "male"),
        "son of" : ("son", "male"),
        "husband of" : ("husband", "male"),
        "wife of" : ("wife", "female"),
        "daughter of" : ("daughter", "female")
    }

    @staticmethod
    def parse_line(line):
        res = None
        for pattern in InputParser.pattern_map.keys():
            if pattern in line:
                values = line.split(pattern)
                p1 = values[0].strip()
                relation = InputParser.pattern_map[pattern][0]
                gender = InputParser.pattern_map[pattern][1]
                p2 = None
                if pattern != "king":
                    p2 = values[1].strip()
                res = (p1, relation, gender, p2)
                break
        return res




