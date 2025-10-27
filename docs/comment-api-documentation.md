# Comment API Documentation

## Overview

The Comment API provides CRUD (Create, Read, Update, Delete) operations for managing comments on tasks. All endpoints require authentication and follow RESTful principles.

## Base URL

```
/api/v1/accounts/{account_id}/tasks/{task_id}/comments
```

## Authentication

All endpoints require authentication via the `access_auth_middleware`. Include the appropriate authentication headers in your requests.

## Error Handling

The API uses standard HTTP status codes and returns error details in JSON format:

```json
{
  "error": {
    "code": "COMMENT_ERR_01",
    "message": "Comment with id 507f1f77bcf86cd799439011 not found."
  }
}
```

### Error Codes

- `COMMENT_ERR_01`: Comment not found
- `COMMENT_ERR_02`: Bad request (validation error)
- `COMMENT_ERR_03`: Task not found

## Endpoints

### 1. Create Comment

Creates a new comment for a specific task.

**Endpoint:** `POST /api/v1/accounts/{account_id}/tasks/{task_id}/comments`

**Request Body:**
```json
{
  "content": "This is a comment about the task",
  "author_name": "John Doe"
}
```

**Validation Rules:**
- `content`: Required, 1-2000 characters, no harmful content
- `author_name`: Required, 1-100 characters, valid format

**Response (201 Created):**
```json
{
  "id": "507f1f77bcf86cd799439011",
  "task_id": "507f1f77bcf86cd799439012",
  "account_id": "account123",
  "content": "This is a comment about the task",
  "author_name": "John Doe",
  "created_at": "2024-01-01T12:00:00Z",
  "updated_at": "2024-01-01T12:00:00Z"
}
```

**Error Responses:**
- `400 Bad Request`: Invalid request data
- `404 Not Found`: Task not found
- `401 Unauthorized`: Authentication required

### 2. Get Comments (Paginated)

Retrieves paginated list of comments for a specific task.

**Endpoint:** `GET /api/v1/accounts/{account_id}/tasks/{task_id}/comments`

**Query Parameters:**
- `page` (optional): Page number (default: 1, min: 1, max: 10000)
- `size` (optional): Page size (default: 10, min: 1, max: 100)

**Response (200 OK):**
```json
{
  "items": [
    {
      "id": "507f1f77bcf86cd799439011",
      "task_id": "507f1f77bcf86cd799439012",
      "account_id": "account123",
      "content": "This is a comment about the task",
      "author_name": "John Doe",
      "created_at": "2024-01-01T12:00:00Z",
      "updated_at": "2024-01-01T12:00:00Z"
    }
  ],
  "pagination_params": {
    "page": 1,
    "size": 10,
    "offset": 0
  },
  "total_count": 1,
  "total_pages": 1
}
```

### 3. Get Single Comment

Retrieves a specific comment by ID.

**Endpoint:** `GET /api/v1/accounts/{account_id}/tasks/{task_id}/comments/{comment_id}`

**Response (200 OK):**
```json
{
  "id": "507f1f77bcf86cd799439011",
  "task_id": "507f1f77bcf86cd799439012",
  "account_id": "account123",
  "content": "This is a comment about the task",
  "author_name": "John Doe",
  "created_at": "2024-01-01T12:00:00Z",
  "updated_at": "2024-01-01T12:00:00Z"
}
```

**Error Responses:**
- `404 Not Found`: Comment or task not found
- `401 Unauthorized`: Authentication required

### 4. Update Comment

Updates the content of an existing comment.

**Endpoint:** `PATCH /api/v1/accounts/{account_id}/tasks/{task_id}/comments/{comment_id}`

**Request Body:**
```json
{
  "content": "Updated comment content"
}
```

**Validation Rules:**
- `content`: Required, 1-2000 characters, no harmful content

**Response (200 OK):**
```json
{
  "id": "507f1f77bcf86cd799439011",
  "task_id": "507f1f77bcf86cd799439012",
  "account_id": "account123",
  "content": "Updated comment content",
  "author_name": "John Doe",
  "created_at": "2024-01-01T12:00:00Z",
  "updated_at": "2024-01-01T13:00:00Z"
}
```

**Error Responses:**
- `400 Bad Request`: Invalid request data
- `404 Not Found`: Comment or task not found
- `401 Unauthorized`: Authentication required

