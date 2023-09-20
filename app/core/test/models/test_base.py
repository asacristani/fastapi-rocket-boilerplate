from unittest import TestCase
from unittest.mock import MagicMock, patch

import pytest

from app.core.models.base import ModelCore


class TestModel(ModelCore, table=True):
    name: str


class TestModelCore(TestCase):
    @pytest.fixture(autouse=True)
    def _db_mocked(self, db_mocked):
        self.db = db_mocked
        self.db.session.connection()

    def test_save(self):
        model_saved = TestModel(name="test").save()

        model_saved.delete()

    def test_delete_soft(self):
        model_to_delete: TestModel = TestModel(name="test_delete").save()

        model_to_delete.delete()

        assert (
            TestModel.get_one(value="test_delete", key=TestModel.name) is None
        )

    def test_delete_hard(self):
        model_to_delete: TestModel = TestModel(name="test_delete").save()

        model_to_delete.delete(hard=True)

        assert (
            TestModel.get_one(value="test_delete", key=TestModel.name) is None
        )

    def test_delete_error(self):
        model_to_delete: TestModel = TestModel(name="test_delete").save()

        with patch(
            "app.core.models.base.ModelCore.save", MagicMock()
        ) as save_method:
            save_method.return_value = False
            assert not model_to_delete.delete()

        model_to_delete.delete()

    def test_get_one(self):
        model_to_get: TestModel = TestModel(name="model_to_get").save()

        assert (
            TestModel.get_one(value="model_to_get", key=TestModel.name)
            == model_to_get
        )

        model_to_get.delete()

    def test_get_one_by_default_id(self):
        model_to_get: TestModel = TestModel(name="model_to_get").save()

        assert TestModel.get_one(value=model_to_get.id) == model_to_get

        model_to_get.delete()

    def test_get_all(self):
        names = ["test1", "test2", "test3"]
        for name in names:
            TestModel(name=name).save()

        assert len(names) == len(model_list := TestModel.get_all())

        for model in model_list:
            model.delete()

    def test_count(self):
        names = ["test1", "test2", "test3"]
        for name in names:
            TestModel(name=name).save()

        assert len(names) == TestModel.count()

        for model in TestModel.get_all():
            model.delete()
