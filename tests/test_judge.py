from judgeaudit.judge import parse_grade

def test_parser_handles_none_and_empty():
    assert parse_grade(None) is None
    assert parse_grade("") is None

def test_parser_handles_clean_json():
    assert parse_grade('{"explanation": "ok", "criteria_met": true}') is True

def test_parser_handles_prose_wrapped_json():
    assert parse_grade('Sure! {"explanation": "ok", "criteria_met": false}') is False

def test_parser_bare_criteria_met():          
    assert parse_grade("Explanation: blah.\n\ncriteria_met: true") is True
    assert parse_grade("explanation: blah.\n\ncriteria_met: false") is False

def test_parser_uses_last_verdict_when_rubric_quoted():
    raw = 'The rubric says criteria_met: true would require X, but here...\n\ncriteria_met: false'
    assert parse_grade(raw) is False

def test_parser_returns_none_on_garbage():
    assert parse_grade("I cannot evaluate this.") is None