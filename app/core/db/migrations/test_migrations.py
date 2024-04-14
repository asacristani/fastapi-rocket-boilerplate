from pytest_alembic import tests as test_alembic


def test_model_definitions_match_ddl(alembic_runner):
    test_alembic.test_model_definitions_match_ddl(alembic_runner)


def test_single_head_revision(alembic_runner):
    test_alembic.test_single_head_revision(alembic_runner)


def test_up_down_consistency(alembic_runner):
    test_alembic.test_up_down_consistency(alembic_runner)


def test_upgrade(alembic_runner):
    test_alembic.test_upgrade(alembic_runner)
