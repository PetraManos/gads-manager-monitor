import importlib
from core.string_utils import collapse_one_line

def test_runlog_ctx_and_stdout_logger(capsys):
    runlog = importlib.import_module("core.runlog")
    RunLogCtx = getattr(runlog, "RunLogCtx")
    stdout_logger = getattr(runlog, "stdout_logger")

    # With extras
    ctx = RunLogCtx(
        customer_id="123-456-7890",
        check="NO_RECENT_IMPRESSIONS",
        message="Line 1\nLine 2   \t  Line 3",
        extras={"note": "something happened"}
    )
    line = ctx.one_line()
    assert line.startswith("[NO_RECENT_IMPRESSIONS] ")
    assert "Line 1 Line 2 Line 3" in line
    assert "{'note': 'something happened'}" in line

    # stdout_logger should print exactly one collapsed line
    stdout_logger.write(ctx)
    out = capsys.readouterr().out.strip()
    assert out == line

    # Without extras
    ctx2 = RunLogCtx(
        customer_id="123-456-7890",
        check="ABC",
        message="A   B\nC"
    )
    line2 = ctx2.one_line()
    assert line2 == "[ABC] " + collapse_one_line("A   B\nC")
