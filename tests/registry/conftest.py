import pytest
import pulumi

@pytest.fixture
def pulumi_mocks():
    class Mocks(pulumi.runtime.Mocks):
        def new_resource(self, args: pulumi.runtime.MockResourceArgs):
            return [args.name + '_id', args.inputs]
        def call(self, args: pulumi.runtime.MockCallArgs):
            return {}

    pulumi.runtime.set_mocks(Mocks())
    yield
