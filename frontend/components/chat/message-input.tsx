import React, { useState } from 'react';
import { useMutation } from '@apollo/client';
import { toast } from 'react-hot-toast';
import { SEND_MESSAGE, SEND_MESSAGE_ACTION } from 'frontend/graphql/queries';

interface MessageInputProps {
  chatId: string;
}

export const MessageInput: React.FC<MessageInputProps> = ({ chatId }) => {
  const [message, setMessage] = useState('');
  const [isSending, setIsSending] = useState(false);

  const [sendMessage] = useMutation(SEND_MESSAGE);
  const [sendMessageAction] = useMutation(SEND_MESSAGE_ACTION);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!message.trim() || !chatId) return;

    setIsSending(true);
    try {
      // First, save the user message to the database
      await sendMessage({
        variables: {
          chat_id: chatId,
          content: message.trim(),
        },
      });

      // Then trigger the chatbot action
      await sendMessageAction({
        variables: {
          chat_id: chatId,
          message: message.trim(),
        },
      });

      setMessage('');
    } catch (error) {
      console.error('Send message error:', error);
      toast.error('Failed to send message');
    } finally {
      setIsSending(false);
    }
  };

  return (
    <div className="border-t border-gray-200 p-4">
      <form onSubmit={handleSubmit} className="flex space-x-2">
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Type your message..."
          disabled={isSending}
          className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 disabled:opacity-50"
        />
        <button
          type="submit"
          disabled={isSending || !message.trim()}
          className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 disabled:opacity-50"
        >
          {isSending ? 'Sending...' : 'Send'}
        </button>
      </form>
    </div>
  );
};