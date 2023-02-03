# Changelog for the `flask_require` library

This changelog details all version bumps and changes made to the `flask_require` library.

## [0.0.3]

### 1. Improved the response function

The response function did not return any other status codes than 200. This has been fixed.


## [0.0.2]

### 1. Improved the response function

The response function caused some issues with some responses. This has been fixed.

## [0.0.1]

### 1. Added admin requirement

Added the `admin` requirement to the `flask_require` library.
This requirement assumes that the session variable `admin` is set to `True` if the user is an admin.

### 2. Added `field` requirement

Added the `field` requirement to the `flask_require` library.
This decorator extracts all function arguments and checks if they are in the JSON `posted` to the server.
If the `field` is not in the JSON, the function will return an error.
If the fields are present in the JSON the fields will be extracted and passed to the function.

### 3. Added response function

Added the `response` function to the `flask_require` library.
This function is used to create a generic text response to the user.