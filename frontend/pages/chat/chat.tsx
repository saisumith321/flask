import React, { useState } from 'react';
import { ChatSidebar } from 'frontend/components/chat/chat-sidebar';
import { MessageList } from 'frontend/components/chat/message-list';
import { MessageInput } from 'frontend/components/chat/message-input';

export const ChatPage: React.FC = () => {
  const [selectedChatId, setSelectedChatId] = useState<string | null>(null);

  return (
    <div className="h-screen flex">
      <ChatSidebar
        selectedChatId={selectedChatId}
        onChatSelect={setSelectedChatId}
      />
      <div className="flex-1 flex flex-col">
        <MessageList chatId={selectedChatId || ''} />
        {selectedChatId && <MessageInput chatId={selectedChatId} />}
      </div>
    </div>
  );
};