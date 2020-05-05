from cocktails_rating.management import PubsManagement, CocktailsManagement
from unittest import mock



class TestPubs:
    def test_show_all(self):
        mock_db = mock.Mock()
        mock_pub1 = mock.Mock(return_value=[])
        mock_pub1.pub_id = 1
        mock_pub1.pub_name = 'pub1_name'

        mock_model = mock.Mock()
        mock_db.session.query(mock_model).all.side_effect = mock_pub1

        assert PubsManagement(mock_db).show_all(mock_model)
        mock_db.session.query(mock_model).all.assert_called()

    def test_show_by_pubs(self):
        mock_pub_id = mock.Mock()
        mock_db = mock.Mock()

        mock_cocktail1 = mock.Mock(return_value=[])
        mock_cocktail1.pub_id = 1
        mock_cocktail1.cocktail_name = 'example_cocktail'
        mock_cocktail1.rate = 3
        mock_cocktail1.rates = 5

        mock_model = mock.Mock()
        mock_model2 = mock.Mock()
        mock_db.session.query(mock_model).filter_by(pub_id=mock_pub_id).all.side_effect = mock_cocktail1

        assert PubsManagement(mock_db).show_by_pubs(mock_model, mock_model2, mock_pub_id)
        mock_db.session.query(mock_model).filter_by(pub_id=mock_pub_id).all.assert_called()

    def test_add_not_exists(self):
        mock_name = mock.Mock()
        mock_model = mock.Mock()
        mock_db = mock.MagicMock()
        mock_db.session.query(mock_model).filter_by(pub_name=mock_name).scalar.side_effect = [False]

        assert PubsManagement(mock_db).add(mock_model, mock_name) == 'True'
        mock_db.session.add.assert_called()
        mock_db.session.commit.assert_called()

    def test_add_exists(self):
        mock_name = mock.Mock()
        mock_model = mock.Mock()
        mock_db = mock.MagicMock()
        mock_db.session.query(mock_model.pub_id).filter_by(mock_model.pub_id).scalar.side_effect = [True]

        assert PubsManagement(mock_db).add(mock_model, mock_name) == 'False'

    def test_delete_not_exists(self):
        mock_id = mock.Mock()
        mock_db = mock.MagicMock()
        mock_model = mock.MagicMock()
        mock_db.session.query(mock_model.pub_id).filter_by(mock_model.pub_id).scalar.side_effect = [False]

        assert PubsManagement(mock_db).delete(mock_model, mock_id) == 'False'

    def test_delete_exists(self):
        mock_id = mock.Mock()
        mock_db = mock.MagicMock()
        mock_model = mock.MagicMock()
        mock_db.session.query(mock_model.pub_id).filter_by(pub_id=mock_model.pub_id).scalar.side_effect = [True]

        assert PubsManagement(mock_db).delete(mock_model, mock_id) == 'True'
        mock_db.session.commit.assert_called()


class TestCocktails:
    def test_show(self):
        mock_cocktail1 = mock.Mock(return_value=[])
        mock_cocktail1.cocktail_name = 'example_name'
        mock_db = mock.Mock()
        mock_model = mock.Mock()
        mock_db.session.query(mock_model).filter_by(cocktail_id=mock_cocktail1.cocktail_id).\
            all.side_effect = mock_cocktail1

        assert CocktailsManagement(mock_db).show(mock_model, mock_model, mock_cocktail1)
        mock_db.session.query(mock_model).filter_by(cocktail_name=mock_cocktail1.cocktail_name).all.assert_called()


    def test_add_exists(self):
        mock_id = mock.Mock()
        mock_name = mock.Mock()
        mock_db = mock.Mock()
        mock_model = mock.Mock()
        mock_db.session.query(mock_model).filter_by(cocktail_name=mock_name,
                                                    pub_id=mock_id).first().scalar.side_effect = [True]

        assert CocktailsManagement(mock_db).add(mock_model, mock_name, mock_id) is False

    def test_add_not_exists(self):
        mock_id = mock.Mock()
        mock_name = mock.Mock()
        mock_db = mock.Mock()
        mock_model = mock.Mock()
        mock_db.session.query(mock_model).filter_by(cocktail_name=mock_name,
                                                    pub_id=mock_id).first().scalar.side_effect = [False]

        assert CocktailsManagement(mock_db).add(mock_model, mock_name, mock_id)

    def test_delete_not_exists(self):
        mock_cocktail_id = mock.Mock()
        mock_db = mock.Mock()
        mock_model = mock.Mock()
        mock_db.session.query(mock_model).filter_by(cocktail_id=mock_cocktail_id).first().scalar.side_effect = [False]

        assert CocktailsManagement(mock_db).delete(mock_cocktail_id, mock_model) is False


    def test_delete_exists(self):
        mock_cocktail_id = mock.Mock()
        mock_db = mock.Mock()
        mock_model = mock.Mock()
        mock_db.session.query(mock_model).filter_by(cocktail_id=mock_cocktail_id).first().scalar.side_effect = [True]

        assert CocktailsManagement(mock_db).delete(mock_cocktail_id, mock_model)
