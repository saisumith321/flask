import { gql } from '@apollo/client';

export const GET_CHATS = gql`
  query GetChats {
    chats(order_by: { updated_at: desc }) {
      id
      title
      created_at
      updated_at
      user_id
    }
  }
`;

export const GET_MESSAGES = gql`
  query GetMessages($chat_id: uuid!) {
    messages(
      where: { chat_id: { _eq: $chat_id } }
      order_by: { created_at: asc }
    ) {
      id
      content
      is_bot
      created_at
      chat_id
      user_id
    }
  }
`;

export const CREATE_CHAT = gql`
  mutation CreateChat($title: String!) {
    insert_chats_one(object: { title: $title }) {
      id
      title
      created_at
      updated_at
      user_id
    }
  }
`;

export const SEND_MESSAGE = gql`
  mutation SendMessage($chat_id: uuid!, $content: String!) {
    insert_messages_one(object: { 
      chat_id: $chat_id, 
      content: $content, 
      is_bot: false 
    }) {
      id
      content
      is_bot
      created_at
      chat_id
      user_id
    }
  }
`;

export const SEND_MESSAGE_ACTION = gql`
  mutation SendMessageAction($chat_id: uuid!, $message: String!) {
    sendMessage(chat_id: $chat_id, message: $message) {
      success
      message
    }
  }
`;

export const MESSAGES_SUBSCRIPTION = gql`
  subscription MessagesSubscription($chat_id: uuid!) {
    messages(
      where: { chat_id: { _eq: $chat_id } }
      order_by: { created_at: asc }
    ) {
      id
      content
      is_bot
      created_at
      chat_id
      user_id
    }
  }
`;

export const CHATS_SUBSCRIPTION = gql`
  subscription ChatsSubscription {
    chats(order_by: { updated_at: desc }) {
      id
      title
      created_at
      updated_at
      user_id
    }
  }
`;