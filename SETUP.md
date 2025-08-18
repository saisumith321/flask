# Chatbot Application Setup Guide

This guide will help you set up the complete chatbot application with Nhost Auth, Hasura GraphQL, and n8n integration.

## Prerequisites

- Node.js 22.13.1
- npm 10.9.2
- Nhost account
- n8n instance (cloud or self-hosted)
- OpenRouter API account

## 1. Nhost Setup

### Create Nhost Project

1. Go to [Nhost Console](https://console.nhost.io)
2. Create a new project
3. Note down your:
   - Subdomain
   - Region
   - Hasura GraphQL endpoint
   - Hasura admin secret

### Configure Authentication

1. In Nhost Console, go to Authentication
2. Enable Email authentication
3. Configure email templates if needed
4. Set up allowed domains (optional)

## 2. Database Setup

### Apply Migrations

1. In Nhost Console, go to Database
2. Run the SQL from `hasura/migrations/001_create_chats_table.sql`
3. Run the SQL from `hasura/migrations/002_create_messages_table.sql`

### Configure Permissions

1. In Nhost Console, go to GraphQL
2. Navigate to Data tab
3. For `chats` table:
   - Apply permissions from `hasura/metadata/databases/default/tables/public_chats.yaml`
4. For `messages` table:
   - Apply permissions from `hasura/metadata/databases/default/tables/public_messages.yaml`

## 3. Hasura Actions Setup

### Create Custom Types

1. In Hasura Console, go to Actions
2. Go to Types tab
3. Add the custom types from `hasura/metadata/types.yaml`

### Create sendMessage Action

1. In Actions tab, click "Create"
2. Action name: `sendMessage`
3. Action definition:
   ```graphql
   type Mutation {
     sendMessage(chat_id: uuid!, message: String!): SendMessageOutput
   }
   ```
4. Handler URL: `https://your-n8n-instance.com/webhook/chatbot`
5. Add permissions for `user` role

## 4. n8n Workflow Setup

### Import Workflow

1. Open your n8n instance
2. Import `n8n/chatbot-workflow.json`
3. Follow the detailed setup in `n8n/README.md`

### Configure Environment Variables

Set these in your n8n environment:
- `HASURA_GRAPHQL_ENDPOINT`
- `HASURA_GRAPHQL_ADMIN_SECRET`
- `OPENROUTER_API_KEY`

## 5. Frontend Configuration

### Environment Variables

1. Copy `.env.example` to `.env`
2. Update with your values:
   ```bash
   REACT_APP_NHOST_SUBDOMAIN=your-nhost-subdomain
   REACT_APP_NHOST_REGION=your-nhost-region
   ```

### Install Dependencies

```bash
npm install --legacy-peer-deps
```

### Development Server

```bash
npm run serve:frontend
```

## 6. OpenRouter Setup

1. Create account at [OpenRouter](https://openrouter.ai)
2. Generate API key
3. Add credits to your account
4. Use the free model: `openai/gpt-3.5-turbo` or any free model available

## 7. Testing the Application

1. Start the frontend development server
2. Navigate to the application
3. Sign up with an email
4. Verify email (check Nhost email settings)
5. Sign in and test chat functionality

## 8. Deployment to Netlify

### Build the Application

```bash
npm run build
```

### Deploy to Netlify

1. Create Netlify account
2. Connect your repository
3. Set build command: `npm run build`
4. Set publish directory: `dist/public`
5. Add environment variables in Netlify dashboard
6. Deploy

### Environment Variables for Netlify

Add these in Netlify dashboard:
- `REACT_APP_NHOST_SUBDOMAIN`
- `REACT_APP_NHOST_REGION`

## Security Considerations

- All API calls go through n8n (no direct frontend API calls)
- Row-Level Security ensures users only access their data
- Hasura Actions are protected by authentication
- OpenRouter API key is securely stored in n8n

## Architecture Overview

```
Frontend (React) → Nhost Auth → Hasura GraphQL → n8n Workflow → OpenRouter API
                                      ↓
                               PostgreSQL Database
```

## Troubleshooting

### Common Issues

1. **Authentication not working**: Check Nhost configuration and environment variables
2. **GraphQL errors**: Verify Hasura permissions and table relationships
3. **Chatbot not responding**: Check n8n workflow logs and OpenRouter API key
4. **Real-time updates not working**: Verify GraphQL subscriptions are properly configured

### Debug Steps

1. Check browser console for errors
2. Verify network requests in browser dev tools
3. Check Hasura logs in Nhost Console
4. Review n8n execution logs
5. Test GraphQL queries in Hasura Console

## Support

For issues with specific services:
- Nhost: [Nhost Documentation](https://docs.nhost.io)
- Hasura: [Hasura Documentation](https://hasura.io/docs)
- n8n: [n8n Documentation](https://docs.n8n.io)
- OpenRouter: [OpenRouter Documentation](https://openrouter.ai/docs)