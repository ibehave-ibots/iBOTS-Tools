from external.zoom_api.list_group_members import list_group_members
from pytest import mark

@mark.slow
def test_get_user_ids_from_group_id(access_token):
    #given 
    group_id = "b_r8HCDBSSqe8gHUVfIyaQ"
    user_1 = "NblGhypARWa7TjfyN2zqaQ"
    user_2 = "vrxh8FQGQk2IFYTsm8a7qg"

    #when
    user_ids = list_group_members(access_token=access_token, group_id=group_id)

    #then
    assert any(user.id == user_1 for user in user_ids)
    assert any(user.id == user_2 for user in user_ids)
