from .console import Console

def test_console(capsys):
    console = Console()
    inp = "Something"
    console.print(inp)
    
    expected_outcome = inp + "\n"
    captured = capsys.readouterr()
    observed_outcome1 = captured.out
    
    assert observed_outcome1 == expected_outcome