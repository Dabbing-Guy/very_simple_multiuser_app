# `/users`

## Get

Returns a list of all users. Users returned are dicts with `icon`, `user_nickname`, and `user_id` set.

## Post

Takes json with `icon` (str of len 1) and `user_nickname` (str of max len 25). Creates a new user and returns json with `user_id` (int), `user_password` (int), `icon`, and `user_nickname`.

## Delete

Removes the specifed user. Requires a json body with `user_password` and `user_id` set. 

# `/icon/<int:user_id>`

## Get

This will return json with `icon` set as a one char string.

## Post

Takes json with `user_password` (int) and `icon` (str of len 1). Changes the user's icon. 
