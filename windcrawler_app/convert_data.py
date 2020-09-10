class Convertdata:

    def degrees_to_cardinal(self, input):
        self.input = input
        dirs = ['N', 'NNO', 'NO', 'ONO', 'O', 'OZO', 'ZO', 'ZZO', 'Z', 'ZZW', 'ZW', 'WZW', 'W', 'WNW', 'NW', 'NNW']
        ix = round(input / (360. / len(dirs)))
        output = dirs[ix % len(dirs)]
        return output