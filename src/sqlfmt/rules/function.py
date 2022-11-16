from functools import partial

from sqlfmt import actions
from sqlfmt.rule import Rule
from sqlfmt.rules.common import group
from sqlfmt.rules.core import CORE
from sqlfmt.token import TokenType

CREATE_FUNCTION = [
    *CORE,
    Rule(
        name="function_as",
        priority=1100,
        pattern=group(
            r"as",
        )
        + group(r"\W", r"$"),
        action=actions.handle_ddl_as,
    ),
    Rule(
        name="word_operator",
        priority=1100,
        pattern=group(
            r"to",
            r"from",
            # snowflake
            r"runtime_version",
        )
        + group(r"\W", r"$"),
        action=partial(actions.add_node_to_buffer, token_type=TokenType.WORD_OPERATOR),
    ),
    Rule(
        name="unterm_keyword",
        priority=1300,
        pattern=group(
            (
                r"create(\s+or\s+replace)?(\s+temp(orary)?)?(\s+secure)?(\s+table)?"
                r"\s+function(\s+if\s+not\s+exists)?"
            ),
            r"language",
            r"transform",
            r"immutable",
            r"stable",
            r"volatile",
            r"(not\s+)?leakproof",
            r"volatile",
            r"called\s+on\s+null\s+input",
            r"returns\s+null\s+on\s+null\s+input",
            r"return(s)?(?!\s+null)",
            r"strict",
            r"(external\s+)?security\s+(invoker|definer)",
            r"parallel\s+(unsafe|restricted|safe)",
            r"cost",
            r"rows",
            r"support",
            r"set",
            r"as",
            # snowflake
            r"comment",
            r"imports",
            r"packages",
            r"handler",
            r"target_path",
            r"(not\s+)?null",
            # bq
            r"options",
            r"remote\s+with\s+connection",
        )
        + group(r"\W", r"$"),
        action=partial(actions.add_node_to_buffer, token_type=TokenType.UNTERM_KEYWORD),
    ),
]
