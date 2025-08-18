import React, { useEffect, useRef } from 'react';
import { useSubscription } from '@apollo/client';
import { Message } from 'frontend/types/chat.types';
import { MESSAGES_SUBSCRIPTION } from 'frontend/graphql/queries';

interface MessageListProps {
  chatId: string;
}

export const MessageList: React.FC<MessageListProps> = ({ chatId }) => {
  const messagesEndRef = useRef<HTMLDivElement>(null);
  
  const { data: messagesData } = useSubscription(MESSAGES_SUBSCRIPTION, {
    variables: { chat_id: chatId },
  });
  
  const messages = messagesData?.messages || [];

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  if (!chatId) {
    return (
      <div className="flex-1 flex items-center justify-center text-gray-500">
        <div className="text-center">
          <h3 className="text-lg font-medium mb-2">Welcome to Chatbot</h3>
          <p>Select a chat from the sidebar or create a new one to get started.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex-1 overflow-y-auto p-4 space-y-4">
      {messages.map((message: Message) => (
        <div
          key={message.id}
          className={`flex ${message.is_bot ? 'justify-start' : 'justify-end'}`}
        >
          <div
            className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
              message.is_bot
                ? 'bg-gray-200 text-gray-900'
                : 'bg-indigo-600 text-white'
            }`}
          >
            <p className="text-sm">{message.content}</p>
            <p className={`text-xs mt-1 ${
              message.is_bot ? 'text-gray-500' : 'text-indigo-200'
            }`}>
              {new Date(message.created_at).toLocaleTimeString()}
            </p>
          </div>
        </div>
      ))}
      <div ref={messagesEndRef} />
    </div>
  );
};