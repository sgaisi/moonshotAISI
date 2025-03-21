import pytest
from pydantic import ValidationError

from moonshot.src.connectors_endpoints.connector_endpoint_arguments import (
    ConnectorEndpointArguments,
)


class TestCollectionConnectorEndpointArguments:
    # ------------------------------------------------------------------------------
    # Test ConnectorEndpointArguments functionality
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "id, name, connector_type, uri, token, max_calls_per_second, max_concurrency, model, params, created_date",
        [
            (
                "id_0",
                "Name 0",
                "Type 0",
                "URI 0",
                "Token 0",
                1,
                1,
                "Model 0",
                {},
                "2023-01-01",
            ),
            (
                "id_1",
                "Name 1",
                "Type 1",
                "URI 1",
                "Token 1",
                2,
                2,
                "Model 1",
                {"param1": "value1"},
                "2023-01-02",
            ),
            (
                "",
                "Name 0",
                "Type 0",
                "URI 0",
                "Token 0",
                1,
                1,
                "Model 0",
                {},
                "2023-01-01",
            ),
            (
                "id_0",
                "Name 0",
                "",
                "URI 0",
                "Token 0",
                1,
                1,
                "Model 0",
                {},
                "2023-01-01",
            ),
            (
                "id_0",
                "Name 0",
                "Type 0",
                "",
                "Token 0",
                1,
                1,
                "Model 0",
                {},
                "2023-01-01",
            ),
            (
                "id_0",
                "Name 0",
                "Type 0",
                "URI 0",
                "",
                1,
                1,
                "Model 0",
                {},
                "2023-01-01",
            ),
            (
                "id_0",
                "Name 0",
                "Type 0",
                "URI 0",
                "Token 0",
                True,
                1,
                "Model 0",
                {},
                "2023-01-01",
            ),
        ],
    )
    def test_create_connector_endpoint_arguments(
        self,
        id,
        name,
        connector_type,
        uri,
        token,
        max_calls_per_second,
        max_concurrency,
        model,
        params,
        created_date,
    ):
        # Test creating a valid connector endpoint arguments instance
        connector_endpoint_arguments = ConnectorEndpointArguments(
            id=id,
            name=name,
            connector_type=connector_type,
            uri=uri,
            token=token,
            max_calls_per_second=max_calls_per_second,
            max_concurrency=max_concurrency,
            model=model,
            params=params,
            created_date=created_date,
        )
        assert connector_endpoint_arguments.id == id
        assert connector_endpoint_arguments.name == name
        assert connector_endpoint_arguments.connector_type == connector_type
        assert connector_endpoint_arguments.uri == uri
        assert connector_endpoint_arguments.token == token
        assert connector_endpoint_arguments.max_calls_per_second == max_calls_per_second
        assert connector_endpoint_arguments.max_concurrency == max_concurrency
        assert connector_endpoint_arguments.model == model
        assert connector_endpoint_arguments.params == params
        assert connector_endpoint_arguments.created_date == created_date

    @pytest.mark.parametrize(
        "id, name, connector_type, uri, token, max_calls_per_second, max_concurrency, model, params",
        [
            (
                "id_1",
                "Name 1",
                "Type 1",
                "URI 1",
                "Token 1",
                2,
                2,
                "Model 1",
                {"param1": "value1"},
            ),
            (
                "id_2",
                "Name 2",
                "Type 2",
                "URI 2",
                "Token 2",
                3,
                3,
                "Model 2",
                {"param2": "value2"},
            ),
        ],
    )
    def test_create_connector_endpoint_arguments_1(
        self,
        id,
        name,
        connector_type,
        uri,
        token,
        max_calls_per_second,
        max_concurrency,
        model,
        params,
    ):
        # Test creating a valid connector endpoint arguments instance
        connector_endpoint_arguments = ConnectorEndpointArguments(
            id=id,
            name=name,
            connector_type=connector_type,
            uri=uri,
            token=token,
            max_calls_per_second=max_calls_per_second,
            max_concurrency=max_concurrency,
            model=model,
            params=params,
        )
        assert connector_endpoint_arguments.id == id
        assert connector_endpoint_arguments.name == name
        assert connector_endpoint_arguments.connector_type == connector_type
        assert connector_endpoint_arguments.uri == uri
        assert connector_endpoint_arguments.token == token
        assert connector_endpoint_arguments.max_calls_per_second == max_calls_per_second
        assert connector_endpoint_arguments.max_concurrency == max_concurrency
        assert connector_endpoint_arguments.model == model
        assert connector_endpoint_arguments.params == params

    @pytest.mark.parametrize(
        "id, name, connector_type, uri, token, max_calls_per_second, max_concurrency, model, params, created_date",
        [
            # Invalid ID
            (
                None,
                "Name A",
                "Type A",
                "URI A",
                "Token A",
                1,
                1,
                "Model A",
                {},
                "2023-01-01",
            ),
            (
                1234,
                "Name A",
                "Type A",
                "URI A",
                "Token A",
                1,
                1,
                "Model A",
                {},
                "2023-01-01",
            ),
            (
                [],
                "Name A",
                "Type A",
                "URI A",
                "Token A",
                1,
                1,
                "Model A",
                {},
                "2023-01-01",
            ),
            (
                {},
                "Name A",
                "Type A",
                "URI A",
                "Token A",
                1,
                1,
                "Model A",
                {},
                "2023-01-01",
            ),
            (
                True,
                "Name A",
                "Type A",
                "URI A",
                "Token A",
                1,
                1,
                "Model A",
                {},
                "2023-01-01",
            ),
            (
                (),
                "Name A",
                "Type A",
                "URI A",
                "Token A",
                1,
                1,
                "Model A",
                {},
                "2023-01-01",
            ),
            # Invalid Name
            (
                "id_1",
                None,
                "Type B",
                "URI B",
                "Token B",
                1,
                1,
                "Model B",
                {},
                "2023-01-01",
            ),
            (
                "id_1",
                1234,
                "Type B",
                "URI B",
                "Token B",
                1,
                1,
                "Model B",
                {},
                "2023-01-01",
            ),
            (
                "id_1",
                [],
                "Type B",
                "URI B",
                "Token B",
                1,
                1,
                "Model B",
                {},
                "2023-01-01",
            ),
            (
                "id_1",
                {},
                "Type B",
                "URI B",
                "Token B",
                1,
                1,
                "Model B",
                {},
                "2023-01-01",
            ),
            (
                "id_1",
                True,
                "Type B",
                "URI B",
                "Token B",
                1,
                1,
                "Model B",
                {},
                "2023-01-01",
            ),
            (
                "id_1",
                (),
                "Type B",
                "URI B",
                "Token B",
                1,
                1,
                "Model B",
                {},
                "2023-01-01",
            ),
            (
                "id_1",
                "",
                "Type B",
                "URI B",
                "Token B",
                1,
                1,
                "Model B",
                {},
                "2023-01-01",
            ),
            # Invalid connector type
            (
                "id_2",
                "Name C",
                None,
                "URI C",
                "Token C",
                1,
                1,
                "Model C",
                {},
                "2023-01-01",
            ),
            (
                "id_2",
                "Name C",
                1234,
                "URI C",
                "Token C",
                1,
                1,
                "Model C",
                {},
                "2023-01-01",
            ),
            (
                "id_2",
                "Name C",
                [],
                "URI C",
                "Token C",
                1,
                1,
                "Model C",
                {},
                "2023-01-01",
            ),
            (
                "id_2",
                "Name C",
                {},
                "URI C",
                "Token C",
                1,
                1,
                "Model C",
                {},
                "2023-01-01",
            ),
            (
                "id_2",
                "Name C",
                True,
                "URI C",
                "Token C",
                1,
                1,
                "Model C",
                {},
                "2023-01-01",
            ),
            (
                "id_2",
                "Name C",
                (),
                "URI C",
                "Token C",
                1,
                1,
                "Model C",
                {},
                "2023-01-01",
            ),
            # Invalid URI
            (
                "id_3",
                "Name D",
                "Type D",
                None,
                "Token D",
                1,
                1,
                "Model D",
                {},
                "2023-01-01",
            ),
            (
                "id_3",
                "Name D",
                "Type D",
                1234,
                "Token D",
                1,
                1,
                "Model D",
                {},
                "2023-01-01",
            ),
            (
                "id_3",
                "Name D",
                "Type D",
                [],
                "Token D",
                1,
                1,
                "Model D",
                {},
                "2023-01-01",
            ),
            (
                "id_3",
                "Name D",
                "Type D",
                {},
                "Token D",
                1,
                1,
                "Model D",
                {},
                "2023-01-01",
            ),
            (
                "id_3",
                "Name D",
                "Type D",
                True,
                "Token D",
                1,
                1,
                "Model D",
                {},
                "2023-01-01",
            ),
            (
                "id_3",
                "Name D",
                "Type D",
                (),
                "Token D",
                1,
                1,
                "Model D",
                {},
                "2023-01-01",
            ),
            # Invalid Token
            (
                "id_4",
                "Name E",
                "Type E",
                "URI E",
                None,
                1,
                1,
                "Model E",
                {},
                "2023-01-01",
            ),
            (
                "id_4",
                "Name E",
                "Type E",
                "URI E",
                1234,
                1,
                1,
                "Model E",
                {},
                "2023-01-01",
            ),
            (
                "id_4",
                "Name E",
                "Type E",
                "URI E",
                [],
                1,
                1,
                "Model E",
                {},
                "2023-01-01",
            ),
            (
                "id_4",
                "Name E",
                "Type E",
                "URI E",
                {},
                1,
                1,
                "Model E",
                {},
                "2023-01-01",
            ),
            (
                "id_4",
                "Name E",
                "Type E",
                "URI E",
                True,
                1,
                1,
                "Model E",
                {},
                "2023-01-01",
            ),
            (
                "id_4",
                "Name E",
                "Type E",
                "URI E",
                (),
                1,
                1,
                "Model E",
                {},
                "2023-01-01",
            ),
            # Invalid Max Call Per Second
            (
                "id_5",
                "Name F",
                "Type F",
                "URI F",
                "Token F",
                None,
                1,
                "Model F",
                {},
                "2023-01-01",
            ),
            (
                "id_5",
                "Name F",
                "Type F",
                "URI F",
                "Token F",
                0,
                1,
                "Model F",
                {},
                "2023-01-01",
            ),
            (
                "id_5",
                "Name F",
                "Type F",
                "URI F",
                "Token F",
                -1,
                1,
                "Model F",
                {},
                "2023-01-01",
            ),
            (
                "id_5",
                "Name F",
                "Type F",
                "URI F",
                "Token F",
                [],
                1,
                "Model F",
                {},
                "2023-01-01",
            ),
            (
                "id_5",
                "Name F",
                "Type F",
                "URI F",
                "Token F",
                {},
                1,
                "Model F",
                {},
                "2023-01-01",
            ),
            (
                "id_5",
                "Name F",
                "Type F",
                "URI F",
                "Token F",
                (),
                1,
                "Model F",
                {},
                "2023-01-01",
            ),
            (
                "id_5",
                "Name F",
                "Type F",
                "URI F",
                "Token F",
                "",
                1,
                "Model F",
                {},
                "2023-01-01",
            ),
            # Invalid Max Concurrency
            (
                "id_6",
                "Name G",
                "Type G",
                "URI G",
                "Token G",
                1,
                None,
                "Model G",
                {},
                "2023-01-01",
            ),
            (
                "id_6",
                "Name G",
                "Type G",
                "URI G",
                "Token G",
                1,
                0,
                "Model G",
                {},
                "2023-01-01",
            ),
            (
                "id_6",
                "Name G",
                "Type G",
                "URI G",
                "Token G",
                1,
                -1,
                "Model G",
                {},
                "2023-01-01",
            ),
            (
                "id_6",
                "Name G",
                "Type G",
                "URI G",
                "Token G",
                1,
                [],
                "Model G",
                {},
                "2023-01-01",
            ),
            (
                "id_6",
                "Name G",
                "Type G",
                "URI G",
                "Token G",
                1,
                {},
                "Model G",
                {},
                "2023-01-01",
            ),
            (
                "id_6",
                "Name G",
                "Type G",
                "URI G",
                "Token G",
                1,
                (),
                "Model G",
                {},
                "2023-01-01",
            ),
            (
                "id_6",
                "Name G",
                "Type G",
                "URI G",
                "Token G",
                1,
                "",
                "Model G",
                {},
                "2023-01-01",
            ),
            # Invalid Model
            (
                "id_7",
                "Name H",
                "Type H",
                "URI H",
                "Token H",
                1,
                1,
                None,
                {},
                "2023-01-01",
            ),
            (
                "id_7",
                "Name H",
                "Type H",
                "URI H",
                "Token H",
                1,
                1,
                1234,
                {},
                "2023-01-01",
            ),
            (
                "id_7",
                "Name H",
                "Type H",
                "URI H",
                "Token H",
                1,
                1,
                [],
                {},
                "2023-01-01",
            ),
            (
                "id_7",
                "Name H",
                "Type H",
                "URI H",
                "Token H",
                1,
                1,
                {},
                {},
                "2023-01-01",
            ),
            (
                "id_7",
                "Name H",
                "Type H",
                "URI H",
                "Token H",
                1,
                1,
                True,
                {},
                "2023-01-01",
            ),
            (
                "id_7",
                "Name H",
                "Type H",
                "URI H",
                "Token H",
                1,
                1,
                (),
                {},
                "2023-01-01",
            ),
            # Invalid Params
            (
                "id_8",
                "Name I",
                "Type I",
                "URI I",
                "Token I",
                1,
                1,
                "Model I",
                None,
                "2023-01-01",
            ),
            (
                "id_8",
                "Name I",
                "Type I",
                "URI I",
                "Token I",
                1,
                1,
                "Model I",
                1234,
                "2023-01-01",
            ),
            (
                "id_8",
                "Name I",
                "Type I",
                "URI I",
                "Token I",
                1,
                1,
                "Model I",
                True,
                "2023-01-01",
            ),
            (
                "id_8",
                "Name I",
                "Type I",
                "URI I",
                "Token I",
                1,
                1,
                "Model I",
                [],
                "2023-01-01",
            ),
            (
                "id_8",
                "Name I",
                "Type I",
                "URI I",
                "Token I",
                1,
                1,
                "Model I",
                (),
                "2023-01-01",
            ),
            # Invalid Params
            ("id_9", "Name J", "Type J", "URI J", "Token J", 1, 1, "Model J", {}, None),
            ("id_9", "Name J", "Type J", "URI J", "Token J", 1, 1, "Model J", {}, 1234),
            ("id_9", "Name J", "Type J", "URI J", "Token J", 1, 1, "Model J", {}, True),
            ("id_9", "Name J", "Type J", "URI J", "Token J", 1, 1, "Model J", {}, []),
            ("id_9", "Name J", "Type J", "URI J", "Token J", 1, 1, "Model J", {}, {}),
            ("id_9", "Name J", "Type J", "URI J", "Token J", 1, 1, "Model J", {}, ()),
        ],
    )
    def test_create_connector_endpoint_arguments_invalid(
        self,
        id,
        name,
        connector_type,
        uri,
        token,
        max_calls_per_second,
        max_concurrency,
        model,
        params,
        created_date,
    ):
        # Ensure that invalid inputs raise a ValidationError
        with pytest.raises(ValidationError):
            ConnectorEndpointArguments(
                id=id,
                name=name,
                connector_type=connector_type,
                uri=uri,
                token=token,
                max_calls_per_second=max_calls_per_second,
                max_concurrency=max_concurrency,
                model=model,
                params=params,
                created_date=created_date,
            )

    # ------------------------------------------------------------------------------
    # Test to_dict functionality
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "id, name, connector_type, uri, token, max_calls_per_second, max_concurrency, model, params, created_date",
        [
            (
                "id_0",
                "Name 0",
                "Type 0",
                "URI 0",
                "Token 0",
                1,
                1,
                "Model 0",
                {},
                "2023-01-01",
            ),
            (
                "id_1",
                "Name 1",
                "Type 1",
                "URI 1",
                "Token 1",
                2,
                2,
                "Model 1",
                {"param1": "value1"},
                "2023-01-02",
            ),
            (
                "id_2",
                "Name 2",
                "Type 2",
                "URI 2",
                "Token 2",
                3,
                3,
                "Model 2",
                {"param2": "value2"},
                "",
            ),
        ],
    )
    def test_to_dict(
        self,
        id,
        name,
        connector_type,
        uri,
        token,
        max_calls_per_second,
        max_concurrency,
        model,
        params,
        created_date,
    ):
        # Test the to_dict method
        connector_endpoint_arguments = ConnectorEndpointArguments(
            id=id,
            name=name,
            connector_type=connector_type,
            uri=uri,
            token=token,
            max_calls_per_second=max_calls_per_second,
            max_concurrency=max_concurrency,
            model=model,
            params=params,
            created_date=created_date,
        )
        expected_dict = {
            "id": id,
            "name": name,
            "connector_type": connector_type,
            "uri": uri,
            "token": token,
            "max_calls_per_second": max_calls_per_second,
            "max_concurrency": max_concurrency,
            "model": model,
            "params": params,
            "created_date": created_date,
        }
        assert connector_endpoint_arguments.to_dict() == expected_dict
