from tests.test_crud.test_crud import create_chain


def test_model_chain_persists_and_relations_work(db_session):
    album, release, medium, user_album, group, item, slot = create_chain(db_session)

    assert release.album_work_id == album.id
    assert medium.release_id == release.id
    assert user_album.medium_id == medium.id
    assert item.group_id == group.id
    assert slot.storage_item_id == item.id
    assert slot.user_album_id == user_album.id


def test_model_defaults(db_session):
    album, release, medium, user_album, group, item, _ = create_chain(db_session)

    assert album.is_verified is False
    assert release.is_public is False
    assert medium.is_public is False
    assert user_album.is_shared is False
    assert group.is_public is False
    assert item.is_public is False
