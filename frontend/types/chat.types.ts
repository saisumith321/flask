export interface Chat {
  id: string;
  title: string;
  created_at: string;
  updated_at: string;
  user_id: string;
}

export interface Message {
  id: string;
  content: string;
  is_bot: boolean;
  created_at: string;
  chat_id: string;
  user_id: string;
}