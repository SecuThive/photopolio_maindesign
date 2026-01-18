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
