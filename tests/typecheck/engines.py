# pyright: reportMissingModuleSource=false

from typing import Iterator
from typing_extensions import assert_type

from pivy import coin


def check_engine_outputs() -> None:
    boolean = coin.SoBoolOperation()
    assert_type(boolean.a, coin.SoMFBool)
    assert_type(boolean.operation, coin.SoMFEnum)
    assert_type(boolean.output, coin.SoEngineOutput)
    assert_type(boolean.inverse, coin.SoEngineOutput)
    assert_type(boolean.__getattr__("a"), coin.SoField | coin.SoEngineOutput)
    assert_type(boolean.__getattr__("output"), coin.SoField | coin.SoEngineOutput)
    assert_type(boolean.getOutput(coin.SbName("missing")), coin.SoEngineOutput | None)
    assert_type(boolean.getOutputName(boolean.output, coin.SbName()), bool)
    assert_type(boolean.getOutputData(), coin.SoEngineOutputData)
    assert_type(boolean.copy(), coin.SoEngine)

    outputs = coin.SoEngineOutputList()
    assert_type(boolean.getOutputs(outputs), int)
    assert_type(outputs.getLength(), int)
    assert_type(outputs.get(0), coin.SoEngineOutput)
    assert_type(outputs[0], coin.SoEngineOutput)
    assert_type(iter(outputs), Iterator[coin.SoEngineOutput])

    output = boolean.output
    assert_type(output.getConnectionType(), coin.SoType)
    assert_type(output.getForwardConnections(coin.SoFieldList()), int)
    assert_type(output.isEnabled(), bool)
    assert_type(output.getNumConnections(), int)
    assert_type(output.getContainer(), coin.SoEngine | None)
    assert_type(output.getNodeContainer(), coin.SoNodeEngine | None)
    assert_type(output.getFieldContainer(), coin.SoFieldContainer | None)

    output_data = boolean.getOutputData()
    assert_type(output_data.getNumOutputs(), int)
    assert_type(output_data.getOutputName(0), coin.SbName)
    assert_type(output_data.getOutput(boolean, 0), coin.SoEngineOutput | None)
    assert_type(output_data.getType(0), coin.SoType)
    assert_type(output_data.getIndex(boolean, output), int)


def check_engine_factory_contract() -> None:
    boolean = coin.SoBoolOperation.createInstance()
    assert_type(boolean, coin.SoBoolOperation)

    composer = coin.SoComposeVec3f.createInstance()
    assert_type(composer, coin.SoComposeVec3f)

    node_engine = coin.SoVRMLTimeSensor.createInstance()
    assert_type(node_engine, coin.SoVRMLTimeSensor)


def check_engine_lookup() -> None:
    assert_type(coin.SoEngine.getByName(coin.SbName("missing")), coin.SoEngine | None)

    engines = coin.SoEngineList()
    assert_type(coin.SoEngine.getByName(coin.SbName("missing"), engines), int)
    assert_type(engines.get(0), coin.SoEngine)
    assert_type(engines[0], coin.SoEngine)
    assert_type(iter(engines), Iterator[coin.SoEngine])

    node_engine = coin.SoVRMLTimeSensor()
    assert_type(
        node_engine.getOutput(coin.SbName("time")), coin.SoEngineOutput | None
    )


def check_representative_engine_fields() -> None:
    composer = coin.SoComposeVec3f()
    assert_type(composer.x, coin.SoMFFloat)
    assert_type(composer.y, coin.SoMFFloat)
    assert_type(composer.z, coin.SoMFFloat)
    assert_type(composer.vector, coin.SoEngineOutput)

    decomposer = coin.SoDecomposeVec3f()
    assert_type(decomposer.vector, coin.SoMFVec3f)
    assert_type(decomposer.x, coin.SoEngineOutput)
    assert_type(decomposer.y, coin.SoEngineOutput)
    assert_type(decomposer.z, coin.SoEngineOutput)


def check_dynamic_engine_and_nodekit_access() -> None:
    engine = coin.SoBoolOperation()
    assert_type(engine.__getattr__("output"), coin.SoField | coin.SoEngineOutput)