### 5. Delete Comment

Soft deletes a comment (marks as inactive).

**Endpoint:** `DELETE /api/v1/accounts/{account_id}/tasks/{task_id}/comments/{comment_id}`

**Response (204 No Content):**
Empty response body

**Error Responses:**
- `404 Not Found`: Comment or task not found
- `401 Unauthorized`: Authentication required

## Data Models

### Comment Object

```json
{
  "id": "string",           // MongoDB ObjectId as string
  "task_id": "string",      // Associated task ID
  "account_id": "string",   // Account ID for authorization
  "content": "string",      // Comment content (1-2000 chars)
  "author_name": "string",  // Name of comment author (1-100 chars)
  "created_at": "datetime", // ISO 8601 timestamp
  "updated_at": "datetime"  // ISO 8601 timestamp
}
```

### Pagination Object

```json
{
  "pagination_params": {
    "page": "number",    // Current page number
    "size": "number",    // Items per page
    "offset": "number"   // Calculated offset
  },
  "total_count": "number",  // Total number of items
  "total_pages": "number"   // Total number of pages
}
```

## Usage Examples

### cURL Examples

**Create a comment:**
```bash
curl -X POST \
  http://localhost:5000/api/v1/accounts/account123/tasks/507f1f77bcf86cd799439012/comments \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-token" \
  -d '{
    "content": "This task looks good to me!",
    "author_name": "Jane Smith"
  }'
```

**Get comments with pagination:**
```bash
curl -X GET \
  "http://localhost:5000/api/v1/accounts/account123/tasks/507f1f77bcf86cd799439012/comments?page=1&size=5" \
  -H "Authorization: Bearer your-token"
```

**Update a comment:**
```bash
curl -X PATCH \
  http://localhost:5000/api/v1/accounts/account123/tasks/507f1f77bcf86cd799439012/comments/507f1f77bcf86cd799439011 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-token" \
  -d '{
    "content": "Updated: This task looks great!"
  }'
```

**Delete a comment:**
```bash
curl -X DELETE \
  http://localhost:5000/api/v1/accounts/account123/tasks/507f1f77bcf86cd799439012/comments/507f1f77bcf86cd799439011 \
  -H "Authorization: Bearer your-token"
```

### JavaScript/Fetch Examples

**Create a comment:**
```javascript
const response = await fetch('/api/v1/accounts/account123/tasks/507f1f77bcf86cd799439012/comments', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer your-token'
  },
  body: JSON.stringify({
    content: 'Great work on this task!',
    author_name: 'Alex Johnson'
  })
});

const comment = await response.json();
```

**Get paginated comments:**
```javascript
const response = await fetch('/api/v1/accounts/account123/tasks/507f1f77bcf86cd799439012/comments?page=1&size=10', {
  headers: {
    'Authorization': 'Bearer your-token'
  }
});

const paginatedComments = await response.json();
```

## Security Considerations

1. **Authentication**: All endpoints require valid authentication
2. **Authorization**: Users can only access comments for their own account
3. **Input Validation**: All input is validated for length, format, and safety
4. **XSS Protection**: Comment content is checked for potentially harmful scripts
5. **Rate Limiting**: Consider implementing rate limiting for comment creation

## Database Schema

### Comments Collection

```javascript
{
  _id: ObjectId,
  task_id: String,      // Reference to task
  account_id: String,   // For authorization
  content: String,      // Comment content
  author_name: String,  // Author name
  active: Boolean,      // Soft delete flag
  created_at: Date,     // Creation timestamp
  updated_at: Date      // Last update timestamp
}
```

### Indexes

- `active_task_account_index`: Compound index on (active, task_id, account_id)
- `task_created_at_index`: Compound index on (task_id, created_at) for sorting

## Testing

Run the test suite to verify API functionality:

```bash
# Run all tests
python run_tests.py

# Run only unit tests
python run_tests.py unit

# Run only integration tests
python run_tests.py integration

# Run with coverage
pytest tests/task/ --cov=task --cov-report=html
```

## Changelog

### Version 1.0.0
- Initial implementation of Comment CRUD APIs
- Full test coverage with unit and integration tests
- Comprehensive input validation and security measures
- MongoDB integration with proper indexing
- RESTful API design following project patterns