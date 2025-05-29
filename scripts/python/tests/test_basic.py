"""Basic tests to ensure the testing framework is working."""


def test_basic_functionality():
    """Test that basic functionality works."""
    assert True


def test_imports():
    """Test that core modules can be imported."""
    import sys
    from pathlib import Path

    # Add project root to path
    project_root = Path(__file__).parent.parent.parent.parent
    sys.path.insert(0, str(project_root))

    try:
        from scripts.python.core.config import get_config
        from scripts.python.core.security import validate_command

        assert True
    except ImportError as e:
        assert False, f"Failed to import core modules: {e}"
