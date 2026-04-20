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
