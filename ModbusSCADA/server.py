class Register:
    def __init__(self, reg_addr, reg_nb):
        self.reg_addr = reg_addr
        self.reg_nb = reg_nb


class Server:
    def __init__(self, num: int, regs: []):
        self.num = 0
        self.regs = []

        self.create_reg_class(regs)

    def create_reg_class(self, regs: []):
        converted_regs = []

        for reg in regs:
            for reg_info in reg.values():
                converted_regs.append(Register(reg_info['reg_addr'], self.type_to_reg_nb(reg_info['reg_type'])))

        self.regs = converted_regs

    @staticmethod
    def type_to_reg_nb(reg_type: str):
        types = {
            "word": 1,
            "float": 2,
            "shortint": 0,
            "integer": 2,
            "dword": 2,
            "int64": 4,
            "bool": 0,
            "datetime": 4,
            "double": 4,
            "string": 2
        }

        return types[reg_type.lower()]
