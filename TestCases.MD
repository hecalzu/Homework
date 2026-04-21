Method	Endpoint	    Test Name	                                Steps	                                                            Validations	                                                                        Expected Results
GET	    /users	        TC_01_List_All_Users_Successfully	        1. Send a GET request to the /users endpoint.	                    1. Validate the HTTP status code.                                                   • Status code is 200 OK.
                                                                                                                                        2. Validate that the response is formatted as a JSON rray.                          • Response body is a valid JSON array of User objects.
                                                                                                                                        3. If the array is not empty, validate that each object matches the User schema.	

POST	/users	        TC_02_Create_Valid_User	                    1. Send a POST request to /users.                                   1. Validate the HTTP status code.                                                   • Status code is 201 Created.
                                                                    2. Include a valid JSON body.	                                    2. Validate that the response body matches the data sent.	                        • Response body contains the newly created User object.

POST	/users	        TC_03_Create_User_Validation_Error	        1. Send a POST request to /users.                                   1. Validate the HTTP status code.                                                   • Status code is 400 Bad Request.
                                                                    2. Provide an invalid JSON body.	                                2. Validate that an error message is returned.                                      • Response returns an ErrorResponse object.


POST	/users	        TC_04_Create_User_Duplicate_Email	        1. Send a POST request to /users using an existing email address.	1. Validate the HTTP status code.                                                   • Response returns an ErrorResponse object.
                                                                                                                                        2. Validate the error response.	                                                    • Status code is 409 Conflict.

GET	    /users/{email}	TC_05_Get_Existing_User_Successfully	    1. Send a GET request to /users/{email} for an existing user.	    1. Validate the HTTP status code.                                                   • Status code is 200 OK.
                                                                                                                                        2. Validate the response body schema.	                                            • Response body contains the correct User object.

GET	    /users/{email}	TC_06_Get_Non_Existent_User	                1. Send a GET request to /users/{email} for a non-existent email.	1. Validate the HTTP status code.	                                                • Status code is 404 Not Found.
                                                                                                                                                                                                                            • Response returns an ErrorResponse object.

PUT	    /users/{email}	TC_07_Update_Existing_User_Successfully	    1. Send a PUT request to /users/{email} for an existing user.       1. Validate the HTTP status code.                                                   • Status code is 200 OK.
                                                                    2. Pass a valid JSON body.	                                        2. Validate the response body reflects the new data.	                            • Response body contains the updated User object.

PUT	    /users/{email}	TC_08_Update_User_Validation_Error	        1. Send a PUT request to /users/{email} for an existing user.       1. Validate the HTTP status code.	                                                • Status code is 400 Bad Request.
                                                                    2. Pass an invalid JSON body.	

PUT	    /users/{email}	TC_09_Update_Non_Existent_User	            1. Send a PUT request to /users/{email} using a non-existent email. 1. Validate the HTTP status code.	                                                • Status code is 404 Not Found.
                                                                    2. Pass a valid JSON body.	                                                                                                                            • Response returns an ErrorResponse object.   

PUT	    /users/{email}	TC_10_Update_User_Duplicate_Email	        1. Send a PUT request to /users/{email} for User A.                 1. Validate the HTTP status code.	                                                • Status code is 409 Conflict.
                                                                    2. Pass the email of User B in the body.	                                                                                                            • Response returns an ErrorResponse object.

DELETE	/users/{email}	TC_11_Delete_Existing_User_Successfully	    1. Send a DELETE request to /users/{email} for an existing user.    1. Validate the HTTP status code.                                                   • Status code is 204 No Content.
                                                                    2. Include a valid Authentication header.	                        2. (Optional) Verify deletion with a GET request.                                   • The user is successfully removed.
	

DELETE	/users/{email}	TC_12_Delete_User_Missing_Or_Invalid_Auth	1. Send a DELETE request to /users/{email}.                         1. Validate the HTTP status code.	                                                • Status code is 401 Unauthorized.
                                                                    2. Omit or pass an invalid Authentication header.	                                                                                                    • Response returns an ErrorResponse object.

DELETE	/users/{email}	TC_13_Delete_Non_Existent_User	            1. Send a DELETE request to /users/{email} for a non-existent user. 1. Validate the HTTP status code.	                                                • Status code is 404 Not Found.
                                                                    2. Include a valid Authentication header.	                                                                                                            • Response returns an ErrorResponse object.

