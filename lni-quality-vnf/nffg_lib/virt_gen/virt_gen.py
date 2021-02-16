from virt_builder import InfraBuilder, Converter


class Generator:
    def __init__(self, model):
        self.model = model
        self.builder = InfraBuilder()
        self.converter = Converter(None)

    def get(self):
        graph = self.builder.get(self.model)
        self.converter.set_graph(graph)
        virt = self.converter.get()
        return virt

    def set_model(self, model):
        self.model = model


if __name__ == "__main__":
    virt_gen = Generator(1)
    for model in range(1,7):
        virt_gen.set_model(model)
        virt = virt_gen.get()
        print 'saving model ' + str(model)
        virt.write_to_file('./tests/configs/model-'+str(model)+'.xml')