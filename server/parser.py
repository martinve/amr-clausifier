import unified_parser

class Parser:
    def __init__(self):
        self.init_pipeline = False

    def init(self):
        if self.init_pipeline:
            return

        unified_parser.init_pipeline()
        self.init_pipeline = True

    def parse_passage(self, passage):
        return unified_parser.get_passage_analysis(passage)

