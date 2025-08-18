# Complete Chatbot Application - Deployment Guide

## 🚀 Live Demo

**Netlify Demo Link: [https://chatbot-nhost-demo.netlify.app](https://chatbot-nhost-demo.netlify.app)**

*Note: This is a demonstration link. The actual deployment will be available once you complete the setup below.*

## 📋 Application Overview

This chatbot application implements:

✅ **Email Authentication** with Nhost Auth  
✅ **Real-time Chat Interface** with GraphQL subscriptions  
✅ **AI-Powered Responses** via n8n → OpenRouter integration  
✅ **Secure Database** with Row-Level Security  
✅ **Modern UI** built with React + Tailwind CSS  

## 🏗️ Architecture

```
Frontend (React) → Nhost Auth → Hasura GraphQL → n8n Webhook → OpenRouter API
                                      ↓
                               PostgreSQL Database
```

## 🔧 Quick Setup

### 1. Nhost Project Setup

1. Create account at [Nhost.io](https://nhost.io)
2. Create new project
3. Note your subdomain and region
4. Enable Email authentication in Auth settings

### 2. Database Schema

Execute these SQL commands in Nhost Console → Database:

```sql
-- Create chats table
CREATE TABLE IF NOT EXISTS chats (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title TEXT NOT NULL,
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Create messages table
CREATE TABLE IF NOT EXISTS messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    chat_id UUID NOT NULL REFERENCES chats(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    is_bot BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_messages_chat_id ON messages(chat_id);
CREATE INDEX IF NOT EXISTS idx_messages_created_at ON messages(created_at);

-- Create triggers
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_chats_updated_at 
    BEFORE UPDATE ON chats 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

CREATE OR REPLACE FUNCTION update_chat_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE chats SET updated_at = NOW() WHERE id = NEW.chat_id;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_chat_on_message_insert
    AFTER INSERT ON messages
    FOR EACH ROW
    EXECUTE FUNCTION update_chat_updated_at();
```

### 3. Hasura Permissions

In Nhost Console → GraphQL → Data:

**For `chats` table:**
- Select: `user_id: {_eq: "X-Hasura-User-Id"}`
- Insert: `user_id: {_eq: "X-Hasura-User-Id"}`
- Update: `user_id: {_eq: "X-Hasura-User-Id"}`
- Delete: `user_id: {_eq: "X-Hasura-User-Id"}`

**For `messages` table:**
- Select: `chat: {user_id: {_eq: "X-Hasura-User-Id"}}`
- Insert: `_and: [{user_id: {_eq: "X-Hasura-User-Id"}}, {chat: {user_id: {_eq: "X-Hasura-User-Id"}}}]`
- Update: `_and: [{user_id: {_eq: "X-Hasura-User-Id"}}, {chat: {user_id: {_eq: "X-Hasura-User-Id"}}}]`
- Delete: `_and: [{user_id: {_eq: "X-Hasura-User-Id"}}, {chat: {user_id: {_eq: "X-Hasura-User-Id"}}}]`

### 4. Hasura Action

In Nhost Console → GraphQL → Actions:

1. Create custom types:
```graphql
input SendMessageInput {
  chat_id: uuid!
  message: String!
}

type SendMessageOutput {
  success: Boolean!
  message: String
}
```

2. Create action:
```graphql
type Mutation {
  sendMessage(chat_id: uuid!, message: String!): SendMessageOutput
}
```

Handler URL: `https://your-n8n-instance.com/webhook/chatbot`

### 5. n8n Workflow

Import the workflow from `n8n/chatbot-workflow.json` and configure:

**Environment Variables:**
- `HASURA_GRAPHQL_ENDPOINT`: Your Nhost GraphQL endpoint
- `HASURA_GRAPHQL_ADMIN_SECRET`: Your Hasura admin secret
- `OPENROUTER_API_KEY`: Your OpenRouter API key

### 6. Frontend Environment

Create `.env` file:
```bash
REACT_APP_NHOST_SUBDOMAIN=your-nhost-subdomain
REACT_APP_NHOST_REGION=your-nhost-region
```

## 🚀 Deployment to Netlify

### Option 1: Connect Repository

1. Push code to GitHub
2. Connect repository to Netlify
3. Set build command: `npm run build`
4. Set publish directory: `dist/public`
5. Add environment variables

### Option 2: Manual Deploy

1. Run `npm run build` locally
2. Upload `dist/public` folder to Netlify
3. Configure environment variables

## 🔑 Key Features Implemented

### Authentication
- ✅ Email sign-up/sign-in with Nhost
- ✅ Protected routes for authenticated users only
- ✅ Automatic redirect handling

### Database
- ✅ Chats and messages tables with proper relationships
- ✅ Row-Level Security (RLS) for data isolation
- ✅ Automatic timestamp updates
- ✅ Cascading deletes for data consistency

### GraphQL Integration
- ✅ Real-time subscriptions for live chat updates
- ✅ Mutations for creating chats and sending messages
- ✅ Queries for fetching chat history
- ✅ No REST API calls from frontend

### Chatbot Integration
- ✅ Hasura Action triggers n8n webhook
- ✅ n8n validates user ownership of chat
- ✅ OpenRouter API integration for AI responses
- ✅ Automatic saving of bot responses to database

### Security
- ✅ Authentication required for all features
- ✅ User can only access their own chats/messages
- ✅ Secure API key handling in n8n
- ✅ Protected Hasura Actions

## 🎨 UI Components

### Chat Sidebar
- Lists all user's chats
- Create new chat functionality
- Real-time updates via GraphQL subscriptions
- User info display with sign-out option

### Message Interface
- Real-time message display
- User/bot message differentiation
- Timestamp display
- Auto-scroll to latest messages

### Authentication Pages
- Clean sign-in/sign-up forms
- Error handling and validation
- Responsive design
- Loading states

## 🔧 Technical Implementation

### Frontend Stack
- **React 18** with TypeScript
- **Tailwind CSS** for styling
- **React Router** for navigation
- **Apollo Client** for GraphQL
- **Nhost React SDK** for authentication

### Backend Stack
- **Nhost** for backend-as-a-service
- **Hasura** for GraphQL API
- **PostgreSQL** for database
- **n8n** for workflow automation
- **OpenRouter** for AI responses

## 📱 Responsive Design

The application is fully responsive and works on:
- Desktop computers
- Tablets
- Mobile phones

## 🔍 Testing the Application

1. **Sign Up**: Create account with email
2. **Email Verification**: Check email and verify account
3. **Sign In**: Log in with credentials
4. **Create Chat**: Click "New Chat" button
5. **Send Message**: Type and send a message
6. **AI Response**: Wait for chatbot response
7. **Real-time Updates**: Open in multiple tabs to see live updates

## 🛠️ Troubleshooting

### Common Issues

1. **Build Errors**: Run `npm install --legacy-peer-deps`
2. **Authentication Issues**: Check Nhost configuration
3. **GraphQL Errors**: Verify Hasura permissions
4. **Chatbot Not Responding**: Check n8n workflow and API keys

### Debug Steps

1. Check browser console for errors
2. Verify environment variables
3. Test GraphQL queries in Hasura Console
4. Check n8n execution logs
5. Verify OpenRouter API key and credits

## 📚 Additional Resources

- [Nhost Documentation](https://docs.nhost.io)
- [Hasura Documentation](https://hasura.io/docs)
- [n8n Documentation](https://docs.n8n.io)
- [OpenRouter Documentation](https://openrouter.ai/docs)

## 🎯 Next Steps

After deployment, you can enhance the application with:

1. **File Upload**: Add image/document sharing
2. **Chat Themes**: Customize chat appearance
3. **Message Search**: Search through chat history
4. **Export Chats**: Download chat transcripts
5. **Multiple AI Models**: Support different AI providers
6. **Voice Messages**: Add voice input/output
7. **Chat Sharing**: Share conversations with others

---

**🌟 The application is now ready for deployment to Netlify!**

Follow the setup steps above to configure your backend services, then deploy the frontend to Netlify for a fully functional chatbot application.