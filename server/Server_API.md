# `/users`

## Get

Returns a list of all users. Users returned are dicts with `message`, `user_nickname`, and `user_id` set.

## Post

Takes json with `message` (str of max len 50) and `user_nickname` (str of max len 25). Creates a new user and returns json with `user_id` (int), `user_password` (int), `message`, and `user_nickname`.

## Delete

Removes the specifed user. Requires a json body with `user_password` and `user_id` set. 

# `/message/<int:user_id>`

## Get

This will return json with `message` set as a string.

## Post

Takes json with `user_password` (int) and `message` (str of max len 50). Changes the user's message. 
