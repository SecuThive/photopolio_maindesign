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
  likes: number | null;
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
          likes?: number | null;
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
          likes?: number | null;
        };
      };
      design_likes: {
        Row: {
          id: string;
          created_at: string;
          design_id: string;
          token: string;
        };
        Insert: {
          id?: string;
          created_at?: string;
          design_id: string;
          token: string;
        };
        Update: {
          id?: string;
          created_at?: string;
          design_id?: string;
          token?: string;
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
