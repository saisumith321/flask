import React from 'react';
import { useMutation, useSubscription } from '@apollo/client';
import { toast } from 'react-hot-toast';
import { Chat } from 'frontend/types/chat.types';
import { CREATE_CHAT, CHATS_SUBSCRIPTION } from 'frontend/graphql/queries';
import { useNhostAuthContext } from 'frontend/contexts/nhost-auth.provider';

interface ChatSidebarProps {
  selectedChatId: string | null;
  onChatSelect: (chatId: string) => void;
}

export const ChatSidebar: React.FC<ChatSidebarProps> = ({
  selectedChatId,
  onChatSelect,
}) => {
  const { signOut, userEmail } = useNhostAuthContext();
  
  const { data: chatsData } = useSubscription(CHATS_SUBSCRIPTION);
  const chats = chatsData?.chats || [];

  const [createChat, { loading: createChatLoading }] = useMutation(CREATE_CHAT, {
    onCompleted: (data) => {
      onChatSelect(data.insert_chats_one.id);
      toast.success('New chat created!');
    },
    onError: (error) => {
      toast.error('Failed to create chat');
      console.error('Create chat error:', error);
    },
  });

  const handleCreateChat = async () => {
    const title = `Chat ${new Date().toLocaleString()}`;
    await createChat({
      variables: { title },
    });
  };

  const handleSignOut = async () => {
    await signOut();
    toast.success('Signed out successfully');
  };

  return (
    <div className="w-64 bg-gray-900 text-white flex flex-col h-full">
      {/* Header */}
      <div className="p-4 border-b border-gray-700">
        <div className="flex items-center justify-between">
          <h1 className="text-xl font-bold">Chatbot</h1>
          <button
            onClick={handleSignOut}
            className="text-gray-400 hover:text-white text-sm"
          >
            Sign Out
          </button>
        </div>
        <p className="text-gray-400 text-sm mt-1">{userEmail}</p>
      </div>

      {/* New Chat Button */}
      <div className="p-4">
        <button
          onClick={handleCreateChat}
          disabled={createChatLoading}
          className="w-full bg-indigo-600 hover:bg-indigo-700 text-white py-2 px-4 rounded-md text-sm font-medium disabled:opacity-50"
        >
          {createChatLoading ? 'Creating...' : '+ New Chat'}
        </button>
      </div>

      {/* Chat List */}
      <div className="flex-1 overflow-y-auto">
        <div className="px-2">
          {chats.map((chat: Chat) => (
            <button
              key={chat.id}
              onClick={() => onChatSelect(chat.id)}
              className={`w-full text-left p-3 rounded-md mb-2 transition-colors ${
                selectedChatId === chat.id
                  ? 'bg-indigo-600 text-white'
                  : 'text-gray-300 hover:bg-gray-700'
              }`}
            >
              <div className="truncate font-medium">{chat.title}</div>
              <div className="text-xs text-gray-400 mt-1">
                {new Date(chat.updated_at).toLocaleDateString()}
              </div>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};