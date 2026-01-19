export type Design = {
  id: string;
  title: string;
  description: string | null;
  image_url: string;
  category: string | null;
  prompt: string | null;
  code: string | null;
  created_at: string;
  updated_at: string;
};

export type PageView = {
  id: string;
  created_at: string;
  page: string | null;
  referer: string | null;
  user_agent: string | null;
};

export type Database = {
  public: {
    Tables: {
      designs: {
        Row: Design;
        Insert: {
          id?: string;
          title: string;
          description?: string | null;
          image_url: string;
          category?: string | null;
          prompt?: string | null;
          code?: string | null;
          created_at?: string;
          updated_at?: string;
        };
        Update: {
          id?: string;
          title?: string;
          description?: string | null;
          image_url?: string;
          category?: string | null;
          prompt?: string | null;
          code?: string | null;
          created_at?: string;
          updated_at?: string;
        };
      };
      page_views: {
        Row: PageView;
        Insert: {
          id?: string;
          created_at?: string;
          page?: string | null;
          referer?: string | null;
          user_agent?: string | null;
        };
        Update: {
          id?: string;
          created_at?: string;
          page?: string | null;
          referer?: string | null;
          user_agent?: string | null;
        };
      };
    };
    Views: {
      [_ in never]: never;
    };
    Functions: {
      [_ in never]: never;
    };
    Enums: {
      [_ in never]: never;
    };
  };
};
