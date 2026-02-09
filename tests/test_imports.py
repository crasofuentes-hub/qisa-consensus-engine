def test_package_imports():
    import qisa  # noqa: F401


def test_version_defined():
    import qisa

    assert isinstance(qisa.__version__, str)
    assert qisa.__version__.count(".") >= 2
