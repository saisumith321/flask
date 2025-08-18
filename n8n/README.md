# n8n Workflow Setup for Chatbot

This directory contains the n8n workflow configuration for the chatbot integration.

## Setup Instructions

### 1. Import the Workflow

1. Open your n8n instance
2. Go to Workflows
3. Click "Import from File"
4. Upload the `chatbot-workflow.json` file

### 2. Configure Environment Variables

Set the following environment variables in your n8n instance:

```bash
HASURA_GRAPHQL_ENDPOINT=https://your-nhost-project.hasura.app/v1/graphql
HASURA_GRAPHQL_ADMIN_SECRET=your-hasura-admin-secret
OPENROUTER_API_KEY=your-openrouter-api-key
```

### 3. Activate the Workflow

1. Open the imported workflow
2. Click "Activate" to enable the webhook
3. Copy the webhook URL (it will be something like: `https://your-n8n-instance.com/webhook/chatbot`)
4. Update your Hasura Action configuration with this webhook URL

### 4. Test the Integration

The workflow will:

1. Receive webhook calls from Hasura Actions
2. Validate that the requesting user owns the chat_id
3. Call OpenRouter API with the user's message
4. Save the bot's response to the database
5. Return the response to the Hasura Action

### Workflow Flow

```
Webhook Trigger → Validate User → Check Chat Ownership → Call OpenRouter → Save Bot Response → Return Response
                     ↓ (if invalid)
                Unauthorized Response
```

### Security Features

- Validates user authentication through Hasura session variables
- Checks chat ownership before processing
- Uses admin secret for database operations
- Secure API key handling for OpenRouter

### Error Handling

The workflow includes error handling for:
- Unauthorized access attempts
- Invalid chat IDs
- OpenRouter API failures
- Database operation errors

## Troubleshooting

1. **Webhook not receiving requests**: Check that the webhook URL in Hasura Action matches the n8n webhook URL
2. **Authentication errors**: Verify that Hasura session variables are being passed correctly
3. **OpenRouter failures**: Check API key and rate limits
4. **Database errors**: Verify Hasura admin secret and permissions