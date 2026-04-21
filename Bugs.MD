test_create_duplicatd_user_01: Duplicated user response not matching expected 409, getting 500 instead.
test_list_unexisting_user_01: Trying to list an unexisting user returns 500 instead of 404
test_create_valid_user_update_data_with_existing_user_email_01: Trying to update an user with data from another won't return any error at all
test_create_user_invalid_email_format_01: Creating a user with invalid email format returns 201 instead of 400 (no email validation)
test_update_user_empty_email_01: Updating a user with empty email returns 500 instead of 400
test_patch_users_returns_405_01: PATCH request to /users returns 500 instead of 405 Method Not Allowed
test_delete_users_returns_405_01: DELETE request to /users returns 500 instead of 405 Method Not Allowed
test_post_users_email_returns_405_01: POST request to /users/{email} returns 500 instead of 405 Method Not Allowed
test_put_users_returns_405_01: PUT request to /users returns 500 instead of 405 Method Not Allowed
test_head_users_returns_405_01: HEAD request to /users returns 200 instead of 405 Method Not Allowed
test_options_users_returns_405_01: OPTIONS request to /users returns 200 instead of 405 Method Not Allowed
test_trace_users_returns_405_01: TRACE request to /users returns 500 instead of 405 Method Not Allowed
test_patch_users_email_returns_405_01: PATCH request to /users/{email} returns 500 instead of 405 Method Not Allowed
test_options_users_email_returns_405_01: OPTIONS request to /users/{email} returns 200 instead of 405 Method Not Allowed