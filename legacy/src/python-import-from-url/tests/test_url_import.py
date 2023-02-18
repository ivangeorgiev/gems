import time
import pytest
from pyimporter import enable_url_import

@pytest.mark.functional
def test_Should_HavePackageImported_When_ImportFromUrl(urlimport):
    import agent
    assert '007' == agent.name 

@pytest.mark.functional
def test_Should_HaveModuleImported_When_ImportFromUrl(urlimport):
    from agent import actions
    assert 'Baff' == actions.bark() 

@pytest.mark.functional
def test_Should_RiseExecption_When_ImportedCodeFailsToCompile(urlimport):
    with pytest.raises(IndentationError):
        from agent import bad_syntax_code

@pytest.mark.functional
def test_Should_RiseExecption_When_ImportedCodeFailsToRun(urlimport):
    with pytest.raises(NameError):
        from agent import bad_execution_code

