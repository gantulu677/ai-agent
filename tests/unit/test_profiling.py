from agent_runtime.profiling import measure


def test_measure_reports_non_negative_duration():
    collected = []
    with measure("unit-test", collected.append) as result:
        sum(range(100))
    assert result["elapsed_seconds"] >= 0
    assert collected[0].operation == "unit-test"