GET	    /users	        TC_14_List_All_Users_Empty_List	            1. Send a GET request to /users when no users exist.	            1. Validate the HTTP status code.	                                                • Status code is 200 OK.
                                                                                                                                        2. Validate the response body.	                                                    • Response body is an empty JSON array [].

POST	/users	        TC_15_Create_User_Missing_Name              1. Send a POST request to /users.                                   1. Validate the HTTP status code.                                                   • Status code is 400 Bad Request.
                                                                    2. Omit the 'name' field from the JSON body.                        2. Validate that no user is created.                                                • No user is added to the system.

POST	/users	        TC_16_Create_User_Missing_Age               1. Send a POST request to /users.                                   1. Validate the HTTP status code.                                                   • Status code is 400 Bad Request.
                                                                    2. Omit the 'age' field from the JSON body.                         2. Validate that no user is created.                                                • No user is added to the system.

POST	/users	        TC_17_Create_User_Missing_Email             1. Send a POST request to /users.                                   1. Validate the HTTP status code.                                                   • Status code is 400 Bad Request.
                                                                    2. Omit the 'email' field from the JSON body.                       2. Validate that no user is created.                                                • No user is added to the system.

POST	/users	        TC_18_Create_User_Age_Below_Minimum         1. Send a POST request to /users.                                   1. Validate the HTTP status code.                                                   • Status code is 400 Bad Request.
                                                                    2. Provide age value of 0 (below minimum of 1).                     2. Validate that no user is created.                                                • No user is added to the system.

POST	/users	        TC_19_Create_User_Age_At_Minimum            1. Send a POST request to /users.                                   1. Validate the HTTP status code.                                                   • Status code is 201 Created.
                                                                    2. Provide age value of 1 (minimum boundary).                       2. Validate the user is created successfully.                                       • User is created with age = 1.

POST	/users	        TC_20_Create_User_Age_At_Maximum            1. Send a POST request to /users.                                   1. Validate the HTTP status code.                                                   • Status code is 201 Created.
                                                                    2. Provide age value of 150 (maximum boundary).                     2. Validate the user is created successfully.                                       • User is created with age = 150.

POST	/users	        TC_21_Create_User_Age_Above_Maximum         1. Send a POST request to /users.                                   1. Validate the HTTP status code.                                                   • Status code is 400 Bad Request.
                                                                    2. Provide age value above 150.                                     2. Validate that no user is created.                                                • No user is added to the system.

POST	/users	        TC_22_Create_User_Negative_Age              1. Send a POST request to /users.                                   1. Validate the HTTP status code.                                                   • Status code is 400 Bad Request.
                                                                    2. Provide a negative age value (e.g., -5).                         2. Validate that no user is created.                                                • No user is added to the system.

POST	/users	        TC_23_Create_User_Non_Integer_Age           1. Send a POST request to /users.                                   1. Validate the HTTP status code.                                                   • Status code is 400 Bad Request.
                                                                    2. Provide a non-integer age value (e.g., 25.5).                    2. Validate that no user is created.                                                • No user is added to the system.

POST	/users	        TC_24_Create_User_Invalid_Email_Format      1. Send a POST request to /users.                                   1. Validate the HTTP status code.                                                   • Status code is 400 Bad Request.
                                                                    2. Provide an invalid email format (e.g., "invalid-email").         2. Validate that no user is created.                                                • No user is added to the system.

POST	/users	        TC_25_Create_User_Empty_Email               1. Send a POST request to /users.                                   1. Validate the HTTP status code.                                                   • Status code is 400 Bad Request.
                                                                    2. Provide an empty string for email.                               2. Validate that no user is created.                                                • No user is added to the system.

                                                                                                                                        2. Validate that no user is created.                                                • No user is added to the system.
POST	/users	        TC_26_Create_User_Empty_Body                1. Send a POST request to /users with an empty JSON object {}.      1. Validate the HTTP status code.                                                   • Status code is 400 Bad Request.

PUT	    /users/{email}	TC_27_Update_User_Age_Below_Minimum         1. Send a PUT request to /users/{email} for an existing user.       1. Validate the HTTP status code.                                                   • Status code is 400 Bad Request.
                                                                    2. Provide age value of 0 (below minimum of 1).

PUT	    /users/{email}	TC_28_Update_User_Age_Above_Maximum         1. Send a PUT request to /users/{email} for an existing user.       1. Validate the HTTP status code.                                                   • Status code is 400 Bad Request.
                                                                    2. Provide age value above 150.

PUT	    /users/{email}	TC_29_Update_User_Negative_Age              1. Send a PUT request to /users/{email} for an existing user.       1. Validate the HTTP status code.                                                   • Status code is 400 Bad Request.
                                                                    2. Provide a negative age value (e.g., -5).

PUT	    /users/{email}	TC_30_Update_User_Invalid_Email_Format      1. Send a PUT request to /users/{email} for an existing user.       1. Validate the HTTP status code.                                                   • Status code is 400 Bad Request.
                                                                    2. Provide an invalid email format (e.g., "invalid-email").

PUT	    /users/{email}	TC_31_Update_User_Empty_Email               1. Send a PUT request to /users/{email} for an existing user.       1. Validate the HTTP status code.                                                   • Status code is 400 Bad Request.
                                                                    2. Provide an empty string for email.

PUT	    /users/{email}	TC_32_Update_User_Empty_Body                1. Send a PUT request to /users/{email} for an existing user.       1. Validate the HTTP status code.                                                   • Status code is 400 Bad Request.
                                                                    2. Provide an empty JSON object {}.

DELETE	/users/{email}	TC_33_Delete_User_Invalid_Auth_Token        1. Send a DELETE request to /users/{email}.                         1. Validate the HTTP status code.                                                   • Status code is 401 Unauthorized.
                                                                    2. Include an invalid Authentication token.                         2. Validate the user still exists.                                                  • User is not deleted.

DELETE	/users/{email}	TC_34_Delete_User_Idempotency               1. Send a DELETE request to /users/{email} for an existing user.    1. Validate the first DELETE returns 204.                                           • First DELETE returns 204 No Content.
                                                                    2. Send a second DELETE request to the same email.                  2. Validate the second DELETE returns 404.                                          • Second DELETE returns 404 Not Found.

DELETE	/users/{email}	TC_35_Delete_User_Empty_Auth_Header         1. Send a DELETE request to /users/{email}.                         1. Validate the HTTP status code.                                                   • Status code is 401 Unauthorized.
                                                                    2. Include an empty Authentication header.                          2. Validate the user still exists.                                                  • User is not deleted.

PATCH	/users	        TC_36_Patch_Users_Unsupported_Method        1. Send a PATCH request to /users.                                  1. Validate the HTTP status code.                                                   • Status code is 405 Method Not Allowed.

DELETE	/users	        TC_37_Delete_Users_Unsupported_Method       1. Send a DELETE request to /users (collection endpoint).           1. Validate the HTTP status code.                                                   • Status code is 405 Method Not Allowed.

POST	/users/{email}	TC_38_Post_User_Email_Unsupported_Method    1. Send a POST request to /users/{email}.                           1. Validate the HTTP status code.                                                   • Status code is 405 Method Not Allowed.

PUT	    /users	        TC_39_Put_Users_Unsupported_Method          1. Send a PUT request to /users (collection endpoint).              1. Validate the HTTP status code.                                                   • Status code is 405 Method Not Allowed.

HEAD	/users	        TC_40_Head_Users_Unsupported_Method         1. Send a HEAD request to /users.                                   1. Validate the HTTP status code.                                                   • Status code is 405 Method Not Allowed.

OPTIONS	/users	        TC_41_Options_Users_Unsupported_Method      1. Send an OPTIONS request to /users.                               1. Validate the HTTP status code.                                                   • Status code is 405 Method Not Allowed.

TRACE	/users	        TC_42_Trace_Users_Unsupported_Method        1. Send a TRACE request to /users.                                  1. Validate the HTTP status code.                                                   • Status code is 405 Method Not Allowed.

PATCH	/users/{email}	TC_43_Patch_User_Email_Unsupported_Method   1. Send a PATCH request to /users/{email}.                          1. Validate the HTTP status code.                                                   • Status code is 405 Method Not Allowed.

OPTIONS	/users/{email}	TC_44_Options_User_Email_Unsupported_Method 1. Send an OPTIONS request to /users/{email}.                       1. Validate the HTTP status code.                                                   • Status code is 405 Method Not Allowed.
